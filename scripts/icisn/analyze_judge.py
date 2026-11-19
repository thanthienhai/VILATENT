"""G1.3/1.4: recompute the main test tables with ACC-LLM next to F1/EM (article bootstrap, 10 000, seed 0).
Usage: python scripts/icisn/analyze_judge.py [--ratios 4 8 16]  ->  results/icisn/judge/tables_r<r>.json"""
import argparse, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, ".")
from vilatent.stats import paired_test, bootstrap_mean

ROOT = Path(".")
LAB = ROOT / "results/icisn/judge/labels/test"
def rows(p): return {r["id"]: r for r in map(json.loads, open(p, encoding="utf-8"))}
def load(setting, stem):
    base = rows(ROOT / f"results/paper/test/{setting}/{stem}.jsonl")
    lab = {r["id"]: r["acc_llm"] for r in map(json.loads, open(LAB / setting / f"{stem}.jsonl", encoding="utf-8"))}
    return {i: dict(f1=100 * r["f1"], em=100 * r["em"], acc=100 * lab[i], aie=r.get("aie"), art=r["title"] or r["cluster"]) for i, r in base.items()}
def ci(d): return [round(d["diff"], 2), round(d["ci_low"], 2), round(d["ci_high"], 2)]
def mean_ci(v, arts):
    b = bootstrap_mean(v, arts, None, 10000, 0); return [round(float(np.mean(v)), 2), round(float(np.percentile(b, 2.5)), 2), round(float(np.percentile(b, 97.5)), 2)]
def sign(c): return 0 if c[1] <= 0 <= c[2] else (1 if c[0] > 0 else -1)
def interaction(dv, flags, arts, n_boot=10000):
    """mean(d | Out) - mean(d | In); bootstrap over articles."""
    ids = sorted(set(arts)); idx = {a: k for k, a in enumerate(ids)}
    S = np.zeros((len(ids), 2)); N = np.zeros((len(ids), 2))
    for d, f, a in zip(dv, flags, arts): S[idx[a], int(f)] += d; N[idx[a], int(f)] += 1   # f: 1 = gold in evidence (In)
    est = lambda S_, N_: S_[:, 0].sum() / N_[:, 0].sum() - S_[:, 1].sum() / N_[:, 1].sum()
    rng = np.random.default_rng(0); out = np.empty(n_boot)
    for b in range(n_boot):
        k = rng.integers(0, len(ids), len(ids)); out[b] = est(S[k], N[k])
    o = est(S, N)
    return [round(o, 2), round(float(np.percentile(out, 2.5)), 2), round(float(np.percentile(out, 97.5)), 2)]

ap = argparse.ArgumentParser(); ap.add_argument("--ratios", nargs="+", type=int, default=[4]); a = ap.parse_args()
PAIRS = [("ME", "prompt"), ("ME", "M"), ("ME", "bm25"), ("ME", "bm25_x2"), ("ME", "phobert"), ("M", "bm25"), ("M", "phobert"),
         ("M", "bm25_x2"), ("ME", "full"), ("M", "full"), ("ME", "none"), ("M", "none")]
for r in a.ratios:
    res = {}
    for s in ("single", "long"):
        stems = {"full": "full", "none": "none", "truncation": f"truncation_r{r}", "lead": f"lead_r{r}", "llmlingua2": f"llmlingua2_r{r}",
                 "bm25": f"bm25_r{r}", "bm25_x2": f"bm25_x2_r{r}", "phobert": f"phobert_r{r}", "M": f"vilatent_m_r{r}",
                 "ME": f"vilatent_me_f2_r{r}", "prompt": f"prompt_bm25_f2_r{r}"}
        D = {k: load(s, v) for k, v in stems.items()}
        ids = sorted(D["ME"]); arts = [D["ME"][i]["art"] for i in ids]
        flags = json.load(open(ROOT / f"results/paper/test/{s}/gold_flags_r{r}.json", encoding="utf-8"))
        fl = [1 if flags[i] else 0 for i in ids]
        table = {k: {m: mean_ci([D[k][i][m] for i in ids], arts) for m in ("f1", "em", "acc")} for k in D}
        pairs = {}
        for x, y in PAIRS:
            e = {m: ci(paired_test([D[x][i][m] for i in ids], [D[y][i][m] for i in ids], arts)) for m in ("f1", "acc")}
            e["discordant"] = sign(e["f1"]) != sign(e["acc"]); pairs[f"{x}-{y}"] = e
        inout = {}
        for x, y in (("ME", "prompt"), ("ME", "M"), ("ME", "phobert"), ("ME", "bm25_x2"), ("M", "bm25")):
            e = {}
            for m in ("f1", "acc"):
                dv = [D[x][i][m] - D[y][i][m] for i in ids]
                for name, sel in (("In", 1), ("Out", 0)):
                    sub = [i for i, f in enumerate(fl) if f == sel]
                    t = paired_test([D[x][ids[i]][m] for i in sub], [D[y][ids[i]][m] for i in sub], [arts[i] for i in sub])
                    e[f"{m}_{name}"] = ci(t)
                e[f"{m}_interaction_Out_minus_In"] = interaction(dv, fl, arts)
            inout[f"{x}-{y}"] = e
        # router: ME when its answer is verbatim in its evidence (aie), else M  (post hoc, as in paper_numbers.py:221)
        route = {m: [D["ME"][i][m] if D["ME"][i]["aie"] else D["M"][i][m] for i in ids] for m in ("f1", "em", "acc")}
        router = {"share_to_M": round(float(np.mean([not D["ME"][i]["aie"] for i in ids])), 3),
                  "router": {m: mean_ci(route[m], arts) for m in route}}
        for y in ("M", "bm25_x2", "prompt"):
            router[f"router-{y}"] = {m: ci(paired_test(route[m], [D[y][i][m] for i in ids], arts)) for m in ("f1", "acc")}
        res[s] = dict(n=len(ids), n_articles=len(set(arts)), n_in=sum(fl), systems=table, pairs=pairs, in_out=inout, router=router)
    out = ROOT / f"results/icisn/judge/tables_r{r}.json"; out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8"); print("wrote", out)
