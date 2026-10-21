"""Auto-generated QA for stage 2 with the iCOMM 27B teacher (OpenAI-compatible endpoint).

One paragraph (80–400 syllables, ViQuAD-like) is taken from each document of the leak-filtered
pool. The teacher writes one question per answer type: number (only when the paragraph has a
number, vilatent.text.has_number), named entity, description. An answer must be copied
verbatim from the paragraph (it is a span, like ViQuAD); others are dropped here, as are
answers longer than MAX_SYLLABLES. scripts/filter_qa.py then drops broken questions and keeps
only those that the reader answers correctly with the full paragraph.

Prompt history (21/10/2026), each run kept for comparison:
- prompt 1 (data/qa_gen/qa_raw_prompt1.jsonl, 2,090 paragraphs): answers cut mid-phrase,
  "number" answers without a number, 25% of the questions copying the answer sentence
  (about 10% in ViQuAD).
- prompt 2 (qa_raw_prompt2.jsonl, 150 paragraphs): adds whole-phrase answers, numbers in
  "number" answers and paraphrased questions. Copies fall to 11%, but the teacher still asks a
  "number" question about paragraphs without a number, and answers stay short (median 3
  syllables, ViQuAD 6) because of the 15-syllable cap.
- prompt 3 (current): the number question only for paragraphs with a number; descriptions
  may take up to 30 syllables.

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
from vilatent.text import has_number, normalize, syllables

ANSWER_TYPES = {"số": "number", "thực thể": "entity", "mô tả": "description"}
# one line of the prompt per requested type; the "số" line is left out for a paragraph without a number
TYPE_LINES = {
    "số": 'một câu có đáp án là một con số (số lượng, năm, ngày tháng, số đo, tỉ lệ…), loại "số"',
    "thực thể": 'một câu có đáp án là một tên riêng (người, địa danh, tổ chức, tác phẩm…), loại "thực thể"',
    "mô tả": 'một câu có đáp án là một cụm từ hoặc mệnh đề mô tả (nguyên nhân, đặc điểm, cách thức…), loại "mô tả"',
}
# ViQuAD train: median answer 6 syllables, 21% longer than 15
MAX_SYLLABLES = {"number": 15, "entity": 15, "description": 30}
PROMPT = """Bạn là người soạn câu hỏi đọc hiểu tiếng Việt. Đọc đoạn văn dưới đây và viết đúng {n} câu hỏi:
{types}

Yêu cầu:
- Đáp án phải được CHÉP NGUYÊN VĂN từ đoạn văn và là một cụm trọn vẹn: không cắt giữa cụm, không bỏ sót thành
  phần khi đáp án gồm nhiều người, nơi chốn hay sự vật.
- Đáp án loại "số" và "thực thể" dài tối đa 15 chữ. Đáp án loại "mô tả" dài tối đa 30 chữ và có thể là cả một
  mệnh đề, miễn là trả lời đầy đủ câu hỏi.
- Đáp án loại "số" phải chứa con số (viết bằng chữ số hoặc bằng chữ).
- Câu hỏi phải trả lời được chỉ bằng đoạn văn và không được chứa đáp án.
- Diễn đạt câu hỏi bằng lời của bạn (đổi cấu trúc câu, dùng từ đồng nghĩa), không chép lại câu chứa đáp án.
- Nếu đoạn văn không có loại đáp án nào thì bỏ câu hỏi loại đó.

Chỉ trả về một mảng JSON, không giải thích, dạng:
[{{"loai": "thực thể", "cau_hoi": "...", "dap_an": "..."}}, ...]

Đoạn văn:
{paragraph}"""


def pick_paragraph(text: str, rng: random.Random, low: int = 80, high: int = 400) -> str | None:
    candidates = [p.strip() for p in text.split("\n") if low <= len(syllables(p)) <= high]
    return rng.choice(candidates) if candidates else None


def requested_types(paragraph: str) -> list[str]:
    return [k for k in TYPE_LINES if k != "số" or has_number(paragraph)]


def build_prompt(paragraph: str) -> str:
    kinds = requested_types(paragraph)
    lines = [f"{i}. {TYPE_LINES[k]}" + (";" if i < len(kinds) else ".") for i, k in enumerate(kinds, 1)]
    return PROMPT.format(n=len(kinds), types="\n".join(lines), paragraph=paragraph)


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
        if kind not in requested_types(paragraph) or not q or not a:
            continue
        if len(syllables(a)) > MAX_SYLLABLES[ANSWER_TYPES[kind]]:
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
            model=args.model, messages=[{"role": "user", "content": build_prompt(paragraph)}],
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
    write_meta(out, docs=args.docs, teacher=args.model, prompt=PROMPT, type_lines=TYPE_LINES,
               max_syllables=MAX_SYLLABLES, seed=args.seed)
    print(f"{n_items} questions written for {len(jobs)} paragraphs")


if __name__ == "__main__":
    main()
