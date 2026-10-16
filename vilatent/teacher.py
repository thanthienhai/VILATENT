"""Teacher distributions, computed once and stored (docs/VILATENT.md §Chiến lược huấn luyện,
"Chi phí tính toán").

The teacher is the frozen reader itself reading the full context with the same fixed
template (self-distillation). For every target token we keep its top-K log probabilities
(K = 20); ``losses.topk_kl`` adds the remaining mass as a 21st bin. A teacher file is tied
to one rendered template (its hash) and refuses to be used with another one.
"""
from __future__ import annotations

from pathlib import Path

import torch
from tqdm import tqdm

from .data import Example
from .template import ReaderTemplate


def teacher_batches(examples: list[Example], template: ReaderTemplate, batch_size: int):
    """Tokenize, sort by length (less padding) and yield batches of (example, prompt, target)."""
    items = []
    for ex in examples:
        prompt = template.text_prompt(ex.task, ex.context, ex.question)
        items.append((ex, prompt, template.target_ids(ex.task, ex.target)))
    items.sort(key=lambda it: len(it[1]) + len(it[2]))
    for start in range(0, len(items), batch_size):
        yield items[start:start + batch_size]


@torch.no_grad()
def compute_teacher(reader, template: ReaderTemplate, examples: list[Example], k: int = 20,
                    batch_size: int = 8) -> dict[str, dict]:
    """``{id: {"ids": int32 (T, k), "logp": fp16 (T, k), "nll": float}}``; ``nll`` is the mean
    negative log likelihood of the target under the teacher (logged as a reference)."""
    device = reader.get_input_embeddings().weight.device
    pad = template.sink_id
    out = {}
    n_batches = (len(examples) + batch_size - 1) // batch_size
    for batch in tqdm(teacher_batches(examples, template, batch_size), total=n_batches, desc="teacher"):
        seqs = [p + t for _, p, t in batch]
        t_max = max(len(s) for s in seqs)
        ids = torch.full((len(seqs), t_max), pad, dtype=torch.long, device=device)
        mask = torch.zeros_like(ids)
        rows, cols = [], []
        for i, (s, (_, p, t)) in enumerate(zip(seqs, batch)):
            ids[i, :len(s)] = torch.tensor(s)
            mask[i, :len(s)] = 1
            rows += [i] * len(t)
            cols += list(range(len(p) - 1, len(s) - 1))
        hidden = reader.model(input_ids=ids, attention_mask=mask, use_cache=False).last_hidden_state
        logp = torch.log_softmax(reader.lm_head(hidden[torch.tensor(rows, device=device),
                                                       torch.tensor(cols, device=device)]).float(), -1)
        top = logp.topk(k, dim=-1)
        target = torch.tensor([x for _, _, t in batch for x in t], device=device)
        nll = -logp.gather(-1, target[:, None]).squeeze(-1)
        offset = 0
        for ex, _, t in batch:
            sl = slice(offset, offset + len(t))
            out[ex.id] = {"ids": top.indices[sl].int().cpu(), "logp": top.values[sl].half().cpu(),
                          "nll": float(nll[sl].mean())}
            offset += len(t)
    return out


def save_teacher(path: str | Path, records: dict, template: ReaderTemplate, k: int, source: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    torch.save({"template_hash": template.hash, "reader": template.cfg["reader"], "k": k,
                "source": source, "records": records}, path)


def load_teacher(path: str | Path, template: ReaderTemplate) -> dict:
    blob = torch.load(path, map_location="cpu", weights_only=False)
    if blob["template_hash"] != template.hash:
        raise ValueError(f"{path}: teacher computed with another template ({blob['template_hash']} "
                         f"!= {template.hash}); recompute it with scripts/precompute_teacher.py")
    return blob["records"]
