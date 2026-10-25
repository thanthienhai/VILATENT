"""ViLatent-MEF (checklist A6/A19, B11): the cascade and the log-prob-only fallback at f*.

Reads, in --results-dir (one split and setting), the rows of ME at f* (vilatent_me_f<f*>_r<r>),
of BM25 at 2k(r) (bm25_x2_r<r>, stage 2) and of the full context (full). Writes:

  cascade_curve_r<r>.json   both curves, one point per τ: F1, retention vs full context, share
                            of questions answered at each stage, mean reader tokens, confident
                            but wrong (Figure 2)
  cascade_r<r>.json         the operating point of each curve at its τ, the token cost of each
                            stage, and the calibration (ECE) of ME, BM25 at 2k and full context
  vilatent_mef_r<r>.jsonl, vilatent_mef_logprob_r<r>.jsonl (+ .summary.json): rows at τ, so the
                            report scripts list them like any method

--choose (select only): τ of each curve = the cheapest point with F1 ≥ --target × full-context
F1, written into choices.json (scripts/choose_f.py made it). Without --choose (gate, test): the
τ of choices.json is applied unchanged.

Usage:
  python scripts/cascade_report.py --results-dir results/paper/select/long --setting long --ratio 4 \
      --choices results/paper/select/choices.json --choose
  python scripts/cascade_report.py --results-dir results/paper/test/long --setting long --ratio 4 \
      --choices results/paper/select/choices.json
"""
import argparse
import json
from pathlib import Path

from vilatent.data import read_jsonl, write_jsonl
from vilatent.evaluate import summarize
from vilatent.fallback import cascade, choose_tau, curve, ece, logprob_fallback, operating_point


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--setting", required=True, help="long or single (key in choices.json)")
    ap.add_argument("--ratio", type=int, default=4)
    ap.add_argument("--choices", required=True)
    ap.add_argument("--choose", action="store_true", help="choose τ here (select split only)")
    ap.add_argument("--target", type=float, default=0.95, help="share of full-context F1 to reach on select")
    args = ap.parse_args()

    d, r = Path(args.results_dir), args.ratio
    choices = json.loads(Path(args.choices).read_text(encoding="utf-8"))
    entry = choices["settings"][args.setting][str(r)]
    f = entry["f_star"]
    me = read_jsonl(d / f"vilatent_me_f{f}_r{r}.jsonl")
    bm = read_jsonl(d / f"bm25_x2_r{r}.jsonl")
    full = read_jsonl(d / "full.jsonl")
    full_f1 = 100 * sum(row["f1"] for row in full) / len(full)
    curves = {"cascade": curve(me, full, bm), "logprob": curve(me, full)}
    if args.choose:
        for name, points in curves.items():
            entry[f"tau_{name}"] = choose_tau(points, full_f1, args.target)["tau"]
        entry["tau_criterion"] = f"cheapest tau with F1 >= {args.target} x full-context F1 on select"
        Path(args.choices).write_text(json.dumps(choices, indent=2), encoding="utf-8")
    report = {"setting": args.setting, "ratio": r, "f_star": f, "full_f1": full_f1, "tau_source": args.choices,
              "stage_tokens": {"stage1_me_k": sum(x["used_tokens"] for x in me) / len(me),
                               "stage2_bm25_2k": sum(x["used_tokens"] for x in bm) / len(bm),
                               "stage3_full_n": sum(x["n_tokens"] for x in full) / len(full)},
              "ece": {"me": ece(me), "bm25_x2": ece(bm), "full": ece(full)}}
    for name, rows in (("cascade", cascade(me, bm, full, entry["tau_cascade"])),
                       ("logprob", logprob_fallback(me, full, entry["tau_logprob"]))):
        method = "vilatent_mef" if name == "cascade" else "vilatent_mef_logprob"
        report[name] = {"tau": entry[f"tau_{name}"], **operating_point(rows, full_f1)}
        write_jsonl(d / f"{method}_r{r}.jsonl", rows)
        (d / f"{method}_r{r}.summary.json").write_text(
            json.dumps({**summarize(rows), **report[name]}, indent=2, ensure_ascii=False), encoding="utf-8")
    (d / f"cascade_curve_r{r}.json").write_text(json.dumps(curves, indent=2), encoding="utf-8")
    (d / f"cascade_r{r}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("cascade", "logprob", "stage_tokens")}, indent=2))
    print(f"ECE: ME {report['ece']['me']['ece']:.3f}, BM25 2k {report['ece']['bm25_x2']['ece']:.3f}, "
          f"full {report['ece']['full']['ece']:.3f}")


if __name__ == "__main__":
    main()
