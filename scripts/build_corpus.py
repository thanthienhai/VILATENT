"""Stage-1 document pool: Vietnamese Wikipedia + BKAINewsCorpus, leak-filtered.

Leak control (docs/VILATENT.md §Dữ liệu, "Chống rò rỉ"):
  1. every Wikipedia article whose title is the title of a dev/test passage is removed;
  2. every document sharing a 13-syllable n-gram with a dev/test context is removed.
Both checks use the evaluation files given with --eval-files (all dev and test files).

Documents are streamed with a shuffle buffer and kept when they are long enough to give one
(A, B) pair (scripts/make_pairs.py). Output rows: {id, source, title, text}.

Usage:
  python scripts/build_corpus.py --eval-files data/tasks/viquad_dev.jsonl data/tasks/viquad_test.jsonl \
      --n-wiki 200000 --n-news 200000 --out data/corpus/docs.jsonl
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from tqdm import tqdm

from vilatent.data import read_jsonl, write_meta
from vilatent.leak import LeakIndex
from vilatent.text import normalize

WIKI = ("wikimedia/wikipedia", "20231101.vi")
NEWS = ("bkai-foundation-models/BKAINewsCorpus", None)


def stream(name: str, config: str | None, seed: int):
    from datasets import load_dataset

    return load_dataset(name, config, split="train", streaming=True).shuffle(seed=seed, buffer_size=10_000)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-files", nargs="+", required=True)
    ap.add_argument("--n-wiki", type=int, default=200_000)
    ap.add_argument("--n-news", type=int, default=200_000)
    ap.add_argument("--min-chars", type=int, default=1500, help="about 300+ reader tokens")
    ap.add_argument("--max-chars", type=int, default=20_000, help="longer documents are cut")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="data/corpus/docs.jsonl")
    args = ap.parse_args()

    eval_rows = [r for path in args.eval_files for r in read_jsonl(path)]
    titles = {normalize(r["title"]).casefold() for r in eval_rows if r.get("title")}
    if not titles:
        raise SystemExit("no titles in the evaluation files: run scripts/prepare_viquad.py first")
    index = LeakIndex(list({r["context"] for r in eval_rows}))
    dropped = Counter()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        for source, (name, config), target in (("wiki", WIKI, args.n_wiki), ("news", NEWS, args.n_news)):
            kept = 0
            bar = tqdm(total=target, desc=source)
            for r in stream(name, config, args.seed):
                text = normalize(r["text"])[:args.max_chars]
                title = normalize(r.get("title") or "")
                if len(text) < args.min_chars:
                    dropped[(source, "short")] += 1
                    continue
                if source == "wiki" and title.casefold() in titles:
                    dropped[(source, "eval_title")] += 1
                    continue
                if index.leaks(text):
                    dropped[(source, "ngram")] += 1
                    continue
                f.write(json.dumps({"id": f"{source}-{r['id']}", "source": source, "title": title, "text": text},
                                   ensure_ascii=False) + "\n")
                kept += 1
                bar.update()
                if kept >= target:
                    break
            bar.close()
    stats = {f"{s}/{reason}": n for (s, reason), n in dropped.items()}
    write_meta(args.out, sources={"wiki": "/".join(WIKI), "news": NEWS[0]}, eval_files=args.eval_files,
               eval_titles=len(titles), dropped=stats)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
