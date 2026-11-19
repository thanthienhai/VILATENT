import json, numpy as np, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
def load(ps,m): return {json.loads(l)['id']:json.loads(l) for l in open(f"results/icisn_longctx/{ps}/{m}_r4.jsonl",encoding="utf-8")}
rng=np.random.default_rng(0)
def cluster_stats(a,b,cl,B=10000):
    ids=sorted(a); d=np.array([a[i]-b[i] for i in ids])*100; c=np.array([cl[i] for i in ids])
    ucl=sorted(set(c)); idx=[np.where(c==u)[0] for u in ucl]
    means=[d[ix].mean() for ix in idx]; w=[len(ix) for ix in idx]
    bs=[]
    for _ in range(B):
        k=rng.integers(0,len(ucl),len(ucl)); bs.append(np.average([means[j] for j in k],weights=[w[j] for j in k]))
    bs=np.array(bs); return d.mean(), np.percentile(bs,2.5), np.percentile(bs,97.5), bs.std(), len(ucl), np.std(means)
for ps in ("p1","p2"):
    data={json.loads(l)['id']:json.loads(l) for l in open(f"data/icisn/longctx_{ps}.jsonl",encoding="utf-8")}
    cl={i:(r['title']) for i,r in data.items()}
    me=load(ps,"vilatent_me_f2"); pr=load(ps,"prompt_bm25_f2"); ph=load(ps,"phobert"); m=load(ps,"vilatent_m")
    for name,(x,y) in {"ME-prompt2":(me,pr),"ME-PhoBERT":(me,ph)}.items():
        mean,lo,hi,se,k,sd=cluster_stats({i:x[i]['f1'] for i in x},{i:y[i]['f1'] for i in y},cl)
        print(f"{ps} {name}: diff {mean:+.2f}  95% CI [{lo:+.2f},{hi:+.2f}]  half-width {(hi-lo)/2:.2f}  SE {se:.2f}  clusters {k}  SD of cluster means {sd:.2f}")
# what article count would be needed for half-width 2 pts with SD~6
for sd in (5,6,7):
    for hw in (2,3):
        print(f"SD {sd}: clusters needed for 95% half-width {hw} pts ≈ {(1.96*sd/hw)**2:.0f}")
# other cluster sources
import glob
for f in ("data/tasks/mlqa_vi_test.jsonl","data/tasks/viquad_long_select.jsonl","data/icisn/xquad_vi_long.jsonl","data/tasks/viquad_long_gate.jsonl"):
    rows=[json.loads(l) for l in open(f,encoding="utf-8")]
    ti=collections.Counter(r.get('title') or r.get('cluster') for r in rows)
    ctx=sorted(len(r['context'].split()) for r in rows)
    print(f, "rows",len(rows),"articles/clusters",len(ti),"ctx syll median",ctx[len(ctx)//2], "keys",list(rows[0].keys())[:8])
