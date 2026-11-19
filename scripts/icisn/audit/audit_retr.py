import json, re, math, collections, sys
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
tok=lambda s: re.findall(r"\w+",s.lower())
def bm25_rank(passages, q, gold_idx, k1=1.2, b=0.75):
    docs=[collections.Counter(tok(p)) for p in passages]; L=np.array([sum(d.values()) for d in docs]); avg=L.mean()
    df=collections.Counter(); 
    for d in docs: df.update(d.keys())
    N=len(docs); qt=set(tok(q)); sc=np.zeros(N)
    for t in qt:
        if t not in df: continue
        idf=math.log(1+(N-df[t]+.5)/(df[t]+.5))
        for i,d in enumerate(docs):
            f=d.get(t,0)
            if f: sc[i]+=idf*f*(k1+1)/(f+k1*(1-b+b*L[i]/avg))
    order=np.argsort(-sc,kind="stable"); return int(np.where(order==gold_idx)[0][0])+1, N
def run(path, name, split=r"\n\n"):
    rows=[json.loads(l) for l in open(path,encoding="utf-8")]
    ranks=[];Ns=[];info=[]
    for r in rows:
        ps=[p for p in re.split(split,r["context"]) if p.strip()]
        ans=r["answers"] if isinstance(r["answers"],list) else r["answers"]["text"]
        gi=[i for i,p in enumerate(ps) if any(a.lower() in p.lower() for a in ans)]
        if not gi: continue
        rk,N=bm25_rank(ps,r["question"],gi[0]); 
        # best rank among all passages containing the gold
        ranks.append(rk); Ns.append(N); info.append(r)
    ranks=np.array(ranks)
    print(f"{name}: n={len(ranks)} passages/context median {int(np.median(Ns))} | gold-passage BM25 rank: top1 {np.mean(ranks==1)*100:.1f}%  top3 {np.mean(ranks<=3)*100:.1f}%  top10 {np.mean(ranks<=10)*100:.1f}%  median rank {int(np.median(ranks))}")
    return ranks,info
r1,i1=run("data/icisn/longctx_p1.jsonl","P1")
for L in (16000,32000,64000):
    s=np.array([x["length"]==L for x in i1]); print(f"   P1 {L}: top1 {np.mean(r1[s]==1)*100:.1f}% top10 {np.mean(r1[s]<=10)*100:.1f}%")
for h in ("random","hard"):
    s=np.array([x["hardness"]==h for x in i1]); print(f"   P1 {h}: top1 {np.mean(r1[s]==1)*100:.1f}% top10 {np.mean(r1[s]<=10)*100:.1f}%")
# original ViQuAD-Long (target article only) for comparison, sampled by P1 question ids
src={}
for f in ("s0","s1"):
    for l in open(f"data/icisn/viquad_long_test_{f}.jsonl",encoding="utf-8"):
        r=json.loads(l); src[r["id"]]=r
rows=[json.loads(l) for l in open("data/icisn/longctx_p1.jsonl",encoding="utf-8")]
ranks=[]
for r in rows:
    o=src[r["id"][3:]]; ps=[p for p in re.split(r"\n\n",o["context"]) if p.strip()]
    ans=o["answers"]; gi=[i for i,p in enumerate(ps) if any(a.lower() in p.lower() for a in ans)]
    if gi: ranks.append(bm25_rank(ps,o["question"],gi[0])[0])
ranks=np.array(ranks); print(f"same questions, target article only (ViQuAD-Long): n={len(ranks)} top1 {np.mean(ranks==1)*100:.1f}% top10 {np.mean(ranks<=10)*100:.1f}%")
run("data/icisn/longctx_p2.jsonl","P2",split=r"\n+")

print("---- retrieval by position label (selection is position-agnostic)")
for p in ("start","middle","end"):
    s=np.array([x["position"]==p for x in i1]); print(f"  {p}: top1 {np.mean(r1[s]==1)*100:.1f}%  top10 {np.mean(r1[s]<=10)*100:.1f}%  n={s.sum()}")
# F1 by position for bm25 with cluster bootstrap start vs middle
def load(m): return {json.loads(l)['id']:json.loads(l) for l in open(f"results/icisn_longctx/p1/{m}_r4.jsonl",encoding="utf-8")}
bm=load("bm25"); pos={x["id"]:x["position"] for x in i1}; ti={x["id"]:x["title"] for x in i1}
rng=np.random.default_rng(0)
def contrast(a,b,B=5000):
    ids=[i for i in pos if pos[i] in (a,b)]; arts=sorted({ti[i] for i in ids})
    per={t:(np.mean([bm[i]['f1'] for i in ids if ti[i]==t and pos[i]==a] or [np.nan]),np.mean([bm[i]['f1'] for i in ids if ti[i]==t and pos[i]==b] or [np.nan])) for t in arts}
    d=np.array([x-y for x,y in per.values()])*100; d=d[~np.isnan(d)]
    bs=[rng.choice(d,len(d)).mean() for _ in range(B)]
    print(f"  bm25 F1 {a}-{b}: {d.mean():+.1f}  CI [{np.percentile(bs,2.5):+.1f},{np.percentile(bs,97.5):+.1f}]  articles {len(d)}")
contrast("start","middle"); contrast("end","middle")
