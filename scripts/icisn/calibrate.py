"""G1.2: run both judges on the 60-item sheet and report Cohen kappa."""
import csv, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import judge, llm
judge.check_lock()
ROOT = judge.ROOT
rows = list(csv.DictReader(open(ROOT / "results/icisn/judge/human_audit_60.csv", encoding="utf-8-sig")))
out = {}
for model, tag in ((judge.PRIMARY, "primary"), (judge.SECONDARY, "secondary")):
    cache = llm.Cache(ROOT / f"results/icisn/judge/cache_{tag}.sqlite")
    res = llm.map_threads(lambda r: judge.judge_one(cache, model, r["question"], r["gold"].split(" | "), r["prediction"]), rows, 8)
    out[tag] = [x[0] for x in res]; out[tag + "_raw"] = [x[1] for x in res]

def kappa(a, b):
    p = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    n = len(p); po = sum(x == y for x, y in p) / n
    pa = sum(x for x, _ in p) / n; pb = sum(y for _, y in p) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3), round(po, 3), n
ref = [int(r["ref_label"]) for r in rows]
rep = {"n": len(rows), "invalid": {t: sum(v is None for v in out[t]) for t in ("primary", "secondary")},
       "kappa_primary_vs_ref": kappa(out["primary"], ref), "kappa_secondary_vs_ref": kappa(out["secondary"], ref),
       "kappa_primary_vs_secondary": kappa(out["primary"], out["secondary"]),
       "pos_rate": {"ref": sum(ref) / 60, "primary": sum(v or 0 for v in out["primary"]) / 60, "secondary": sum(v or 0 for v in out["secondary"]) / 60},
       "format": "(kappa, observed agreement, n)", "stats": llm.STATS}
for t in ("primary", "secondary"):
    tp = sum(1 for a, b in zip(out[t], ref) if a == 1 and b == 1); fp = sum(1 for a, b in zip(out[t], ref) if a == 1 and b == 0)
    fn = sum(1 for a, b in zip(out[t], ref) if a != 1 and b == 1); tn = sum(1 for a, b in zip(out[t], ref) if a != 1 and b == 0)
    rep[f"confusion_{t}_vs_ref"] = {"judge1_ref1": tp, "judge1_ref0": fp, "judge0_ref1": fn, "judge0_ref0": tn}
dis = [dict(item=r["item"], setting=r["setting"], system=r["system"], ref=ref[i], primary=out["primary"][i], secondary=out["secondary"][i],
            question=r["question"], gold=r["gold"][:120], prediction=r["prediction"][:120], note=r["note"]) for i, r in enumerate(rows)
       if not (out["primary"][i] == out["secondary"][i] == ref[i])]
rep["disagreements"] = dis
(ROOT / "results/icisn/judge/calibration.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in rep.items() if k != "disagreements"}, ensure_ascii=False, indent=1)); print(len(dis), "dòng bất đồng")
