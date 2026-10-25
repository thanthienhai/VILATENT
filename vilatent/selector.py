"""PhoBERT sentence selector, a trained hard baseline (revision of 25/10/2026, checklist A12/B5).

A cross-encoder (vinai/phobert-base-v2, one logit) reads a (question, sentence) pair and is
trained with binary cross-entropy on the label "the sentence contains a gold answer verbatim",
on the sentences of ViQuAD train passages. PhoBERT was pre-trained on word-segmented text, so
both sides are segmented with pyvi (syllables of a word joined by "_"), as for BM25. The
checkpoint with the lowest loss on ViQuAD select is kept. At evaluation the scores rank the
sentences of a context and baselines.pack_sentences packs them into the budget, as for BM25.

The selector never sees the gold answer of an evaluation question: labels exist only for the
training and select files.
"""
from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path

import torch
from tqdm import tqdm

from .data import Example
from .text import segment, split_sentences

SELECTOR_MODEL = "vinai/phobert-base-v2"
MAX_LEN = 256  # PhoBERT's position limit


def sentence_pairs(examples: list[Example]) -> list[tuple[str, str, int]]:
    """(question, sentence, label) for every sentence of every example's context."""
    pairs = []
    for ex in examples:
        for a, b in split_sentences(ex.context):
            sentence = ex.context[a:b]
            pairs.append((ex.question, sentence, int(any(ans in sentence for ans in ex.answers))))
    return pairs


class SentenceScorer:
    def __init__(self, model, tokenizer, device: str = "cuda", batch_size: int = 128):
        self.model, self.tokenizer, self.device, self.batch_size = model, tokenizer, device, batch_size

    @classmethod
    def load(cls, path: str | Path, device: str = "cuda") -> "SentenceScorer":
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        model = AutoModelForSequenceClassification.from_pretrained(path).to(device).eval()
        return cls(model, AutoTokenizer.from_pretrained(path), device)

    def encode(self, questions: list[str], sentences: list[str]):
        return self.tokenizer([segment(q) for q in questions], [segment(s) for s in sentences],
                              truncation="longest_first", max_length=MAX_LEN, padding=True,
                              return_tensors="pt").to(self.device)

    def logits(self, questions: list[str], sentences: list[str]) -> torch.Tensor:
        return self.model(**self.encode(questions, sentences)).logits.squeeze(-1).float()

    @torch.no_grad()
    def score(self, question: str, sentences: list[str]) -> list[float]:
        out = []
        for start in range(0, len(sentences), self.batch_size):
            part = sentences[start:start + self.batch_size]
            out += self.logits([question] * len(part), part).tolist()
        return out


@torch.no_grad()
def dev_metrics(scorer: SentenceScorer, examples: list[Example]) -> dict[str, float]:
    """Mean BCE over the dev pairs, and the share of questions whose top-ranked sentence contains
    a gold answer (among questions where some sentence does)."""
    scorer.model.eval()
    loss, n, hits, answerable = 0.0, 0, 0, 0
    for ex in examples:
        pairs = sentence_pairs([ex])
        labels = torch.tensor([y for *_, y in pairs], dtype=torch.float, device=scorer.device)
        scores = torch.tensor(scorer.score(ex.question, [s for _, s, _ in pairs]), device=scorer.device)
        loss += float(torch.nn.functional.binary_cross_entropy_with_logits(scores, labels, reduction="sum"))
        n += len(pairs)
        if labels.any():
            answerable += 1
            hits += int(labels[int(scores.argmax())] > 0)
    scorer.model.train()
    return {"dev_loss": loss / max(n, 1), "dev_top1": hits / max(answerable, 1)}


def train_selector(train: list[Example], dev: list[Example], out_dir: str | Path, epochs: int = 2,
                   lr: float = 2e-5, batch_size: int = 32, warmup_frac: float = 0.06, eval_every: int = 1000,
                   seed: int = 0, dtype: str = "float16", device: str | None = None) -> dict:
    """Fine-tune PhoBERT on the sentence pairs of ``train``; keep the lowest ``dev`` loss in ``out_dir``."""
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    if device == "cpu":
        dtype = "float32"
    random.seed(seed)
    torch.manual_seed(seed)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(SELECTOR_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(SELECTOR_MODEL, num_labels=1).to(device)
    scorer = SentenceScorer(model, tokenizer, device)
    pairs = sentence_pairs(train)
    steps = epochs * math.ceil(len(pairs) / batch_size)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    warmup = round(warmup_frac * steps)
    scheduler = torch.optim.lr_scheduler.LambdaLR(
        optimizer, lambda s: (s + 1) / warmup if s < warmup else max(0.0, (steps - s) / max(1, steps - warmup)))
    amp = {"float16": torch.float16, "bfloat16": torch.bfloat16}.get(dtype)
    scaler = torch.amp.GradScaler(enabled=dtype == "float16")
    log = open(out_dir / "metrics.jsonl", "w", encoding="utf-8")

    def write(**row):
        log.write(json.dumps(row) + "\n")
        log.flush()
        print(json.dumps(row))

    write(event="start", n_pairs=len(pairs), positive_share=sum(y for *_, y in pairs) / len(pairs), steps=steps)
    best, step, t0 = math.inf, 0, time.time()
    model.train()
    for epoch in range(epochs):
        random.shuffle(pairs)
        for start in tqdm(range(0, len(pairs), batch_size), desc=f"selector epoch {epoch + 1}"):
            batch = pairs[start:start + batch_size]
            labels = torch.tensor([y for *_, y in batch], dtype=torch.float, device=device)
            with torch.autocast(device.split(":")[0], dtype=amp, enabled=amp is not None):
                logits = scorer.logits([q for q, _, _ in batch], [s for _, s, _ in batch])
            loss = torch.nn.functional.binary_cross_entropy_with_logits(logits.float(), labels)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()
            optimizer.zero_grad(set_to_none=True)
            step += 1
            if step % 50 == 0:
                write(event="train", step=step, loss=float(loss), sec_per_step=(time.time() - t0) / step)
            if step % eval_every == 0 or step == steps:
                metrics = dev_metrics(scorer, dev)
                improved = metrics["dev_loss"] < best
                if improved:
                    best = metrics["dev_loss"]
                    model.save_pretrained(out_dir)
                    tokenizer.save_pretrained(out_dir)
                    (out_dir / "selector.json").write_text(json.dumps(
                        {"base": SELECTOR_MODEL, "step": step, "epochs": epochs, "lr": lr, "batch_size": batch_size,
                         "seed": seed, "label": "sentence contains a gold answer verbatim", **metrics}, indent=2),
                        encoding="utf-8")
                write(event="eval", step=step, best=improved, **metrics)
    write(event="end", best_dev_loss=best, hours=(time.time() - t0) / 3600)
    return {"best_dev_loss": best}
