"""Write results/icisn/judge/labels/* for every file whose triples are all in the primary cache (read-only on the cache)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import judge, llm
judge.check_lock()
ROOT, SRC = judge.ROOT, judge.ROOT / "results/paper"
QA = {}
for f, tag in (("viquad_test", "test"), ("mlqa_vi_test", "mlqa")):
    for l in open(ROOT / f"data/tasks/{f}.jsonl", encoding="utf-8"):
        r = json.loads(l); QA[(tag, r["id"])] = (r["question"], judge.uniq(r["answers"]))
cache = llm.Cache(ROOT / "results/icisn/judge/cache_primary.sqlite")
import hashlib
def get(model, q, golds, pred):
    m = judge.messages(q, golds, pred)
    k = hashlib.sha256(json.dumps([model, m, judge.P["max_tokens"], judge.P["temperature"], llm.EXTRA[model]], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return cache.get(k)
def miss_ok(p):
    t = p.relative_to(SRC).parts
    return t[0] == "test" and (t[-1].endswith("_r4.jsonl") or t[-1] in ("full.jsonl", "none.jsonl"))
done, partial, inv = [], {}, 0
for p in sorted(q for d in ("test", "mlqa") for q in (SRC / d).rglob("*.jsonl")):
    tag = p.relative_to(SRC).parts[0]; rows, miss = [], 0
    for l in open(p, encoding="utf-8"):
        r = json.loads(l); q = QA[(tag, r["id"])]; pred = r["prediction"].strip(); s = judge.rule(pred, r.get("unreadable"))
        if s: acc, src = 0, s
        else:
            rec = get(judge.PRIMARY, q[0], q[1], pred[:judge.P["prediction_max_chars"]])
            if rec is None and "--fill" in sys.argv and miss_ok(p):  # judge the few missing triples of these files now
                judge.judge_one(cache, judge.PRIMARY, q[0], q[1], pred[:judge.P["prediction_max_chars"]])
                rec = get(judge.PRIMARY, q[0], q[1], pred[:judge.P["prediction_max_chars"]])
            if rec is None: miss += 1; continue
            lab = judge.parse(rec["content"])
            acc, src = (0, "invalid") if lab is None else (lab, "judge"); inv += lab is None
        rows.append(json.dumps({"id": r["id"], "acc_llm": acc, "src": src}))
    if miss: partial[str(p.relative_to(SRC))] = miss; continue
    out = ROOT / "results/icisn/judge/labels" / p.relative_to(SRC); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(rows) + "\n", encoding="utf-8"); done.append(str(p.relative_to(SRC)))
print(len(done), "files complete;", len(partial), "incomplete;", "invalid", inv)
json.dump({"complete": done, "incomplete_missing_rows": partial}, open(ROOT / "results/icisn/judge/collect_status.json", "w"), indent=1)
