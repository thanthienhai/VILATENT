"""Precompute the teacher's top-20 log probabilities on the target tokens of a data file.

The teacher is the frozen reader reading the full context with the fixed template
(``enable_thinking=False`` is part of the rendered template). Run once per data file and
reader; the output is tied to the template hash.

Usage:
  python scripts/precompute_teacher.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
      --data data/stage1/pairs_train.jsonl --task continue --out data/teacher/qwen3.5-2b/pairs_train.pt
"""
import argparse
import json

from vilatent.data import load_examples
from vilatent.reader import DTYPES, QUANTS, load_reader
from vilatent.teacher import compute_teacher, save_teacher
from vilatent.template import ReaderTemplate, load_reader_config


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True)
    ap.add_argument("--reader-config", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--task", choices=["qa", "continue"], required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--k", type=int, default=20)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--dtype", choices=list(DTYPES), default="bfloat16", help="float16 on GPUs without bf16 (T4)")
    ap.add_argument("--quant", choices=list(QUANTS), default="none", help="int4 reader: T4 smoke test only")
    args = ap.parse_args()

    reader, tokenizer = load_reader(args.reader, dtype=args.dtype, quant=args.quant)
    template = ReaderTemplate(load_reader_config(args.reader_config), tokenizer)
    examples = load_examples(args.data, args.task, args.limit)
    records = compute_teacher(reader, template, examples, k=args.k, batch_size=args.batch_size)
    save_teacher(args.out, records, template, args.k, source=args.data)
    nll = sum(r["nll"] for r in records.values()) / len(records)
    print(json.dumps({"examples": len(records), "teacher_mean_nll": nll, "template_hash": template.hash}))


if __name__ == "__main__":
    main()
