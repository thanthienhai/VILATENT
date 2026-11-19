"""P1: ViQuAD-XL, ngữ cảnh dài tổng hợp có điều khiển (độ dài, vị trí bài đích, độ khó của nhiễu).

Chỉ dựng dữ liệu và in thống kê; KHÔNG chạy mô hình đọc. Độ dài đo bằng token của Qwen3.5-2B.
  python scripts/icisn/build_longctx.py --preview   # ghi docs/icisn/XEM_TRUOC_LONGCTX_P1.md (mẫu nhỏ)
Quy tắc (cố định trước khi đọc kết quả):
 - bài đích: 19 bài của tập kiểm thử ViQuAD; câu hỏi lấy mẫu cân bằng theo bài (tối đa N_PER_ARTICLE);
 - nhiễu: 18 bài kiểm thử ViQuAD khác và 48 bài XQuAD-vi (66 bài sạch; Wikipedia vi dài bị loại vì đã nằm trong kho giai đoạn 1);
 - 3 độ dài x 3 vị trí (đầu/giữa/cuối) x 2 độ khó nhiễu (ngẫu nhiên / gần chủ đề theo TF-IDF); mỗi câu hỏi nhận
   MỘT ô, xoay vòng có seed để cân bằng;
 - loại câu hỏi có đáp án vàng xuất hiện nguyên văn (không phân biệt hoa thường) trong bất kỳ bài nhiễu nào.
"""
import argparse, glob, json, random
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
LENGTHS = [16000, 32000, 64000]       # token
POSITIONS = ["start", "middle", "end"]
HARDNESS = ["random", "hard"]
N_PER_ARTICLE = 32
USE_WIKI = False   # quyết định 2026-11: bài Wikipedia dài đều đã nằm trong kho giai đoạn 1 (xem longctx_overlap.py)
SEED = 0
NL = chr(10)
SEP = NL + NL
WIKI = glob.glob(str(Path.home() / ".cache/huggingface/hub/datasets--wikimedia--wikipedia/snapshots/*/20231101.vi/train-00001-of-00004.parquet"))


def ntok(tok, s):
    return len(tok(s).input_ids)


def load_pool(tok):
    rows = [json.loads(l) for f in ("s0", "s1")
            for l in open(ROOT / f"data/icisn/viquad_long_test_{f}.jsonl", encoding="utf-8")]
    targets = {}
    for r in rows:
        targets.setdefault(r["title"], r["context"])
    pool = {("v", t): c for t, c in targets.items()}
    for l in open(ROOT / "data/icisn/xquad_vi_long.jsonl", encoding="utf-8"):
        r = json.loads(l)
        pool.setdefault(("x", r["title"]), r["context"])
    nwiki = 0
    if USE_WIKI and WIKI:
        import pandas as pd
        d = pd.read_parquet(WIKI[0])
        d = d[d.text.str.split().str.len() >= 5000]
        d = d[~d.title.str.startswith("Danh sách")]
        vq = {t.lower() for t in targets}
        for t, x in zip(d.title, d.text):
            if t.lower() not in vq:
                pool[("w", t)] = x
                nwiki += 1
    cache = {k: ntok(tok, c) for k, c in pool.items()}
    return rows, targets, pool, cache, nwiki


def neighbours(pool):
    from sklearn.feature_extraction.text import TfidfVectorizer
    keys = list(pool)
    X = TfidfVectorizer(max_features=50000, sublinear_tf=True).fit_transform([pool[k] for k in keys])
    S = (X @ X.T).toarray()
    return {k: [keys[j] for j in np.argsort(-S[i]) if j != i] for i, k in enumerate(keys)}


def assemble(r, pool, ntk, nb, length, position, hardness, rng):
    key = ("v", r["title"])
    cand = list(nb[key]) if hardness == "hard" else [k for k in pool if k != key]
    if hardness == "random":
        rng.shuffle(cand)
    chosen, n = [], ntk[key]
    for k in cand:
        if n >= length:
            break
        if n + ntk[k] > length * 1.25:     # tránh một bài nhiễu đẩy vượt quá xa mục tiêu
            continue
        chosen.append(k)
        n += ntk[k]
    rng.shuffle(chosen)
    cut = {"start": 0, "end": len(chosen), "middle": len(chosen) // 2}[position]
    order = chosen[:cut] + [key] + chosen[cut:]
    gold = [a.lower() for a in (r["answers"] if isinstance(r["answers"], list) else r["answers"]["text"])]
    if any(g in pool[k].lower() for k in chosen for g in gold):
        return None
    return dict(order=order, n_tok=n, n_docs=len(order), rank=order.index(key))


def build(preview=False):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-2B")
    rows, targets, pool, ntk, nwiki = load_pool(tok)
    nb = neighbours(pool)
    rng = random.Random(SEED)
    by = {}
    for r in rows:
        by.setdefault(r["title"], []).append(r)
    sample = []
    for t, v in by.items():
        rng.shuffle(v)
        sample += v[:N_PER_ARTICLE]
    cells = [(L, p, h) for L in LENGTHS for p in POSITIONS for h in HARDNESS]
    rng.shuffle(cells)
    out, dropped = [], 0
    for i, r in enumerate(sample):
        L, p, h = cells[i % len(cells)]
        a = assemble(r, pool, ntk, nb, L, p, h, random.Random(f"{SEED}-{r['id']}"))
        if a is None:
            dropped += 1
            continue
        out.append(dict(id=r["id"], question=r["question"], answers=r["answers"], target=r["title"],
                        length=L, position=p, hardness=h, **{k: a[k] for k in ("n_tok", "n_docs", "rank")},
                        order=[k[1] for k in a["order"]], keys=a["order"]))
    return out, dropped, len(sample), pool, nwiki, ntk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--write", action="store_true", help="ghi data/icisn/longctx_p1.jsonl (có ngữ cảnh đầy đủ)")
    a = ap.parse_args()
    out, dropped, n, pool, nwiki, ntk = build()
    if a.write:
        rows = []
        for o in out:
            rows.append(dict(id="xl-" + o["id"], cluster="xl-" + o["id"], title=o["target"], question=o["question"],
                             answers=o["answers"], position=o["position"], length=o["length"], hardness=o["hardness"],
                             n_tok=o["n_tok"], n_docs=o["n_docs"],
                             context=SEP.join(pool[k] for k in o["keys"])))
        pth = ROOT / "data/icisn/longctx_p1.jsonl"
        pth.write_text(NL.join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
        print("wrote", pth, len(rows))
    import collections
    c = collections.Counter((o["length"], o["position"], o["hardness"]) for o in out)
    L = ["# Xem trước P1 (ViQuAD-XL tổng hợp có điều khiển); chưa chạy mô hình đọc\n",
         f"- Mẫu: {n} câu hỏi (tối đa {N_PER_ARTICLE}/bài đích); còn {len(out)} sau khi loại {dropped} câu có đáp án trong bài nhiễu.",
         f"- Kho bài nhiễu: {len(pool)} bài, không dùng Wikipedia dài (đã nằm trong kho giai đoạn 1).",
         "- Độ dài đo bằng token Qwen3.5-2B (khoảng 1,26 token/âm tiết trên 19 bài kiểm thử).",
         f"- Số câu hỏi mỗi ô (độ dài × vị trí × nhiễu): min {min(c.values())}, max {max(c.values())}, {len(c)} ô.\n",
         "| độ dài mục tiêu | số bài nhiễu (trung vị) | token thực (trung vị) |", "|---|---|---|"]
    for Ln in LENGTHS:
        s = [o for o in out if o["length"] == Ln]
        L.append(f"| {Ln:,} | {sorted(o['n_docs'] for o in s)[len(s)//2]} | {sorted(o['n_tok'] for o in s)[len(s)//2]:,} |")
    L.append("\n## Ví dụ (một cho mỗi độ dài, nhiễu 'hard')\n")
    for Ln in LENGTHS:
        o = next(x for x in out if x["length"] == Ln and x["hardness"] == "hard")
        g = (o["answers"] if isinstance(o["answers"], list) else o["answers"]["text"])[0]
        L += [f"**Câu hỏi:** {o['question']}  ", f"**Đáp án vàng:** {g}  ",
              f"**Ngữ cảnh:** {o['n_tok']:,} token, {o['n_docs']} bài; bài đích '{o['target']}' ở vị trí {o['rank']+1}/{o['n_docs']} ({o['position']}); nhiễu {o['hardness']}  ",
              "**Bài nhiễu gần nhất (đầu danh sách):** " + "; ".join(t for t in o["order"] if t != o["target"])[:300] + "\n"]
    if a.preview:
        p = ROOT / "docs/icisn/XEM_TRUOC_LONGCTX_P1.md"
        p.write_text("\n".join(L), encoding="utf-8")
        print("wrote", p)
    print("\n".join(L[:13]))


if __name__ == "__main__":
    main()
