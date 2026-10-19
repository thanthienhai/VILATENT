"""Gate G1 report on ViQuAD dev (docs/VILATENT.md §Cổng quyết định và lộ trình).

Criterion, fixed before the run: at budget ratio r (default 4), the main system ViLatent-ME
(rows ``vilatent_me``: the memory factor f chosen on dev loss by scripts/select_me.py) passes G1 when its mean F1 minus the mean F1 of the best hard baseline
(truncation, lead, bm25, llmlingua2; the best is the one with the highest mean F1 at that
ratio) is at least 3 F1 points AND the lower bound of its 95% cluster-bootstrap CI (passages
as clusters) is above 0 AND every method in the report has fewer than 2% unreadable answers
(docs/RUN_G0_G1.md, "Tiêu chí G1").

Also reported: F1/EM of every method, the best hard baseline of each group (without and with
the question), retention (F1 / full-context F1), the unreadable share of each method, the MDE
of the paired difference (used to size H2), and, descriptively, the other ViLatent
configurations found in the folder (vilatent_m, vilatent_w5, vilatent_mef) with the paired
differences W5 − M (H6: cost of the question-blind writer) and ME − M (what the sentences add).

Usage:
  python scripts/g1_report.py --results-dir results/g1_dev --ratio 4
"""
import argparse
import json
from pathlib import Path

from vilatent.data import read_jsonl
from vilatent.stats import mde, paired_test

HARD = ["truncation", "lead", "bm25", "llmlingua2"]
HARD_GROUPS = {"without_question": ["truncation", "lead", "llmlingua2"], "with_question": ["bm25"]}
OTHER_VILATENT = ["vilatent_me_f2", "vilatent_me_f4", "vilatent_me_f8", "vilatent_m", "vilatent_w5", "vilatent_mef"]
PAIRS = [("vilatent_w5", "vilatent_m"), ("vilatent_me", "vilatent_m")]
THRESHOLD_F1 = 3.0
MAX_UNREADABLE = 0.02


def load(results_dir: Path, stem: str) -> dict[str, dict] | None:
    path = results_dir / f"{stem}.jsonl"
    return {r["id"]: r for r in read_jsonl(path)} if path.exists() else None


def mean_f1(rows: dict) -> float:
    return 100 * sum(r["f1"] for r in rows.values()) / len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--ratio", type=int, default=4)
    ap.add_argument("--vilatent", default="vilatent_me", help="method name of the gated ViLatent rows")
    ap.add_argument("--n-boot", type=int, default=10_000)
    args = ap.parse_args()

    d = Path(args.results_dir)
    soft = load(d, f"{args.vilatent}_r{args.ratio}")
    if soft is None:
        raise SystemExit(f"missing {args.vilatent}_r{args.ratio}.jsonl in {d}")
    hard = {m: rows for m in HARD if (rows := load(d, f"{m}_r{args.ratio}")) is not None}
    missing = [m for m in HARD if m not in hard]
    refs = {m: rows for m in ("full", "none") if (rows := load(d, m)) is not None}
    others = {m: rows for m in OTHER_VILATENT if m != args.vilatent
              and (rows := load(d, f"{m}_r{args.ratio}")) is not None}

    ids = sorted(soft)
    for name, rows in {**hard, **refs, **others}.items():
        if set(rows) != set(ids):
            raise SystemExit(f"{name} was not evaluated on the same questions as {args.vilatent}")
    clusters = [soft[i]["cluster"] for i in ids]
    every = {args.vilatent: soft, **others, **hard, **refs}

    def diff(a: str, b: str) -> dict:
        return paired_test([100 * every[a][i]["f1"] for i in ids], [100 * every[b][i]["f1"] for i in ids],
                           clusters, n_boot=args.n_boot)

    table = {name: {"f1": mean_f1(rows), "em": 100 * sum(r["em"] for r in rows.values()) / len(rows),
                    "unreadable_rate": sum(r["unreadable"] for r in rows.values()) / len(rows),
                    "mean_used_tokens": sum(r["used_tokens"] for r in rows.values()) / len(rows)}
             for name, rows in every.items()}
    best = max(hard, key=lambda m: table[m]["f1"])
    test = diff(args.vilatent, best)
    unreadable_ok = {m: t["unreadable_rate"] < MAX_UNREADABLE for m, t in table.items()}
    passed = (test["diff"] >= THRESHOLD_F1 and test["ci_low"] > 0 and not missing
              and all(unreadable_ok.values()))
    by_group = {g: max((m for m in ms if m in hard), key=lambda m: table[m]["f1"], default=None)
                for g, ms in HARD_GROUPS.items()}
    report = {
        "ratio": args.ratio, "n_questions": len(ids), "n_passages": len(set(clusters)),
        "methods": table, "missing_hard_baselines": missing, "best_hard": best,
        "best_hard_by_group": by_group,
        "diff_vs_best_hard": test, "mde_80pct_power": mde(test["se"]),
        "diff_vs_best_hard_by_group": {g: diff(args.vilatent, m) for g, m in by_group.items() if m},
        "descriptive_pairs": {f"{a} - {b}": diff(a, b) for a, b in PAIRS if a in every and b in every},
        "retention_vs_full": table[args.vilatent]["f1"] / table["full"]["f1"] if "full" in table else None,
        "unreadable_ok": unreadable_ok,
        "criterion": (f"diff >= {THRESHOLD_F1} F1 and 95% CI lower bound > 0 and unreadable < "
                      f"{MAX_UNREADABLE:.0%} for every method"),
        "G1_pass": passed,
    }
    out = d / f"g1_report_r{args.ratio}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"| method | F1 | EM | unreadable | tokens |\n|---|---|---|---|---|")
    for name, t in sorted(table.items(), key=lambda kv: -kv[1]["f1"]):
        print(f"| {name} | {t['f1']:.2f} | {t['em']:.2f} | {t['unreadable_rate']:.1%} | {t['mean_used_tokens']:.1f} |")
    print(f"\n{args.vilatent} − {best}: {test['diff']:+.2f} F1, 95% CI [{test['ci_low']:.2f}, {test['ci_high']:.2f}], "
          f"MDE {report['mde_80pct_power']:.2f}")
    for name, t in {**report["diff_vs_best_hard_by_group"], **report["descriptive_pairs"]}.items():
        print(f"  {name}: {t['diff']:+.2f} F1, 95% CI [{t['ci_low']:.2f}, {t['ci_high']:.2f}]")
    if missing:
        print(f"WARNING: hard baselines not evaluated: {missing}; G1 needs all of them")
    if bad := [m for m, ok in unreadable_ok.items() if not ok]:
        print(f"WARNING: {MAX_UNREADABLE:.0%} or more unreadable answers: {bad}; G1 needs every method below it")
    print(f"G1: {'PASS' if passed else 'FAIL'} ({report['criterion']}) -> {out}")


if __name__ == "__main__":
    main()
