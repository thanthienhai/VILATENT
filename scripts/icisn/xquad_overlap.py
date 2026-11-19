"""G0.4: XQuAD-vi vs UIT-ViQuAD (all splits) and the stage-1 corpus: exact paragraph match and word 8-gram overlap."""
import glob, json, re, sys, unicodedata
from collections import defaultdict

XQ, N = sys.argv[1], 8
def norm(s): return re.sub(r"\W+", " ", unicodedata.normalize("NFC", s).lower()).split()
def grams(w): return {" ".join(w[i:i + N]) for i in range(len(w) - N + 1)}

paras = [p["context"] for a in json.load(open(XQ, encoding="utf-8"))["data"] for p in a["paragraphs"]]
sh = [grams(norm(p)) for p in paras]
owner = defaultdict(list)
for i, s in enumerate(sh):
    for g in s: owner[g].append(i)
def scan(texts):
    hit = [set() for _ in paras]
    for t in texts:
        for g in grams(norm(t)):
            for i in owner.get(g, ()): hit[i].add(g)
    return hit
def report(name, hit):
    n1 = sum(bool(h) for h in hit); frac = [len(h) / max(1, len(s)) for h, s in zip(hit, sh)]
    n50 = sum(f >= .5 for f in frac)
    print(f"{name}: paragraphs with >=1 shared 8-gram {n1}/240; with >=50% of 8-grams shared {n50}/240; max frac {max(frac):.2f}", flush=True)
vq = []
for f in sorted(glob.glob("data/tasks/viquad_*.jsonl")):
    vq += [json.loads(l)["context"] for l in open(f, encoding="utf-8")]
vq = list(dict.fromkeys(vq)); print("viquad unique contexts", len(vq))
report("UIT-ViQuAD (all splits)", scan(vq))
def corpus():
    with open("data/corpus/docs.jsonl", encoding="utf-8") as f:
        for l in f:
            d = json.loads(l); yield d.get("text") or d.get("content") or ""
hc = scan(corpus()); report("stage-1 corpus", hc)
# ids of the paragraphs sharing >=50% of their 8-grams with the stage-1 corpus: xquad-<article>-<paragraph> (4 digits each)
arts = json.load(open(XQ, encoding="utf-8"))["data"]
ids = [f"xquad-{a:04d}-{q:04d}" for a, art in enumerate(arts) for q in range(len(art["paragraphs"]))]
sel = [ids[i] for i, (h, s_) in enumerate(zip(hc, sh)) if len(h) / max(1, len(s_)) >= .5]
json.dump({"rule": "paragraph shares >=50% of its word 8-grams (NFC, lower, \W split) with data/corpus/docs.jsonl", "paragraph_prefixes": sel},
          open("results/icisn/g0/xquad_overlap_ids.json", "w"), indent=1)
print("overlap ids", sel)
