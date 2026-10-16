"""ViLatent = frozen reader + writer + fixed reader template, in one of three modes
(docs/VILATENT.md §Kiến trúc, "Đọc theo câu hỏi" and variant W5):

  M    W0 writer (question-blind) at ratio r; the slot holds ⟨mem⟩ m_1 … m_k ⟨/mem⟩, k = Σ⌈n_i/r⌉
  ME   W0 writer at ratio r·f (memory factor f ∈ {2, 4, 8}, chosen on dev loss), then the
       original sentences chosen by BM25 for the question, in the rest of the same budget:
       k_m = Σ⌈n_i/(r·f)⌉ vectors + (k − k_m) tokens = k. The main system.
  W5   writer that sees the question ([sink][question][chunk]) at ratio r; memory is written
       again for every question

Reader input:

    [prefix ids] ⟨mem⟩ m_1 … m_k ⟨/mem⟩ [evidence ids, ME] [suffix ids, with the question] [target ids]

Memory takes consecutive position ids right after the prefix, like ordinary tokens. In M and
ME the memory of a context is written once and reused for every question on it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import torch

from .baselines import BM25Sentences, TokenCounter
from .budget import DEFAULT_CHUNK_TOKENS, chunk_context, memory_budget
from .data import Example
from .losses import ce_kl_loss
from .reader import embed_ids, eos_ids, greedy_generate
from .template import ReaderTemplate
from .writer import MemoryWriter

MODES = ("M", "ME", "W5")


@dataclass
class Prepared:
    """One tokenized example."""
    example: Example
    chunks: list[list[int]]  # reader ids of the context, cut into chunks
    prefix_ids: list[int]
    suffix_ids: list[int]
    target_ids: list[int]
    budget: int  # k = Σ⌈n_i / r⌉ at the budget ratio r
    question_ids: list[int] = field(default_factory=list)  # W5: the question given to the writer
    evidence_ids: list[int] = field(default_factory=list)  # ME: BM25 sentences placed after ⟨/mem⟩

    @property
    def n_tokens(self) -> int:
        return sum(len(c) for c in self.chunks)


def writer_ratio(mode: str, budget_ratio: int, memory_factor: int = 2) -> int:
    """Pooling ratio of the writer for a budget ratio r: r·f in ME (about 1 − 1/f of k goes to
    text: f = 2, 4, 8 gives ≈ 50%, 75%, 87.5%), r otherwise."""
    return memory_factor * budget_ratio if mode == "ME" else budget_ratio


class ViLatent:
    def __init__(self, reader, tokenizer, template: ReaderTemplate, writer: MemoryWriter, mode: str = "M",
                 memory_factor: int = 2, chunk_tokens: int = DEFAULT_CHUNK_TOKENS, max_chunks_per_pass: int = 64):
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}")
        if writer.sees_question != (mode == "W5"):
            raise ValueError(f"mode {mode} needs a writer with sees_question={mode == 'W5'}")
        if mode == "ME" and (memory_factor < 2 or writer.ratio % memory_factor):
            raise ValueError(f"ME needs a writer at r·f with f ≥ 2 (writer ratio {writer.ratio}, f {memory_factor})")
        self.reader, self.tokenizer, self.template, self.writer, self.mode = reader, tokenizer, template, writer, mode
        self.memory_factor = memory_factor if mode == "ME" else 1
        self.chunk_tokens, self.max_chunks_per_pass = chunk_tokens, max_chunks_per_pass
        self.budget_ratio = writer.ratio // self.memory_factor
        self.stop_ids = eos_ids(reader, template.eos_id)
        self.selector = BM25Sentences()

    @property
    def device(self) -> torch.device:
        return self.reader.get_input_embeddings().weight.device

    # ------------------------------------------------------------------ tokenization

    def prepare(self, ex: Example) -> Prepared:
        lead = self.template.lead[ex.task]
        chunked = chunk_context(ex.context, self.tokenizer, self.chunk_tokens, lead=lead)
        k = memory_budget(chunked.lengths, self.budget_ratio)
        evidence, question = [], []
        if self.mode == "ME":
            if ex.task != "qa":
                raise ValueError("ME needs a question: run stage 1 in mode M")
            k_text = k - memory_budget(chunked.lengths, self.writer.ratio)
            text = self.selector.compress(ex.context, ex.question, k_text, TokenCounter(self.tokenizer, lead))
            evidence = self.template.context_ids(ex.task, text)
        if self.mode == "W5":
            question = self.template.ids(ex.question)
        return Prepared(ex, chunked.chunks, self.template.prefix_ids(ex.task),
                        self.template.suffix_ids(ex.task, ex.question),
                        self.template.target_ids(ex.task, ex.target), k, question, evidence)

    def budget(self, prepared: Prepared) -> int:
        return prepared.budget

    def memory_key(self, prepared: Prepared):
        """Memory can be shared by every question on a context, except in W5."""
        ex = prepared.example
        return (ex.context, ex.question) if self.mode == "W5" else ex.context

    # ------------------------------------------------------------------ memory

    def encode_memory(self, contexts: list[list[list[int]]],
                      questions: list[list[int]] | None = None) -> list[torch.Tensor]:
        """One memory per context (given as its chunks): (k_m + 2, d) with the two boundary
        embeddings, k_m = Σ ceil(n_i / writer ratio). ``questions`` (W5 only) are the question
        ids given to the writer for each context. Gradients flow when the writer is training."""
        questions = questions or [[] for _ in contexts]
        flat = [(q, c) for chunks, q in zip(contexts, questions) for c in chunks]
        per_chunk = []
        for start in range(0, len(flat), self.max_chunks_per_pass):
            per_chunk += self._write_chunks(flat[start:start + self.max_chunks_per_pass])
        memories, i = [], 0
        for chunks in contexts:
            parts = per_chunk[i:i + len(chunks)]
            i += len(chunks)
            memories.append(torch.cat([self.writer.mem_start[None], *parts, self.writer.mem_end[None]]))
        return memories

    def _write_chunks(self, items: list[tuple[list[int], list[int]]]) -> list[torch.Tensor]:
        """Rows [sink] + question + chunk, right-padded; the writer keeps the chunk positions."""
        if not items:
            return []
        sink = self.template.sink_id
        rows = [[sink] + q + c for q, c in items]
        t_max = max(len(r) for r in rows)
        ids = torch.full((len(rows), t_max), sink, dtype=torch.long, device=self.device)
        for i, r in enumerate(rows):
            ids[i, :len(r)] = torch.tensor(r, dtype=torch.long)
        starts = torch.tensor([1 + len(q) for q, _ in items], device=self.device)
        lengths = torch.tensor([len(c) for _, c in items], device=self.device)
        with torch.no_grad():
            embeds = self.reader.get_input_embeddings()(ids)
        return self.writer(embeds, starts, lengths)

    def memory_prompt(self, prepared: Prepared, memory: torch.Tensor, with_target: bool = False) -> torch.Tensor:
        """Reader input embeddings: prefix, memory, evidence (ME), suffix and, for training, target."""
        dtype = self.reader.get_input_embeddings().weight.dtype
        tail = prepared.evidence_ids + prepared.suffix_ids + (prepared.target_ids if with_target else [])
        return torch.cat([embed_ids(self.reader, prepared.prefix_ids), memory.to(dtype), embed_ids(self.reader, tail)])

    # ------------------------------------------------------------------ training loss

    def loss(self, batch: list[Prepared], teacher: list[tuple[torch.Tensor, torch.Tensor]] | None,
             lambda_kl: float) -> dict[str, torch.Tensor]:
        memories = self.encode_memory([p.chunks for p in batch], [p.question_ids for p in batch])
        seqs = [self.memory_prompt(p, m, with_target=True) for p, m in zip(batch, memories)]
        out = self.target_loss(seqs, [p.target_ids for p in batch], teacher, lambda_kl)
        with torch.no_grad():  # logged: mean L2 norm of the memory vectors (boundaries excluded)
            out["mem_norm"] = torch.cat([m[1:-1] for m in memories]).float().norm(dim=-1).mean()
        return out

    def target_loss(self, seqs: list[torch.Tensor], targets: list[list[int]],
                    teacher: list[tuple[torch.Tensor, torch.Tensor]] | None, lambda_kl: float):
        """CE (+ KL) of the reader on the last len(target) tokens of every sequence."""
        t_max, d = max(s.shape[0] for s in seqs), seqs[0].shape[1]
        x = seqs[0].new_zeros(len(seqs), t_max, d)
        mask = torch.zeros(len(seqs), t_max, dtype=torch.long, device=x.device)
        rows, cols = [], []
        for i, (s, tgt) in enumerate(zip(seqs, targets)):
            x[i, :s.shape[0]] = s
            mask[i, :s.shape[0]] = 1
            first = s.shape[0] - len(tgt)  # position of the first target token
            rows += [i] * len(tgt)
            cols += list(range(first - 1, s.shape[0] - 1))  # positions that predict them
        hidden = self.reader.model(inputs_embeds=x, attention_mask=mask, use_cache=False).last_hidden_state
        logits = self.reader.lm_head(hidden[torch.tensor(rows, device=x.device), torch.tensor(cols, device=x.device)])
        target = torch.tensor([t for tgt in targets for t in tgt], device=x.device)
        t_ids = t_logp = None
        if teacher is not None:
            for tgt, (ids, _) in zip(targets, teacher):
                if ids.shape[0] != len(tgt):
                    raise ValueError("teacher and student target tokens differ; recompute the teacher")
            t_ids = torch.cat([ids for ids, _ in teacher]).to(x.device).long()
            t_logp = torch.cat([lp for _, lp in teacher]).to(x.device)
        return ce_kl_loss(logits, target, t_ids, t_logp, lambda_kl)

    # ------------------------------------------------------------------ generation

    def generate_from_memory(self, prepared: list[Prepared], memories: list[torch.Tensor], max_new_tokens: int):
        seqs = [self.memory_prompt(p, m) for p, m in zip(prepared, memories)]
        return greedy_generate(self.reader, seqs, max_new_tokens, self.stop_ids)

    # ------------------------------------------------------------------ checkpoints

    def save(self, path: str | Path, extra: dict | None = None) -> None:
        torch.save({"writer_config": self.writer.config(), "state_dict": self.writer.state_dict(),
                    "mode": self.mode, "memory_factor": self.memory_factor,
                    "reader": self.template.cfg["reader"], "template_hash": self.template.hash,
                    "chunk_tokens": self.chunk_tokens, **(extra or {})}, path)


def load_vilatent(path: str | Path, reader, tokenizer, template: ReaderTemplate) -> ViLatent:
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    if ckpt["template_hash"] != template.hash:
        raise ValueError(f"{path} was trained with another reader template ({ckpt['template_hash']})")
    writer = MemoryWriter(reader, tokenizer, **ckpt["writer_config"])
    writer.load_state_dict(ckpt["state_dict"])
    writer.eval()
    return ViLatent(reader, tokenizer, template, writer, mode=ckpt["mode"], memory_factor=ckpt["memory_factor"],
                    chunk_tokens=ckpt["chunk_tokens"])
