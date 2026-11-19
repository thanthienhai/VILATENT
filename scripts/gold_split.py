"""Split the questions of one split by whether a gold answer is verbatim in ViLatent-ME's BM25
evidence, and compare the methods within each group (analysis planned after the gate failed;
CPU, reader tokenizer only).

The evidence is rebuilt exactly as ViLatent.prepare builds it (same chunks, budget k(r) − k(rf),
selector and template); its token count is checked against ``evidence_tokens`` of every ME row.
Unlike the AiE flag of the rows, the split does not depend on any model output. Within each group:
ME − prompt, M − ME and ME − PhoBERT, paired, with the article-level cluster bootstrap.

Writes <results-dir>/gold_split_r<r>.json; with --match syllable (the gold answer's syllables as a
contiguous run, as the AiE flag tests the prediction) gold_split_syl_r<r>.json, a sensitivity check.

Usage:
  python scripts/gold_split.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
      --data data/tasks/viquad_long_select.jsonl --results-dir results/paper/select/long \
      --choices results/paper/select/choices.json --setting long
"""
import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from vilatent.baselines import BM25Sentences, TokenCounter, load_bm25_params
from vilatent.budget import chunk_context, memory_budget
from vilatent.data import load_examples
from vilatent.stats import paired_test
from vilatent.template import ReaderTemplate, load_reader_config
from vilatent.text import contains_syllables

PAIRS = {"ME - prompt": ("me", "prompt"), "M - ME": ("m", "me"), "ME - phobert": ("me", "phobert"),
         "ME - bm25": ("me", "bm25"), "M - bm25": ("m", "bm25")}  # bm25: BM25 at the whole budget k(r)


def interaction(diff: list[float], flags: list[bool], clusters: list, n_boot: int, seed: int = 0) -> dict:
    """Mean of ``diff`` on the questions without the answer in the evidence minus its mean on the
    questions with it, and its 95% percentile CI from a bootstrap that resamples articles (both
    groups of one article move together)."""
    ids = {c: k for k, c in enumerate(dict.fromkeys(clusters))}
    sums, counts = np.zeros((len(ids), 2)), np.zeros((len(ids), 2))
    for v, f, c in zip(diff, flags, clusters):
        sums[ids[c], int(not f)] += v
        counts[ids[c], int(not f)] += 1
    observed = sums[:, 1].sum() / counts[:, 1].sum() - sums[:, 0].sum() / counts[:, 0].sum()
    rng = np.random.default_rng(seed)
    w = rng.multinomial(len(ids), np.full(len(ids), 1 / len(ids)), size=n_boot)
    s, n = w @ sums, w @ counts
    with np.errstate(invalid="ignore", divide="ignore"):
        boot = s[:, 1] / n[:, 1] - s[:, 0] / n[:, 0]
    boot = boot[np.isfinite(boot)]
    return {"diff": float(observed), "ci_low": float(np.percentile(boot, 2.5)),
            "ci_high": float(np.percentile(boot, 97.5)), "n_clusters": len(ids), "n_boot_used": int(len(boot))}


def rows(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return {r["id"]: r for r in map(json.loads, f)}


_WORKER = {}


def _init(reader: str, reader_config: str, bm25_config: str, chunk_tokens: int, match: str) -> None:
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(reader)
    template = ReaderTemplate(load_reader_config(reader_config), tokenizer)
    lead = template.lead["qa"]
    _WORKER.update(tokenizer=tokenizer, template=template, lead=lead, chunk_tokens=chunk_tokens, match=match,
                   counter=TokenCounter(tokenizer, lead), selector=BM25Sentences(**load_bm25_params(bm25_config)))


def _evidence(job):
    """(ratio, factor, context, [(id, question, answers)]) -> [(id, gold present, evidence token count)]"""
    r, f, context, questions = job
    w = _WORKER
    lengths = chunk_context(context, w["tokenizer"], w["chunk_tokens"], lead=w["lead"]).lengths
    budget = memory_budget(lengths, r) - memory_budget(lengths, r * f)
    out = []
    for qid, question, answers in questions:
        text = w["selector"].compress(context, question, budget, w["counter"])
        present = (any(contains_syllables(text, a) for a in answers) if w["match"] == "syllable"
                   else any(a in text for a in answers))
        out.append((qid, present, len(w["template"].context_ids("qa", text))))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True)
    ap.add_argument("--reader-config", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--choices", required=True)
    ap.add_argument("--setting", required=True, help="long or single (key in choices.json)")
    ap.add_argument("--ratios", type=int, nargs="+", default=[4, 8, 16])
    ap.add_argument("--bm25-config", default="configs/bm25.json")
    ap.add_argument("--chunk-tokens", type=int, default=512)
    ap.add_argument("--n-boot", type=int, default=10_000)
    ap.add_argument("--workers", type=int, default=8, help="processes; one job per (ratio, context), CPU only")
    ap.add_argument("--chunk-questions", type=int, default=50, help="questions per job on one context")
    ap.add_argument("--match", choices=["substring", "syllable"], default="substring")
    args = ap.parse_args()

    choices = json.loads(Path(args.choices).read_text(encoding="utf-8"))["settings"][args.setting]
    examples = load_examples(args.data, "qa")
    by_context = {}
    for ex in examples:
        by_context.setdefault(ex.context, []).append((ex.id, ex.question, ex.answers))
    jobs = [(r, choices[str(r)]["f_star"], c, qs[i:i + args.chunk_questions])
            for r in args.ratios for c, qs in by_context.items() for i in range(0, len(qs), args.chunk_questions)]
    jobs.sort(key=lambda j: -len(j[2]) * len(j[3]))  # longest first, so the pool ends together
    found = {r: {} for r in args.ratios}
    with ProcessPoolExecutor(args.workers, initializer=_init,
                             initargs=(args.reader, args.reader_config, args.bm25_config, args.chunk_tokens, args.match)) as pool:
        for job, result in zip(jobs, pool.map(_evidence, jobs)):
            found[job[0]].update({qid: (p, n) for qid, p, n in result})

    d = Path(args.results_dir)
    for r in args.ratios:
        f = choices[str(r)]["f_star"]
        methods = {"me": rows(d / f"vilatent_me_f{f}_r{r}.jsonl"), "prompt": rows(d / f"prompt_bm25_f{f}_r{r}.jsonl"),
                   "m": rows(d / f"vilatent_m_r{r}.jsonl")}
        for name in ("phobert", "bm25"):
            if (d / f"{name}_r{r}.jsonl").exists():
                methods[name] = rows(d / f"{name}_r{r}.jsonl")
        present = {i: p for i, (p, _) in found[r].items()}
        mismatched = sum(n != methods["me"][i]["evidence_tokens"] for i, (_, n) in found[r].items())
        out = {"setting": args.setting, "ratio": r, "f_star": f, "data": args.data, "n": len(examples),
               "evidence_token_mismatches": mismatched, "groups": {}}
        for name, flag in (("in", True), ("out", False)):
            ids = [i for i in methods["me"] if present[i] == flag]
            group = {"n": len(ids), "share": len(ids) / len(examples),
                     "f1": {m: 100 * sum(v[i]["f1"] for i in ids) / len(ids) for m, v in methods.items()}, "diffs": {}}
            clusters = [methods["me"][i]["title"] or methods["me"][i]["cluster"] for i in ids]
            for pair, (a, b) in PAIRS.items():
                if a in methods and b in methods and len(set(clusters)) >= 2:
                    group["diffs"][pair] = paired_test([100 * methods[a][i]["f1"] for i in ids],
                                                       [100 * methods[b][i]["f1"] for i in ids], clusters,
                                                       n_boot=args.n_boot)
            out["groups"][name] = group

        # difference of differences (not-in minus in), and the same split restricted to the questions
        # the full-context reader answers (F1 >= 0.5): are the missed questions merely harder?
        full = rows(d / "full.jsonl") if (d / "full.jsonl").exists() else None
        subsets = {"all": list(methods["me"])}
        if full is not None:
            subsets["full_correct"] = [i for i in methods["me"] if full[i]["f1"] >= 0.5]
        out["interaction"], out["full_correct"] = {}, {}
        for subset, ids in subsets.items():
            clusters = [methods["me"][i]["title"] or methods["me"][i]["cluster"] for i in ids]
            for pair, (a, b) in PAIRS.items():
                if a not in methods or b not in methods:
                    continue
                diff = [100 * (methods[a][i]["f1"] - methods[b][i]["f1"]) for i in ids]
                inter = interaction(diff, [present[i] for i in ids], clusters, args.n_boot)
                if subset == "all":
                    out["interaction"][pair] = inter
                else:
                    groups = {}
                    for name, flag in (("in", True), ("out", False)):
                        sub = [k for k, i in enumerate(ids) if present[i] == flag]
                        groups[name] = paired_test([100 * methods[a][ids[k]]["f1"] for k in sub],
                                                   [100 * methods[b][ids[k]]["f1"] for k in sub],
                                                   [clusters[k] for k in sub], n_boot=args.n_boot)
                    out["full_correct"][pair] = {"share": len(ids) / len(examples), "interaction": inter, **groups}
        tag = "_syl" if args.match == "syllable" else ""
        (d / f"gold_split{tag}_r{r}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
        (d / f"gold_flags{tag}_r{r}.json").write_text(json.dumps(present), encoding="utf-8")
        g = out["groups"]
        print(f"{args.setting} r={r}: mismatches {mismatched}; in {g['in']['n']} out {g['out']['n']}; "
              + "; ".join(f"{k} {p}: {v['diff']:+.1f} [{v['ci_low']:+.1f}, {v['ci_high']:+.1f}]"
                          for k in ("in", "out") for p, v in g[k]["diffs"].items()))
        print("  interaction: " + "; ".join(f"{p}: {v['diff']:+.1f} [{v['ci_low']:+.1f}, {v['ci_high']:+.1f}]"
                                            for p, v in out["interaction"].items()))
        for p, v in out["full_correct"].items():
            print(f"  full correct ({100 * v['share']:.0f}%) {p}: in {v['in']['diff']:+.1f}, out {v['out']['diff']:+.1f}, "
                  f"interaction {v['interaction']['diff']:+.1f} [{v['interaction']['ci_low']:+.1f}, {v['interaction']['ci_high']:+.1f}]")


if __name__ == "__main__":
    main()
