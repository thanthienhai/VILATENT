"""Gate G1 report (docs/VILATENT.md §Cổng quyết định và lộ trình; criteria revised 22/10/2026).

Reads every ``<method>_r<r>.jsonl`` (and full.jsonl, none.jsonl) in --results-dir, and the
choices made on ViQuAD select before any evaluation (scripts/choose_by_loss.py):
me_choice_r<r>.json (memory factor f*) and pe_choice_r<r>.json (learning rate of the control).

Roles:
  ME         vilatent_me_f<f*> (seed 0) and vilatent_me_f<f*>_s1 (seed 1), pooled: one row per
             (question, seed), bootstrap over seeds × passages
  best hard  the hard baseline (truncation, lead, bm25, llmlingua2) with the highest mean F1
  prompt     prompt_bm25_f<f*>: learned context-independent vectors + the same BM25 sentences,
             trained like ME (the answer-style control), one seed

With --gate (ViQuAD gate, whole articles held out of training), G1 passes when
  1. F1(ME) − F1(best hard) ≥ 3 points and the 95% CI lower bound of that difference > 0;
  2. the 95% CI lower bound of F1(ME) − F1(prompt) > 0: the memory content helps, beyond
     what training on the answers teaches;
  3. ME and the best hard baseline each have fewer than 2% unreadable answers (the other
     methods' share is reported; a warning is printed when the prompt control reaches 2%).
Without --gate (auxiliary table, ViWord-C dev) the same numbers are printed, with no decision.

Also reported: every method (F1, EM, unreadable, tokens, empty contexts, answer length), the
best hard baseline of each group (without and with the question), the main differences again
with articles as clusters (sensitivity: passages of one article are not independent), the MDE
of the main difference, and descriptive pairs on seed 0: W5 − M, ME − M, and for each f the
ME minus the same ME with swapped memory (what the memory content adds at that f).

Usage:
  python scripts/g1_report.py --results-dir results/g1/gate --choices-dir results/g1 --ratio 4 --gate
"""
import argparse
import json
from pathlib import Path

from vilatent.data import read_jsonl
from vilatent.stats import mde, paired_test

HARD = ["truncation", "lead", "bm25", "llmlingua2"]
HARD_GROUPS = {"without_question": ["truncation", "lead", "llmlingua2"], "with_question": ["bm25"]}
THRESHOLD_F1 = 3.0
MAX_UNREADABLE = 0.02


def load_results(d: Path, ratio: int) -> dict[str, dict[str, dict]]:
    suffix = f"_r{ratio}.jsonl"
    out = {p.name[:-len(suffix)]: p for p in d.glob(f"*{suffix}")}
    out.update({m: d / f"{m}.jsonl" for m in ("full", "none") if (d / f"{m}.jsonl").exists()})
    return {name: {r["id"]: r for r in read_jsonl(path)} for name, path in sorted(out.items())}


def stats_of(rows: list[dict]) -> dict:
    n = len(rows)
    return {"f1": 100 * sum(r["f1"] for r in rows) / n, "em": 100 * sum(r["em"] for r in rows) / n,
            "unreadable_rate": sum(r["unreadable"] for r in rows) / n,
            "mean_used_tokens": sum(r["used_tokens"] for r in rows) / n,
            "empty_context_rate": sum(r["used_tokens"] == 0 for r in rows) / n,
            "mean_answer_syllables": sum(len(r["prediction"].split()) for r in rows) / n, "n_rows": n}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--choices-dir", required=True)
    ap.add_argument("--ratio", type=int, default=4)
    ap.add_argument("--gate", action="store_true", help="decide G1 (ViQuAD gate only)")
    ap.add_argument("--n-boot", type=int, default=10_000)
    args = ap.parse_args()

    d, r = Path(args.results_dir), args.ratio
    choices = Path(args.choices_dir)
    f_star = json.loads((choices / f"me_choice_r{r}.json").read_text(encoding="utf-8"))["memory_factor"]
    every = load_results(d, r)
    me_names = [m for m in (f"vilatent_me_f{f_star}", f"vilatent_me_f{f_star}_s1") if m in every]
    prompt_name = f"prompt_bm25_f{f_star}"
    if not me_names or me_names[0] != f"vilatent_me_f{f_star}":
        raise SystemExit(f"missing vilatent_me_f{f_star}_r{r}.jsonl in {d}")
    ids = sorted(every[me_names[0]])
    for name, rows in every.items():
        if set(rows) != set(ids):
            raise SystemExit(f"{name} was not evaluated on the same questions as {me_names[0]}")
    passage = {i: every[me_names[0]][i]["cluster"] for i in ids}
    article = {i: every[me_names[0]][i]["title"] or passage[i] for i in ids}

    def diff(a: list[str], b: str, cluster: dict) -> dict:
        """Paired F1 difference; ``a`` may hold several seeds of one system, each paired with b."""
        x, y, clusters, seeds = [], [], [], []
        for s, name in enumerate(a):
            for i in ids:
                x.append(100 * every[name][i]["f1"])
                y.append(100 * every[b][i]["f1"])
                clusters.append(cluster[i])
                seeds.append(s)
        return paired_test(x, y, clusters, seeds, n_boot=args.n_boot)

    table = {name: stats_of(list(rows.values())) for name, rows in every.items()}
    me_pooled = f"ME (f={f_star}, {len(me_names)} seed{'s' if len(me_names) > 1 else ''})"
    table[me_pooled] = stats_of([row for m in me_names for row in every[m].values()])
    hard = [m for m in HARD if m in every]
    missing = [m for m in HARD if m not in every]
    best = max(hard, key=lambda m: table[m]["f1"], default=None)
    main_test = diff(me_names, best, passage) if best else None
    control = diff(me_names, prompt_name, passage) if prompt_name in every else None
    by_article = {}  # sensitivity only: needs at least two articles (always true on ViQuAD gate)
    if len(set(article.values())) >= 2:
        if best:
            by_article[f"ME - {best}"] = diff(me_names, best, article)
        if control:
            by_article[f"ME - {prompt_name}"] = diff(me_names, prompt_name, article)
    by_group = {g: max((m for m in ms if m in every), key=lambda m: table[m]["f1"], default=None)
                for g, ms in HARD_GROUPS.items()}
    pairs = [("vilatent_w5", "vilatent_m"), (me_names[0], "vilatent_m"), (me_names[0], prompt_name)]
    pairs += [(f"vilatent_me_f{f}", f"vilatent_me_f{f}_swap") for f in (2, 4, 8)]
    unreadable_ok = {m: t["unreadable_rate"] < MAX_UNREADABLE for m, t in table.items()}
    report = {
        "ratio": r, "results_dir": str(d), "memory_factor": f_star, "me_runs": me_names,
        "n_questions": len(ids), "n_passages": len(set(passage.values())), "n_articles": len(set(article.values())),
        "methods": table, "missing_hard_baselines": missing, "best_hard": best, "best_hard_by_group": by_group,
        "diff_vs_best_hard": main_test, "mde_80pct_power": mde(main_test["se"]) if main_test else None,
        "diff_vs_prompt_control": control,
        "diff_vs_best_hard_by_group": {g: diff(me_names, m, passage) for g, m in by_group.items() if m},
        "article_clusters_sensitivity": by_article,
        "descriptive_pairs_seed0": {f"{a} - {b}": diff([a], b, passage) for a, b in pairs if a in every and b in every},
        "retention_vs_full": table[me_pooled]["f1"] / table["full"]["f1"] if "full" in table else None,
        "unreadable_ok": unreadable_ok,
    }
    if args.gate:
        conditions = {
            "seed_1_present": len(me_names) == 2,
            "all_hard_baselines": not missing,
            "diff_vs_best_hard_ge_threshold": bool(main_test and main_test["diff"] >= THRESHOLD_F1),
            "diff_vs_best_hard_ci_low_gt_0": bool(main_test and main_test["ci_low"] > 0),
            "diff_vs_prompt_ci_low_gt_0": bool(control and control["ci_low"] > 0),
            "unreadable_me_and_best_hard": bool(best) and unreadable_ok[me_pooled] and unreadable_ok[best],
        }
        report["criterion"] = (f"ME (f*, 2 seeds) - best hard >= {THRESHOLD_F1} F1 with 95% CI lower bound > 0, "
                               f"ME - prompt control with 95% CI lower bound > 0, and unreadable < "
                               f"{MAX_UNREADABLE:.0%} for ME and the best hard baseline")
        report["conditions"] = conditions
        report["G1_pass"] = all(conditions.values())
    out = d / (f"g1_report_r{r}.json" if args.gate else f"report_r{r}.json")
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"{d}: {len(ids)} questions, {report['n_passages']} passages, {report['n_articles']} articles")
    print("| method | F1 | EM | unreadable | tokens | empty ctx | answer syl. |\n|---|---|---|---|---|---|---|")
    for name, t in sorted(table.items(), key=lambda kv: -kv[1]["f1"]):
        print(f"| {name} | {t['f1']:.2f} | {t['em']:.2f} | {t['unreadable_rate']:.1%} | {t['mean_used_tokens']:.1f} "
              f"| {t['empty_context_rate']:.1%} | {t['mean_answer_syllables']:.1f} |")
    lines = {}
    if main_test:
        lines[f"{me_pooled} - {best} (best hard)"] = main_test
    if control:
        lines[f"{me_pooled} - {prompt_name}"] = control
    lines.update({f"{me_pooled} - {m} (best {g})": report["diff_vs_best_hard_by_group"][g]
                  for g, m in by_group.items() if m})
    lines.update({f"{k} [article clusters]": v for k, v in by_article.items()})
    lines.update(report["descriptive_pairs_seed0"])
    print()
    for name, t in lines.items():
        print(f"  {name}: {t['diff']:+.2f} F1, 95% CI [{t['ci_low']:.2f}, {t['ci_high']:.2f}]")
    if main_test:
        print(f"  MDE (80% power, two-sided 5%): {report['mde_80pct_power']:.2f} F1")
    if missing:
        print(f"WARNING: hard baselines not evaluated: {missing}")
    if args.gate and prompt_name in table and not unreadable_ok[prompt_name]:
        print(f"WARNING: the prompt control has {table[prompt_name]['unreadable_rate']:.1%} unreadable answers "
              f"(>= {MAX_UNREADABLE:.0%}): ME - prompt is hard to read")
    if bad := [m for m, ok in unreadable_ok.items() if not ok]:
        print(f"WARNING: {MAX_UNREADABLE:.0%} or more unreadable answers: {bad}")
    if args.gate:
        failed = [c for c, ok in report["conditions"].items() if not ok]
        print(f"G1: {'PASS' if report['G1_pass'] else 'FAIL'} ({report['criterion']})"
              + (f"; failed: {failed}" if failed else "") + f" -> {out}")
    else:
        print(f"auxiliary table, no gate decision -> {out}")


if __name__ == "__main__":
    main()
