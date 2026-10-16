"""QA evaluation of ViLatent and of the text methods on the same reader and the same budget.

Both paths end in ``reader.greedy_generate`` on input embeddings with the same template and
``max_new_tokens``. One row per question:

  id, cluster, method, ratio, n_tokens (context, reader tokens), budget (k), used_tokens,
  prediction, raw, f1, em, unreadable, repetitive, confidence (mean log-prob of the answer)

ViLatent rows also give memory_vectors and evidence_tokens (ME): used_tokens is their sum.
"""
from __future__ import annotations

import torch
from tqdm import tqdm

from .baselines import TokenCounter
from .budget import DEFAULT_CHUNK_TOKENS, context_budget
from .data import Example
from .metrics import is_repetitive, is_unreadable, parse_answer, score_qa
from .model import ViLatent
from .reader import Generation, decode, embed_ids, eos_ids, greedy_generate
from .template import ReaderTemplate

# No gold answer of ViQuAD dev needs more than 128 Qwen3.5 tokens (10% need more than 32), so
# an answer that does not end within the limit is never a correct one cut short.
MAX_NEW_TOKENS = {"qa": 128}
QUERY_AGNOSTIC = {"full", "none", "truncation", "lead", "llmlingua2"}
NO_BUDGET = {"full", "none"}


def make_row(ex: Example, method: str, ratio: int | None, n_tokens: int, budget: int | None,
             used: int, raw: str, clean: str, generation: Generation, **extra) -> dict:
    prediction = parse_answer(clean)
    return {"id": ex.id, "cluster": ex.cluster, "method": method, "ratio": ratio, "n_tokens": n_tokens,
            "budget": budget, "used_tokens": used, "prediction": prediction, "raw": raw,
            **score_qa(prediction, ex.answers), "unreadable": is_unreadable(raw, generation.stopped),
            "repetitive": is_repetitive(clean), "confidence": generation.confidence, **extra,
            **{k: v for k, v in ex.extra.items() if k == "answer_type"}}


def _generate_sorted(reader, seqs: list[torch.Tensor], stop_ids: set[int], batch_size: int,
                     max_new_tokens: int, desc: str):
    """Greedy generation in batches of similar length; results in the input order."""
    order = sorted(range(len(seqs)), key=lambda i: seqs[i].shape[0])
    out = [None] * len(seqs)
    for start in tqdm(range(0, len(order), batch_size), desc=desc):
        idx = order[start:start + batch_size]
        for i, g in zip(idx, greedy_generate(reader, [seqs[i] for i in idx], max_new_tokens, stop_ids)):
            out[i] = g
    return out


@torch.no_grad()
def evaluate_vilatent(model: ViLatent, examples: list[Example], batch_size: int = 16,
                      method: str = "vilatent") -> list[dict]:
    """Memory is written once per distinct context and reused for all its questions (M, ME);
    W5 writes one memory per (context, question). ``ratio`` in the rows is the budget ratio r."""
    model.writer.eval()
    model.reader.eval()
    prepared = [model.prepare(ex) for ex in tqdm(examples, desc="prepare")]
    first = {}
    for p in prepared:
        first.setdefault(model.memory_key(p), p)
    keys = list(first)
    memory = {}
    for start in tqdm(range(0, len(keys), batch_size), desc="write memory"):
        part = [first[k] for k in keys[start:start + batch_size]]
        for key, m in zip(keys[start:start + batch_size],
                          model.encode_memory([p.chunks for p in part], [p.question_ids for p in part])):
            memory[key] = m
    seqs = [model.memory_prompt(p, memory[model.memory_key(p)]) for p in prepared]
    gens = _generate_sorted(model.reader, seqs, model.stop_ids, batch_size, MAX_NEW_TOKENS["qa"], method)
    rows = []
    for p, g in zip(prepared, gens):
        raw, clean = decode(model.tokenizer, g)
        k_m = memory[model.memory_key(p)].shape[0] - 2
        used = k_m + len(p.evidence_ids)
        if used > p.budget:
            raise RuntimeError(f"{method} exceeded the budget on {p.example.id}: {used} > {p.budget}")
        rows.append(make_row(p.example, method, model.budget_ratio, p.n_tokens, p.budget, used, raw, clean, g,
                             mode=model.mode, memory_vectors=k_m, evidence_tokens=len(p.evidence_ids)))
    return rows


@torch.no_grad()
def evaluate_text(reader, tokenizer, template: ReaderTemplate, baseline, examples: list[Example],
                  ratio: int | None, chunk_tokens: int = DEFAULT_CHUNK_TOKENS, batch_size: int = 16) -> list[dict]:
    """Compress every context to the budget k of ``ratio`` with ``baseline``, then read it."""
    counter = TokenCounter(tokenizer, lead=template.lead["qa"])
    stop_ids = eos_ids(reader, template.eos_id)
    budgets, cache, items = {}, {}, []
    for ex in tqdm(examples, desc=f"compress {baseline.name}"):
        if ex.context not in budgets:
            budgets[ex.context] = context_budget(ex.context, tokenizer, ratio or 1, chunk_tokens,
                                                 lead=template.lead[ex.task])
        n_tokens, k = budgets[ex.context]
        budget = None if baseline.name in NO_BUDGET else k
        key = ex.context if baseline.name in QUERY_AGNOSTIC else (ex.context, ex.question)
        if key not in cache:
            cache[key] = baseline.compress(ex.context, ex.question, budget, counter)
        text = cache[key]
        used = counter.count(text)
        if budget is not None and used > budget:
            raise RuntimeError(f"{baseline.name} exceeded the budget on {ex.id}: {used} > {budget}")
        items.append((ex, n_tokens, budget, used, template.text_prompt(ex.task, text, ex.question)))
    seqs = [embed_ids(reader, ids) for *_, ids in items]
    gens = _generate_sorted(reader, seqs, stop_ids, batch_size, MAX_NEW_TOKENS["qa"], baseline.name)
    rows = []
    for (ex, n_tokens, budget, used, _), g in zip(items, gens):
        raw, clean = decode(tokenizer, g)
        rows.append(make_row(ex, baseline.name, None if budget is None else ratio, n_tokens, budget, used,
                             raw, clean, g))
    return rows


def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    used = [r["used_tokens"] for r in rows]
    summary = {"method": rows[0]["method"], "ratio": rows[0]["ratio"], "n": n,
               "n_clusters": len({r["cluster"] for r in rows}),
               "f1": 100 * sum(r["f1"] for r in rows) / n, "em": 100 * sum(r["em"] for r in rows) / n,
               "unreadable_rate": sum(r["unreadable"] for r in rows) / n,
               "repetitive_rate": sum(r["repetitive"] for r in rows) / n,
               "mean_answer_syllables": sum(len(r["prediction"].split()) for r in rows) / n,
               "mean_context_tokens": sum(r["n_tokens"] for r in rows) / n,
               "mean_used_tokens": sum(used) / n}
    if rows[0]["budget"] is not None:
        summary["actual_ratio"] = sum(r["n_tokens"] for r in rows) / max(1, sum(used))
        summary["budget_use"] = sum(used) / max(1, sum(r["budget"] for r in rows))
    return summary
