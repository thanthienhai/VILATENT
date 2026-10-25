"""Train the PhoBERT sentence selector (trained hard baseline, checklist A12/B5; vilatent.selector).

Pairs (question, sentence) of the leak-filtered ViQuAD train passages, label "the sentence
contains a gold answer verbatim"; the checkpoint with the lowest loss on ViQuAD select is kept.
Runs on a T4 (fp16) in about 15–30 minutes.

Usage:
  python scripts/train_selector.py --train data/tasks/viquad_train_clean.jsonl \
      --dev data/tasks/viquad_select.jsonl --out-dir runs/paper/selector --dtype float16
"""
import argparse

from vilatent.data import load_examples
from vilatent.selector import train_selector


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True)
    ap.add_argument("--dev", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--eval-every", type=int, default=1000)
    ap.add_argument("--limit", type=int, default=None, help="first N questions of each file (smoke test)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dtype", choices=["float16", "bfloat16", "float32"], default="bfloat16")
    args = ap.parse_args()
    train_selector(load_examples(args.train, "qa", args.limit), load_examples(args.dev, "qa", args.limit),
                   args.out_dir, epochs=args.epochs, lr=args.lr, batch_size=args.batch_size,
                   eval_every=args.eval_every, seed=args.seed, dtype=args.dtype)


if __name__ == "__main__":
    main()
