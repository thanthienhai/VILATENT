"""QA metrics on syllables and output checks (docs/VILATENT.md §Thiết kế thực nghiệm, "Độ đo").

F1 and EM are SQuAD-style, on lowercased syllables without punctuation, maximised over the
gold answers. An answer is unreadable when it contains a thinking block or when the reader
did not end its turn within ``max_new_tokens`` (128 for QA; a long reasoning text); the share of
unreadable answers must stay below 2%. Greedy repetition is counted separately.
"""
from __future__ import annotations

from collections import Counter

from .text import normalize, syllables


def _syllables(text: str) -> list[str]:
    return syllables(normalize(text))  # NFC first: \w does not match NFD combining marks


def qa_f1(prediction: str, reference: str) -> float:
    p, r = _syllables(prediction), _syllables(reference)
    overlap = sum((Counter(p) & Counter(r)).values())
    if not overlap:
        return 0.0
    precision, recall = overlap / len(p), overlap / len(r)
    return 2 * precision * recall / (precision + recall)


def qa_em(prediction: str, reference: str) -> float:
    r = _syllables(reference)
    return float(bool(r) and _syllables(prediction) == r)  # an empty answer never matches


def parse_answer(text: str) -> str:
    """The first non-empty line of the reader output (the QA prompt asks for a short phrase)."""
    for line in text.strip().split("\n"):
        if line.strip():
            return line.strip()
    return ""


def score_qa(prediction: str, answers: list[str]) -> dict[str, float]:
    return {"f1": max(qa_f1(prediction, a) for a in answers),
            "em": max(qa_em(prediction, a) for a in answers)}


def is_unreadable(raw: str, stopped: bool) -> bool:
    return "<think>" in raw or "</think>" in raw or not stopped


def is_repetitive(text: str, n: int = 3, times: int = 3) -> bool:
    """A syllable n-gram that occurs at least ``times`` times (greedy decoding loops)."""
    s = syllables(text)
    grams = Counter(tuple(s[i:i + n]) for i in range(len(s) - n + 1))
    return any(c >= times for c in grams.values())
