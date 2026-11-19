import json, re, unicodedata, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
N=8
def norm(s): return re.sub(r"\W+"," ",unicodedata.normalize("NFC",s).lower()).split()
def grams(w): return {" ".join(w[i:i+N]) for i in range(len(w)-N+1)}
# 19 target articles of P1 (ViQuAD test), and ViQuAD splits
tg={}
for f in ("s0","s1"):
    for l in open(f"data/icisn/viquad_long_test_{f}.jsonl",encoding="utf-8"):
        r=json.loads(l); tg.setdefault(r["title"],r["context"])
sh={t:grams(norm(c)) for t,c in tg.items()}
owner=collections.defaultdict(list)
for t,s in sh.items():
    for g in s: owner[g].append(t)
def scan(texts):
    hit={t:set() for t in sh}
    for x in texts:
        for g in grams(norm(x)):
            for t in owner.get(g,()): hit[t].add(g)
    return {t:len(hit[t])/max(1,len(sh[t])) for t in sh}
def show(name,fr):
    v=sorted(fr.values()); print(f"{name}: articles>0: {sum(x>0 for x in v)}/19, >=10%: {sum(x>=.1 for x in v)}, >=50%: {sum(x>=.5 for x in v)}, max {v[-1]:.3f}, mean {sum(v)/len(v):.3f}",flush=True)
    return fr
res={}
for sp in ("train","train_clean","dev","gate","select"):
    try:
        ctxs=list({json.loads(l)["context"] for l in open(f"data/tasks/viquad_{sp}.jsonl",encoding="utf-8")})
    except FileNotFoundError: continue
    res[sp]=show(f"viquad_{sp} contexts ({len(ctxs)})",scan(ctxs))
tt=set(tg); 
for sp in ("train","dev"):
    ti={json.loads(l)["title"] for l in open(f"data/tasks/viquad_{sp}.jsonl",encoding="utf-8")} if True else set()
    print("title overlap test∩",sp,len(tt&ti),sorted(tt&ti)[:5])
def corpus():
    with open("data/corpus/docs.jsonl",encoding="utf-8") as f:
        for l in f:
            d=json.loads(l); yield d.get("text") or d.get("content") or ""
res["corpus"]=show("stage-1 corpus (346,752 docs)",scan(corpus()))
json.dump(res,open(sys.argv[1],"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("DONE")
