"""Auto-generated QA for stage 2 with the iCOMM 27B teacher (OpenAI-compatible endpoint).

One paragraph (80–400 syllables, ViQuAD-like) is taken from each document of the leak-filtered
pool. The teacher writes three questions per paragraph, one per answer type: number, named
entity, short description. An answer must be copied verbatim from the paragraph (it is a
span, like ViQuAD); others are dropped here. scripts/filter_qa.py then keeps only the
questions that the reader answers correctly with the full paragraph.

The job appends to --out and skips paragraphs already done, so it can run in the
background from week 1 and be restarted.

Usage:
  python scripts/generate_qa.py --docs data/corpus/docs.jsonl --n-paragraphs 20000 \
      --base-url $TEACHER_URL --model $TEACHER_MODEL --out data/qa_gen/qa_raw.jsonl
"""
import argparse
import json
import random
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tqdm import tqdm

from vilatent.data import read_jsonl, short_hash, write_meta
from vilatent.text import normalize, syllables

ANSWER_TYPES = {"số": "number", "thực thể": "entity", "mô tả": "description"}
PROMPT = """Bạn là người soạn câu hỏi đọc hiểu tiếng Việt. Đọc đoạn văn dưới đây và viết đúng 3 câu hỏi:
1. một câu có đáp án là một con số (số lượng, năm, ngày tháng, số đo, tỉ lệ…), loại "số";
2. một câu có đáp án là một tên riêng (người, địa danh, tổ chức, tác phẩm…), loại "thực thể";
3. một câu có đáp án là một cụm từ mô tả ngắn (nguyên nhân, đặc điểm, cách thức…), loại "mô tả".

Yêu cầu:
- Đáp án phải được CHÉP NGUYÊN VĂN từ đoạn văn, dài tối đa 15 chữ.
- Câu hỏi phải trả lời được chỉ bằng đoạn văn, không lặp lại nguyên văn câu chứa đáp án.
- Nếu đoạn văn không có loại đáp án nào thì bỏ câu hỏi loại đó.

Chỉ trả về một mảng JSON, không giải thích, dạng:
[{{"loai": "số", "cau_hoi": "...", "dap_an": "..."}}, ...]

Đoạn văn:
{paragraph}"""


def pick_paragraph(text: str, rng: random.Random, low: int = 80, high: int = 400) -> str | None:
    candidates = [p.strip() for p in text.split("\n") if low <= len(syllables(p)) <= high]
    return rng.choice(candidates) if candidates else None


def parse_items(reply: str, paragraph: str) -> list[dict]:
    match = re.search(r"\[.*\]", reply, flags=re.S)
    if not match:
        return []
    try:
        items = json.loads(match.group())
    except json.JSONDecodeError:
        return []
    out = []
    for it in items if isinstance(items, list) else []:
        if not isinstance(it, dict):
            continue
        kind, q, a = (normalize(str(it.get(k, ""))).strip() for k in ("loai", "cau_hoi", "dap_an"))
        if kind not in ANSWER_TYPES or not q or not a or len(syllables(a)) > 15:
            continue
        if a not in paragraph:  # verbatim span only
            continue
        out.append({"question": q, "answer": a, "answer_type": ANSWER_TYPES[kind]})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="data/corpus/docs.jsonl")
    ap.add_argument("--n-paragraphs", type=int, default=20_000)
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--api-key", default="EMPTY")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default="data/qa_gen/qa_raw.jsonl")
    args = ap.parse_args()

    from openai import OpenAI

    client = OpenAI(base_url=args.base_url, api_key=args.api_key, max_retries=5, timeout=600)
    rng = random.Random(args.seed)
    docs = read_jsonl(args.docs)
    rng.shuffle(docs)
    jobs = []
    for doc in docs:
        paragraph = pick_paragraph(doc["text"], rng)
        if paragraph:
            jobs.append((doc, paragraph))
        if len(jobs) >= args.n_paragraphs:
            break
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = {r["cluster"] for r in read_jsonl(out)} if out.exists() else set()
    jobs = [(d, p) for d, p in jobs if short_hash(p) not in done]

    def ask(job):
        doc, paragraph = job
        reply = client.chat.completions.create(
            model=args.model, messages=[{"role": "user", "content": PROMPT.format(paragraph=paragraph)}],
            temperature=0.0, max_tokens=1024, extra_body={"chat_template_kwargs": {"enable_thinking": False}})
        return doc, paragraph, parse_items(reply.choices[0].message.content or "", paragraph)

    n_items = 0
    with open(out, "a", encoding="utf-8") as f, ThreadPoolExecutor(args.workers) as pool:
        for doc, paragraph, items in tqdm(pool.map(ask, jobs), total=len(jobs), desc="teacher QA"):
            cluster = short_hash(paragraph)
            for j, it in enumerate(items):
                f.write(json.dumps({"id": f"gen-{cluster}-{j}", "cluster": cluster, "source": doc["source"],
                                    "doc_id": doc["id"], "context": paragraph, "question": it["question"],
                                    "answers": [it["answer"]], "answer_type": it["answer_type"]},
                                   ensure_ascii=False) + "\n")
                n_items += 1
            if not items:  # remember the paragraph so a restart does not ask again
                f.write(json.dumps({"id": f"gen-{cluster}-none", "cluster": cluster, "empty": True}) + "\n")
            f.flush()
    write_meta(out, docs=args.docs, teacher=args.model, prompt=PROMPT, seed=args.seed)
    print(f"{n_items} questions written for {len(jobs)} paragraphs")


if __name__ == "__main__":
    main()
