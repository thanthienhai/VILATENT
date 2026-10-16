"""UIT-ViQuAD 2.0 in the normalized QA format, with ViWord-C's split.

The public test split has no answers, so the validation split is our test set (2,653
answerable questions / 557 passages) and dev is 250 passages sampled from train
(1,175 questions). Train is the rest of train. Unanswerable questions are dropped. The
passage id (``cluster``), the seed and the sampling are those of ViWord-C, so dev and test
are the same questions in both projects.

Usage:
  python scripts/prepare_viquad.py --out-dir data/tasks
"""
import argparse
import os
import random

from vilatent.data import short_hash, write_jsonl, write_meta
from vilatent.text import normalize

SOURCE = "taidng/UIT-ViQuAD2.0"


def rows_of(split) -> list[dict]:
    rows = []
    for r in split:
        answers = list(dict.fromkeys(r["answers"]["text"])) if r["answers"] else []
        if r["is_impossible"] or not answers:
            continue
        # cluster = hash of the raw context, as in ViWord-C; the text itself is normalized
        rows.append({"id": f"viquad-{r['id']}", "cluster": short_hash(r["context"]), "title": normalize(r["title"]),
                     "context": normalize(r["context"]), "question": normalize(r["question"]),
                     "answers": [normalize(a) for a in answers]})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="data/tasks")
    ap.add_argument("--n-dev-passages", type=int, default=250)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    from datasets import load_dataset

    data = load_dataset(SOURCE)
    test, train_all = rows_of(data["validation"]), rows_of(data["train"])
    passages = sorted({r["cluster"] for r in train_all})
    dev_passages = set(random.Random(args.seed).sample(passages, args.n_dev_passages))
    splits = {"train": [r for r in train_all if r["cluster"] not in dev_passages],
              "dev": [r for r in train_all if r["cluster"] in dev_passages], "test": test}
    for name, rows in splits.items():
        path = os.path.join(args.out_dir, f"viquad_{name}.jsonl")
        write_jsonl(path, rows)
        write_meta(path, source=SOURCE, split={"train": "train minus dev passages", "dev": "train, 250 passages",
                                               "test": "validation"}[name],
                   passages=len({r["cluster"] for r in rows}))
        print(f"viquad {name}: {len(rows)} answerable questions, {len({r['cluster'] for r in rows})} passages")


if __name__ == "__main__":
    main()
