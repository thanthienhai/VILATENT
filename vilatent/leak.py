"""Leak check: 13-syllable n-gram overlap with the evaluation contexts (docs/VILATENT.md
§Dữ liệu, "Chống rò rỉ"). Wikipedia articles of the evaluation passages are removed by title
first (scripts/build_corpus.py); this n-gram check then runs on every training file.
"""
from __future__ import annotations

from .text import syllables


def shingles(text: str, n: int = 13) -> set[int]:
    s = syllables(text)
    return {hash(tuple(s[i:i + n])) for i in range(len(s) - n + 1)}


class LeakIndex:
    """n-gram index of all evaluation contexts. It refuses to be empty: a check that silently
    compares against nothing is worse than no check."""

    def __init__(self, texts: list[str], n: int = 13):
        self.n = n
        self.grams: set[int] = set()
        for t in texts:
            self.grams |= shingles(t, n)
        if not self.grams:
            raise ValueError("leak index is empty: evaluation files missing or too short")

    def leaks(self, text: str) -> bool:
        return not shingles(text, self.n).isdisjoint(self.grams)
