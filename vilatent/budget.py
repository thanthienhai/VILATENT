"""Chunking and the reader-token budget, shared by training, evaluation and every baseline.

The compression ratio r is "reader tokens of the context / memory tokens" (docs/VILATENT.md
§Câu hỏi nghiên cứu). The context is cut into chunks of at most ``max_tokens`` reader
tokens that end at a sentence end; every chunk gives ceil(n_i / r) memory vectors (the last
group of a chunk may hold fewer than r tokens). The budget

    k = Σ_i ceil(n_i / r)

is the number of memory vectors. The two boundary embeddings ⟨mem⟩ ⟨/mem⟩ are not counted:
they play the role of the "Đoạn văn:" label of a text prompt. Hard baselines receive exactly
k reader tokens, so both sides are compared on the same reader budget.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from .text import split_sentences

DEFAULT_CHUNK_TOKENS = 512


@dataclass
class Chunked:
    ids: list[int]  # reader token ids of the whole context (no special tokens)
    bounds: list[tuple[int, int]]  # [start, end) token range of every chunk

    @property
    def chunks(self) -> list[list[int]]:
        return [self.ids[a:b] for a, b in self.bounds]

    @property
    def lengths(self) -> list[int]:
        return [b - a for a, b in self.bounds]

    @property
    def n_tokens(self) -> int:
        return len(self.ids)


def tokenize_context(text: str, tokenizer) -> tuple[list[int], list[tuple[int, int]]]:
    enc = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
    return list(enc["input_ids"]), [tuple(o) for o in enc["offset_mapping"]]


def sentence_cuts(text: str, offsets: list[tuple[int, int]]) -> list[int]:
    """Token indices at which a sentence ends: the first token that starts at or after the
    end character of a sentence (the token that carries the following space starts there)."""
    cuts, t = [], 0
    for _, end in split_sentences(text):
        while t < len(offsets) and offsets[t][0] < end:
            t += 1
        cuts.append(t)
    return sorted(set(c for c in cuts if 0 < c <= len(offsets)) | {len(offsets)})


def pack_chunks(cuts: list[int], n_tokens: int, max_tokens: int) -> list[tuple[int, int]]:
    """Greedily pack whole sentences into chunks of at most ``max_tokens`` tokens. A single
    sentence longer than ``max_tokens`` is split into pieces of ``max_tokens`` tokens."""
    bounds, start, last_cut = [], 0, 0
    for cut in cuts:
        while cut - start > max_tokens:
            if last_cut > start:
                bounds.append((start, last_cut))
                start = last_cut
            else:
                bounds.append((start, start + max_tokens))
                start += max_tokens
        last_cut = cut
    if start < n_tokens:
        bounds.append((start, n_tokens))
    return bounds


def chunk_context(text: str, tokenizer, max_tokens: int = DEFAULT_CHUNK_TOKENS, lead: str = "") -> Chunked:
    """``lead`` is the template's slot prefix (a space, see template.ReaderTemplate.slot), so
    the chunk ids are exactly the ids of the context as it appears in a text prompt."""
    text = lead + text if text else ""
    ids, offsets = tokenize_context(text, tokenizer)
    if not ids:
        return Chunked(ids=[], bounds=[])
    return Chunked(ids=ids, bounds=pack_chunks(sentence_cuts(text, offsets), len(ids), max_tokens))


def memory_budget(chunk_lengths: list[int], ratio: int) -> int:
    """k = Σ ceil(n_i / r): the number of memory vectors, and the hard-baseline token budget."""
    return sum(math.ceil(n / ratio) for n in chunk_lengths)


def context_budget(text: str, tokenizer, ratio: int, max_tokens: int = DEFAULT_CHUNK_TOKENS,
                   lead: str = "") -> tuple[int, int]:
    """``(n_tokens, k)`` of a context for one ratio, the single entry point used everywhere."""
    chunked = chunk_context(text, tokenizer, max_tokens, lead)
    return chunked.n_tokens, memory_budget(chunked.lengths, ratio)
