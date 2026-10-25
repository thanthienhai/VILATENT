"""Evaluate methods on a QA file at given budget ratios; one JSONL of rows and one summary per
(method, ratio), named ``<method>_r<r>`` (``full`` and ``none`` have no ratio).

Text methods: full, none, truncation, lead, bm25, phobert (needs --selector), llmlingua2; a
``_x<s>`` suffix multiplies the budget by s (``bm25_x2``: stage 2 of the cascade, BM25 at 2k(r)).

ViLatent: ``vilatent:<checkpoint>[,f=<factors>][,tag=<tag>][,swap=<seed>]``. One checkpoint
serves every (r, f) it was trained on (multi-rate writer); it is read at every --ratios r with
the factors ``f`` ("1", "2+4+8" or "all", the default: every trained f at that r; pairs that
were not trained are skipped). Names:

  vilatent_m (f = 1), vilatent_me_f<f> (f ≥ 2)     the writer of the main run
  frozen_m, frozen_me_f<f>                         a frozen-writer checkpoint
  prompt_m, prompt_bm25_f<f>                       the learned-prompt control
  vilatent_q                                       a writer that sees the question (ViLatent-Q)

then ``_<tag>`` (e.g. tag=s1 for the second seed) and ``_swap`` with ``swap=<seed>`` (every
question reads another article's memory, vilatent.evaluate.swap_memories). BM25 (baseline and
ME evidence) uses --bm25-config; an ME checkpoint must have been trained with the same values.

Usage:
  python scripts/evaluate.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
      --data data/tasks/viquad_long_select.jsonl --ratios 4 8 16 \
      --methods full none truncation lead bm25 bm25_x2 phobert llmlingua2 vilatent:runs/paper/stage2_mem/best.pt \
      --selector runs/paper/selector --out-dir results/paper/select/long
"""
import argparse
import json
import re
from pathlib import Path

from vilatent.baselines import build_baseline, load_bm25_params
from vilatent.data import load_examples, write_jsonl
from vilatent.evaluate import MAX_BATCH_TOKENS, evaluate_text, evaluate_vilatent, summarize
from vilatent.model import load_vilatent
from vilatent.reader import DTYPES, QUANTS, load_reader
from vilatent.template import ReaderTemplate, load_reader_config


def save(rows: list[dict], out_dir: Path, stem: str) -> None:
    write_jsonl(out_dir / f"{stem}.jsonl", rows)
    summary = summarize(rows)
    (out_dir / f"{stem}.summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


def vilatent_name(model, factor: int, tag: str | None, swap: bool) -> str:
    cfg = model.writer.config()
    if model.sees_question:
        base = "vilatent_q"
    else:
        prefix = "prompt" if cfg.get("kind") == "prompt" else ("frozen" if cfg.get("frozen") else "vilatent")
        evidence = "_bm25" if prefix == "prompt" else "_me"
        base = f"{prefix}_m" if factor == 1 else f"{prefix}{evidence}_f{factor}"
    return base + (f"_{tag}" if tag else "") + ("_swap" if swap else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True)
    ap.add_argument("--reader-config", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--methods", nargs="+", required=True)
    ap.add_argument("--ratios", nargs="+", type=int, default=[4])
    ap.add_argument("--chunk-tokens", type=int, default=512)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--max-batch-tokens", type=int, default=MAX_BATCH_TOKENS,
                    help="prompt tokens per generation batch (lower it on a 16 GB GPU)")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--bm25-config", default="configs/bm25.json", help="tuned k1, b, units (scripts/tune_bm25.py)")
    ap.add_argument("--selector", default=None, help="trained PhoBERT selector (scripts/train_selector.py)")
    ap.add_argument("--skip-existing", action="store_true", help="do not redo a (method, ratio) already written")
    ap.add_argument("--dtype", choices=list(DTYPES), default="bfloat16", help="float16 on GPUs without bf16 (T4)")
    ap.add_argument("--quant", choices=list(QUANTS), default="none", help="int4 reader: T4 smoke test only")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    reader, tokenizer = load_reader(args.reader, dtype=args.dtype, quant=args.quant)
    template = ReaderTemplate(load_reader_config(args.reader_config), tokenizer)
    examples = load_examples(args.data, "qa", args.limit)
    bm25 = load_bm25_params(args.bm25_config)

    def done(stem: str) -> bool:
        return args.skip_existing and (out_dir / f"{stem}.summary.json").exists()

    for spec in args.methods:
        if spec.startswith("vilatent:"):
            path, _, opts = spec.removeprefix("vilatent:").partition(",")
            opts = dict(o.split("=", 1) for o in opts.split(",") if o)
            swap = int(opts["swap"]) if "swap" in opts else None
            model = load_vilatent(path, reader, tokenizer, template)
            if model.chunk_tokens != args.chunk_tokens:  # budgets of all methods must use the same chunks
                raise SystemExit(f"{path} uses chunks of {model.chunk_tokens} tokens, not {args.chunk_tokens}")
            if model.bm25 is not None and model.bm25 != bm25:
                raise SystemExit(f"{path} was trained with BM25 {model.bm25}, not those of {args.bm25_config}")
            for ratio in args.ratios:
                trained = sorted(f for r, f in model.pairs if r == ratio)
                wanted = trained if opts.get("f", "all") == "all" else [int(f) for f in opts["f"].split("+")]
                for factor in wanted:
                    if factor not in trained:
                        print(f"skip {path} at r={ratio}, f={factor}: not trained (pairs {model.pairs})")
                        continue
                    name = vilatent_name(model, factor, opts.get("tag"), swap is not None)
                    if done(f"{name}_r{ratio}"):
                        continue
                    rows = evaluate_vilatent(model, examples, ratio, factor, args.batch_size, method=name,
                                             swap_seed=swap, max_batch_tokens=args.max_batch_tokens)
                    save(rows, out_dir, f"{name}_r{ratio}")
            del model
            continue
        match = re.fullmatch(r"(.+?)(?:_x(\d+))?", spec)
        base, scale = match.group(1), int(match.group(2) or 1)
        baseline = build_baseline(base, bm25=bm25 if base == "bm25" else None, selector=args.selector)
        for ratio in [None] if base in ("full", "none") else args.ratios:
            stem = f"{spec}_r{ratio}" if ratio else spec
            if done(stem):
                continue
            rows = evaluate_text(reader, tokenizer, template, baseline, examples, ratio, args.chunk_tokens,
                                 args.batch_size, budget_scale=scale, method=spec,
                                 max_batch_tokens=args.max_batch_tokens)
            save(rows, out_dir, stem)


if __name__ == "__main__":
    main()
