"""Stage-1 (A, B) pairs: the writer compresses A, the reader must continue with B.

For each document (one pair per document): start at a random sentence start, draw a target
length ℓ ~ U[a_min, a_max] reader tokens, end A at the sentence end closest to ℓ within
[a_min, a_max], and take the next ``b_len`` reader tokens as B. Wikipedia and news are mixed
50 : 50. Train and dev pairs come from different documents.

Output rows: {id, cluster (= document id), source, title, context (= A), target (= B)}.

Usage:
  python scripts/make_pairs.py --docs data/corpus/docs.jsonl --reader Qwen/Qwen3.5-2B \
      --n-train 96000 --n-dev 1000 --out-dir data/stage1
"""
import argparse
import os
import random

from tqdm import tqdm

from vilatent.budget import sentence_cuts, tokenize_context
from vilatent.data import read_jsonl, write_jsonl, write_meta


def make_pair(text: str, tokenizer, rng: random.Random, a_min: int, a_max: int, b_len: int):
    ids, offsets = tokenize_context(text, tokenizer)
    cuts = sentence_cuts(text, offsets)
    starts = [0] + [c for c in cuts if c < len(ids)]
    starts = [s for s in starts if len(ids) - s >= a_min + b_len]
    if not starts:
        return None
    start = rng.choice(starts)
    target = rng.randint(a_min, a_max)
    ends = [c for c in cuts if a_min <= c - start <= a_max and c + b_len <= len(ids)]
    if not ends:
        return None
    end = min(ends, key=lambda c: abs(c - start - target))
    a = text[offsets[start][0]:offsets[end - 1][1]].strip()
    b = text[offsets[end][0]:offsets[end + b_len - 1][1]].strip()
    return a, b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="data/corpus/docs.jsonl")
    ap.add_argument("--reader", required=True, help="tokenizer that defines the token lengths")
    ap.add_argument("--n-train", type=int, default=96_000)
    ap.add_argument("--n-dev", type=int, default=1_000)
    ap.add_argument("--a-min", type=int, default=128)
    ap.add_argument("--a-max", type=int, default=1024)
    ap.add_argument("--b-len", type=int, default=128)
    ap.add_argument("--wiki-share", type=float, default=0.5)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out-dir", default="data/stage1")
    args = ap.parse_args()

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.reader)
    rng = random.Random(args.seed)
    docs = read_jsonl(args.docs)
    rng.shuffle(docs)
    total = args.n_train + args.n_dev
    want = {"wiki": round(total * args.wiki_share), "news": total - round(total * args.wiki_share)}
    pairs = {"wiki": [], "news": []}
    for doc in tqdm(docs, desc="pairs"):
        src = doc["source"]
        if len(pairs[src]) >= want[src]:
            if all(len(pairs[s]) >= want[s] for s in want):
                break
            continue
        pair = make_pair(doc["text"], tokenizer, rng, args.a_min, args.a_max, args.b_len)
        if pair:
            pairs[src].append({"id": f"s1-{doc['id']}", "cluster": doc["id"], "source": src,
                               "title": doc.get("title", ""), "context": pair[0], "target": pair[1]})
    for src in want:
        if len(pairs[src]) < want[src]:
            raise SystemExit(f"only {len(pairs[src])} {src} pairs for {want[src]} wanted: build a larger corpus")
    # dev: the same 50:50 mix, from documents not used in train
    n_dev_wiki = round(args.n_dev * args.wiki_share)
    dev = pairs["wiki"][:n_dev_wiki] + pairs["news"][:args.n_dev - n_dev_wiki]
    train = pairs["wiki"][n_dev_wiki:] + pairs["news"][args.n_dev - n_dev_wiki:]
    rng.shuffle(train)
    for name, rows in (("train", train), ("dev", dev)):
        path = os.path.join(args.out_dir, f"pairs_{name}.jsonl")
        write_jsonl(path, rows)
        write_meta(path, docs=args.docs, reader_tokenizer=args.reader, a_tokens=[args.a_min, args.a_max],
                   b_tokens=args.b_len, wiki_share=args.wiki_share, seed=args.seed)
        print(f"{name}: {len(rows)} pairs")


if __name__ == "__main__":
    main()
