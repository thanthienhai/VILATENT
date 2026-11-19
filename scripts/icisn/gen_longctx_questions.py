"""P2: câu hỏi do LLM sinh trên bài Wikipedia vi dài tự nhiên (bản xem trước nhỏ, mặc định 4 bài x 3 cửa sổ).

Quy trình (cố định trước khi chạy đầy đủ):
 1. chọn bài Wikipedia vi dài (>= 8.000 âm tiết, không 'Danh sách', không trùng tiêu đề ViQuAD);
 2. lấy cửa sổ ~12 câu liên tiếp ở vị trí ngẫu nhiên có seed;
 3. mô hình SINH (Qwen3.8-27B, khác DeepSeek đang viết Sum/chấm) viết một câu hỏi tự đủ nghĩa và đáp án là một đoạn trích nguyên văn;
 4. bộ lọc cơ học: đáp án nguyên văn trong cửa sổ, xuất hiện đúng 1 lần trong cả bài, câu hỏi không nhắc 'đoạn văn/bài viết', 1-12 âm tiết;
 5. mô hình KIỂM (DeepSeek-V4.1-Flash) trả lời chỉ từ cửa sổ; giữ nếu F1 với đáp án vàng >= 0,8.
Không đọc/in khóa API (scripts/icisn/llm.py tự nạp). Kết quả: docs/icisn/XEM_TRUOC_LONGCTX_P2.md và results/icisn/longctx/p2_preview.jsonl
"""
import argparse, glob, json, random, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/icisn"))
sys.path.insert(0, str(ROOT))
import llm  # noqa: E402

GEN, CHK = "Qwen3.8-27B", "DeepSeek-V4.1-Flash"
WIKI = glob.glob(str(Path.home() / ".cache/huggingface/hub/datasets--wikimedia--wikipedia/snapshots/*/20231101.vi/train-00001-of-00004.parquet"))
GEN_P = ("Dưới đây là một đoạn trích từ một bài Wikipedia tiếng Việt.\n\n{w}\n\n"
         "Hãy viết MỘT câu hỏi tiếng Việt mà đoạn trích trả lời được, sao cho câu hỏi tự đủ nghĩa khi đứng riêng "
         "(nêu rõ chủ thể, không dùng các từ như 'đoạn văn', 'bài viết', 'văn bản', 'ở trên') và đáp án là một cụm "
         "từ ngắn được SAO NGUYÊN VĂN từ đoạn trích. Trả lời đúng định dạng JSON: "
         '{{"question": "...", "answer": "..."}}')
CHK_P = ("Đoạn trích:\n{w}\n\nCâu hỏi: {q}\n\nTrả lời bằng một cụm từ ngắn trích nguyên văn từ đoạn trích. "
         'Chỉ đưa ra JSON: {{"answer": "..."}}')


def f1(a, b):
    a, b = a.lower().split(), b.lower().split()
    c = sum(min(a.count(w), b.count(w)) for w in set(a))
    if not a or not b or not c:
        return 0.0
    p, r = c / len(a), c / len(b)
    return 2 * p * r / (p + r)


def js(s):
    m = re.search(r"\{.*\}", s, re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", type=int, default=4)
    ap.add_argument("--windows", type=int, default=3)
    ap.add_argument("--full", action="store_true", help="bài có chồng lấn < 50%% với kho GĐ1, >= 5.000 âm tiết; ghi data/icisn/longctx_p2.jsonl")
    a = ap.parse_args()
    import pandas as pd
    d = pd.read_parquet(WIKI[0])
    if a.full:
        ov = json.load(open(ROOT / "results/icisn/longctx/wiki_overlap.json", encoding="utf-8"))["frac"]
        d = d[d.text.str.split().str.len() >= 5000]
        d = d[~d.title.str.startswith("Danh sách")]
        d = d[d.title.map(lambda t: ov.get(t, 1.0) < 0.5)]
    else:
        d = d[d.text.str.split().str.len() >= 8000]
        d = d[~d.title.str.startswith("Danh sách")].sample(a.docs, random_state=0)
    cache = llm.Cache(ROOT / "results/icisn/longctx/llm_cache.sqlite")
    out = []
    rng = random.Random(0)
    for title, text in zip(d.title, d.text):
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if len(s.split()) >= 5]
        for _ in range(a.windows):
            i = rng.randrange(len(sents) - 12)
            w = " ".join(sents[i:i + 12])
            rec = {"title": title, "n_syll_doc": len(text.split()), "window_at": i / len(sents), "window": w}
            g = js(llm.chat(cache, GEN, [{"role": "user", "content": GEN_P.format(w=w)}], max_tokens=200)["content"])
            if not g or "question" not in g or "answer" not in g:
                rec["status"] = "gen_failed"; out.append(rec); continue
            q, ans = g["question"].strip(), g["answer"].strip()
            rec.update(question=q, answer=ans)
            n = len(ans.split())
            if ans not in w:
                rec["status"] = "answer_not_verbatim"
            elif (not a.full) and text.count(ans) != 1:
                rec["status"] = f"answer_appears_{text.count(ans)}x_in_doc"
            elif re.search(r"đoạn văn|bài viết|văn bản|ở trên|đoạn trích", q, re.I):
                rec["status"] = "question_refers_to_text"
            elif not 1 <= n <= 12:
                rec["status"] = "answer_length"
            else:
                c = js(llm.chat(cache, CHK, [{"role": "user", "content": CHK_P.format(w=w, q=q)}], max_tokens=100)["content"])
                rec["check_answer"] = (c or {}).get("answer", "")
                rec["check_f1"] = round(f1(rec["check_answer"], ans), 2)
                rec["status"] = "kept" if rec["check_f1"] >= 0.8 else "check_disagrees"
            out.append(rec)
    if a.full:
        docs = dict(zip(d.title, d.text))
        rows = [dict(id=f"xl2-{i:05d}", cluster="xl2-" + r["title"], title=r["title"], question=r["question"],
                     answers=[r["answer"]], position="bin%d" % min(2, int(3 * r["window_at"])), n_occ=docs[r["title"]].count(r["answer"]),
                     overlap=ov[r["title"]], context=docs[r["title"]])
                for i, r in enumerate(x for x in out if x["status"] == "kept")]
        pth = ROOT / "data/icisn/longctx_p2.jsonl"
        pth.write_text(chr(10).join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
        print("wrote", pth, len(rows), "kept of", len(out))
    p = ROOT / "results/icisn/longctx/p2_preview.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out), encoding="utf-8")
    L = ["# Xem trước P2 (câu hỏi sinh bằng LLM trên bài Wikipedia dài); mẫu nhỏ, chưa chạy mô hình đọc\n",
         f"- {a.docs} bài, {a.windows} cửa sổ mỗi bài, mô hình sinh {GEN}, mô hình kiểm {CHK}.",
         "- Trạng thái: " + ", ".join(f"{s}={sum(r['status']==s for r in out)}" for s in sorted({r['status'] for r in out})) + "\n"]
    for r in out:
        L += [f"**Bài:** {r['title']} ({r['n_syll_doc']:,} âm tiết), cửa sổ ở {r['window_at']:.0%} bài  ",
              f"**Trạng thái:** {r['status']}  ", f"**Câu hỏi:** {r.get('question','-')}  ",
              f"**Đáp án sinh:** {r.get('answer','-')}  ", f"**Kiểm:** {r.get('check_answer','-')} (F1 {r.get('check_f1','-')})  ",
              f"**Cửa sổ (rút gọn):** {r['window'][:350]}…\n"]
    pp = ROOT / "docs/icisn/XEM_TRUOC_LONGCTX_P2.md"
    pp.write_text("\n".join(L), encoding="utf-8")
    print("wrote", pp, llm.STATS)
    print(L[2])


if __name__ == "__main__":
    main()
