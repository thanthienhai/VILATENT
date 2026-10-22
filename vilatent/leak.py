"""Leak check: 13-syllable n-gram overlap with the evaluation contexts (docs/VILATENT.md
§Dữ liệu, "Chống rò rỉ"). Wikipedia articles of the evaluation passages are removed by title
first (scripts/build_corpus.py); this n-gram check then runs on every training file.

The evaluation side includes VietNews (about 45 thousand articles, some 30 million n-grams), so
the index is a sorted int64 array of n-gram hashes searched with ``np.searchsorted`` rather
than a Python set (several GB). Hashes use Python's ``hash``, salted per process: an index is
only valid in the process that built it.
"""
from __future__ import annotations

import numpy as np

from .text import syllables


def shingle_hashes(text: str, n: int = 13) -> np.ndarray:
    s = syllables(text)
    return np.fromiter((hash(tuple(s[i:i + n])) for i in range(len(s) - n + 1)), dtype=np.int64)


def read_contexts(paths) -> list[str]:
    """Distinct ``context`` fields of the evaluation files."""
    from .data import read_jsonl

    return list(dict.fromkeys(r["context"] for path in paths for r in read_jsonl(path)))


class LeakIndex:
    """n-gram index of all evaluation contexts. It refuses to be empty: a check that silently
    compares against nothing is worse than no check."""

    def __init__(self, texts: list[str], n: int = 13):
        self.n = n
        parts = [shingle_hashes(t, n) for t in texts]
        self.grams = np.unique(np.concatenate(parts)) if parts else np.empty(0, dtype=np.int64)
        if not len(self.grams):
            raise ValueError("leak index is empty: evaluation files missing or too short")

    def __len__(self) -> int:
        return len(self.grams)

    def leaks(self, text: str) -> bool:
        q = shingle_hashes(text, self.n)
        if not len(q):
            return False
        idx = np.searchsorted(self.grams, q).clip(max=len(self.grams) - 1)
        return bool((self.grams[idx] == q).any())
