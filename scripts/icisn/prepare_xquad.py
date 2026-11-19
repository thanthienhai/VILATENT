"""XQuAD-vi (Artetxe et al. 2020; github.com/google-deepmind/xquad, xquad.vi.json, CC BY-SA 4.0) as QA rows.

  xquad_vi_single.jsonl  one paragraph per context (as ViQuAD single-passage)
  xquad_vi_long.jsonl    every question reads its whole article: the article's paragraphs in file order joined by a
                         blank line (vilatent.data.long_rows, the same procedure as ViQuAD-Long)

Ids are xquad-<article>-<paragraph>-<question> (file order), so vilatent.data.paragraph_key and article_passages work.
Text is NFC-normalized; a question is dropped when no gold answer is verbatim in its paragraph. cluster = md5 of the
paragraph (as ViQuAD). Usage: python scripts/icisn/prepare_xquad.py
"""
import json, statistics, sys
from pathlib import Path
sys.path.insert(0, ".")
from vilatent.data import article_passages, long_rows, sha256_file, short_hash, write_jsonl, write_meta
from vilatent.text import normalize

RAW = Path("data/icisn/xquad_raw/xquad.vi.json"); OUT = Path("data/icisn")
SRC = "https://github.com/google-deepmind/xquad/blob/master/xquad.vi.json"
data = json.load(open(RAW, encoding="utf-8"))["data"]
rows, dropped = [], 0
for a, art in enumerate(data):
    for p, para in enumerate(art["paragraphs"]):
        ctx = normalize(para["context"])
        for q, qa in enumerate(para["qas"]):
            answers = [x for x in dict.fromkeys(normalize(t["text"]) for t in qa["answers"]) if x]
            if not any(x in ctx for x in answers): dropped += 1; continue
            rows.append({"id": f"xquad-{a:04d}-{p:04d}-{q:04d}", "cluster": short_hash(ctx), "title": normalize(art["title"]),
                         "context": ctx, "question": normalize(qa["question"]), "answers": answers, "xquad_id": qa["id"]})
single = OUT / "xquad_vi_single.jsonl"; write_jsonl(single, rows)
longr = long_rows(rows, article_passages(rows)); lg = OUT / "xquad_vi_long.jsonl"; write_jsonl(lg, longr)
miss = [r["id"] for r in longr if not any(x in r["context"] for x in r["answers"])]
assert not miss, miss[:3]
stats = {"source": SRC, "source_sha256": sha256_file(RAW), "questions": len(rows), "dropped_answer_not_in_context": dropped,
         "paragraphs": len({r["cluster"] for r in rows}), "articles": len({r["title"] for r in rows})}
write_meta(single, **stats); write_meta(lg, **stats, note="article = all its paragraphs joined by a blank line")
print(json.dumps(stats, ensure_ascii=False))
for p in (single, lg): print(p, sha256_file(p))
chars = [len(r["context"]) for r in longr]; print("long context chars: mean", round(statistics.mean(chars)), "max", max(chars))
