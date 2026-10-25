"""Data records, JSONL I/O and provenance sidecars.

Every task is a JSONL file with one example per line:

  qa        {id, cluster, context, question, answers, [title], [answer_type], [source],
             [passage_index, n_passages, position]}   the last three on ViQuAD-Long and multi-passage rows
  continue  {id, cluster, context, target, [source], [title]}   stage-1 pairs: context = A, target = B

``cluster`` is the source passage (QA) or document (stage 1). Several questions share one
passage, so the bootstrap resamples clusters, and a memory is written once per cluster.

Every data file written by a script gets a ``<file>.meta.json`` sidecar (script, arguments,
row count, SHA-256, git commit): the LACC pilot leaked its holdout set, so each file must say
where it came from (docs/VILATENT.md §Dữ liệu, "Chống rò rỉ").
"""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Example:
    id: str
    cluster: str
    task: str  # "qa" or "continue"
    context: str
    question: str = ""
    answers: list[str] = field(default_factory=list)
    target: str = ""  # training target: answers[0] for qa, B for continue
    extra: dict = field(default_factory=dict)


def read_jsonl(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: str | Path, rows) -> int:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


# optional QA fields carried into the evaluation rows
QA_EXTRA = ("title", "answer_type", "source", "passage_index", "n_passages", "position")


def load_examples(path: str | Path, task: str, limit: int | None = None) -> list[Example]:
    out = []
    for r in read_jsonl(path)[:limit]:
        if task == "qa":
            answers = list(r["answers"])
            out.append(Example(r["id"], r["cluster"], "qa", r["context"], question=r["question"],
                               answers=answers, target=answers[0],
                               extra={k: r[k] for k in QA_EXTRA if k in r}))
        elif task == "continue":
            out.append(Example(r["id"], r["cluster"], "continue", r["context"], target=r["target"],
                               extra={k: r[k] for k in ("title", "source") if k in r}))
        else:
            raise ValueError(f"unknown task {task!r}")
    return out


def short_hash(text: str) -> str:
    """Passage id used as the cluster (same definition as ViWord-C, so splits match)."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


def split_viquad_train(rows: list[dict], n_viwordc_passages: int = 250, gate_questions: int = 1175,
                       select_questions: int = 600, max_article_questions: int = 200,
                       seed: int = 0) -> tuple[dict[str, list[dict]], dict[str, list[str]]]:
    """Split the ViQuAD train rows (with ``title`` = Wikipedia article) into train, gate,
    select and viwordc_dev.

    * viwordc_dev: ViWord-C's dev, 250 passages sampled by passage (same seed and sampling, so
      the same questions). Its articles also have passages in train, so it is kept out of
      training and reported as an auxiliary table only (comparison with ViWord-C).
    * gate and select: whole articles, disjoint from train and from each other, like the test
      split (ViQuAD validation). Articles are shuffled with ``seed``; only articles with at
      most ``max_article_questions`` questions are eligible, so that no article dominates; gate
      takes articles until it has ``gate_questions`` questions, then select until
      ``select_questions``. gate is only for the G1 gate; select chooses checkpoints, f, τ and
      the BM25 parameters.
    * train: every other row. A passage of viwordc_dev inside a gate or select article is in
      both files (it belongs to that article)."""
    passages = sorted({r["cluster"] for r in rows})
    viwordc = set(random.Random(seed).sample(passages, n_viwordc_passages))
    per_article = Counter(r["title"] for r in rows)
    titles = [t for t in sorted(per_article) if per_article[t] <= max_article_questions]
    random.Random(seed).shuffle(titles)
    held, i = {}, 0
    for name, target in (("gate", gate_questions), ("select", select_questions)):
        held[name], n = [], 0
        while n < target:
            if i == len(titles):
                raise ValueError(f"not enough eligible articles for {name}")
            held[name].append(titles[i])
            n += per_article[titles[i]]
            i += 1
    gate, select = set(held["gate"]), set(held["select"])
    splits = {"train": [r for r in rows if r["title"] not in gate | select and r["cluster"] not in viwordc],
              "gate": [r for r in rows if r["title"] in gate],
              "select": [r for r in rows if r["title"] in select],
              "viwordc_dev": [r for r in rows if r["cluster"] in viwordc]}
    return splits, held


# ---------------------------------------------------------------------------- long contexts

PASSAGE_SEPARATOR = "\n\n"  # a newline always ends a sentence (text.split_sentences), so chunks never span passages


def paragraph_key(row: dict) -> tuple:
    """Position of a ViQuAD row's passage in the official JSON file: ids are
    ``viquad-<article>-<paragraph>-<question>``, numbered in file order."""
    return tuple(int(x) for x in row["id"].split("-")[1:3])


def article_passages(rows: list[dict]) -> dict[str, list[str]]:
    """Distinct passages of every article (``title``), in JSON order. Duplicates are removed by
    exact text (none occur in ViQuAD 2.0 train or validation)."""
    order = {}
    for r in rows:
        order.setdefault(r["title"], {}).setdefault(r["context"], paragraph_key(r))
    return {t: sorted(ps, key=ps.get) for t, ps in order.items()}


def position_bin(index: int, n_passages: int) -> str:
    """Third of the article that holds a passage: beginning, middle or end (checklist A25)."""
    x = (index + 0.5) / n_passages
    return "beginning" if x < 1 / 3 else ("middle" if x < 2 / 3 else "end")


def long_rows(rows: list[dict], passages: dict[str, list[str]]) -> list[dict]:
    """ViQuAD-Long (revision of 25/10/2026): every question reads the whole article, i.e. all its
    passages in JSON order joined by a blank line, with no length limit. ``cluster`` stays the
    question's own passage and ``title`` the article; ``passage_index`` / ``n_passages`` locate
    the passage. The memory of an article is written once and shared by all its questions."""
    out = []
    for r in rows:
        ps = passages[r["title"]]
        i = ps.index(r["context"])
        out.append({**r, "context": PASSAGE_SEPARATOR.join(ps), "passage_index": i, "n_passages": len(ps),
                    "position": position_bin(i, len(ps))})
    return out


def multi_passage_rows(rows: list[dict], seed: int = 0, min_passages: int = 2,
                       max_passages: int = 8) -> list[dict]:
    """Multi-passage training samples (checklist A22): for every question of an article with at
    least ``min_passages`` passages in ``rows``, a contiguous window of n ~ U{min, max} passages
    (at most the article's count) of that article, in JSON order, that contains the question's
    passage at a uniformly drawn offset. Only passages present in ``rows`` are used, so a
    leak-filtered training file stays clean. Ids get a "multi-" prefix."""
    rng = random.Random(seed)
    passages = article_passages(rows)
    out = []
    for r in rows:
        ps = passages[r["title"]]
        if len(ps) < min_passages:
            continue
        n = rng.randint(min_passages, min(max_passages, len(ps)))
        g = ps.index(r["context"])
        start = rng.randint(max(0, g - n + 1), min(g, len(ps) - n))
        out.append({**r, "id": f"multi-{r['id']}", "context": PASSAGE_SEPARATOR.join(ps[start:start + n]),
                    "passage_index": g - start, "n_passages": n})
    return out


# ---------------------------------------------------------------------------- provenance

def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def git_commit() -> str:
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True,
                                         stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"],
                                        text=True, stderr=subprocess.DEVNULL).strip()
        return commit + ("-dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def write_meta(path: str | Path, **info) -> Path:
    """Write ``<path>.meta.json`` next to a data file just written."""
    path = Path(path)
    meta = {
        "file": path.name,
        "sha256": sha256_file(path),
        "rows": sum(1 for _ in open(path, encoding="utf-8")),
        "command": " ".join(sys.argv),
        "git_commit": git_commit(),
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        **info,
    }
    meta_path = path.with_name(path.name + ".meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return meta_path
