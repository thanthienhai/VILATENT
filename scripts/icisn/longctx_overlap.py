"""Kiểm tra chồng lấn 8-gram giữa các bài Wikipedia vi dài (làm nhiễu P1 / tài liệu P2) và corpus giai đoạn 1.
Quy tắc (như G0.4): một bài bị coi là trùng nếu >= 50% 8-gram từ của nó xuất hiện trong data/corpus/docs.jsonl.
Ghi results/icisn/longctx/wiki_overlap.json (tiêu đề -> tỉ lệ)."""
import glob, json, re, unicodedata
from pathlib import Path
import pandas as pd
N = 8
def norm(s): return re.sub(r"\W+", " ", unicodedata.normalize("NFC", s).lower()).split()
def grams(w): return {" ".join(w[i:i + N]) for i in range(len(w) - N + 1)}
W = glob.glob(str(Path.home() / ".cache/huggingface/hub/datasets--wikimedia--wikipedia/snapshots/*/20231101.vi/train-00001-of-00004.parquet"))[0]
d = pd.read_parquet(W)
d = d[d.text.str.split().str.len() >= 5000]
d = d[~d.title.str.startswith("Danh sách")]
sh = {t: grams(norm(x)) for t, x in zip(d.title, d.text)}
owner = {}
for t, s in sh.items():
    for g in s: owner.setdefault(g, []).append(t)
hit = {t: set() for t in sh}
n = 0
with open("data/corpus/docs.jsonl", encoding="utf-8") as f:
    for l in f:
        n += 1
        x = json.loads(l); txt = x.get("text") or x.get("content") or ""
        for g in grams(norm(txt)):
            for t in owner.get(g, ()): hit[t].add(g)
frac = {t: len(hit[t]) / max(1, len(sh[t])) for t in sh}
Path("results/icisn/longctx").mkdir(parents=True, exist_ok=True)
json.dump({"rule": "overlap if >=50% of word 8-grams shared with data/corpus/docs.jsonl", "n_corpus_docs": n, "frac": frac},
          open("results/icisn/longctx/wiki_overlap.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
v = sorted(frac.values())
print("corpus docs", n, "| wiki docs", len(v), "| >=1 shared:", sum(x > 0 for x in v), "| >=10%:", sum(x >= .1 for x in v), "| >=50%:", sum(x >= .5 for x in v), "| max %.2f" % v[-1])
