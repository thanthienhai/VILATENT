"""G0.2: compare 1080 Ti (fp16) predictions with the H100 (bf16) ones on the same ids."""
import json, sys
from pathlib import Path
def load(p): return {r["id"]: r for r in map(json.loads, open(p, encoding="utf-8"))}
out = {}
for kind in ("single", "long"):
    for m in ("vilatent_m_r4", "vilatent_me_f2_r4"):
        a = Path(f"results/icisn/g0/{kind}/{m}.jsonl")
        if not a.exists(): continue
        new, old = load(a), load(f"results/paper/test/{kind}/{m}.jsonl")
        ids = [i for i in new if i in old]
        pred = lambda r: (r.get("prediction") or r.get("pred") or r.get("answer") or "")
        same = sum(pred(new[i]).strip() == pred(old[i]).strip() for i in ids)
        f1n = sum(new[i]["f1"] for i in ids) / len(ids); f1o = sum(old[i]["f1"] for i in ids) / len(ids)
        emn = sum(new[i]["em"] for i in ids) / len(ids); emo = sum(old[i]["em"] for i in ids) / len(ids)
        out[f"{kind}/{m}"] = dict(n=len(ids), exact_match_pred=round(same / len(ids), 4), f1_new=round(100 * f1n, 2), f1_h100=round(100 * f1o, 2),
                                  dF1=round(100 * (f1n - f1o), 2), device=("GTX 1080 Ti" if kind == "single" else "Tesla T4"), em_new=round(100 * emn, 2), em_h100=round(100 * emo, 2))
print(json.dumps(out, indent=1))
Path("results/icisn/g0").mkdir(parents=True, exist_ok=True)
json.dump(out, open("results/icisn/g0/compare.json", "w"), indent=1)
