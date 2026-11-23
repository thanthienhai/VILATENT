"""Primary-judge labels (ACC-LLM) for the PREREG_MORONG conditions on P1: results/icisn_morong/p1/*.jsonl (1080 Ti controls) and
results/icisn_h100/p1 (H100 bf16: full, bm25_x2), results/icisn_h100_memctl/p1 (H100 bf16: M intact/swap/zero/shuf); the T4 shards were lost. Resumable (sqlite cache, shared with the longctx judge).
Output: results/icisn/morong/judge/<dir>/<stem>.jsonl with id, acc_llm, src."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import judge, llm
judge.check_lock()
ROOT = judge.ROOT
QA = {}
for s in ("p1",):
    for l in open(ROOT / f"data/icisn/longctx_{s}.jsonl", encoding="utf-8"):
        r = json.loads(l)
        a = r["answers"]
        QA[(s, r["id"])] = (r["question"], judge.uniq(a if isinstance(a, list) else a["text"]))
cache = llm.Cache(ROOT / "results/icisn/longctx/judge_cache_primary.sqlite")
files = sorted(p for d in ("icisn_morong/p1", "icisn_h100/p1", "icisn_h100_memctl/p1", "icisn_morong_t4/p1") for p in (ROOT / "results" / d).glob("*.jsonl"))
need = {}
for p in files:
    s = "p1"
    for l in open(p, encoding="utf-8"):
        r = json.loads(l); q = QA[(s, r["id"])]; pred = r["prediction"].strip()
        if judge.rule(pred, r.get("unreadable")): continue
        need[(q[0], tuple(q[1]), pred[:judge.P["prediction_max_chars"]])] = None
print(len(files), "files;", len(need), "unique triples", flush=True)
def work(k):
    try:
        need[k] = judge.judge_one(cache, judge.PRIMARY, k[0], list(k[1]), k[2])
    except RuntimeError as e:
        print("FAIL", str(e)[:100], flush=True)
t0 = time.time()
llm.map_threads(work, list(need), 16)
if any(v is None for v in need.values()):
    sys.exit("some triples failed; rerun to resume from the cache")
print("judged", llm.STATS, round(time.time() - t0), "s", flush=True)
inv = 0
for p in files:
    s = "p1"; out = ROOT / "results/icisn/morong/judge" / p.parent.parent.name / p.name
    out.parent.mkdir(parents=True, exist_ok=True); rows = []
    for l in open(p, encoding="utf-8"):
        r = json.loads(l); q = QA[(s, r["id"])]; pred = r["prediction"].strip()
        sr = judge.rule(pred, r.get("unreadable"))
        if sr: acc, src = 0, sr
        else:
            lab, _ = need[(q[0], tuple(q[1]), pred[:judge.P["prediction_max_chars"]])]
            if lab is None: acc, src, inv = 0, "invalid", inv + 1
            else: acc, src = lab, "judge"
        rows.append(json.dumps({"id": r["id"], "acc_llm": acc, "src": src}))
    out.write_text(chr(10).join(rows) + chr(10), encoding="utf-8")
print("DONE invalid", inv, flush=True)
