"""Smoke subset of P1 for the H100 runs: 12 questions, 4 per length (16k/32k/64k), spread over >= 3 articles, so that the
64k path and the memory swap (which needs >= 2 articles) are exercised. Deterministic (first rows by file order).
  python scripts/icisn/make_smoke_p1.py            # writes data/icisn/longctx_p1_smoke.jsonl; never use its numbers as results
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
src, dst = ROOT / "data/icisn/longctx_p1.jsonl", ROOT / "data/icisn/longctx_p1_smoke.jsonl"
rows = [json.loads(l) for l in open(src, encoding="utf-8") if l.strip()]
pick, seen = [], {}
for r in rows:
    L = r["length"]; titles = seen.setdefault(L, [])
    if sum(1 for p in pick if p["length"] == L) >= 4: continue
    # take a row only if it adds a new article until 3 articles are covered for this length, then fill by order
    if r["title"] not in titles and len(titles) < 3 or len(titles) >= 3:
        titles.append(r["title"]); pick.append(r)
assert len(pick) == 12 and {p["length"] for p in pick} == {16000, 32000, 64000}, (len(pick), {p["length"] for p in pick})
assert len({p["title"] for p in pick}) >= 3
with open(dst, "w", encoding="utf-8", newline="\n") as f:
    for r in pick: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", dst, len(pick), "questions;", len({p["title"] for p in pick}), "articles;", sorted({p["length"] for p in pick}))
