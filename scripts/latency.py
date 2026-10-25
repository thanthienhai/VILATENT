"""End-to-end latency and break-even point (checklist A14/A20, B11). GPU (H100, bf16), batch 1.

For --docs contexts of --data (spread over the file) and up to --questions-per-doc of their
questions, it times, with CUDA synchronisation and after a warm-up:

  writer         memory of the context at ρ = r·f* (ME) and at ρ = r (M), once per document
  selection      BM25 sentences for the question (ME evidence, budget k(r) − k(r·f*); the bm25
                 baseline, k(r); stage 2 of the cascade, 2k(r)); PhoBERT scoring with --selector;
                 LLMLingua-2 compression once per document with --llmlingua
  reader         time to first token (one prefill forward) and end-to-end greedy answer, for full,
                 truncation, bm25, bm25_x2, phobert, llmlingua2, ViLatent-M and ViLatent-ME

Per question, a method costs selection + reader end-to-end; ViLatent also pays the writer once
per document. Break-even (questions per document) against a method X:
    N* = writer / (t_X − t_ViLatent)   (no break-even when t_X ≤ t_ViLatent).
With --cascade (cascade_r<r>.json of the same split), the expected cost of MEF per question is
t_ME + (1 − stage-1 rate)·t_bm25_x2 + fallback rate·t_full.

Usage:
  python scripts/latency.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
      --data data/tasks/viquad_long_test.jsonl --checkpoint runs/paper/stage2_mem/best.pt --ratio 4 \
      --factor 2 --cascade results/paper/test/long/cascade_r4.json --out results/paper/test/latency_long.json
"""
import argparse
import json
import statistics
import time
from pathlib import Path

import torch

from vilatent.baselines import LLMLingua2, PhoBERTSentences, TokenCounter, Truncation
from vilatent.budget import context_budget
from vilatent.data import load_examples
from vilatent.evaluate import MAX_NEW_TOKENS
from vilatent.model import load_vilatent
from vilatent.reader import DTYPES, embed_ids, greedy_generate


def sync():
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def timed(fn):
    sync()
    t0 = time.perf_counter()
    out = fn()
    sync()
    return out, 1000 * (time.perf_counter() - t0)


@torch.no_grad()
def read_times(model, seq: torch.Tensor) -> tuple[float, float]:
    """(time to first token, end-to-end greedy answer) in ms for one prompt."""
    reader = model.reader
    x = seq[None]
    _, ttft = timed(lambda: reader(inputs_embeds=x, use_cache=True, logits_to_keep=1))
    _, e2e = timed(lambda: greedy_generate(reader, [seq], MAX_NEW_TOKENS["qa"], model.stop_ids))
    return ttft, e2e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True)
    ap.add_argument("--reader-config", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--checkpoint", required=True, help="multi-rate ME/M checkpoint")
    ap.add_argument("--ratio", type=int, default=4)
    ap.add_argument("--factor", type=int, required=True, help="f* of ME at this ratio (choices.json)")
    ap.add_argument("--docs", type=int, default=20)
    ap.add_argument("--questions-per-doc", type=int, default=5)
    ap.add_argument("--selector", default=None, help="PhoBERT selector directory (adds phobert)")
    ap.add_argument("--llmlingua", action="store_true", help="add LLMLingua-2 (compression once per document)")
    ap.add_argument("--cascade", default=None, help="cascade_r<r>.json for the expected MEF cost")
    ap.add_argument("--dtype", choices=list(DTYPES), default="bfloat16")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    from vilatent.reader import load_reader
    from vilatent.template import ReaderTemplate, load_reader_config

    reader, tokenizer = load_reader(args.reader, dtype=args.dtype)
    template = ReaderTemplate(load_reader_config(args.reader_config), tokenizer)
    model = load_vilatent(args.checkpoint, reader, tokenizer, template)
    r, f = args.ratio, args.factor
    examples = load_examples(args.data, "qa")
    by_doc = {}
    for ex in examples:
        by_doc.setdefault(ex.context, []).append(ex)
    contexts = list(by_doc)
    step = max(1, len(contexts) // args.docs)
    docs = contexts[::step][:args.docs]
    counter = TokenCounter(tokenizer, lead=template.lead["qa"])
    bm25 = model.selector
    phobert = PhoBERTSentences(args.selector) if args.selector else None
    lingua = LLMLingua2() if args.llmlingua else None
    t = {}  # name -> list of ms

    def add(name, ms):
        t.setdefault(name, []).append(ms)

    for i, ctx in enumerate([docs[0]] + docs):  # the first document is a warm-up, not recorded
        warm = i == 0
        qs = by_doc[ctx][:args.questions_per_doc]
        n, k = context_budget(ctx, tokenizer, r, model.chunk_tokens, lead=template.lead["qa"])
        p_me = [model.prepare(ex, r, f) for ex in qs]
        p_m = [model.prepare(ex, r, 1) for ex in qs]
        mem_me, w_me = timed(lambda: model.encode_memory([p_me[0]])[0])
        mem_m, w_m = timed(lambda: model.encode_memory([p_m[0]])[0])
        compressed = {"truncation": Truncation().compress(ctx, "", k, counter)}
        if lingua:
            compressed["llmlingua2"], ms = timed(lambda: lingua.compress(ctx, "", k, counter))
            if not warm:
                add("llmlingua2_compress_per_doc", ms)
        if not warm:
            add("writer_me_per_doc", w_me)
            add("writer_m_per_doc", w_m)
            add("context_tokens", n)
        for ex, pe, pm in zip(qs, p_me, p_m):
            sel = {}
            k_text = k - (mem_me.shape[0] - 2)  # the budget of ME's evidence: k(r) − k(r·f)
            _, sel["me_evidence"] = timed(lambda: bm25.compress(ctx, ex.question, k_text, counter))
            texts = dict(compressed)
            texts["bm25"], sel["bm25"] = timed(lambda: bm25.compress(ctx, ex.question, k, counter))
            texts["bm25_x2"], sel["bm25_x2"] = timed(lambda: bm25.compress(ctx, ex.question, 2 * k, counter))
            if phobert:
                texts["phobert"], sel["phobert"] = timed(lambda: phobert.compress(ctx, ex.question, k, counter))
            texts["full"] = ctx
            seqs = {name: embed_ids(reader, template.text_prompt("qa", text, ex.question))
                    for name, text in texts.items()}
            seqs["vilatent_me"] = model.memory_prompt(pe, mem_me)
            seqs["vilatent_m"] = model.memory_prompt(pm, mem_m)
            for name, seq in seqs.items():
                ttft, e2e = read_times(model, seq)
                if not warm:
                    add(f"{name}_ttft", ttft)
                    add(f"{name}_read", e2e)
                    add(f"{name}_tokens", seq.shape[0])
            if not warm:
                for name, ms in sel.items():
                    add(f"{name}_select", ms)
        print(f"doc {i}/{len(docs)}: {n} tokens, k = {k}" + (" (warm-up)" if warm else ""))

    mean = {name: statistics.mean(v) for name, v in t.items()}
    per_question = {name: mean[f"{name}_read"] + mean.get(f"{name}_select", 0.0)
                    for name in ("full", "truncation", "bm25", "bm25_x2", "phobert", "llmlingua2")
                    if f"{name}_read" in mean}
    per_question["vilatent_me"] = mean["vilatent_me_read"] + mean["me_evidence_select"]
    per_question["vilatent_m"] = mean["vilatent_m_read"]
    writer = {"vilatent_me": mean["writer_me_per_doc"], "vilatent_m": mean["writer_m_per_doc"]}
    break_even = {}
    for ours in ("vilatent_me", "vilatent_m"):
        for other in ("full", "bm25", "llmlingua2", "phobert"):
            if other in per_question:
                gain = per_question[other] - per_question[ours]
                if other == "llmlingua2":  # LLMLingua-2 also compresses once per document
                    w = writer[ours] - mean["llmlingua2_compress_per_doc"]
                    break_even[f"{ours} vs {other}"] = (w / gain if gain > 0 else None) if w > 0 else 0.0
                else:
                    break_even[f"{ours} vs {other}"] = writer[ours] / gain if gain > 0 else None
    report = {"data": args.data, "checkpoint": args.checkpoint, "ratio": r, "factor": f, "dtype": args.dtype,
              "device": torch.cuda.get_device_name() if torch.cuda.is_available() else "cpu",
              "docs": len(docs), "questions_per_doc_measured": args.questions_per_doc,
              "questions_per_doc_in_data": statistics.mean(len(v) for v in by_doc.values()),
              "mean_ms": mean, "per_question_ms": per_question, "writer_ms_per_doc": writer,
              "break_even_questions_per_doc": break_even}
    if args.cascade:
        c = json.loads(Path(args.cascade).read_text(encoding="utf-8"))["cascade"]
        per_question["vilatent_mef"] = (per_question["vilatent_me"]
                                        + (1 - c["stage1_rate"]) * per_question["bm25_x2"]
                                        + c["fallback_rate"] * per_question["full"])
        writer["vilatent_mef"] = writer["vilatent_me"]
        report["mef_expected_ms_per_question"] = per_question["vilatent_mef"]
        report["mef_rates"] = {k: c[k] for k in ("stage1_rate", "stage2_rate", "fallback_rate")}
    # N* of Table 4: questions per document after which a method with a per-document cost is cheaper
    # than reading the full document every time
    per_doc = dict(writer)
    if "llmlingua2_compress_per_doc" in mean:
        per_doc["llmlingua2"] = mean["llmlingua2_compress_per_doc"]
    report["break_even_vs_full"] = {
        name: (w / (per_question["full"] - per_question[name]) if per_question["full"] > per_question[name] else None)
        for name, w in per_doc.items() if name in per_question}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("per_question_ms", "writer_ms_per_doc", "break_even_questions_per_doc")},
                     indent=2))


if __name__ == "__main__":
    main()
