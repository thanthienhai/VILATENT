"""Question-blind summaries (one per distinct context) written by DeepSeek-V4.1-Flash, G2.1.
Usage: python scripts/icisn/make_summaries.py --variant v1 --out data/icisn/summaries/select_v1.json --data a.jsonl b.jsonl
Output {"meta": {...}, "summaries": {sha256(context): text}}. Resumable (sqlite cache). The summary is NOT cut here:
the reader baselines cut it at k(r) tokens (vilatent.baselines.Summary)."""
import argparse, json, math, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); sys.path.insert(0, ".")
import llm
from vilatent.baselines import context_key
from vilatent.budget import context_budget
from vilatent.data import read_jsonl
from vilatent.text import syllables

ap = argparse.ArgumentParser()
ap.add_argument("--variant", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--data", nargs="+", required=True); ap.add_argument("--workers", type=int, default=16)
a = ap.parse_args()
P = json.load(open("docs/icisn/summary_prompts.json", encoding="utf-8")); model = P["model"]
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-2B")
ctxs = list(dict.fromkeys(r["context"] for f in a.data for r in read_jsonl(f)))
jobs = []
for c in ctxs:
    n_tok, k4 = context_budget(c, tok, 4, 512, lead=" ")
    per_syl = n_tok / max(1, len(syllables(c)))                   # reader tokens per syllable of this document
    jobs.append((c, k4, max(30, math.ceil(P["length_margin"] * k4 / per_syl)), len(syllables(c))))
cache = llm.Cache(f"results/icisn/summaries_cache.sqlite")
def work(job):
    c, k4, n, src = job
    msgs = [{"role": "system", "content": P["system"]}, {"role": "user", "content": P["variants"][a.variant].format(n=n, src=src, pct=round(100 * n / src), doc=c)}]
    rec = llm.chat(cache, model, msgs, max_tokens=P["max_tokens"], temperature=P["temperature"])
    return context_key(c), rec["content"].strip(), rec["finish"]
t0 = time.time(); res = llm.map_threads(work, jobs, a.workers)
summ = {k: t for k, t, _ in res}
meta = {"variant": a.variant, "prompt_version": P["version"], "model": model, "data": a.data, "n_docs": len(jobs),
        "truncated_by_max_tokens": sum(f == "length" for *_, f in res), "empty": sum(not t for t in summ.values()),
        "mean_summary_reader_tokens": round(sum(len(tok(" " + t)["input_ids"]) for t in summ.values()) / len(summ), 1),
        "mean_k4": round(sum(j[1] for j in jobs) / len(jobs), 1), "seconds": round(time.time() - t0), "llm_stats": llm.STATS}
Path(a.out).parent.mkdir(parents=True, exist_ok=True)
json.dump({"meta": meta, "summaries": summ}, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(meta, ensure_ascii=False))
