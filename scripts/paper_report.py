"""Report of one split × setting × budget ratio, and the pre-specified decision rule (checklist
A13, A24; fixed 25/10/2026, before any ViLatent run).

Reads every ``<method>_r<r>.jsonl`` of --results-dir (plus full.jsonl, none.jsonl) and the
choices made on select (choices.json: f* per setting and r, the frozen writer's f*, τ).

Roles:
  ME         vilatent_me_f<f*> (seed 0); with vilatent_me_f<f*>_s1 also pooled over seeds
             (descriptive: the decision uses seed 0 only, the second seed comes later)
  best hard  the highest-F1 of truncation, lead, llmlingua2, bm25, phobert (PhoBERT selector
             included, decision of 25/10/2026)
  prompt     prompt_bm25_f<f*>: learned context-free vectors + the same BM25 evidence
  others     vilatent_me_f<f*>_swap, frozen_me_f<frozen f*>, vilatent_m, vilatent_q (r = 4 only),
             vilatent_mef (cascade), vilatent_mef_logprob

Every difference is paired on the same questions, with a cluster bootstrap (10,000 replicates):
clusters = articles (primary; ViQuAD-Long has 16 gate and 19 test articles) and passages
(secondary).

--decide (gate split, setting long, r = 4): ME passes when
  1. F1(ME) − F1(best hard) ≥ 3 and the article-level 95% CI lower bound > 0;
  2. the article-level 95% CI lower bound of F1(ME) − F1(prompt) > 0;
  3. ME and the best hard compressor each have < 2% unreadable answers.
The result goes to decision.json in the parent of --results-dir (results/paper/gate/).

Usage:
  python scripts/paper_report.py --results-dir results/paper/gate/long --setting long --ratio 4 \
      --choices results/paper/select/choices.json --decide
"""
import argparse
import json
from pathlib import Path

from vilatent.data import read_jsonl
from vilatent.stats import mde, paired_test

HARD = ["truncation", "lead", "llmlingua2", "bm25", "phobert"]
HARD_GROUPS = {"without_question": ["truncation", "lead", "llmlingua2"], "with_question": ["bm25", "phobert"]}
THRESHOLD_F1 = 3.0
MAX_UNREADABLE = 0.02


def load_results(d: Path, ratio: int) -> dict[str, dict[str, dict]]:
    suffix = f"_r{ratio}.jsonl"
    out = {p.name[:-len(suffix)]: p for p in d.glob(f"*{suffix}")}
    out.update({m: d / f"{m}.jsonl" for m in ("full", "none") if (d / f"{m}.jsonl").exists()})
    return {name: {r["id"]: r for r in read_jsonl(path)} for name, path in sorted(out.items())}


def stats_of(rows: list[dict]) -> dict:
    n = len(rows)
    out = {"f1": 100 * sum(r["f1"] for r in rows) / n, "em": 100 * sum(r["em"] for r in rows) / n,
           "unreadable_rate": sum(r["unreadable"] for r in rows) / n,
           "mean_used_tokens": sum(r["used_tokens"] for r in rows) / n,
           "empty_context_rate": sum(r["used_tokens"] == 0 for r in rows) / n,
           "mean_answer_syllables": sum(len(r["prediction"].split()) for r in rows) / n, "n_rows": n}
    if rows[0].get("aie") is not None:
        out["aie_rate"] = sum(bool(r["aie"]) for r in rows) / n
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--setting", required=True, help="long or single (key in choices.json)")
    ap.add_argument("--ratio", type=int, default=4)
    ap.add_argument("--choices", required=True)
    ap.add_argument("--decide", action="store_true", help="apply the decision rule (gate, long, r = 4 only)")
    ap.add_argument("--n-boot", type=int, default=10_000)
    args = ap.parse_args()

    d, r = Path(args.results_dir), args.ratio
    entry = json.loads(Path(args.choices).read_text(encoding="utf-8"))["settings"][args.setting][str(r)]
    f_star, frozen_f = entry["f_star"], entry.get("frozen_f_star")
    every = load_results(d, r)
    me = f"vilatent_me_f{f_star}"
    if me not in every:
        raise SystemExit(f"missing {me}_r{r}.jsonl in {d}")
    ids = sorted(every[me])
    for name, rows in every.items():
        if set(rows) != set(ids):
            raise SystemExit(f"{name} was not evaluated on the same questions as {me}")
    passage = {i: every[me][i]["cluster"] for i in ids}
    article = {i: every[me][i]["title"] or passage[i] for i in ids}
    roles = {"me": me, "me_s1": f"{me}_s1", "prompt": f"prompt_bm25_f{f_star}", "swap": f"{me}_swap",
             "frozen": f"frozen_me_f{frozen_f}" if frozen_f else None, "m": "vilatent_m", "q": "vilatent_q",
             "mef": "vilatent_mef", "mef_logprob": "vilatent_mef_logprob"}
    roles = {k: v for k, v in roles.items() if v in every}

    def diff(a: list[str], b: str) -> dict:
        """Paired F1 difference (a may hold several seeds of one system, each paired with b),
        with article clusters (primary) and passage clusters (secondary)."""
        x, y, seeds, keys = [], [], [], []
        for s, name in enumerate(a):
            for i in ids:
                x.append(100 * every[name][i]["f1"])
                y.append(100 * every[b][i]["f1"])
                seeds.append(s)
                keys.append(i)
        out = {}
        for level, cluster in (("article", article), ("passage", passage)):
            if len({cluster[i] for i in ids}) >= 2:
                out[level] = paired_test(x, y, [cluster[i] for i in keys], seeds, n_boot=args.n_boot)
        return out

    table = {name: stats_of(list(rows.values())) for name, rows in every.items()}
    seeds = [me] + ([roles["me_s1"]] if "me_s1" in roles else [])
    if len(seeds) > 1:
        table["ME, seeds pooled"] = stats_of([row for m in seeds for row in every[m].values()])
    hard = [m for m in HARD if m in every]
    missing = [m for m in HARD if m not in every]
    best = max(hard, key=lambda m: table[m]["f1"], default=None)
    by_group = {g: max((m for m in ms if m in every), key=lambda m: table[m]["f1"], default=None)
                for g, ms in HARD_GROUPS.items()}
    pairs = {f"ME - {m}": ([me], m) for m in hard + ["full", "none"] if m in every}
    pairs.update({f"ME - {role}": ([me], roles[role]) for role in ("prompt", "swap", "frozen", "m") if role in roles})
    if "m" in roles and best:
        pairs[f"M - {best}"] = (["vilatent_m"], best)
    if "q" in roles and "m" in roles:
        pairs["Q - M"] = (["vilatent_q"], "vilatent_m")
    if "q" in roles:
        pairs["ME - Q"] = ([me], "vilatent_q")
    if len(seeds) > 1 and best:
        pairs[f"ME seeds pooled - {best}"] = (seeds, best)
    for role in ("mef", "mef_logprob"):
        if role in roles and "full" in every:
            pairs[f"{role} - full"] = ([roles[role]], "full")
    diffs = {name: diff(a, b) for name, (a, b) in pairs.items()}
    main_test = diffs.get(f"ME - {best}", {}).get("article")
    control = diffs.get("ME - prompt", {}).get("article")
    unreadable_ok = {m: t["unreadable_rate"] < MAX_UNREADABLE for m, t in table.items()}
    report = {
        "setting": args.setting, "ratio": r, "results_dir": str(d), "f_star": f_star, "frozen_f_star": frozen_f,
        "roles": roles, "n_questions": len(ids), "n_passages": len(set(passage.values())),
        "n_articles": len(set(article.values())), "methods": table, "missing_hard_baselines": missing,
        "best_hard": best, "best_hard_by_group": by_group, "differences": diffs,
        "mde_80pct_power_article": mde(main_test["se"]) if main_test else None,
        "retention_vs_full": table[me]["f1"] / table["full"]["f1"] if table.get("full", {}).get("f1") else None,
        "unreadable_ok": unreadable_ok,
    }
    if args.decide:
        if not (args.setting == "long" and r == 4 and d.parent.name == "gate"):
            raise SystemExit("the decision rule is pre-specified for the gate split, ViQuAD-Long, r = 4")
        conditions = {
            "all_hard_baselines": not missing,
            "prompt_control_present": control is not None,
            "diff_vs_best_hard_ge_threshold": bool(main_test and main_test["diff"] >= THRESHOLD_F1),
            "diff_vs_best_hard_ci_low_gt_0": bool(main_test and main_test["ci_low"] > 0),
            "diff_vs_prompt_ci_low_gt_0": bool(control and control["ci_low"] > 0),
            "unreadable_me_and_best_hard": bool(best) and unreadable_ok[me] and unreadable_ok[best],
        }
        decision = {"criterion": (f"gate, ViQuAD-Long, r=4, ME at f*={f_star} (seed 0): ME - best hard "
                                  f"(over {HARD}) >= {THRESHOLD_F1} F1 with article-level 95% CI lower bound > 0; "
                                  f"ME - prompt control with article-level 95% CI lower bound > 0; unreadable < "
                                  f"{MAX_UNREADABLE:.0%} for ME and the best hard compressor"),
                    "conditions": conditions, "pass": all(conditions.values()), "best_hard": best,
                    "diff_vs_best_hard": main_test, "diff_vs_prompt": control,
                    "f1": {m: table[m]["f1"] for m in (me, best, roles.get("prompt")) if m}}
        report["decision"] = decision
        (d.parent / "decision.json").write_text(json.dumps(decision, indent=2), encoding="utf-8")
    out = d / f"report_r{r}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"{d} r={r}: {len(ids)} questions, {report['n_passages']} passages, {report['n_articles']} articles; "
          f"f* = {f_star}")
    print("| method | F1 | EM | unreadable | tokens | empty ctx | answer syl. |\n|---|---|---|---|---|---|---|")
    for name, t in sorted(table.items(), key=lambda kv: -kv[1]["f1"]):
        print(f"| {name} | {t['f1']:.2f} | {t['em']:.2f} | {t['unreadable_rate']:.1%} | {t['mean_used_tokens']:.1f} "
              f"| {t['empty_context_rate']:.1%} | {t['mean_answer_syllables']:.1f} |")
    print()
    for name, levels in diffs.items():
        cells = [f"{lv}: {t['diff']:+.2f} [{t['ci_low']:.2f}, {t['ci_high']:.2f}]" for lv, t in levels.items()]
        print(f"  {name}: " + "; ".join(cells))
    if missing:
        print(f"WARNING: hard baselines not evaluated: {missing}")
    if bad := [m for m, ok in unreadable_ok.items() if not ok]:
        print(f"WARNING: {MAX_UNREADABLE:.0%} or more unreadable answers: {bad}")
    if args.decide:
        failed = [c for c, ok in report["decision"]["conditions"].items() if not ok]
        print(f"DECISION: {'PASS' if report['decision']['pass'] else 'FAIL'}"
              + (f"; failed: {failed}" if failed else "") + f" -> {d.parent / 'decision.json'}")


if __name__ == "__main__":
    main()
