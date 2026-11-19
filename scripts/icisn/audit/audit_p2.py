import json, collections, statistics as st, sys, re
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
rows=[json.loads(l) for l in open("data/icisn/longctx_p2.jsonl",encoding="utf-8")]
print("rows",len(rows),"articles",len({r['title'] for r in rows}),"unique q",len({r['question'] for r in rows}))
c=collections.Counter(r['title'] for r in rows); print("q/article min/med/max",min(c.values()),st.median(c.values()),max(c.values()), "top3",c.most_common(3))
print("position bins",dict(collections.Counter(r['position'] for r in rows)))
nsy=[len(r['context'].split()) for r in rows]; print("doc syllables min/med/max",min(nsy),int(st.median(nsy)),max(nsy))
ov=[r['overlap'] for r in rows]; print("overlap quantiles",np.round(np.quantile(ov,[0,.25,.5,.75,1]),2),">=0.4:",sum(o>=.4 for o in ov))
no=[r['n_occ'] for r in rows]; print("n_occ==1:",sum(x==1 for x in no),">1:",sum(x>1 for x in no),">=5:",sum(x>=5 for x in no),"==0:",sum(x==0 for x in no))
al=[len(r['answers'][0].split()) for r in rows]; print("answer len med",st.median(al),"<=2:",sum(x<=2 for x in al),"pure number:",sum(bool(re.fullmatch(r"[\d\.\,\s]+",r['answers'][0])) for r in rows))
ql=[len(r['question'].split()) for r in rows]; print("question len med",st.median(ql),"<=6:",sum(x<=6 for x in ql))
def toks(s): return {w for w in re.findall(r"\w+",s.lower()) if len(w)>2}
print("question shares a title word:",sum(bool(toks(r['title'])&toks(r['question'])) for r in rows))
# lexical overlap of question with its answer sentence: fraction of question content words appearing in the doc window... proxy: words of question in answer sentence
def sent_with(ctx,a):
    i=ctx.find(a); s=ctx.rfind(".",0,i)+1; e=ctx.find(".",i); return ctx[s:e if e>0 else i+200]
ratios=[]
for r in rows:
    s=sent_with(r['context'],r['answers'][0]).lower(); q=toks(r['question']); ratios.append(len(q & set(re.findall(r"\w+",s)))/max(1,len(q)))
print("share of question content words that also occur in the answer sentence: mean %.2f median %.2f"%(np.mean(ratios),np.median(ratios)))
# same for P1 for comparison
p1=[json.loads(l) for l in open("data/icisn/longctx_p1.jsonl",encoding="utf-8")]
rr=[]
for r in p1:
    a=r['answers'][0] if isinstance(r['answers'],list) else r['answers']['text'][0]
    s=sent_with(r['context'],a).lower(); q=toks(r['question']); rr.append(len(q&set(re.findall(r"\w+",s)))/max(1,len(q)))
print("P1 same stat: mean %.2f median %.2f"%(np.mean(rr),np.median(rr)))
for r in rows[:0]: pass
import random
random.Random(2).shuffle(rows)
for r in rows[:15]: print(f"[{r['title'][:20]}] {r['question']} -> {r['answers'][0][:40]} (occ {r['n_occ']})")
