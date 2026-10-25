"""ViQuAD-Long (evaluation) and multi-passage samples (stage-2 training), checklist A10/A22, B4.

  viquad_long_{gate,select,test}.jsonl  every answerable question of the split, reading its whole
        article: all distinct passages of the article in the order of the official JSON file
        (ids are numbered in that order), joined by a blank line, no length limit. Splits are
        those of prepare_viquad.py (whole articles), so gate, select and test stay disjoint.
        Every passage of ViQuAD 2.0 has at least one answerable question, so the split files hold
        all passages of their articles; duplicates are removed by exact text (none occur).
  viquad_train_multi.jsonl, viquad_select_multi.jsonl  one sample per question: a contiguous
        window of 2–8 passages of the question's article that contains its passage
        (vilatent.data.multi_passage_rows). Train windows use only the leak-filtered train file.
  viquad_long_stats.json  per Long split: articles, passages, questions, context length in reader
        tokens (min / median / max), answer-in-context check, distribution of the answer
        passage's position (beginning / middle / end third of the article, checklist B16).

Usage:
  python scripts/build_long.py --tasks-dir data/tasks --reader Qwen/Qwen3.5-2B
"""
import argparse
import json
import os
import statistics
from collections import Counter

from vilatent.data import (article_passages, long_rows, multi_passage_rows, read_jsonl, write_jsonl,
                           write_meta)


def length_stats(values: list[int]) -> dict:
    return {"min": min(values), "median": statistics.median(values), "mean": statistics.mean(values),
            "max": max(values)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks-dir", default="data/tasks")
    ap.add_argument("--reader", required=True, help="tokenizer that measures the context lengths")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--min-passages", type=int, default=2)
    ap.add_argument("--max-passages", type=int, default=8)
    args = ap.parse_args()

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.reader)

    def n_tokens(text: str) -> int:  # as the text sits in the context slot (" " + text)
        return len(tokenizer(" " + text, add_special_tokens=False)["input_ids"])

    stats = {}
    for split in ("gate", "select", "test"):
        src = os.path.join(args.tasks_dir, f"viquad_{split}.jsonl")
        rows = read_jsonl(src)
        passages = article_passages(rows)
        out = long_rows(rows, passages)
        missing = [r["id"] for r in out if not any(a in r["context"] for a in r["answers"])]
        if missing:
            raise SystemExit(f"{split}: {len(missing)} answers not in the article, e.g. {missing[:3]}")
        lengths = {t: n_tokens(r["context"]) for t, r in {r["title"]: r for r in out}.items()}
        passage_lengths = [n_tokens(p) for ps in passages.values() for p in ps]
        stats[split] = {
            "articles": len(passages), "passages": sum(len(ps) for ps in passages.values()), "questions": len(out),
            "duplicate_passages_removed": len({r["cluster"] for r in rows}) - sum(len(ps) for ps in passages.values()),
            "article_tokens": length_stats(list(lengths.values())),
            "question_weighted_article_tokens": length_stats([lengths[r["title"]] for r in out]),
            "passage_tokens": length_stats(passage_lengths),
            "answers_in_context": f"{len(out)}/{len(out)}",
            "answer_position": dict(Counter(r["position"] for r in out)),
            "passages_per_article": length_stats([len(ps) for ps in passages.values()]),
        }
        path = os.path.join(args.tasks_dir, f"viquad_long_{split}.jsonl")
        write_jsonl(path, out)
        write_meta(path, source=src, separator="blank line", dedup="exact passage text",
                   order="official JSON order (paragraph number in the id)", reader_tokenizer=args.reader)
        print(f"long {split}: {json.dumps(stats[split], ensure_ascii=False)}")

    for name, src in (("train_multi", "viquad_train_clean.jsonl"), ("select_multi", "viquad_select.jsonl")):
        rows = read_jsonl(os.path.join(args.tasks_dir, src))
        out = multi_passage_rows(rows, args.seed, args.min_passages, args.max_passages)
        path = os.path.join(args.tasks_dir, f"viquad_{name}.jsonl")
        write_jsonl(path, out)
        write_meta(path, source=src, seed=args.seed, passages=[args.min_passages, args.max_passages],
                   window="contiguous, JSON order, contains the question's passage")
        sizes = [r["n_passages"] for r in out]
        stats[name] = {"questions": len(out), "of": len(rows), "passages_per_sample": length_stats(sizes),
                       "tokens": length_stats([n_tokens(r["context"]) for r in out[::10]])}
        print(f"{name}: {json.dumps(stats[name])}")
    path = os.path.join(args.tasks_dir, "viquad_long_stats.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
