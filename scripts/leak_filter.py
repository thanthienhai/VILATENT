"""Drop training rows that share a 13-syllable n-gram with any evaluation context.

Run on every training file before use (docs/VILATENT.md §Dữ liệu): stage-1 pairs, ViQuAD
train, generated QA. The fields checked are those present among context, target, question.

Usage:
  python scripts/leak_filter.py --input data/tasks/viquad_train.jsonl \
      --eval-files data/tasks/viquad_gate.jsonl ... data/eval_ext/vietnews_test.jsonl \
      --out data/tasks/viquad_train_clean.jsonl
"""
import argparse
import json

from vilatent.data import read_jsonl, write_jsonl, write_meta
from vilatent.leak import LeakIndex, read_contexts

FIELDS = ("context", "target", "question")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--eval-files", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    index = LeakIndex(read_contexts(args.eval_files))
    rows = read_jsonl(args.input)
    kept = [r for r in rows if not any(index.leaks(r[f]) for f in FIELDS if f in r)]
    write_jsonl(args.out, kept)
    stats = {"n_input": len(rows), "kept": len(kept), "dropped": len(rows) - len(kept)}
    write_meta(args.out, input=args.input, eval_files=args.eval_files, ngram=index.n, **stats)
    print(json.dumps(stats))


if __name__ == "__main__":
    main()
