"""Two-way check of auto-generated QA: keep a question only when the reader, reading the full
paragraph with the fixed template, answers it with F1 ≥ 0.8 (syllable F1 against the
teacher's verbatim answer). The leak filter runs first.

If more than 20% of the questions are rejected, the run prints a warning: the risk table of
docs/VILATENT.md then asks for a 200-sample human check and a smaller share of generated data.

Usage:
  python scripts/filter_qa.py --input data/qa_gen/qa_raw.jsonl --reader Qwen/Qwen3.5-2B \
      --reader-config configs/readers/qwen3.5-2b.json \
      --eval-files data/tasks/viquad_dev.jsonl data/tasks/viquad_test.jsonl --out data/qa_gen/qa_clean.jsonl
"""
import argparse
import json
from collections import Counter

from vilatent.baselines import Full
from vilatent.data import Example, read_jsonl, write_jsonl, write_meta
from vilatent.evaluate import evaluate_text
from vilatent.leak import LeakIndex
from vilatent.reader import DTYPES, QUANTS, load_reader
from vilatent.template import ReaderTemplate, load_reader_config

REJECTION_ALERT = 0.20


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/qa_gen/qa_raw.jsonl")
    ap.add_argument("--reader", required=True)
    ap.add_argument("--reader-config", required=True)
    ap.add_argument("--eval-files", nargs="+", required=True)
    ap.add_argument("--threshold", type=float, default=0.8)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--out", default="data/qa_gen/qa_clean.jsonl")
    ap.add_argument("--dtype", choices=list(DTYPES), default="bfloat16", help="float16 on GPUs without bf16 (T4)")
    ap.add_argument("--quant", choices=list(QUANTS), default="none", help="int4 reader: T4 smoke test only")
    args = ap.parse_args()

    rows = [r for r in read_jsonl(args.input) if not r.get("empty")]
    index = LeakIndex(list({r["context"] for path in args.eval_files for r in read_jsonl(path)}))
    leaked = {r["id"] for r in rows if index.leaks(r["context"]) or index.leaks(r["question"])}
    rows = [r for r in rows if r["id"] not in leaked]

    reader, tokenizer = load_reader(args.reader, dtype=args.dtype, quant=args.quant)
    template = ReaderTemplate(load_reader_config(args.reader_config), tokenizer)
    examples = [Example(r["id"], r["cluster"], "qa", r["context"], question=r["question"], answers=r["answers"],
                        target=r["answers"][0]) for r in rows]
    scored = {s["id"]: s for s in evaluate_text(reader, tokenizer, template, Full(), examples, None,
                                                batch_size=args.batch_size)}
    kept = [r for r in rows if scored[r["id"]]["f1"] >= args.threshold]
    write_jsonl(args.out, kept)

    by_type = Counter(r["answer_type"] for r in rows)
    kept_by_type = Counter(r["answer_type"] for r in kept)
    rejection = 1 - len(kept) / max(1, len(rows))
    stats = {"n_input": len(rows) + len(leaked), "leaked": len(leaked), "checked": len(rows), "kept": len(kept),
             "rejection_rate": rejection,
             "kept_share_by_type": {t: kept_by_type[t] / by_type[t] for t in by_type}}
    write_meta(args.out, input=args.input, reader=args.reader, template_hash=template.hash,
               f1_threshold=args.threshold, **stats)
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    if rejection > REJECTION_ALERT:
        print(f"WARNING: {rejection:.0%} rejected (> {REJECTION_ALERT:.0%}): check 200 samples by hand "
              "and lower the share of generated QA (docs/VILATENT.md, risk table)")


if __name__ == "__main__":
    main()
