"""ViLatent-MEF (H7): choose τ on ViQuAD select, or apply that fixed τ elsewhere.

select: reads <dir>/<me>_r<r>.jsonl and <dir>/full.jsonl, writes the whole trade-off curve
        (F1, fallback rate, mean reader tokens, confident-but-wrong rate for every τ), the
        chosen operating point (smallest τ with F1 ≥ 95% of full context) to mef_tau_r<r>.json,
        and the combined rows to vilatent_mef_r<r>.jsonl (so g1_report.py lists them).
gate, ViWord-C dev, test: the same with --tau-file pointing to the select choice; τ is not
        chosen again.

Usage:
  python scripts/fallback_report.py --results-dir results/g1/select --ratio 4 --me vilatent_me_f4
  python scripts/fallback_report.py --results-dir results/g1/gate --ratio 4 --me vilatent_me_f4 \
      --tau-file results/g1/select/mef_tau_r4.json
"""
import argparse
import json
from pathlib import Path

from vilatent.data import read_jsonl, write_jsonl
from vilatent.evaluate import summarize
from vilatent.fallback import choose_tau, combine, curve, operating_point


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--ratio", type=int, default=4)
    ap.add_argument("--me", default="vilatent_me", help="method name of the ME rows")
    ap.add_argument("--target", type=float, default=0.95, help="share of full-context F1 to reach on dev")
    ap.add_argument("--tau-file", default=None, help="apply this dev-chosen τ instead of choosing one")
    args = ap.parse_args()

    d = Path(args.results_dir)
    me_rows = read_jsonl(d / f"{args.me}_r{args.ratio}.jsonl")
    full_rows = read_jsonl(d / "full.jsonl")
    points = curve(me_rows, full_rows)
    if args.tau_file:
        tau = json.loads(Path(args.tau_file).read_text(encoding="utf-8"))["tau"]
        rows = combine(me_rows, full_rows, tau)
        full_f1 = 100 * sum(r["f1"] for r in full_rows) / len(full_rows)
        chosen = {"tau": tau, "source": args.tau_file, **operating_point(rows, full_f1)}
    else:
        chosen = choose_tau(me_rows, full_rows, args.target)
        rows = combine(me_rows, full_rows, chosen["tau"])
        (d / f"mef_tau_r{args.ratio}.json").write_text(json.dumps(chosen, indent=2), encoding="utf-8")
    (d / f"mef_curve_r{args.ratio}.json").write_text(json.dumps(points, indent=2), encoding="utf-8")
    write_jsonl(d / f"vilatent_mef_r{args.ratio}.jsonl", rows)
    (d / f"vilatent_mef_r{args.ratio}.summary.json").write_text(
        json.dumps({**summarize(rows), **chosen}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(chosen, indent=2))


if __name__ == "__main__":
    main()
