"""Data records, JSONL I/O and provenance sidecars.

Every task is a JSONL file with one example per line:

  qa        {id, cluster, context, question, answers, [title], [answer_type], [source]}
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
import subprocess
import sys
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


def load_examples(path: str | Path, task: str, limit: int | None = None) -> list[Example]:
    out = []
    for r in read_jsonl(path)[:limit]:
        if task == "qa":
            answers = list(r["answers"])
            out.append(Example(r["id"], r["cluster"], "qa", r["context"], question=r["question"],
                               answers=answers, target=answers[0],
                               extra={k: r[k] for k in ("title", "answer_type", "source") if k in r}))
        elif task == "continue":
            out.append(Example(r["id"], r["cluster"], "continue", r["context"], target=r["target"],
                               extra={k: r[k] for k in ("title", "source") if k in r}))
        else:
            raise ValueError(f"unknown task {task!r}")
    return out


def short_hash(text: str) -> str:
    """Passage id used as the cluster (same definition as ViWord-C, so splits match)."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


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
