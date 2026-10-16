"""Hard-compression baselines (docs/VILATENT.md §Thiết kế thực nghiệm, "Mốc so sánh").

Every compressor returns a text whose length in reader tokens is at most the budget k given
by ``budget.context_budget`` (the number of memory vectors of ViLatent at the same ratio).

  truncation   keep the head of the context, cut at the k-th reader token
  lead         keep whole sentences from the start while they fit; never cut a sentence, so
               part of the budget may stay unused (reported as tokens actually used)
  bm25         rank sentences by BM25 against the question, keep the best that fit, fill the
               rest of the budget with the head of the best sentence that did not fit, restore
               the original order
  llmlingua2   LLMLingua-2 (xlm-roberta-large), its ``rate`` binary-searched to land in
               [0.97·k, k] reader tokens
  full, none   full context and no context (upper and lower references, no budget)
"""
from __future__ import annotations

import math
from collections import Counter

from .text import split_sentences, syllables


class TokenCounter:
    """Counts reader tokens of a text exactly as it sits in the context slot of the prompt:
    ``lead`` + text (template.ReaderTemplate.slot), no special tokens."""

    def __init__(self, tokenizer, lead: str = ""):
        self.tokenizer, self.lead = tokenizer, lead

    def _slot(self, text: str) -> str:
        return self.lead + text if text else ""

    def offsets(self, text: str) -> list[tuple[int, int]]:
        """Token character spans, relative to ``text`` (the lead is removed)."""
        enc = self.tokenizer(self._slot(text), add_special_tokens=False, return_offsets_mapping=True)
        n = len(self.lead) if text else 0
        return [(max(0, a - n), max(0, b - n)) for a, b in enc["offset_mapping"]]

    def count(self, text: str) -> int:
        return len(self.tokenizer(self._slot(text), add_special_tokens=False)["input_ids"])


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


def bm25_scores(query: str, documents: list[str], k1: float = 1.5, b: float = 0.75) -> list[float]:
    """Okapi BM25 on lowercased syllables; IDF over ``documents`` (the sentences of one context)."""
    docs = [syllables(d) for d in documents]
    n = len(docs)
    avg_len = sum(len(d) for d in docs) / max(n, 1) or 1.0
    df = Counter(t for d in docs for t in set(d))
    q_terms = set(syllables(query))
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


class BM25Sentences:
    name = "bm25"

    def compress(self, context, question, budget, counter):
        sentences = _sentences(context)
        if not sentences:
            return ""
        scores = bm25_scores(question, sentences)
        order = sorted(range(len(sentences)), key=lambda i: (-scores[i], i))

        def render(keep: set[int], partial: tuple[int, str] | None = None) -> str:
            parts = []
            for i, s in enumerate(sentences):
                if i in keep:
                    parts.append(s)
                elif partial is not None and i == partial[0] and partial[1]:
                    parts.append(partial[1])
            return " ".join(parts)

        keep, best_rest = set(), None
        for i in order:
            if counter.count(render(keep | {i})) <= budget:
                keep.add(i)
            elif best_rest is None:
                best_rest = i
        if best_rest is None:
            return render(keep)
        # fill: longest head of the best non-fitting sentence that keeps the total within budget
        words = sentences[best_rest].split()
        low, high = 0, len(words)
        while low < high:
            mid = (low + high + 1) // 2
            if counter.count(render(keep, (best_rest, " ".join(words[:mid])))) <= budget:
                low = mid
            else:
                high = mid - 1
        return render(keep, (best_rest, " ".join(words[:low])))


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


def build_baseline(name: str, device: str = "cuda"):
    simple = {"full": Full, "none": NoContext, "truncation": Truncation, "lead": LeadSentences,
              "bm25": BM25Sentences}
    if name in simple:
        return simple[name]()
    if name == "llmlingua2":
        return LLMLingua2(device)
    raise ValueError(f"unknown baseline {name!r}")
