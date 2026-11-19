"""G1.2: stratified calibration sample (setting x system, 3 each, seed 0). Writes the blind labelling sheet."""
import csv, json, random
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys_names = ["full", "none", "truncation_r4", "bm25_r4", "bm25_x2_r4", "phobert_r4", "llmlingua2_r4",
             "prompt_bm25_f2_r4", "vilatent_m_r4", "vilatent_me_f2_r4"]
qa = {}
for l in open(ROOT / "data/tasks/viquad_test.jsonl", encoding="utf-8"):
    r = json.loads(l); qa[r["id"]] = r
rng = random.Random(0)
rows = []
for setting in ("single", "long"):
    for s in sys_names:
        pool = [r for r in map(json.loads, open(ROOT / f"results/paper/test/{setting}/{s}.jsonl", encoding="utf-8"))
                if r["prediction"].strip() and any(c.isalnum() for c in r["prediction"]) and not r.get("unreadable")]
        pool.sort(key=lambda r: r["id"])
        for r in rng.sample(pool, 3):
            q = qa[r["id"]]
            rows.append(dict(item=len(rows) + 1, id=r["id"], setting=setting, system=s, question=q["question"],
                             gold=" | ".join(dict.fromkeys(q["answers"])), prediction=r["prediction"].strip()))
out = ROOT / "results/icisn/judge/human_audit_60.csv"
# the blind sheet shows NO f1/em/judge output; f1/em are kept in a separate file for the analysis
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["item", "id", "setting", "system", "question", "gold", "prediction", "ref_label", "note"])
    w.writeheader()
    for r in rows: w.writerow({**r, "ref_label": "", "note": ""})
print(len(rows), out)
