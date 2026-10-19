"""Evaluate methods on a QA file at given compression ratios; one JSONL of rows and one summary
per (method, ratio).

Methods: full, none, truncation, lead, bm25, llmlingua2, and ``vilatent:<checkpoint>``. A
ViLatent run uses the mode and budget ratio it was trained for (--ratios is ignored for it) and
is named ``vilatent_<mode>`` (vilatent_m, vilatent_w5, and vilatent_me_f<f> for ME) unless
``name=`` follows after a comma, e.g. ``vilatent:runs/g1_stage2_me_f2_r4/best.pt,name=vilatent_me_s1``.

Usage:
  python scripts/evaluate.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
      --data data/tasks/viquad_dev.jsonl --ratios 4 \
      --methods full none truncation lead bm25 llmlingua2 vilatent:runs/g1_stage2_me_f2_r4/best.pt \
      --out-dir results/g1_dev
"""
import argparse
import json
from pathlib import Path

from vilatent.baselines import build_baseline
from vilatent.data import load_examples, write_jsonl
from vilatent.evaluate import evaluate_text, evaluate_vilatent, summarize
from vilatent.model import load_vilatent
from vilatent.reader import DTYPES, QUANTS, load_reader
from vilatent.template import ReaderTemplate, load_reader_config


def save(rows: list[dict], out_dir: Path, method: str, ratio) -> None:
    stem = f"{method}_r{ratio}" if ratio else method
    write_jsonl(out_dir / f"{stem}.jsonl", rows)
    summary = summarize(rows)
    (out_dir / f"{stem}.summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True)
    ap.add_argument("--reader-config", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--methods", nargs="+", required=True)
    ap.add_argument("--ratios", nargs="+", type=int, default=[4])
    ap.add_argument("--chunk-tokens", type=int, default=512)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--dtype", choices=list(DTYPES), default="bfloat16", help="float16 on GPUs without bf16 (T4)")
    ap.add_argument("--quant", choices=list(QUANTS), default="none", help="int4 reader: T4 smoke test only")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    reader, tokenizer = load_reader(args.reader, dtype=args.dtype, quant=args.quant)
    template = ReaderTemplate(load_reader_config(args.reader_config), tokenizer)
    examples = load_examples(args.data, "qa", args.limit)
    for spec in args.methods:
        if spec.startswith("vilatent:"):
            path, _, opts = spec.removeprefix("vilatent:").partition(",")
            model = load_vilatent(path, reader, tokenizer, template)
            default = f"vilatent_{model.mode.lower()}" + (f"_f{model.memory_factor}" if model.mode == "ME" else "")
            name = dict(o.split("=", 1) for o in opts.split(",") if o).get("name", default)
            if model.chunk_tokens != args.chunk_tokens:  # budgets of all methods must use the same chunks
                raise SystemExit(f"{path} uses chunks of {model.chunk_tokens} tokens, not {args.chunk_tokens}")
            save(evaluate_vilatent(model, examples, args.batch_size, method=name), out_dir, name, model.budget_ratio)
            del model
            continue
        baseline = build_baseline(spec)
        ratios = [None] if spec in ("full", "none") else args.ratios
        for ratio in ratios:
            rows = evaluate_text(reader, tokenizer, template, baseline, examples, ratio, args.chunk_tokens,
                                 args.batch_size)
            save(rows, out_dir, spec, ratio)


if __name__ == "__main__":
    main()
