"""G1.3: judge every prediction *.jsonl under results/paper/{test,mlqa} with the primary judge (resumable via sqlite cache).
Output: results/icisn/judge/labels/<path under results/paper>.jsonl with id, acc_llm, src."""
import json, sys, time, threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import judge, llm
judge.check_lock()
ROOT = judge.ROOT
SRC = ROOT / "results/paper"
QA = {}
for f, tag in (("viquad_test", "test"), ("mlqa_vi_test", "mlqa")):
    for l in open(ROOT / f"data/tasks/{f}.jsonl", encoding="utf-8"):
        r = json.loads(l); QA[(tag, r["id"])] = (r["question"], judge.uniq(r["answers"]))
files = sorted(p for d in ("test", "mlqa") for p in (SRC / d).rglob("*.jsonl"))
cache = llm.Cache(ROOT / "results/icisn/judge/cache_primary.sqlite")
need, missing, prio = {}, 0, {}
def priority(p):  # 4x and no-compression first, then 8x, 16x, MLQA last
    n = p.name
    return 3 if p.relative_to(SRC).parts[0] == "mlqa" else (2 if "_r16" in n else 1 if "_r8" in n else 0)
for p in files:
    tag = p.relative_to(SRC).parts[0]
    for l in open(p, encoding="utf-8"):
        r = json.loads(l); q = QA.get((tag, r["id"]))
        if q is None: missing += 1; continue
        pred = r["prediction"].strip()
        if judge.rule(pred, r.get("unreadable")): continue
        k = (q[0], tuple(q[1]), pred[:judge.P["prediction_max_chars"]])
        need[k] = None; prio[k] = min(prio.get(k, 9), priority(p))
print(f"{len(files)} files; {len(need)} unique triples to judge; {missing} rows without gold", flush=True)
keys = sorted(need, key=lambda k: prio[k]); done = [0]; t0 = time.time(); lk = threading.Lock()
def work(k):
    try:
        lab, raw = judge.judge_one(cache, judge.PRIMARY, k[0], list(k[1]), k[2])
    except RuntimeError as e:
        print("FAIL", str(e)[:100], flush=True); return
    need[k] = (lab, raw)
    with lk:
        done[0] += 1
        if done[0] % 2000 == 0: print(f"{done[0]}/{len(keys)} {time.time()-t0:.0f}s {llm.STATS}", flush=True)
llm.map_threads(work, keys, int(sys.argv[1]) if len(sys.argv) > 1 else 16)
if any(v is None for v in need.values()):
    sys.exit("some triples failed; rerun to resume from the cache")
print("judged", llm.STATS, flush=True)
inv = 0
for p in files:
    tag = p.relative_to(SRC).parts[0]; out = ROOT / "results/icisn/judge/labels" / p.relative_to(SRC)
    out.parent.mkdir(parents=True, exist_ok=True); rows = []
    for l in open(p, encoding="utf-8"):
        r = json.loads(l); q = QA.get((tag, r["id"])); pred = r["prediction"].strip()
        if q is None: continue
        s = judge.rule(pred, r.get("unreadable"))
        if s: acc, src = 0, s
        else:
            lab, raw = need[(q[0], tuple(q[1]), pred[:judge.P["prediction_max_chars"]])]
            if lab is None: acc, src, inv = 0, "invalid", inv + 1
            else: acc, src = lab, "judge"
        rows.append(json.dumps({"id": r["id"], "acc_llm": acc, "src": src}))
    out.write_text("\n".join(rows) + "\n", encoding="utf-8")
(ROOT / "results/icisn/judge/judge_all_stats.json").write_text(json.dumps({"files": len(files), "triples": len(keys), "invalid": inv, "stats": llm.STATS}, indent=1))
print("DONE invalid", inv, flush=True)
