"""Numbers of PREREG_LONGCTX: L1-L4 (P1, 4x), Holm per metric, secondary tables, P2 exploratory. Files only; no GPU, no API.
Output: results/icisn/longctx/numbers.json and docs/icisn/KET_QUA_LONGCTX.md"""
import json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from vilatent.stats import holm, paired_test  # noqa: E402
R = ROOT / "results/icisn_longctx"; J = ROOT / "results/icisn/longctx/judge"
STEM = dict(bm25="bm25", phobert="phobert", prompt2="prompt_bm25_f2", prompt8="prompt_bm25_f8", m="vilatent_m", me="vilatent_me_f2")


def load(s):
    meta = {}
    for l in open(ROOT / f"data/icisn/longctx_{s}.jsonl", encoding="utf-8"):
        r = json.loads(l); meta[r["id"]] = {k: r.get(k) for k in ("title", "length", "position", "hardness", "overlap", "n_occ")}
    c = {}
    for k, st in STEM.items():
        rows = {r["id"]: r for r in map(json.loads, open(R / s / f"{st}_r4.jsonl", encoding="utf-8"))}
        lab = {r["id"]: r["acc_llm"] for r in map(json.loads, open(J / s / f"{st}_r4.jsonl", encoding="utf-8"))} if (J / s / f"{st}_r4.jsonl").exists() else None
        c[k] = {i: {"f1": 100 * r["f1"], "acc": None if lab is None else 100 * lab[i], "aie": bool(r.get("aie"))} for i, r in rows.items()}
    ids = sorted(meta)
    for i in ids:
        for key in ("f1", "acc"):
            pass
    c["router"] = {i: dict(c["me"][i] if c["me"][i]["aie"] else c["m"][i]) for i in ids}
    return meta, ids, c


def vec(c, ids, key):
    return [c[i][key] for i in ids]


def gap_test(diff, grp, cl, n_boot=10_000, seed=0):
    """mean(diff | grp==1) - mean(diff | grp==0); cluster bootstrap over articles; one-sided p (H1 > 0)."""
    u = {c: k for k, c in enumerate(dict.fromkeys(cl))}
    S, N = np.zeros((len(u), 2)), np.zeros((len(u), 2))
    for d, g, c in zip(diff, grp, cl):
        S[u[c], g] += d; N[u[c], g] += 1
    obs = S[:, 1].sum() / N[:, 1].sum() - S[:, 0].sum() / N[:, 0].sum()
    w = np.random.default_rng(seed).multinomial(len(u), np.full(len(u), 1 / len(u)), size=n_boot)
    s, n = w @ S, w @ N
    with np.errstate(invalid="ignore", divide="ignore"):
        b = s[:, 1] / n[:, 1] - s[:, 0] / n[:, 0]
    b = b[np.isfinite(b)]
    return {"diff": float(obs), "ci_low": float(np.percentile(b, 2.5)), "ci_high": float(np.percentile(b, 97.5)),
            "p_one_sided": float(((b - obs) >= obs).mean()), "n": len(diff), "n_clusters": len(u)}


def main():
    out = {}
    for s in ("p1", "p2"):
        meta, ids, c = load(s)
        cl = [meta[i]["title"] for i in ids]
        has_acc = all(c["me"][i]["acc"] is not None for i in ids)
        res = {"n": len(ids), "n_clusters": len(set(cl)), "means": {}, "tests": {}}
        for k in c:
            res["means"][k] = {m: float(np.mean(vec(c[k], ids, m))) for m in (("f1", "acc") if has_acc else ("f1",))}
        for m in (("f1", "acc") if has_acc else ("f1",)):
            t = {}
            t["L1 ME-prompt2"] = paired_test(vec(c["me"], ids, m), vec(c["prompt2"], ids, m), cl)
            t["L2 ME-PhoBERT"] = paired_test(vec(c["me"], ids, m), vec(c["phobert"], ids, m), cl)
            t["L4 router-M"] = paired_test(vec(c["router"], ids, m), vec(c["m"], ids, m), cl)
            if s == "p1":
                sel = [i for i in ids if meta[i]["length"] in (16000, 64000)]
                d = [c["me"][i][m] - c["phobert"][i][m] for i in sel]
                t["L3 gap64-16"] = gap_test(d, [int(meta[i]["length"] == 64000) for i in sel], [meta[i]["title"] for i in sel])
            adj = holm({k: v["p_one_sided"] for k, v in t.items()})
            for k in t: t[k]["p_holm"] = adj[k]
            res["tests"][m] = t
        if s == "p1":
            res["by"] = {}
            for fld in ("length", "position", "hardness"):
                res["by"][fld] = {}
                for v in sorted({meta[i][fld] for i in ids}):
                    sub = [i for i in ids if meta[i][fld] == v]
                    res["by"][fld][str(v)] = {"n": len(sub), **{k: float(np.mean(vec(c[k], sub, "f1"))) for k in ("phobert", "prompt2", "m", "me", "router")}}
        else:
            lo = [i for i in ids if meta[i]["overlap"] < 0.40]
            res["sens_overlap_lt_40"] = {"n": len(lo), "n_clusters": len({meta[i]["title"] for i in lo}),
                                         "ME-prompt2": paired_test(vec(c["me"], lo, "f1"), vec(c["prompt2"], lo, "f1"), [meta[i]["title"] for i in lo]),
                                         "ME-PhoBERT": paired_test(vec(c["me"], lo, "f1"), vec(c["phobert"], lo, "f1"), [meta[i]["title"] for i in lo])}
        res["fallback_share"] = float(np.mean([not c["me"][i]["aie"] for i in ids]))
        out[s] = res
    (ROOT / "results/icisn/longctx/numbers.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps({s: {"means": out[s]["means"], "tests": {m: {k: [round(v["diff"], 2), round(v["ci_low"], 2), round(v["ci_high"], 2), round(v["p_holm"], 4)] for k, v in t.items()} for m, t in out[s]["tests"].items()}, "fallback": out[s]["fallback_share"]} for s in out}, indent=1, ensure_ascii=False))
    if "by" in out["p1"]: print(json.dumps(out["p1"]["by"], indent=1))


main()
