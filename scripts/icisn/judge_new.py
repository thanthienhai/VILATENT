"""Judge the Phase-4 predictions with the locked judge_v1 prompt (resumable through the sqlite cache).
Usage: python judge_new.py <primary|secondary> <threads> [--only-hyp]   (--only-hyp: only conditions used by the hypotheses)
Inputs (pulled from gpu1080): results/icisn/xquad/{single,long}/*.jsonl and results/icisn/test_extra/{single,long}/*.jsonl
Output: results/icisn/judge/labels_new[_secondary]/<set>/<setting>/<stem>.jsonl with id, acc_llm, src."""
import json, sys, time, threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import judge, llm
judge.check_lock()
ROOT = judge.ROOT
which = sys.argv[1]; threads = int(sys.argv[2]) if len(sys.argv) > 2 else 16
only_hyp = "--only-hyp" in sys.argv
model = judge.PRIMARY if which == "primary" else judge.SECONDARY
cache = llm.Cache(ROOT / f"results/icisn/judge/cache_{which}.sqlite")
OUT = ROOT / "results/icisn/judge" / ("labels_new" if which == "primary" else "labels_new_secondary")
SETS = {"xquad": {"single": "data/icisn/xquad_vi_single.jsonl", "long": "data/icisn/xquad_vi_long.jsonl"},
        "test_extra": {"single": "data/tasks/viquad_test.jsonl", "long": "data/tasks/viquad_long_test.jsonl"}}
HYP = ("vilatent_m_", "vilatent_me_f2_", "prompt_bm25_f2_", "bm25_x2_", "sum_v1_", "sumE_v1_f2_")
QA = {}
for s, d in SETS.items():
    for st, f in d.items():
        for l in open(ROOT / f, encoding="utf-8"):
            r = json.loads(l); QA[(s, st, r["id"])] = (r["question"], judge.uniq(r["answers"]))
files = []
for s in SETS:
    if only_hyp and s != "xquad": continue
    for st in ("single", "long"):
        for p in sorted((ROOT / "results/icisn" / s / st).glob("*.jsonl")):
            if only_hyp and not (p.name.startswith(HYP) and "_r4" in p.name): continue
            files.append((s, st, p))
need = {}
for s, st, p in files:
    for l in open(p, encoding="utf-8"):
        r = json.loads(l); q = QA[(s, st, r["id"])]; pred = r["prediction"].strip()
        if judge.rule(pred, r.get("unreadable")): continue
        need[(q[0], tuple(q[1]), pred[:judge.P["prediction_max_chars"]])] = None
print(f"{which}: {len(files)} files, {len(need)} triples", flush=True)
keys = list(need); done = [0]; t0 = time.time(); lk = threading.Lock()
def work(k):
    try:
        need[k] = judge.judge_one(cache, model, k[0], list(k[1]), k[2])
    except RuntimeError as e:
        print("FAIL", str(e)[:100], flush=True); return
    with lk:
        done[0] += 1
        if done[0] % 2000 == 0: print(f"{done[0]}/{len(keys)} {time.time()-t0:.0f}s", flush=True)
llm.map_threads(work, keys, threads)
if any(v is None for v in need.values()): sys.exit("some triples failed; rerun to resume")
inv = 0
for s, st, p in files:
    rows = []
    for l in open(p, encoding="utf-8"):
        r = json.loads(l); q = QA[(s, st, r["id"])]; pred = r["prediction"].strip()
        src = judge.rule(pred, r.get("unreadable"))
        if src: acc = 0
        else:
            lab, _ = need[(q[0], tuple(q[1]), pred[:judge.P["prediction_max_chars"]])]
            acc, src, inv = (0, "invalid", inv + 1) if lab is None else (lab, "judge", inv)
        rows.append(json.dumps({"id": r["id"], "acc_llm": acc, "src": src}))
    o = OUT / s / st / p.name; o.parent.mkdir(parents=True, exist_ok=True); o.write_text("\n".join(rows) + "\n", encoding="utf-8")
print("DONE invalid", inv, flush=True)
