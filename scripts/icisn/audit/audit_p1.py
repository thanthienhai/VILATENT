import json, collections, statistics as st, re, unicodedata, sys
sys.stdout.reconfigure(encoding="utf-8")
P="data/icisn/longctx_p1.jsonl"
rows=[json.loads(l) for l in open(P,encoding="utf-8")]
print("rows",len(rows),"unique id",len({r['id'] for r in rows}),"unique question text",len({r['question'] for r in rows}))
by=collections.Counter(r['title'] for r in rows)
print("articles",len(by),"q/article min/med/max",min(by.values()),st.median(by.values()),max(by.values()))
cell=collections.Counter((r['length'],r['position'],r['hardness']) for r in rows)
print("cells",len(cell),"min/max",min(cell.values()),max(cell.values()))
for k in ("length","position","hardness"):
    print(k, dict(collections.Counter(r[k] for r in rows)))
# per article x length
print("per-article counts by length:")
tl=collections.defaultdict(collections.Counter)
for r in rows: tl[r['title']][r['length']]+=1
for t,c in sorted(tl.items(), key=lambda x:-sum(x[1].values())): print(f"  {t[:28]:28s} {c[16000]:3d} {c[32000]:3d} {c[64000]:3d}")
# n_tok
for L in (16000,32000,64000):
    s=[r for r in rows if r['length']==L]
    n=[r['n_tok'] for r in s]; nd=[r['n_docs'] for r in s]
    print(L,"n_tok min/med/max",min(n),int(st.median(n)),max(n),"| over target by >25%:",sum(x>L*1.25 for x in n),"| n_docs min/med",min(nd),st.median(nd),"| n_docs==1:",sum(x==1 for x in nd),"| n_docs<=2:",sum(x<=2 for x in nd))
# answers
def ans(r): return r['answers'] if isinstance(r['answers'],list) else r['answers']['text']
al=[len(ans(r)[0].split()) for r in rows]
print("answer len (words) med",st.median(al),"max",max(al),"<=2 words:",sum(x<=2 for x in al))
num=sum(bool(re.fullmatch(r"[\d\.\,\s]+",ans(r)[0])) for r in rows)
print("pure-number first answers",num)
# context contains answer
nf=0; occ=[]
for r in rows:
    c=unicodedata.normalize("NFC",r['context']).lower()
    k=[c.count(unicodedata.normalize("NFC",a).lower()) for a in ans(r)]
    if max(k)==0: nf+=1
    occ.append(max(k))
print("answer missing in context:",nf,"| occurs >1x in whole context:",sum(o>1 for o in occ),"| >3x:",sum(o>3 for o in occ))
# question quality heuristics
q=[r['question'] for r in rows]
ql=[len(x.split()) for x in q]
print("question len med",st.median(ql),"<=5 words:",sum(x<=5 for x in ql))
pron=re.compile(r"\b(ông ấy|bà ấy|anh ấy|cô ấy|họ|nó|này|đó|ấy|trên|nêu trên|như thế nào so với|tác phẩm này|nhân vật này)\b",re.I)
print("questions with deictic words (này/đó/ấy/...):",sum(bool(pron.search(x)) for x in q))
# does the question mention the article title tokens?
def toks(s): return {w for w in re.findall(r"\w+",s.lower()) if len(w)>2}
hit=sum(bool(toks(r['title'])&toks(r['question'])) for r in rows)
print("question shares a title word with its target article:",hit,"/",len(rows))
# gold position within context relative
rel=[]
for r in rows:
    c=r['context'].lower(); i=min([c.find(a.lower()) for a in ans(r) if a.lower() in c] or [-1])
    rel.append(i/len(c))
import numpy as np
print("relative char pos of first gold answer: quantiles",np.round(np.quantile(rel,[0,.1,.25,.5,.75,.9,1]),2))
print("label position vs actual:")
for p in ("start","middle","end"):
    s=[x for x,r in zip(rel,rows) if r['position']==p]; print(" ",p,len(s),np.round(np.quantile(s,[.1,.5,.9]),2))
