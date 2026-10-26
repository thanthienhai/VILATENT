"""Built data on the Hugging Face Hub, so a later run can download it instead of building it again
(decision of 26/10/2026).

Two bundles, each pushed as one commit of a private dataset repo together with a manifest
(``MANIFEST_<bundle>.json``: path, size and SHA-256 of every file, the git commit that built
them, the time):

  data      what the ``data`` stage writes: data/tasks (ViQuAD splits, ViQuAD-Long, multi-passage
            windows, leak-filtered train), data/eval_ext (contexts used by the leak filter),
            data/corpus (stage-1 documents and the dropped list), data/stage1 (A, B pairs), each
            with its .meta.json sidecar
  teacher   data/teacher/<reader>/*.pt (top-20 teacher log-probs, tied to the template hash)

A download checks every file against the manifest of the requested revision and refuses to
replace a local file that differs, so a run never mixes two builds silently.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .data import git_commit, sha256_file

BUNDLES = {
    "data": ["data/tasks/*.jsonl", "data/tasks/*.meta.json", "data/tasks/*_stats.json",
             "data/eval_ext/*.jsonl", "data/eval_ext/*.meta.json",
             "data/corpus/docs.jsonl", "data/corpus/docs.jsonl.meta.json", "data/corpus/docs.dropped.jsonl",
             "data/stage1/*.jsonl", "data/stage1/*.meta.json"],
    "teacher": ["data/teacher/*/*.pt"],
}


def manifest_name(bundle: str) -> str:
    return f"MANIFEST_{bundle}.json"


def bundle_files(root: str | Path, bundle: str) -> list[str]:
    """Repository-relative paths (forward slashes) of the files of a bundle under ``root``."""
    root = Path(root)
    paths = sorted({p.relative_to(root).as_posix() for pattern in BUNDLES[bundle] for p in root.glob(pattern)
                    if p.is_file()})
    if not paths:
        raise FileNotFoundError(f"no file of the {bundle!r} bundle under {root}: build it first")
    return paths


def build_manifest(root: str | Path, bundle: str) -> dict:
    root = Path(root)
    files = {path: {"size": (root / path).stat().st_size, "sha256": sha256_file(root / path)}
             for path in bundle_files(root, bundle)}
    return {"bundle": bundle, "git_commit": git_commit(),
            "created": datetime.now(timezone.utc).isoformat(timespec="seconds"), "files": files}


def check_files(root: str | Path, manifest: dict) -> list[str]:
    """Paths whose local copy is missing or differs from the manifest (empty when all match)."""
    root = Path(root)
    bad = []
    for path, info in manifest["files"].items():
        local = root / path
        if not local.exists() or local.stat().st_size != info["size"] or sha256_file(local) != info["sha256"]:
            bad.append(path)
    return bad


def conflicts(root: str | Path, manifest: dict) -> list[str]:
    """Local files that exist but differ from the manifest: a download must not replace them silently."""
    root = Path(root)
    return [path for path in check_files(root, manifest) if (root / path).exists()]


def write_manifest(path: str | Path, manifest: dict) -> None:
    Path(path).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
