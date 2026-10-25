"""Tune k1 and b of the BM25 sentence selection on ViQuAD select, before any ViLatent run (decision
of 22/10/2026; docs/VILATENT.md, "Nội tại": hard baselines are tuned as much as the method).
Re-run on 25/10/2026 after the switch to pyvi words without question words (``--units word``,
the default; G1 tuned syllables: k1 = 2.0, b = 1.0).

For every (k1, b) of the grid, the bm25 baseline compresses each context of --data to the
budget k of --ratio and the reader answers greedily, exactly as scripts/evaluate.py does; the
pair with the highest mean F1 wins (ties: the earlier pair in the grid, which starts with the
textbook values 1.5 / 0.75). Prompts that several pairs share are generated once. The result
goes to configs/bm25.json, read by the bm25 baseline and by ViLatent-ME (its sentences), and
is fixed before training. The select split is disjoint from the gate split by article.

Usage:
  python scripts/tune_bm25.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
      --data data/tasks/viquad_select.jsonl --out configs/bm25.json
"""
import argparse
import itertools
import json
from pathlib import Path

from vilatent.baselines import BM25Sentences, TokenCounter
from vilatent.budget import context_budget
from vilatent.data import load_examples, sha256_file
from vilatent.evaluate import MAX_NEW_TOKENS, _generate_sorted
from vilatent.metrics import parse_answer, score_qa
from vilatent.reader import DTYPES, QUANTS, decode, embed_ids, eos_ids, load_reader
from vilatent.template import ReaderTemplate, load_reader_config


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True)
    ap.add_argument("--reader-config", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--ratio", type=int, default=4)
    ap.add_argument("--k1", type=float, nargs="+", default=[1.5, 0.9, 1.2, 2.0])
    ap.add_argument("--b", type=float, nargs="+", default=[0.75, 0.3, 0.5, 1.0])
    ap.add_argument("--units", choices=["word", "syllable"], default="word")
    ap.add_argument("--chunk-tokens", type=int, default=512)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default="configs/bm25.json")
    ap.add_argument("--dtype", choices=list(DTYPES), default="bfloat16", help="float16 on GPUs without bf16 (T4)")
    ap.add_argument("--quant", choices=list(QUANTS), default="none")
    args = ap.parse_args()

    reader, tokenizer = load_reader(args.reader, dtype=args.dtype, quant=args.quant)
    template = ReaderTemplate(load_reader_config(args.reader_config), tokenizer)
    examples = load_examples(args.data, "qa", args.limit)
    counter = TokenCounter(tokenizer, lead=template.lead["qa"])
    budgets = {ex.context: context_budget(ex.context, tokenizer, args.ratio, args.chunk_tokens,
                                          lead=template.lead["qa"])[1] for ex in examples}
    grid = list(itertools.product(args.k1, args.b))
    prompts, per_pair = {}, {}  # prompt ids -> index; pair -> prompt index of every question
    for k1, b in grid:
        selector = BM25Sentences(k1, b, args.units)
        idx = []
        for ex in examples:
            ids = tuple(template.text_prompt("qa", selector.compress(ex.context, ex.question, budgets[ex.context],
                                                                     counter), ex.question))
            idx.append(prompts.setdefault(ids, len(prompts)))
        per_pair[(k1, b)] = idx
    print(f"{len(grid)} pairs x {len(examples)} questions -> {len(prompts)} distinct prompts")
    gens = _generate_sorted(reader, [embed_ids(reader, list(p)) for p in prompts], eos_ids(reader, template.eos_id),
                            args.batch_size, MAX_NEW_TOKENS["qa"], "bm25 grid")
    answers = [parse_answer(decode(tokenizer, g)[1]) for g in gens]
    results = []
    for (k1, b), idx in per_pair.items():
        scores = [score_qa(answers[j], ex.answers) for j, ex in zip(idx, examples)]
        results.append({"k1": k1, "b": b, "f1": 100 * sum(s["f1"] for s in scores) / len(scores),
                        "em": 100 * sum(s["em"] for s in scores) / len(scores)})
    best = max(results, key=lambda r: r["f1"])  # max keeps the first of equal values
    cfg = {"k1": best["k1"], "b": best["b"], "units": args.units,
           "criterion": f"highest mean F1 of the bm25 baseline at {args.ratio}x on {args.data}",
           "data": args.data, "data_sha256": sha256_file(args.data), "n_questions": len(examples),
           "reader": args.reader, "dtype": args.dtype, "quant": args.quant, "ratio": args.ratio, "grid": results}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    for r in sorted(results, key=lambda r: -r["f1"]):
        print(f"k1={r['k1']:<4} b={r['b']:<5} F1 {r['f1']:.2f} EM {r['em']:.2f}")
    print(f"chosen k1={best['k1']} b={best['b']} -> {args.out}")


if __name__ == "__main__":
    main()
