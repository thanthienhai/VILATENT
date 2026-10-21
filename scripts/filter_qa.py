"""Filter auto-generated QA, in this order:

1. Leak filter against the evaluation files.
2. Rules (survey of 21/10/2026): drop a question that contains its answer (as whole syllables,
   e.g. "Đoạn văn đề cập đến loài cây nào?" -> "cây"), and a "number" question whose answer
   has no digit, number word or Roman numeral (the teacher labels "ATP" or "thời trung cổ"
   as numbers). Survey of the full prompt-3 run: also drop a question that names "đoạn văn"
   ("Nhân vật chính trong đoạn văn là ai?"): 4.5% of the generated questions, 2 in ViQuAD
   train, and the source of most questions repeated across paragraphs.
3. Two-way check: keep a question only when the reader, reading the full paragraph with the
   fixed template, answers it with F1 ≥ 0.8 (syllable F1 against the teacher's verbatim answer).
4. Copy share: a question is a copy when ≥ 80% of its syllables are in the sentence that holds
   the answer (vilatent.text.question_overlap). The teacher writes more copies than people do
   (25% vs about 10% in ViQuAD), so copies are subsampled (fixed seed) until their share
   matches the reference file (ViQuAD train). Every row keeps its overlap in "question_overlap".

If more than 20% of the questions are rejected at step 3, the run prints a warning: the risk
table of docs/VILATENT.md then asks for a 200-sample human check and a smaller share of
generated data.

Usage:
  python scripts/filter_qa.py --input data/qa_gen/qa_raw.jsonl --reader Qwen/Qwen3.5-2B \
      --reader-config configs/readers/qwen3.5-2b.json \
      --eval-files data/tasks/viquad_dev.jsonl data/tasks/viquad_test.jsonl --out data/qa_gen/qa_clean.jsonl
"""
import argparse
import json
import random
from collections import Counter

from vilatent.baselines import Full
from vilatent.data import Example, read_jsonl, write_jsonl, write_meta
from vilatent.evaluate import evaluate_text
from vilatent.leak import LeakIndex
from vilatent.reader import DTYPES, QUANTS, load_reader
from vilatent.template import ReaderTemplate, load_reader_config
from vilatent.text import contains_syllables, has_number, question_overlap

REJECTION_ALERT = 0.20


def rule_reject(row: dict) -> str | None:
    answer = row["answers"][0]
    if contains_syllables(row["question"], answer):
        return "answer_in_question"
    if row["answer_type"] == "number" and not has_number(answer):
        return "number_without_number"
    if contains_syllables(row["question"], "đoạn văn"):
        return "mentions_paragraph"
    return None


def is_copy(row: dict, threshold: float) -> bool:
    return question_overlap(row["question"], row["context"], row["answers"][0]) >= threshold


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/qa_gen/qa_raw.jsonl")
    ap.add_argument("--reader", required=True)
    ap.add_argument("--reader-config", required=True)
    ap.add_argument("--eval-files", nargs="+", required=True)
    ap.add_argument("--threshold", type=float, default=0.8)
    ap.add_argument("--reference", default="data/tasks/viquad_train.jsonl", help="human QA whose copy share is matched")
    ap.add_argument("--copy-overlap", type=float, default=0.8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--out", default="data/qa_gen/qa_clean.jsonl")
    ap.add_argument("--dtype", choices=list(DTYPES), default="bfloat16", help="float16 on GPUs without bf16 (T4)")
    ap.add_argument("--quant", choices=list(QUANTS), default="none", help="int4 reader: T4 smoke test only")
    args = ap.parse_args()

    rows = [r for r in read_jsonl(args.input) if not r.get("empty")]
    n_input = len(rows)
    index = LeakIndex(list({r["context"] for path in args.eval_files for r in read_jsonl(path)}))
    leaked = {r["id"] for r in rows if index.leaks(r["context"]) or index.leaks(r["question"])}
    rows = [r for r in rows if r["id"] not in leaked]
    rule_rejected = Counter(filter(None, map(rule_reject, rows)))
    rows = [r for r in rows if rule_reject(r) is None]

    reader, tokenizer = load_reader(args.reader, dtype=args.dtype, quant=args.quant)
    template = ReaderTemplate(load_reader_config(args.reader_config), tokenizer)
    examples = [Example(r["id"], r["cluster"], "qa", r["context"], question=r["question"], answers=r["answers"],
                        target=r["answers"][0]) for r in rows]
    scored = {s["id"]: s for s in evaluate_text(reader, tokenizer, template, Full(), examples, None,
                                                batch_size=args.batch_size)}
    checked = [r for r in rows if scored[r["id"]]["f1"] >= args.threshold]

    reference = list(read_jsonl(args.reference))
    ref_share = sum(is_copy(r, args.copy_overlap) for r in reference) / len(reference)
    for r in checked:
        r["question_overlap"] = question_overlap(r["question"], r["context"], r["answers"][0])
    copies = [r for r in checked if r["question_overlap"] >= args.copy_overlap]
    others = [r for r in checked if r["question_overlap"] < args.copy_overlap]
    # keep n copies so that n / (n + len(others)) = ref_share
    n_copies = min(len(copies), round(ref_share / (1 - ref_share) * len(others)))
    kept_copies = {r["id"] for r in random.Random(args.seed).sample(copies, n_copies)}
    kept = [r for r in checked if r["question_overlap"] < args.copy_overlap or r["id"] in kept_copies]
    write_jsonl(args.out, kept)

    by_type = Counter(r["answer_type"] for r in rows)
    kept_by_type = Counter(r["answer_type"] for r in kept)
    rejection = 1 - len(checked) / max(1, len(rows))
    stats = {"n_input": n_input, "leaked": len(leaked), "rule_rejected": dict(rule_rejected), "checked": len(rows),
             "passed_reader": len(checked), "rejection_rate": rejection,
             "copies": len(copies), "copies_kept": n_copies, "reference_copy_share": ref_share, "kept": len(kept),
             "kept_share_by_type": {t: kept_by_type[t] / by_type[t] for t in by_type}}
    write_meta(args.out, input=args.input, reader=args.reader, template_hash=template.hash,
               f1_threshold=args.threshold, reference=args.reference, copy_overlap=args.copy_overlap,
               seed=args.seed, **stats)
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    if rejection > REJECTION_ALERT:
        print(f"WARNING: {rejection:.0%} rejected by the reader (> {REJECTION_ALERT:.0%}): check 200 samples by "
              "hand and lower the share of generated QA (docs/VILATENT.md, risk table)")


if __name__ == "__main__":
    main()
