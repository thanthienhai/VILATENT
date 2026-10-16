"""Text utilities: normalization, regex sentence splitting and syllables.

Sentence boundaries drive the chunking of the writer (chunks always end at a sentence end,
docs/VILATENT.md §Kiến trúc, item 1) and the Lead-k and BM25 baselines, so all of them use
the same splitter.
"""
from __future__ import annotations

import re
import unicodedata

# Lowercase tokens (without their final period) after which a period does not end a sentence.
ABBREVIATIONS = {
    "tp", "tx", "tt", "q", "p", "ths", "th.s", "ts", "pgs", "pgs.ts", "gs", "gs.ts", "bs", "ks",
    "cn", "đ/c", "st", "mr", "mrs", "ms", "dr", "jr", "sr", "vs", "v.v", "vv", "tr", "no", "vol",
    "ed", "etc", "e.g", "i.e", "ca", "ltd", "co", "inc", "corp", "dept",
}

# Candidate end of sentence: terminal punctuation, optional closing quotes or brackets, then
# whitespace. A run of newlines is always a boundary.
_END = re.compile(r"[.!?…]+[\"'”’)\]»]*(?=\s)|\n+")
_PREV_TOKEN = re.compile(r"(\S+)$")


def normalize(text: str) -> str:
    """NFC: Vietnamese text in NFD changes token counts and breaks string matching."""
    return unicodedata.normalize("NFC", text)


def syllables(text: str) -> list[str]:
    """Lowercased syllables without punctuation, the unit of QA F1 and of BM25."""
    return re.findall(r"\w+", text.lower())


def _is_abbreviation(text: str, punct_start: int) -> bool:
    match = _PREV_TOKEN.search(text[:punct_start + 1])
    if not match:
        return False
    token = match.group(1).lower().rstrip(".")
    return token in ABBREVIATIONS or (len(token) == 1 and token.isalpha())


def split_sentences(text: str) -> list[tuple[int, int]]:
    """Return character spans ``(start, end)`` of the sentences of ``text``.

    A period does not end a sentence after a known abbreviation (``TP.``, ``PGS.TS.``,
    ``v.v.``) or a single-letter initial (``J. K. Rowling``), nor when the next word starts
    with a lowercase letter. Decimal numbers never match because no space follows the
    period. Spans exclude surrounding whitespace and cover every non-space character.
    """
    spans, start = [], 0
    for match in _END.finditer(text):
        end = match.end()
        if not match.group().startswith("\n"):
            if match.group().startswith(".") and _is_abbreviation(text, match.start()):
                continue
            rest = text[end:].lstrip()
            if rest and rest[0].islower():
                continue
        _append(spans, text, start, end)
        start = end
    _append(spans, text, start, len(text))
    return spans


def _append(spans: list, text: str, start: int, end: int) -> None:
    piece = text[start:end]
    if piece.strip():
        lead = len(piece) - len(piece.lstrip())
        trail = len(piece) - len(piece.rstrip())
        spans.append((start + lead, end - trail))
