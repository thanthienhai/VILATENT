"""QA evaluation of ViLatent and of the text methods on the same reader and the same budget.

Both paths end in ``reader.greedy_generate`` on input embeddings with the same template and
``max_new_tokens``. One row per question:

  id, cluster (passage), title (article), method, ratio, n_tokens (context, reader tokens),
  budget (k), used_tokens, prediction, raw, f1, em, unreadable, repetitive, confidence (mean
  log-prob of the answer), aie (answer in evidence: the prediction's syllables occur contiguously
  in the text the reader got; None for memory-only reading and for the unbudgeted references),
  and passage_index / n_passages / position on ViQuAD-Long

ViLatent rows also give factor (f), pool (ρ = r·f), memory_vectors and evidence_tokens (ME):
used_tokens is their sum. The cascade (vilatent.fallback) uses aie and confidence.

Swapped memory (control of the review of 22/10/2026, ``swap_seed``): every question is read
with the memory of another context, from another article when possible, cut to the same
number of vectors, while its own BM25 sentences stay. ME minus this shows what the memory
content adds; the vector count, the sentences and the trained boundaries are unchanged.
"""
from __future__ import annotations

import random

import torch
from tqdm import tqdm

from .baselines import TokenCounter
from .budget import DEFAULT_CHUNK_TOKENS, context_budget
from .data import QA_EXTRA, Example
from .metrics import is_repetitive, is_unreadable, parse_answer, score_qa
from .model import ViLatent
from .reader import Generation, decode, embed_ids, eos_ids, greedy_generate
from .template import ReaderTemplate
from .text import contains_syllables

# With the Qwen3.5 tokenizer and the end-of-turn token, the shortest gold answer of a question
# needs more than 128 tokens for 1 of the 1,228 gate questions and for none in select, the
# ViWord-C dev or test (6–10% of the answers need more than 32), so an answer that does not
# end within the limit is almost never a correct one cut short.
MAX_NEW_TOKENS = {"qa": 128}
QUERY_AGNOSTIC = {"full", "none", "truncation", "lead", "llmlingua2"}
NO_BUDGET = {"full", "none"}
MAX_BATCH_TOKENS = 32_768  # prompt tokens per generation batch (ViQuAD-Long articles reach ~18k tokens)


def make_row(ex: Example, method: str, ratio: int | None, n_tokens: int, budget: int | None,
             used: int, raw: str, clean: str, generation: Generation, evidence: str | None = None, **extra) -> dict:
    prediction = parse_answer(clean)
    return {"id": ex.id, "cluster": ex.cluster, "title": ex.extra.get("title"), "method": method, "ratio": ratio,
            "n_tokens": n_tokens,
            "budget": budget, "used_tokens": used, "prediction": prediction, "raw": raw,
            **score_qa(prediction, ex.answers), "unreadable": is_unreadable(raw, generation.stopped),
            "repetitive": is_repetitive(clean), "confidence": generation.confidence,
            "aie": None if evidence is None else contains_syllables(evidence, prediction), **extra,
            **{k: v for k, v in ex.extra.items() if k in QA_EXTRA and k != "title"}}


def length_batches(lengths: list[int], batch_size: int, max_batch_tokens: int | None) -> list[list[int]]:
    """Indices sorted by length, cut into batches of at most ``batch_size`` sequences and at most
    ``max_batch_tokens`` padded tokens (a sequence longer than that is a batch of its own)."""
    order = sorted(range(len(lengths)), key=lambda i: lengths[i])
    batches, current = [], []
    for i in order:
        if current and (len(current) == batch_size
                        or (max_batch_tokens and (len(current) + 1) * lengths[i] > max_batch_tokens)):
            batches.append(current)
            current = []
        current.append(i)
    return batches + ([current] if current else [])


def _generate_sorted(reader, seqs: list[torch.Tensor], stop_ids: set[int], batch_size: int,
                     max_new_tokens: int, desc: str, max_batch_tokens: int | None = MAX_BATCH_TOKENS):
    """Greedy generation in batches of similar length; results in the input order."""
    out = [None] * len(seqs)
    for idx in tqdm(length_batches([s.shape[0] for s in seqs], batch_size, max_batch_tokens), desc=desc):
        for i, g in zip(idx, greedy_generate(reader, [seqs[i] for i in idx], max_new_tokens, stop_ids)):
            out[i] = g
    return out


def swap_memories(memory: dict, info: dict, seed: int) -> tuple[dict, dict]:
    """Give every context the memory of a donor: another context from another article (any
    other context when there is no other article), the one with the fewest vectors among
    those with at least as many, ties drawn with ``seed``; its vectors are cut to the
    receiver's count (the longest donor, repeated, when none is long enough). ``info``:
    key -> (article, number of memory vectors). Returns the new memory and the donor of
    every key."""
    rng = random.Random(seed)
    swapped, donors = {}, {}
    for key, (title, k_m) in info.items():
        others = [o for o in info if o != key and info[o][0] != title] or [o for o in info if o != key]
        if not others:
            raise ValueError("swapping memory needs at least two contexts")
        longer = [o for o in others if info[o][1] >= k_m]
        if longer:
            best = min(info[o][1] for o in longer)
            donor = rng.choice([o for o in longer if info[o][1] == best])
        else:
            donor = max(others, key=lambda o: info[o][1])
        inner = memory[donor][1:-1]
        inner = inner.repeat(-(-k_m // inner.shape[0]), 1)[:k_m]
        swapped[key] = torch.cat([memory[key][:1], inner, memory[key][-1:]])
        donors[key] = donor
    return swapped, donors


@torch.no_grad()
def evaluate_vilatent(model: ViLatent, examples: list[Example], ratio: int, factor: int = 1, batch_size: int = 16,
                      method: str = "vilatent", swap_seed: int | None = None,
                      max_batch_tokens: int | None = MAX_BATCH_TOKENS) -> list[dict]:
    """Read every question at budget ratio r = ``ratio`` with memory factor f = ``factor``.
    A question-blind memory is written once per distinct context and reused for all its
    questions; Q writes one memory per (context, question). ``swap_seed``: read every question
    with another context's memory (swap_memories)."""
    model.check_pair(ratio, factor)
    model.writer.eval()
    model.reader.eval()
    prepared = [model.prepare(ex, ratio, factor) for ex in tqdm(examples, desc="prepare")]
    first = {}
    for p in prepared:
        first.setdefault(model.memory_key(p), p)
    keys = list(first)
    memory = {}
    for start in tqdm(range(0, len(keys), batch_size), desc="write memory"):
        part = [first[k] for k in keys[start:start + batch_size]]
        for key, m in zip(keys[start:start + batch_size], model.encode_memory(part)):
            memory[key] = m
    donors = {}
    if swap_seed is not None:
        if model.sees_question:
            raise ValueError("ViLatent-Q memory depends on the question: it cannot be swapped between contexts")
        info = {k: (p.example.extra.get("title") or p.example.cluster, memory[k].shape[0] - 2)
                for k, p in first.items()}
        memory, donors = swap_memories(memory, info, swap_seed)
    seqs = [model.memory_prompt(p, memory[model.memory_key(p)]) for p in prepared]
    gens = _generate_sorted(model.reader, seqs, model.stop_ids, batch_size, MAX_NEW_TOKENS["qa"], method,
                            max_batch_tokens)
    rows = []
    for p, g in zip(prepared, gens):
        raw, clean = decode(model.tokenizer, g)
        k_m = memory[model.memory_key(p)].shape[0] - 2
        used = k_m + len(p.evidence_ids)
        if used > p.budget:
            raise RuntimeError(f"{method} exceeded the budget on {p.example.id}: {used} > {p.budget}")
        if donors:
            donor = first[donors[model.memory_key(p)]].example
            extra = {"memory_from": donor.extra.get("title") or donor.cluster}
        else:
            extra = {}
        rows.append(make_row(p.example, method, ratio, p.n_tokens, p.budget, used, raw, clean, g,
                             evidence=p.evidence if factor > 1 else None, factor=factor, pool=p.pool,
                             memory_vectors=k_m, evidence_tokens=len(p.evidence_ids), **extra))
    return rows


@torch.no_grad()
def evaluate_text(reader, tokenizer, template: ReaderTemplate, baseline, examples: list[Example],
                  ratio: int | None, chunk_tokens: int = DEFAULT_CHUNK_TOKENS, batch_size: int = 16,
                  budget_scale: int = 1, method: str | None = None,
                  max_batch_tokens: int | None = MAX_BATCH_TOKENS) -> list[dict]:
    """Compress every context to ``budget_scale`` × the budget k of ``ratio`` with ``baseline``,
    then read it. ``budget_scale`` = 2 gives stage 2 of the cascade (BM25 at 2k(r))."""
    method = method or baseline.name
    counter = TokenCounter(tokenizer, lead=template.lead["qa"])
    stop_ids = eos_ids(reader, template.eos_id)
    budgets, cache, items = {}, {}, []
    for ex in tqdm(examples, desc=f"compress {method}"):
        if ex.context not in budgets:
            budgets[ex.context] = context_budget(ex.context, tokenizer, ratio or 1, chunk_tokens,
                                                 lead=template.lead[ex.task])
        n_tokens, k = budgets[ex.context]
        budget = None if baseline.name in NO_BUDGET else budget_scale * k
        key = ex.context if baseline.name in QUERY_AGNOSTIC else (ex.context, ex.question)
        if key not in cache:
            cache[key] = baseline.compress(ex.context, ex.question, budget, counter)
        text = cache[key]
        used = counter.count(text)
        if budget is not None and used > budget:
            raise RuntimeError(f"{method} exceeded the budget on {ex.id}: {used} > {budget}")
        items.append((ex, n_tokens, budget, used, text, template.text_prompt(ex.task, text, ex.question)))
    seqs = [embed_ids(reader, ids) for *_, ids in items]
    gens = _generate_sorted(reader, seqs, stop_ids, batch_size, MAX_NEW_TOKENS["qa"], method, max_batch_tokens)
    rows = []
    for (ex, n_tokens, budget, used, text, _), g in zip(items, gens):
        raw, clean = decode(tokenizer, g)
        rows.append(make_row(ex, method, None if budget is None else ratio, n_tokens, budget, used,
                             raw, clean, g, evidence=None if budget is None else text, budget_scale=budget_scale))
    return rows


def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    used = [r["used_tokens"] for r in rows]
    summary = {"method": rows[0]["method"], "ratio": rows[0]["ratio"], "n": n,
               "n_clusters": len({r["cluster"] for r in rows}), "n_articles": len({r["title"] for r in rows}),
               "f1": 100 * sum(r["f1"] for r in rows) / n, "em": 100 * sum(r["em"] for r in rows) / n,
               "unreadable_rate": sum(r["unreadable"] for r in rows) / n,
               "repetitive_rate": sum(r["repetitive"] for r in rows) / n,
               "mean_answer_syllables": sum(len(r["prediction"].split()) for r in rows) / n,
               "empty_context_rate": sum(r["used_tokens"] == 0 for r in rows) / n,
               "mean_context_tokens": sum(r["n_tokens"] for r in rows) / n,
               "mean_used_tokens": sum(used) / n}
    if rows[0].get("aie") is not None:
        summary["aie_rate"] = sum(bool(r["aie"]) for r in rows) / n
    if rows[0]["budget"] is not None:
        summary["actual_ratio"] = sum(r["n_tokens"] for r in rows) / max(1, sum(used))
        summary["budget_use"] = sum(used) / max(1, sum(r["budget"] for r in rows))
    for key in ("factor", "pool"):
        if key in rows[0]:
            summary[key] = rows[0][key]
    if "evidence_tokens" in rows[0]:  # ViLatent: share of the budget held by evidence text (Table 3)
        summary["text_share"] = sum(r["evidence_tokens"] / r["budget"] for r in rows if r["budget"]) / n
    return summary
