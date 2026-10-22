"""Contexts of the evaluation sets used after G1, for the leak filters only (decision of
22/10/2026): build_corpus.py, leak_filter.py and filter_qa.py drop training text that shares a
13-syllable n-gram with them, and build_corpus.py drops the Wikipedia articles whose title is
an MLQA title (MLQA paragraphs come from Wikipedia, like ViQuAD). Vi-MQA (VMLU) is added once
its licence is checked.

  mlqa_vi_dev.jsonl, mlqa_vi_test.jsonl   MLQA v1, context vi / question vi (H2)
  belebele_vi.jsonl                        Belebele vie_Latn passages (FLORES; no title)
  vietnews_dev.jsonl, vietnews_test.jsonl  VietNews validation and test, all articles (summaries);
                                           the release is word-segmented ("Cơ_quan") and is
                                           detokenized as in ViWord-C; context = abstract + article

Output rows: {id, cluster, context, [title]}. Sources are pinned (URL or Hub revision) and the
meta sidecar of each file records the SHA-256 of the downloaded source.

Usage:
  python scripts/prepare_external_eval.py --out-dir data/eval_ext
"""
import argparse
import json
import os
import re
import urllib.request
import zipfile
from pathlib import Path

from vilatent.data import sha256_file, short_hash, write_jsonl, write_meta
from vilatent.text import normalize

MLQA_URL = "https://dl.fbaipublicfiles.com/MLQA/MLQA_V1.zip"
BELEBELE = ("facebook/belebele", "7899cdfa4e1e0d733fd77c848e2c273cb1d32be2", "data/vie_Latn.jsonl")
VIETNEWS = ("nam194/vietnews", "39e2837bd57c09af5ca6f80a6483d40d904ad1ca",
            {"dev": "data/validation-00000-of-00001-210cc51bf3cdb90f.parquet",
             "test": "data/test-00000-of-00001-123f98d55067eb7b.parquet"})


def detokenize_vietnews(text: str) -> str:
    """'Cơ_quan điều_tra , TP. Hưng_Yên' -> 'Cơ quan điều tra, TP. Hưng Yên' (ViWord-C)."""
    text = text.replace("_", " ")
    text = re.sub(r" ([,.;:!?)\]}%…])", r"\1", text)
    text = re.sub(r"([(\[{]) ", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def mlqa(raw_dir: Path, out_dir: Path) -> None:
    zip_path = raw_dir / "MLQA_V1.zip"
    if not zip_path.exists():
        urllib.request.urlretrieve(MLQA_URL, zip_path)
    with zipfile.ZipFile(zip_path) as z:
        for split in ("dev", "test"):
            data = json.loads(z.read(f"MLQA_V1/{split}/{split}-context-vi-question-vi.json"))["data"]
            rows = {}
            for article in data:
                for p in article["paragraphs"]:
                    context = normalize(p["context"])
                    cluster = short_hash(context)
                    rows.setdefault(context, {"id": f"mlqa-vi-{split}-{cluster}", "cluster": cluster,
                                              "context": context, "title": normalize(article["title"])})
            path = out_dir / f"mlqa_vi_{split}.jsonl"
            write_jsonl(path, rows.values())
            write_meta(path, source=MLQA_URL, source_sha256=sha256_file(zip_path),
                       member=f"{split}-context-vi-question-vi.json")
            print(f"mlqa vi {split}: {len(rows)} paragraphs, {len({r['title'] for r in rows.values()})} articles")


def belebele(out_dir: Path) -> None:
    from huggingface_hub import hf_hub_download

    repo, rev, name = BELEBELE
    src = hf_hub_download(repo, name, repo_type="dataset", revision=rev)
    rows = {}
    with open(src, encoding="utf-8") as f:
        for line in f:
            context = normalize(json.loads(line)["flores_passage"])
            rows.setdefault(context, {"id": f"belebele-vi-{short_hash(context)}", "cluster": short_hash(context),
                                      "context": context})
    path = out_dir / "belebele_vi.jsonl"
    write_jsonl(path, rows.values())
    write_meta(path, source=f"{repo}@{rev}/{name}", source_sha256=sha256_file(src))
    print(f"belebele vi: {len(rows)} passages")


def vietnews(out_dir: Path) -> None:
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download

    repo, rev, files = VIETNEWS
    for split, name in files.items():
        src = hf_hub_download(repo, name, repo_type="dataset", revision=rev)
        table = pq.read_table(src, columns=["guid", "abstract", "article"]).to_pylist()
        rows = [{"id": f"vietnews-{split}-{r['guid']}", "cluster": f"vietnews-{split}-{r['guid']}",
                 "context": normalize(detokenize_vietnews(f"{r['abstract']}\n{r['article']}"))}
                for r in table if r["article"]]
        path = out_dir / f"vietnews_{split}.jsonl"
        write_jsonl(path, rows)
        write_meta(path, source=f"{repo}@{rev}/{name}", source_sha256=sha256_file(src))
        print(f"vietnews {split}: {len(rows)} articles")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="data/eval_ext")
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    raw_dir = out_dir / "raw"
    os.makedirs(raw_dir, exist_ok=True)
    mlqa(raw_dir, out_dir)
    belebele(out_dir)
    vietnews(out_dir)


if __name__ == "__main__":
    main()
