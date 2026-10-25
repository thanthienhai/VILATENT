"""ViLatent = frozen reader + multi-rate writer + fixed reader template (docs/VILATENT.md
§Kiến trúc, "Đọc theo câu hỏi"; revision of 25/10/2026).

Every example is read at a budget ratio r and a memory factor f, chosen per example (training
samples them, evaluation fixes them), so ONE checkpoint serves every (r, f) it was trained on:

  M   f = 1   question-blind writer pooling at ρ = r; the slot holds ⟨mem⟩ m_1 … m_k ⟨/mem⟩,
              k = k(r) = Σ⌈n_i/r⌉
  ME  f ≥ 2   question-blind writer pooling at ρ = r·f, then the original sentences chosen by
              BM25 for the question in the rest of the same budget: k(r·f) vectors +
              (k(r) − k(r·f)) tokens. The main system.
  Q   f = 1   writer that sees the question ([sink][question][chunk]), pooling at ρ = r; memory
              is written again for every question (``writer.sees_question``; W5 in the code
              history, ViLatent-Q in the paper)

The control "learned prompt + BM25" is ME with a writer.PromptWriter in place of the writer:
the same vectors, sentences and training, but memory that ignores the context.

Reader input:

    [prefix ids] ⟨mem⟩ m_1 … m_k ⟨/mem⟩ [evidence ids, ME] [suffix ids, with the question] [target ids]

Memory takes consecutive position ids right after the prefix, like ordinary tokens. A
question-blind memory of a context at a ratio ρ is written once and reused for every question.
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
from .writer import build_writer

# Pooling ratios of stage 1, and the largest ρ = r·f stage 2 samples (decision of 25/10/2026: every
# pooled ratio was seen in stage 1)
STAGE1_RATIOS = (4, 8, 16, 32)
MAX_POOL = 32


def allowed_pairs(ratios: list[int], factors: list[int], max_pool: int = MAX_POOL) -> list[tuple[int, int]]:
    """(r, f) pairs with r·f ≤ max_pool, e.g. r ∈ {4, 8, 16}, f ∈ {1, 2, 4, 8} gives
    (4,1) (4,2) (4,4) (4,8) (8,1) (8,2) (8,4) (16,1) (16,2)."""
    pairs = [(r, f) for r in ratios for f in factors if r * f <= max_pool]
    if not pairs:
        raise ValueError(f"no (r, f) with r·f <= {max_pool} among r {ratios}, f {factors}")
    return pairs


@dataclass
class Prepared:
    """One tokenized example at a budget ratio r and memory factor f."""
    example: Example
    chunks: list[list[int]]  # reader ids of the context, cut into chunks
    prefix_ids: list[int]
    suffix_ids: list[int]
    target_ids: list[int]
    budget: int  # k = Σ⌈n_i / r⌉
    ratio: int  # r
    factor: int  # f; 1 = no evidence
    question_ids: list[int] = field(default_factory=list)  # Q: the question given to the writer
    evidence_ids: list[int] = field(default_factory=list)  # ME: BM25 sentences placed after ⟨/mem⟩
    evidence: str = ""  # their text (answer-in-evidence check of the cascade)

    @property
    def pool(self) -> int:
        return self.ratio * self.factor

    @property
    def n_tokens(self) -> int:
        return sum(len(c) for c in self.chunks)


class ViLatent:
    def __init__(self, reader, tokenizer, template: ReaderTemplate, writer, chunk_tokens: int = DEFAULT_CHUNK_TOKENS,
                 max_chunks_per_pass: int = 64, bm25: dict | None = None, pairs: list | None = None):
        """``bm25``: ``{"k1", "b", "units"}`` of the sentence selector, needed for f ≥ 2 (the values
        tuned for the bm25 baseline, configs/bm25.json); ``pairs``: the (r, f) pairs the writer
        was trained on (saved with the checkpoint; evaluation refuses other pairs)."""
        self.reader, self.tokenizer, self.template, self.writer = reader, tokenizer, template, writer
        self.chunk_tokens, self.max_chunks_per_pass = chunk_tokens, max_chunks_per_pass
        self.sees_question = writer.sees_question
        self.stop_ids = eos_ids(reader, template.eos_id)
        self.bm25 = bm25
        self.selector = BM25Sentences(**bm25) if bm25 else None
        self.pairs = [tuple(p) for p in pairs] if pairs else None

    @property
    def device(self) -> torch.device:
        return self.reader.get_input_embeddings().weight.device

    def check_pair(self, ratio: int, factor: int) -> None:
        if self.pairs is not None and (ratio, factor) not in self.pairs:
            raise ValueError(f"(r={ratio}, f={factor}) was not trained; trained pairs: {self.pairs}")

    # ------------------------------------------------------------------ tokenization

    def prepare(self, ex: Example, ratio: int, factor: int = 1) -> Prepared:
        if factor > 1 and self.sees_question:
            raise ValueError("ViLatent-Q reads memory only (f = 1)")
        lead = self.template.lead[ex.task]
        chunked = chunk_context(ex.context, self.tokenizer, self.chunk_tokens, lead=lead)
        k = memory_budget(chunked.lengths, ratio)
        evidence, text, question = [], "", []
        if factor > 1:
            if ex.task != "qa":
                raise ValueError("evidence needs a question: stage 1 runs with f = 1")
            if self.selector is None:
                raise ValueError("f > 1 needs the BM25 parameters of the bm25 baseline (configs/bm25.json)")
            k_text = k - memory_budget(chunked.lengths, ratio * factor)
            text = self.selector.compress(ex.context, ex.question, k_text, TokenCounter(self.tokenizer, lead))
            evidence = self.template.context_ids(ex.task, text)
        if self.sees_question:
            question = self.template.ids(ex.question)
        return Prepared(ex, chunked.chunks, self.template.prefix_ids(ex.task),
                        self.template.suffix_ids(ex.task, ex.question),
                        self.template.target_ids(ex.task, ex.target), k, ratio, factor, question, evidence, text)

    def memory_key(self, prepared: Prepared):
        """A memory is shared by every question on a context at one pooling ratio, except in Q."""
        ex = prepared.example
        return (ex.context, ex.question, prepared.pool) if self.sees_question else (ex.context, prepared.pool)

    # ------------------------------------------------------------------ memory

    def encode_memory(self, prepared: list[Prepared]) -> list[torch.Tensor]:
        """One memory per prepared example: (k_m + 2, d) with the two boundary embeddings,
        k_m = Σ ceil(n_i / ρ). Gradients flow when the writer is training."""
        flat = [(p.question_ids, c, p.pool) for p in prepared for c in p.chunks]
        per_chunk = []
        for start in range(0, len(flat), self.max_chunks_per_pass):
            per_chunk += self._write_chunks(flat[start:start + self.max_chunks_per_pass])
        memories, i = [], 0
        for p in prepared:
            parts = per_chunk[i:i + len(p.chunks)]
            i += len(p.chunks)
            memories.append(torch.cat([self.writer.mem_start[None], *parts, self.writer.mem_end[None]]))
        return memories

    def _write_chunks(self, items: list[tuple[list[int], list[int], int]]) -> list[torch.Tensor]:
        """Rows [sink] + question + chunk, right-padded; the writer keeps the chunk positions."""
        if not items:
            return []
        sink = self.template.sink_id
        rows = [[sink] + q + c for q, c, _ in items]
        t_max = max(len(r) for r in rows)
        ids = torch.full((len(rows), t_max), sink, dtype=torch.long, device=self.device)
        for i, r in enumerate(rows):
            ids[i, :len(r)] = torch.tensor(r, dtype=torch.long)
        starts = torch.tensor([1 + len(q) for q, _, _ in items], device=self.device)
        lengths = torch.tensor([len(c) for _, c, _ in items], device=self.device)
        with torch.no_grad():
            embeds = self.reader.get_input_embeddings()(ids)
        return self.writer(embeds, starts, lengths, [pool for *_, pool in items])

    def memory_prompt(self, prepared: Prepared, memory: torch.Tensor, with_target: bool = False) -> torch.Tensor:
        """Reader input embeddings: prefix, memory, evidence (ME), suffix and, for training, target."""
        dtype = self.reader.get_input_embeddings().weight.dtype
        tail = prepared.evidence_ids + prepared.suffix_ids + (prepared.target_ids if with_target else [])
        return torch.cat([embed_ids(self.reader, prepared.prefix_ids), memory.to(dtype), embed_ids(self.reader, tail)])

    # ------------------------------------------------------------------ training loss

    def loss(self, batch: list[Prepared], teacher: list[tuple[torch.Tensor, torch.Tensor]] | None,
             lambda_kl: float) -> dict[str, torch.Tensor]:
        memories = self.encode_memory(batch)
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
                    "pairs": self.pairs, "reader": self.template.cfg["reader"], "template_hash": self.template.hash,
                    "chunk_tokens": self.chunk_tokens, "bm25": self.bm25, **(extra or {})}, path)


def load_vilatent(path: str | Path, reader, tokenizer, template: ReaderTemplate) -> ViLatent:
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    if ckpt["template_hash"] != template.hash:
        raise ValueError(f"{path} was trained with another reader template ({ckpt['template_hash']})")
    writer = build_writer(reader, tokenizer, ckpt["writer_config"])
    writer.load_state_dict(ckpt["state_dict"])
    writer.eval()
    return ViLatent(reader, tokenizer, template, writer, chunk_tokens=ckpt["chunk_tokens"], bm25=ckpt.get("bm25"),
                    pairs=ckpt.get("pairs"))
