"""Hard-compression baselines (docs/VILATENT.md §Thiết kế thực nghiệm, "Mốc so sánh").

Every compressor returns a text whose length in reader tokens is at most the budget k given
by ``budget.context_budget`` (the number of memory vectors of ViLatent at the same ratio).

  truncation   keep the head of the context, cut at the k-th reader token
  lead         keep whole sentences from the start while they fit; never cut a sentence, so
               part of the budget may stay unused (reported as tokens actually used)
  bm25         rank sentences by BM25 against the question, keep the best that fit (only those
               sharing a term with the question, score > 0), fill the rest of the budget
               with the head of the best sentence that did not fit (cut at a reader token),
               restore the original order. Terms are pyvi words, lowercased, with the question
               words removed from the query (revision of 25/10/2026; G1 used syllables). k1 and b
               come from configs/bm25.json, tuned on ViQuAD select (scripts/tune_bm25.py);
               ViLatent-ME uses the same values
  phobert      the same packing, sentences ranked by a trained PhoBERT cross-encoder
               ("the sentence contains the answer", vilatent.selector)
  llmlingua2   LLMLingua-2 (xlm-roberta-large), its ``rate`` binary-searched to land in
               [0.97·k, k] reader tokens
  full, none   full context and no context (upper and lower references, no budget)
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

from .text import query_words, split_sentences, syllables, words


class TokenCounter:
    """Counts reader tokens of a text exactly as it sits in the context slot of the prompt:
    ``lead`` + text (template.ReaderTemplate.slot), no special tokens."""

    def __init__(self, tokenizer, lead: str = ""):
        self.tokenizer, self.lead = tokenizer, lead
        self._short = {}  # counts of short texts (sentences), reused across questions and budgets

    def _slot(self, text: str) -> str:
        return self.lead + text if text else ""

    def offsets(self, text: str) -> list[tuple[int, int]]:
        """Token character spans, relative to ``text`` (the lead is removed)."""
        enc = self.tokenizer(self._slot(text), add_special_tokens=False, return_offsets_mapping=True)
        n = len(self.lead) if text else 0
        return [(max(0, a - n), max(0, b - n)) for a, b in enc["offset_mapping"]]

    def count(self, text: str) -> int:
        if len(text) <= 2000 and text in self._short:
            return self._short[text]
        n = len(self.tokenizer(self._slot(text), add_special_tokens=False)["input_ids"])
        if len(text) <= 2000 and len(self._short) < 1_000_000:
            self._short[text] = n
        return n


def fit_head(text: str, budget: int, counter: TokenCounter) -> str:
    """Longest prefix of ``text`` (cut at a token end) with at most ``budget`` reader tokens."""
    if budget <= 0:
        return ""
    offsets = counter.offsets(text)
    if len(offsets) <= budget:
        return text
    n = budget
    while n > 0:
        head = text[:offsets[n - 1][1]].rstrip()
        if counter.count(head) <= budget:
            return head
        n -= 1
    return ""


def _sentences(text: str) -> list[str]:
    return [text[a:b] for a, b in split_sentences(text)]


class Full:
    name = "full"

    def compress(self, context, question, budget, counter):
        return context


class NoContext:
    name = "none"

    def compress(self, context, question, budget, counter):
        return ""


class Truncation:
    name = "truncation"

    def compress(self, context, question, budget, counter):
        return fit_head(context, budget, counter)


class LeadSentences:
    name = "lead"

    def compress(self, context, question, budget, counter):
        kept = []
        for sentence in _sentences(context):
            if counter.count(" ".join(kept + [sentence])) > budget:
                break
            kept.append(sentence)
        return " ".join(kept)


def bm25_terms(text: str, units: str = "word", query: bool = False) -> list[str]:
    """BM25 terms: pyvi words (``units="word"``; question words removed from a query) or lowercased
    syllables (``"syllable"``, the G1 version, kept to measure the change)."""
    if units == "word":
        return query_words(text) if query else words(text)
    if units == "syllable":
        return syllables(text)
    raise ValueError(f"unknown BM25 units {units!r}")


def bm25_scores(query: str, documents: list[str], k1: float = 1.5, b: float = 0.75,
                units: str = "word") -> list[float]:
    """Okapi BM25 of ``query`` against ``documents`` (the sentences of one context, which also give
    the IDF)."""
    docs = [bm25_terms(d, units) for d in documents]
    n = len(docs)
    avg_len = sum(len(d) for d in docs) / max(n, 1) or 1.0
    df = Counter(t for d in docs for t in set(d))
    q_terms = set(bm25_terms(query, units, query=True))
    scores = []
    for d in docs:
        tf = Counter(d)
        s = 0.0
        for t in q_terms:
            if tf[t]:
                idf = math.log((n - df[t] + 0.5) / (df[t] + 0.5) + 1)
                s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(d) / avg_len))
        scores.append(s)
    return scores


def load_bm25_params(path: str | Path) -> dict:
    """``{"k1", "b", "units"}`` of a configs/bm25.json written by scripts/tune_bm25.py (a file
    without ``units`` was tuned on syllables)."""
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    return {"k1": float(cfg["k1"]), "b": float(cfg["b"]), "units": cfg.get("units", "syllable")}


def pack_sentences(sentences: list[str], scores: list[float], budget: int, counter: TokenCounter,
                   positive_only: bool) -> str:
    """Keep the best-scored sentences that fit whole (only those with score > 0 when
    ``positive_only``), fill the rest of the budget with the head of the best sentence that did
    not fit, cut at a reader-token end, and restore the original order.

    Sentences are packed with their own token counts (each sits after one space, the slot lead
    or the joining space), so long contexts (ViQuAD-Long) are not re-tokenized for every
    candidate; the joined text is then counted exactly and the lowest-ranked kept sentences are
    dropped in the rare case where tokens merge across a join."""
    if not sentences or budget <= 0:
        return ""
    order = sorted(range(len(sentences)), key=lambda i: (-scores[i], i))
    rank = {i: r for r, i in enumerate(order)}

    def render(keep: set[int], partial: tuple[int, str] | None = None) -> str:
        parts = []
        for i, s in enumerate(sentences):
            if i in keep:
                parts.append(s)
            elif partial is not None and i == partial[0] and partial[1]:
                parts.append(partial[1])
        return " ".join(parts)

    # sentences sharing no term with the question (score 0) are never packed whole when
    # positive_only: they would take the budget from the head of the best sentence that does not fit
    keep, used, best_rest = set(), 0, None
    for i in order:
        cost = counter.count(sentences[i])
        if (scores[i] > 0 or not positive_only) and used + cost <= budget:
            keep.add(i)
            used += cost
        elif best_rest is None:
            best_rest = i
    for i in sorted(keep, key=lambda i: -rank[i]):
        if counter.count(render(keep)) <= budget:
            break
        keep.discard(i)
        best_rest = i if best_rest is None or rank[i] < rank[best_rest] else best_rest
    if best_rest is None:
        return render(keep)
    # fill: longest head of the best non-fitting sentence, cut at a reader token end (as
    # truncation), that keeps the total within budget; a whole word such as "1010," may be
    # several tokens, so cutting at words would leave budget unused
    sentence = sentences[best_rest]
    heads = [""] + [sentence[:end].rstrip() for _, end in counter.offsets(sentence)]
    low, high = 0, len(heads) - 1
    while low < high:
        mid = (low + high + 1) // 2
        if counter.count(render(keep, (best_rest, heads[mid]))) <= budget:
            low = mid
        else:
            high = mid - 1
    return render(keep, (best_rest, heads[low]))


class BM25Sentences:
    name = "bm25"

    def __init__(self, k1: float = 1.5, b: float = 0.75, units: str = "word"):
        self.k1, self.b, self.units = k1, b, units

    def compress(self, context, question, budget, counter):
        sentences = _sentences(context)
        scores = bm25_scores(question, sentences, self.k1, self.b, self.units)
        return pack_sentences(sentences, scores, budget, counter, positive_only=True)


class PhoBERTSentences:
    """Trained hard compressor (revision of 25/10/2026): a PhoBERT cross-encoder scores every
    (question, sentence) pair for "the sentence contains the answer" (vilatent.selector); the
    sentences are packed like BM25's, without the score > 0 rule. Scores do not depend on the
    budget, so they are cached per (context, question) and reused across ratios."""
    name = "phobert"

    def __init__(self, model_dir: str, device: str = "cuda"):
        from .selector import SentenceScorer

        self.scorer = SentenceScorer.load(model_dir, device)
        self.cache = {}

    def compress(self, context, question, budget, counter):
        sentences = _sentences(context)
        key = (context, question)
        if key not in self.cache:
            self.cache[key] = self.scorer.score(question, sentences)
        return pack_sentences(sentences, self.cache[key], budget, counter, positive_only=False)


class LLMLingua2:
    name = "llmlingua2"
    MODEL = "microsoft/llmlingua-2-xlm-roberta-large-meetingbank"

    def __init__(self, device: str = "cuda"):
        from llmlingua import PromptCompressor

        self.pc = PromptCompressor(model_name=self.MODEL, use_llmlingua2=True, device_map=device)

    def compress(self, context, question, budget, counter, tolerance: float = 0.03, steps: int = 12):
        """Binary search of LLMLingua-2's rate; the longest output within the budget wins."""
        low, high, best, best_n = 0.01, 1.0, "", -1
        for _ in range(steps):
            rate = (low + high) / 2
            text = self.pc.compress_prompt(context, rate=rate)["compressed_prompt"]
            n = counter.count(text)
            if n <= budget:
                if n > best_n:
                    best, best_n = text, n
                if n >= budget * (1 - tolerance):
                    break
                low = rate
            else:
                high = rate
        return best


def build_baseline(name: str, device: str | None = None, bm25: dict | None = None, selector: str | None = None):
    """``bm25``: the tuned ``{"k1", "b", "units"}`` (load_bm25_params), required for the bm25
    baseline; ``selector``: the trained PhoBERT selector directory, required for phobert."""
    if device is None:
        import torch

        device = "cuda" if torch.cuda.is_available() else "cpu"
    simple = {"full": Full, "none": NoContext, "truncation": Truncation, "lead": LeadSentences}
    if name in simple:
        return simple[name]()
    if name == "bm25":
        if bm25 is None:
            raise ValueError("the bm25 baseline needs its tuned parameters (configs/bm25.json)")
        return BM25Sentences(**bm25)
    if name == "phobert":
        if selector is None:
            raise ValueError("the phobert baseline needs a trained selector (scripts/train_selector.py)")
        return PhoBERTSentences(selector, device)
    if name == "llmlingua2":
        return LLMLingua2(device)
    raise ValueError(f"unknown baseline {name!r}")
