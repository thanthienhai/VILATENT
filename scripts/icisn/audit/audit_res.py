import json, glob, collections, sys, statistics as st
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
for ps in ("p1","p2"):
    data={json.loads(l)['id']:json.loads(l) for l in open(f"data/icisn/longctx_{ps}.jsonl",encoding="utf-8")}
    print("=====",ps,"dataset n",len(data))
    R={}
    for f in sorted(glob.glob(f"results/icisn_longctx/{ps}/*_r4.jsonl")):
        m=f.split("/")[-1].replace("_r4.jsonl","")
        R[m]=[json.loads(l) for l in open(f,encoding="utf-8")]
    k0=R[next(iter(R))][0]; print("row keys:",sorted(k0.keys()))
    ids0=set(data)
    F={}
    for m,rows in R.items():
        ids=[r['id'] for r in rows]
        dup=len(ids)-len(set(ids)); miss=len(ids0-set(ids)); extra=len(set(ids)-ids0)
        f1=np.array([r['f1'] for r in rows])*100
        pred=[(r.get('prediction') or r.get('pred') or r.get('answer') or '') for r in rows]
        empty=sum(1 for p in pred if not str(p).strip())
        stopped=[r.get('stopped') for r in rows if 'stopped' in r]
        print(f"{m:22s} n={len(rows)} dup={dup} missing={miss} extra={extra} F1={f1.mean():.2f} empty={empty} notstopped={sum(1 for s in stopped if s is False)}")
        F[m]={r['id']:r['f1']*100 for r in rows}
    ids=sorted(ids0)
    M=np.array([[F[m].get(i,np.nan) for m in F] for i in ids])
    names=list(F)
    best=np.nanmax(M,axis=1)
    print("oracle (best of 6) mean F1 %.1f ; questions with max F1==0 across all 6: %d (%.1f%%); max F1<20: %d"%(np.nanmean(best),(best==0).sum(),100*(best==0).mean(),(best<20).sum()))
    z=(M==0).sum(1)
    print("number of conditions scoring exactly 0:",dict(sorted(collections.Counter(z).items())))
    if ps=="p1":
        for key in ("length","position","hardness"):
            print(key)
            for v in sorted({data[i][key] for i in ids}):
                sel=[j for j,i in enumerate(ids) if data[i][key]==v]
                print("  ",v,len(sel)," ".join(f"{n}={np.nanmean(M[sel,k]):.1f}" for k,n in enumerate(names)))
