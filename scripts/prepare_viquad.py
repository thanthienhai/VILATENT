"""UIT-ViQuAD 2.0 in the normalized QA format, split by Wikipedia article for training and
selection (review of 22/10/2026).

The public test split has no answers, so the validation split is our test set (2,653
answerable questions / 557 passages / 19 articles, none of them in train). The train split is
divided by vilatent.data.split_viquad_train:

  viquad_gate.jsonl         whole articles held out of train: the G1 gate only (~1,228 questions)
  viquad_select.jsonl       other held-out articles: checkpoints, f, τ, BM25 parameters (~621)
  viquad_viwordc_dev.jsonl  ViWord-C's dev (250 passages sampled by passage, same questions as
                            ViWord-C); its articles are also in train, so it is an auxiliary
                            table only, kept out of training
  viquad_train.jsonl        the rest

ViWord-C's dev alone shared all its 90 articles with train (81% of the training rows came from
them), so a trained method was favoured over the untrained hard baselines on it. Unanswerable
questions are dropped. ``cluster`` (the passage) and the sampling of the ViWord-C dev are those
of ViWord-C.

Usage:
  python scripts/prepare_viquad.py --out-dir data/tasks
"""
import argparse
import os

from vilatent.data import short_hash, split_viquad_train, write_jsonl, write_meta
from vilatent.text import normalize

SOURCE = "taidng/UIT-ViQuAD2.0"
DESCRIPTION = {"train": "train minus the gate and select articles and the ViWord-C dev passages",
               "gate": "train, whole articles (G1 gate only)",
               "select": "train, whole articles (checkpoints, f, tau, BM25 parameters)",
               "viwordc_dev": "train, ViWord-C dev passages (auxiliary, same articles as train)",
               "test": "validation"}


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
    ap.add_argument("--n-viwordc-passages", type=int, default=250)
    ap.add_argument("--gate-questions", type=int, default=1175)
    ap.add_argument("--select-questions", type=int, default=600)
    ap.add_argument("--max-article-questions", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    from datasets import load_dataset

    data = load_dataset(SOURCE)
    splits, held = split_viquad_train(rows_of(data["train"]), args.n_viwordc_passages, args.gate_questions,
                                      args.select_questions, args.max_article_questions, args.seed)
    splits["test"] = rows_of(data["validation"])
    for name, rows in splits.items():
        path = os.path.join(args.out_dir, f"viquad_{name}.jsonl")
        write_jsonl(path, rows)
        articles = sorted({r["title"] for r in rows})
        write_meta(path, source=SOURCE, split=DESCRIPTION[name], passages=len({r["cluster"] for r in rows}),
                   n_articles=len(articles), **({"articles": articles} if name in held else {}))
        print(f"viquad {name}: {len(rows)} answerable questions, {len({r['cluster'] for r in rows})} passages, "
              f"{len(articles)} articles")


if __name__ == "__main__":
    main()
