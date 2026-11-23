"""Numbers of PREREG_MORONG (P1, 4x): C1/C2 memory-swap controls with Holm per metric, zero/shuffle controls, equivalence margins
for L1/L2, ME vs full/bm25_x2. Files only; no GPU, no API. Missing conditions or missing judge labels are skipped (partial run ok).
Inputs: results/icisn_longctx/p1 (intact), results/icisn_morong/p1 (ME controls, 1080 Ti fp16), results/icisn_h100/p1 (full, bm25_x2) and results/icisn_h100_memctl/p1 (M intact/swap/zero/shuf), H100 bf16,
results/icisn/longctx/judge/p1 and results/icisn/morong/judge/* (ACC-LLM). Output: results/icisn/morong/numbers.json"""
import json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from vilatent.stats import bootstrap_mean, holm, paired_test  # noqa: E402
RES = ROOT / "results"
DELTA = {"f1": 3.0, "acc": 3.0}
SRC = {  # name -> (rows dir, judge dir, stem)
    "m": ("icisn_longctx/p1", "icisn/longctx/judge/p1", "vilatent_m_r4"), "me": ("icisn_longctx/p1", "icisn/longctx/judge/p1", "vilatent_me_f2_r4"),
    "prompt2": ("icisn_longctx/p1", "icisn/longctx/judge/p1", "prompt_bm25_f2_r4"), "phobert": ("icisn_longctx/p1", "icisn/longctx/judge/p1", "phobert_r4"),
    "bm25": ("icisn_longctx/p1", "icisn/longctx/judge/p1", "bm25_r4"),
    **{f"{b}_{k}": ("icisn_morong/p1", "icisn/morong/judge/icisn_morong", f"vilatent_{n}_{k}_r4")
       for b, n in (("m", "m"), ("me", "me_f2")) for k in ("swap", "zero", "shuf")},
    "full": ("icisn_h100/p1", "icisn/morong/judge/icisn_h100", "full"),
    "bm25x2": ("icisn_h100/p1", "icisn/morong/judge/icisn_h100", "bm25_x2_r4"),
    # lượt H100 bf16 (errata mục 5): cặp cùng phần cứng cho C1; zero/shuf thứ yếu
    "m_h": ("icisn_h100_memctl/p1", "icisn/morong/judge/icisn_h100_memctl", "vilatent_m_r4"),
    **{f"m_h_{k}": ("icisn_h100_memctl/p1", "icisn/morong/judge/icisn_h100_memctl", f"vilatent_m_{k}_r4") for k in ("swap", "zero", "shuf")},
}


def rows(path):
    return {r["id"]: r for r in map(json.loads, open(path, encoding="utf-8"))} if path.exists() else None


def main():
    meta = {}
    for l in open(ROOT / "data/icisn/longctx_p1.jsonl", encoding="utf-8"):
        r = json.loads(l); meta[r["id"]] = {k: r.get(k) for k in ("title", "length", "position")}
    ids = sorted(meta)
    peeked = set(open(RES / "icisn/morong/peeked_ids.txt", encoding="utf-8").read().split())
    cond = {}
    for k, (d, jd, st) in SRC.items():
        r = rows(RES / d / f"{st}.jsonl")
        if r is None or set(r) != set(ids):
            print("SKIP", k, "missing" if r is None else f"incomplete {len(r)}/{len(ids)}"); continue
        lab = rows(RES / jd / f"{st}.jsonl")
        cond[k] = {i: {"f1": 100 * r[i]["f1"], "acc": None if lab is None else 100 * lab[i]["acc_llm"]} for i in ids}
    metrics = lambda k: [m for m in ("f1", "acc") if all(cond[k][i][m] is not None for i in ids)]  # noqa: E731
    cl = lambda sub: [meta[i]["title"] for i in sub]  # noqa: E731
    vec = lambda k, sub, m: [cond[k][i][m] for i in sub]  # noqa: E731
    out = {"means": {k: {m: float(np.mean(vec(k, ids, m))) for m in metrics(k)} for k in cond}, "n": len(ids), "n_clusters": len(set(cl(ids)))}

    def pt(a, b, sub, m):
        return paired_test(vec(a, sub, m), vec(b, sub, m), cl(sub))
    out["C"] = {}
    for m in ("f1", "acc"):
        t = {}
        for name, a, b in (("C1 M-swap (H100 bf16 pair)", "m_h", "m_h_swap"), ("C2 ME-swap", "me", "me_swap")):
            if a in cond and b in cond and m in metrics(a) and m in metrics(b): t[name] = pt(a, b, ids, m)
        if t:
            adj = holm({k: v["p_one_sided"] for k, v in t.items()})
            for k in t: t[k]["p_holm"] = adj[k]
            out["C"][m] = t
    sub_np = [i for i in ids if i not in peeked]
    out["C_excl_peeked"] = {m: {name: pt(a, b, sub_np, m) for name, a, b in (("C1 M-swap (H100 bf16 pair)", "m_h", "m_h_swap"), ("C2 ME-swap", "me", "me_swap"))
                                if a in cond and b in cond and m in metrics(a) and m in metrics(b)} for m in ("f1", "acc")}
    out["secondary"] = {m: {f"{b}-{k}": pt(b, f"{b}_{k}", ids, m) for b in ("m", "m_h", "me") for k in ("zero", "shuf", "swap")
                            if f"{b}_{k}" in cond and m in metrics(b) and m in metrics(f"{b}_{k}")} for m in ("f1", "acc")}
    out["by_length"] = {}
    for name, a, b in (("C1 M-swap (H100 bf16 pair)", "m_h", "m_h_swap"), ("C2 ME-swap", "me", "me_swap"), ("ME-full", "me", "full"), ("ME-bm25x2", "me", "bm25x2")):
        if a in cond and b in cond:
            out["by_length"][name] = {}
            for L in (16000, 32000, 64000):
                sub = [i for i in ids if meta[i]["length"] == L]
                out["by_length"][name][str(L)] = {m: pt(a, b, sub, m) for m in ("f1", "acc") if m in metrics(a) and m in metrics(b)} | {"n": len(sub)}
    out["by_position"] = {}
    for name, a, b in (("C1 M-swap (H100 bf16 pair)", "m_h", "m_h_swap"), ("C2 ME-swap", "me", "me_swap")):
        if a in cond and b in cond:
            out["by_position"][name] = {}
            for pos in ("start", "middle", "end"):
                sub = [i for i in ids if meta[i]["position"] == pos]
                if sub: out["by_position"][name][pos] = {m: pt(a, b, sub, m) for m in ("f1", "acc") if m in metrics(a) and m in metrics(b)} | {"n": len(sub)}
    out["equivalence"] = {}
    for name, b in (("L1 ME-prompt2", "prompt2"), ("L2 ME-PhoBERT", "phobert")):
        out["equivalence"][name] = {}
        for m in ("f1", "acc"):
            if m not in metrics("me") or m not in metrics(b): continue
            d = np.asarray(vec("me", ids, m)) - np.asarray(vec(b, ids, m))
            boot = bootstrap_mean(d, cl(ids), None, 10_000, 0)
            lo, hi = float(np.percentile(boot, 5)), float(np.percentile(boot, 95))
            out["equivalence"][name][m] = {"diff": float(d.mean()), "ci90": [lo, hi], "delta": DELTA[m], "equivalent": bool(lo > -DELTA[m] and hi < DELTA[m])}
    (RES / "icisn/morong/numbers.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    r2 = lambda v: round(v, 2)  # noqa: E731
    print(json.dumps(out["means"], indent=1))
    for m, t in out["C"].items():
        for k, v in t.items(): print(m, k, r2(v["diff"]), [r2(v["ci_low"]), r2(v["ci_high"])], "p_holm", round(v["p_holm"], 4))
    for k, v in out["equivalence"].items(): print(k, json.dumps(v))


main()
