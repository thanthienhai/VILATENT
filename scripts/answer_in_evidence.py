"""How often the gold answer survives text selection (checklist B3; CPU, reader tokenizer only).

For every question of each --data file and every budget ratio r, the text each method keeps is
checked against the gold answers:

  present    a gold answer occurs verbatim in the kept text
  truncated  absent, but the kept text holds the head of a sentence that contains the answer:
             the fill cut that sentence before the answer (the budget, not the ranking, lost it)
  absent     the rest

Methods: truncation, bm25 (the configured units, normally pyvi words without question words),
bm25_syllable (the G1 selector: syllables, all question syllables, --syllable-k1/--syllable-b),
and me_f<f>: the BM25 evidence of ViLatent-ME, budget k(r) − k(r·f), for every f with r·f ≤ 32.
Run on ViQuAD select only (gold answers of gate and test are not looked at).

Usage:
  python scripts/answer_in_evidence.py --reader Qwen/Qwen3.5-2B \
      --data data/tasks/viquad_select.jsonl data/tasks/viquad_long_select.jsonl \
      --out results/paper/select/answer_in_evidence.json
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from vilatent.baselines import BM25Sentences, TokenCounter, Truncation, load_bm25_params
from vilatent.budget import chunk_context, memory_budget
from vilatent.data import load_examples
from vilatent.model import MAX_POOL
from vilatent.text import split_sentences

HEAD_CHARS = 15  # a sentence counts as cut when its first characters are in the kept text


def outcome(text: str, context: str, answers: list[str]) -> str:
    if any(a in text for a in answers):
        return "present"
    for a, b in split_sentences(context):
        sentence = context[a:b]
        if any(ans in sentence for ans in answers) and sentence[:HEAD_CHARS] in text:
            return "truncated"
    return "absent"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True)
    ap.add_argument("--data", nargs="+", required=True)
    ap.add_argument("--ratios", type=int, nargs="+", default=[4, 8, 16])
    ap.add_argument("--factors", type=int, nargs="+", default=[2, 4, 8])
    ap.add_argument("--bm25-config", default="configs/bm25.json")
    ap.add_argument("--syllable-k1", type=float, default=2.0)
    ap.add_argument("--syllable-b", type=float, default=1.0)
    ap.add_argument("--chunk-tokens", type=int, default=512)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.reader)
    counter = TokenCounter(tokenizer, lead=" ")
    bm25 = load_bm25_params(args.bm25_config)
    selectors = {"truncation": Truncation(), "bm25": BM25Sentences(**bm25),
                 "bm25_syllable": BM25Sentences(args.syllable_k1, args.syllable_b, "syllable")}
    report = {"bm25": bm25, "syllable_bm25": {"k1": args.syllable_k1, "b": args.syllable_b}, "files": {}}
    for path in args.data:
        examples = load_examples(path, "qa", args.limit)
        lengths = {}
        for ex in examples:
            if ex.context not in lengths:
                lengths[ex.context] = chunk_context(ex.context, tokenizer, args.chunk_tokens, lead=" ").lengths
        table = {}
        for r in args.ratios:
            jobs = {name: (sel, 0) for name, sel in selectors.items()}
            jobs.update({f"me_f{f}": (selectors["bm25"], f) for f in args.factors if r * f <= MAX_POOL})
            for name, (sel, f) in jobs.items():
                counts, used, cache = Counter(), 0, {}
                for ex in examples:
                    k = memory_budget(lengths[ex.context], r)
                    budget = k - memory_budget(lengths[ex.context], r * f) if f else k
                    key = (ex.context, budget) if name == "truncation" else (ex.context, ex.question, budget)
                    if key not in cache:
                        cache[key] = sel.compress(ex.context, ex.question, budget, counter)
                    counts[outcome(cache[key], ex.context, ex.answers)] += 1
                    used += counter.count(cache[key])
                n = len(examples)
                table[f"{name}_r{r}"] = {**{k: counts[k] / n for k in ("present", "truncated", "absent")},
                                         "mean_tokens": used / n, "n": n}
                print(f"{Path(path).name} r={r} {name}: " + json.dumps(table[f"{name}_r{r}"]))
        report["files"][path] = table
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
