"""Phase 5: the single script that turns Phase-4 predictions and judge labels into every confirmatory number.

Implements docs/icisn/PREREG_CONFIRM.md (H-R1, H-R2a, H-R2b, H-S1, H-S2 at 4x on XQuAD-vi, both settings, F1 and
ACC-LLM, Holm over 10 tests per metric; sensitivity; supplementary ViQuAD test). Reads only files; no GPU, no API.

Inputs (pulled from gpu1080 / produced locally):
  results/icisn/xquad/{single,long}/<stem>.jsonl            reader predictions (stem as written by scripts/evaluate.py)
  results/icisn/xquad/{single,long}/gold_flags_r4.json      scripts/gold_split.py output (gold answer in ME's BM25 evidence)
  results/icisn/test_extra/{single,long}/<stem>.jsonl       supplementary ViQuAD test reads
  results/icisn/judge/labels_new/<set>/<setting>/<stem>.jsonl   primary-judge labels of the files above
  results/icisn/judge/labels_new_secondary/...              secondary judge (XQuAD hypothesis conditions only)
  results/icisn/judge/labels/test/<setting>/<stem>.jsonl    primary-judge labels of the older H100 predictions
  results/paper/test/<setting>/<stem>.jsonl                 older H100 (bf16) predictions of ViViQuAD test
Outputs: results/icisn/confirm/numbers.json, docs/icisn/KET_QUA_XAC_NHAN.md, paper_icisn/numbers_icisn.tex
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from vilatent.stats import bootstrap_mean, holm, mde, paired_test  # noqa: E402

DELTA = 2.0                      # points of F1 and of ACC-LLM (x100), PREREG_CONFIRM s2
SETTINGS = ("single", "long")
OVERLAP = json.loads((ROOT / "results/icisn/g0/xquad_overlap_ids.json").read_text(encoding="utf-8"))["paragraph_prefixes"]
R = ROOT / "results/icisn"


def read(path):
    with open(path, encoding="utf-8") as f:
        return {r["id"]: r for r in map(json.loads, f)}


def labels(path):
    if not path.exists():
        return None
    return {r["id"]: r["acc_llm"] for r in map(json.loads, open(path, encoding="utf-8"))}


def load_cond(pred_dir, lab_dirs, stem):
    """{id: dict(f1, em, acc, acc2, aie, cl)} for one stem, or None if the prediction file is missing."""
    p = pred_dir / f"{stem}.jsonl"
    if not p.exists():
        return None
    rows = read(p)
    acc = labels(lab_dirs[0] / f"{stem}.jsonl") if lab_dirs[0] else None
    acc2 = labels(lab_dirs[1] / f"{stem}.jsonl") if lab_dirs[1] else None
    return {i: {"f1": 100 * r["f1"], "em": 100 * r["em"], "acc": None if acc is None else 100 * acc[i],
                "acc2": None if acc2 is None else 100 * acc2[i], "aie": bool(r.get("aie", False)),
                "cl": r["title"] or r["cluster"], "used": r.get("used_tokens"), "dev": r.get("device")}
            for i, r in rows.items()}


def vec(c, ids, key):
    return [c[i][key] for i in ids]


def ptwo(a, b, cl):
    """two-sided bootstrap p: min(1, 2 min(p(a>b), p(b>a)))."""
    t, u = paired_test(a, b, cl), paired_test(b, a, cl)
    t["p_two"] = min(1.0, 2 * min(t["p_one_sided"], u["p_one_sided"]))
    return t


def interaction_test(diff, out_flags, clusters, n_boot=10_000, seed=0):
    """mean(diff | gold NOT in evidence) − mean(diff | gold in evidence); cluster bootstrap over articles; one-sided p."""
    ids = {c: k for k, c in enumerate(dict.fromkeys(clusters))}
    sums, counts = np.zeros((len(ids), 2)), np.zeros((len(ids), 2))
    for v, out, c in zip(diff, out_flags, clusters):
        sums[ids[c], int(out)] += v
        counts[ids[c], int(out)] += 1
    obs = sums[:, 1].sum() / counts[:, 1].sum() - sums[:, 0].sum() / counts[:, 0].sum()
    rng = np.random.default_rng(seed)
    w = rng.multinomial(len(ids), np.full(len(ids), 1 / len(ids)), size=n_boot)
    s, n = w @ sums, w @ counts
    with np.errstate(invalid="ignore", divide="ignore"):
        boot = s[:, 1] / n[:, 1] - s[:, 0] / n[:, 0]
    boot = boot[np.isfinite(boot)]
    return {"diff": float(obs), "ci_low": float(np.percentile(boot, 2.5)), "ci_high": float(np.percentile(boot, 97.5)),
            "p_one_sided": float(((boot - obs) >= obs).mean()), "se": float(boot.std()), "n": len(diff),
            "n_clusters": len(ids), "n_out": int(counts[:, 1].sum()), "n_in": int(counts[:, 0].sum())}


def router(me, m, ids, key):
    return [me[i][key] if me[i]["aie"] else m[i][key] for i in ids]


def hypotheses(c, flags, ids, key):
    """The five tests for one metric (key 'f1' or 'acc') on the question ids; flags: {id: gold in ME evidence}."""
    cl = [c["me"][i]["cl"] for i in ids]
    me, m, pr = vec(c["me"], ids, key), vec(c["m"], ids, key), vec(c["prompt"], ids, key)
    rt = router(c["me"], c["m"], ids, key)
    out = {}
    out["H-R1"] = interaction_test([a - b for a, b in zip(me, pr)], [not flags[i] for i in ids], cl)
    if c.get("prompt_best"):
        pb = vec(c["prompt_best"], ids, key)
        out["H-R1_prompt_fbest"] = interaction_test([a - b for a, b in zip(me, pb)], [not flags[i] for i in ids], cl)
    out["H-R2a"] = paired_test(rt, m, cl)
    out["H-R2b"] = paired_test([x + DELTA for x in rt], vec(c["bm25x2"], ids, key), cl)      # H0: router − bm25_x2 <= −δ
    out["H-R2b"]["raw_diff"] = float(np.mean(rt) - np.mean(vec(c["bm25x2"], ids, key)))
    out["H-S1"] = ptwo(m, vec(c["sum"], ids, key), cl)
    out["H-S2"] = ptwo(me, vec(c["sumE"], ids, key), cl)
    for t in out.values():
        t["mde"] = mde(t["se"])
    return out


def pstar(t, name):
    return t["p_two"] if name in ("H-S1", "H-S2") else t["p_one_sided"]


STEMS = {"me": "vilatent_me_f2_r4", "m": "vilatent_m_r4", "prompt": "prompt_bm25_f2_r4", "prompt_best": "prompt_bm25_f8_r4",
         "bm25x2": "bm25_x2_r4", "bm25": "bm25_r4", "phobert": "phobert_r4", "bgem3": "bgem3_r4", "truncation": "truncation_r4",
         "lead": "lead_r4", "llmlingua2": "llmlingua2_r4", "sum": "sum_v1_r4", "sumE": "sumE_v1_f2_r4", "full": "full", "none": "none"}


def main():
    res = {"delta": DELTA, "xquad": {}, "sensitivity": {}, "table": {}, "supplementary": {}}
    for st in SETTINGS:
        pdir = R / "xquad" / st
        labs = (R / "judge/labels_new/xquad" / st, R / "judge/labels_new_secondary/xquad" / st)
        conds = {k: load_cond(pdir, labs, s) for k, s in STEMS.items()}
        need = ("me", "m", "prompt", "bm25x2", "sum", "sumE")
        miss = [k for k in need if conds[k] is None]
        if miss:
            print(f"[{st}] missing {miss}; skipping hypotheses")
            continue
        flags = {k: bool(v) for k, v in json.loads((pdir / "gold_flags_r4.json").read_text()).items()}
        ids = sorted(conds["me"])
        # table of every condition (F1, EM, ACC-LLM primary and secondary)
        res["table"][st] = {k: {m: (None if v[next(iter(v))][m] is None else float(np.mean([r[m] for r in v.values()])))
                                for m in ("f1", "em", "acc", "acc2")} | {"n": len(v)} for k, v in conds.items() if v}
        res["table"][st]["router"] = {m: (None if conds["me"][ids[0]][m] is None else float(np.mean(router(conds["me"], conds["m"], ids, m))))
                                      for m in ("f1", "em", "acc", "acc2")} | {"n": len(ids)}
        res["table"][st]["router"]["fallback_share"] = float(np.mean([not conds["me"][i]["aie"] for i in ids]))
        res["table"][st]["sum_budget_fill"] = None
        for key in ("f1", "acc"):
            if conds["me"][ids[0]][key] is None:
                continue
            res["xquad"].setdefault(st, {})[key] = hypotheses(conds, flags, ids, key)
            keep = [i for i in ids if i[:15] not in OVERLAP]            # sensitivity: drop the 6 overlapping paragraphs
            res["sensitivity"].setdefault(st, {})[key] = {"n": len(keep), **{"tests": hypotheses(conds, flags, keep, key)}}

    # Holm over the 10 tests (5 hypotheses x 2 settings) per metric, then "đạt" only if F1 AND ACC-LLM pass
    verdict = {}
    for key in ("f1", "acc"):
        raw = {f"{st}:{h}": pstar(t, h) for st in res["xquad"] for h, t in res["xquad"][st].get(key, {}).items()
               if h in ("H-R1", "H-R2a", "H-R2b", "H-S1", "H-S2")}
        if raw:
            for name, p in holm(raw).items():
                st, h = name.split(":")
                res["xquad"][st][key][h]["p_holm"], res["xquad"][st][key][h]["p_raw"] = p, raw[name]
    for st in res["xquad"]:
        for h in ("H-R1", "H-R2a", "H-R2b", "H-S1", "H-S2"):
            ok = {}
            for key in ("f1", "acc"):
                t = res["xquad"][st].get(key, {}).get(h)
                if t is None:
                    continue
                sign_ok = True if h in ("H-S1", "H-S2") else (t["diff"] > 0 if h != "H-R2b" else True)
                ok[key] = bool(t["p_holm"] < 0.05 and sign_ok)
            verdict[f"{st}:{h}"] = ({"f1": ok.get("f1"), "acc": ok.get("acc"),
                                     "status": "đạt" if ok.get("f1") and ok.get("acc") else
                                     ("một phần" if (ok.get("f1") or ok.get("acc")) else "không đạt")})
    res["verdict"] = verdict

    # supplementary: the same hypotheses on ViQuAD test at 4x (not Holm-corrected, not confirmatory)
    for st in SETTINGS:
        old, new = ROOT / "results/paper/test" / st, R / "test_extra" / st
        lab_old = (R / "judge/labels/test" / st, None)
        lab_new = (R / "judge/labels_new/test_extra" / st, None)
        c = {k: load_cond(old, lab_old, s) for k, s in (("me", "vilatent_me_f2_r4"), ("m", "vilatent_m_r4"), ("prompt", "prompt_bm25_f2_r4"),
                                                         ("bm25x2", "bm25_x2_r4"), ("bm25", "bm25_r4"))}
        c |= {k: load_cond(new, lab_new, s) for k, s in (("sum", "sum_v1_r4"), ("sumE", "sumE_v1_f2_r4"), ("bgem3", "bgem3_r4"),
                                                          ("prompt_best", "prompt_bm25_f8_r4"))}
        if any(c[k] is None for k in ("me", "m", "prompt", "bm25x2", "sum", "sumE")):
            continue
        ids = sorted(c["me"])
        flag_path = old / "gold_flags_r4.json"
        flags = {k: bool(v) for k, v in json.loads(flag_path.read_text()).items()}
        res["supplementary"][st] = {key: hypotheses(c, flags, ids, key) for key in ("f1", "acc") if c["me"][ids[0]][key] is not None}
        res["supplementary"][st]["table"] = {k: {m: (None if v[ids[0]][m] is None else float(np.mean([v[i][m] for i in ids])))
                                                  for m in ("f1", "em", "acc")} for k, v in c.items() if v is not None}
    # supplementary at every ratio for the new baselines (descriptive)
    sup = {}
    for st in SETTINGS:
        for r in (4, 8, 16):
            row = {}
            for k, stem in (("sum", f"sum_v1_r{r}"), ("sumE", f"sumE_v1_f2_r{r}"), ("bgem3", f"bgem3_r{r}"),
                            ("m", f"vilatent_m_r{r}"), ("me", f"vilatent_me_f2_r{r}"), ("bm25", f"bm25_r{r}")):
                base = R / "test_extra" / st if k in ("sum", "sumE", "bgem3") else ROOT / "results/paper/test" / st
                lab = (R / "judge/labels_new/test_extra" / st, None) if k in ("sum", "sumE", "bgem3") else (R / "judge/labels/test" / st, None)
                v = load_cond(base, lab, stem)
                if v is not None:
                    row[k] = {m: (None if next(iter(v.values()))[m] is None else float(np.mean([x[m] for x in v.values()])))
                              for m in ("f1", "em", "acc")} | {"n": len(v)}
            sup[f"{st}:{r}"] = row
    res["supplementary"]["ratios"] = sup

    out = R / "confirm"
    out.mkdir(exist_ok=True)
    (out / "numbers.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    write_markdown(res)
    write_tex(res)
    print("wrote", out / "numbers.json")


def fmt(t, key="diff"):
    return f"{t['diff']:+.2f} [{t['ci_low']:+.2f}; {t['ci_high']:+.2f}]"


def write_markdown(res):
    L = ["# KET_QUA_XAC_NHAN — kết quả pha xác nhận trên XQuAD-vi (tạo tự động bởi `scripts/icisn/confirm_numbers.py`)", "",
         "Đăng ký trước: `docs/icisn/PREREG_CONFIRM.md` (SHA trong `PREREG_CONFIRM.sha256`). 4×, hiệu = điểm (×100). p hiệu chỉnh Holm trên 10 kiểm định mỗi độ đo.", ""]
    L.append("## Bảng điều kiện (XQuAD-vi, 4×)")
    for st, tab in res["table"].items():
        L += ["", f"### {st}", "", "| Điều kiện | n | F1 | EM | ACC-LLM (chính) | ACC-LLM (phụ) |", "|---|---|---|---|---|---|"]
        for k, v in tab.items():
            if not isinstance(v, dict) or "f1" not in v:
                continue
            f = lambda x: "—" if x is None else f"{x:.1f}"
            L.append(f"| {k} | {v.get('n', '')} | {f(v['f1'])} | {f(v['em'])} | {f(v['acc'])} | {f(v['acc2'])} |")
    L += ["", "## Kiểm định xác nhận", "", "| Thiết lập | Giả thuyết | F1: hiệu [CI95] | p Holm | ACC-LLM: hiệu [CI95] | p Holm | MDE F1 | Kết luận |", "|---|---|---|---|---|---|---|---|"]
    for st, d in res["xquad"].items():
        for h in ("H-R1", "H-R2a", "H-R2b", "H-S1", "H-S2"):
            a, b = d.get("f1", {}).get(h), d.get("acc", {}).get(h)
            if a is None:
                continue
            g = lambda t: "—" if t is None else fmt(t)
            p = lambda t: "—" if t is None else f"{t['p_holm']:.3f}"
            note = " (raw_diff " + f"{a['raw_diff']:+.2f})" if h == "H-R2b" else ""
            L.append(f"| {st} | {h} | {g(a)}{note} | {p(a)} | {g(b)} | {p(b)} | {a['mde']:.2f} | {res['verdict'][f'{st}:{h}']['status']} |")
    L += ["", "H-R2b: hiệu đã cộng δ=2,0 trước khi kiểm (H0: router − bm25_x2 ≤ −2,0); CI là của hiệu + δ.", ""]
    L += ["## Độ nhạy: loại 6 đoạn trùng corpus giai đoạn 1 (không vào họ Holm)", "", "| Thiết lập | n | Giả thuyết | F1: hiệu [CI95] | p thô |", "|---|---|---|---|---|"]
    for st, d in res["sensitivity"].items():
        for h, t in d.get("f1", {}).get("tests", {}).items():
            L.append(f"| {st} | {d['f1']['n']} | {h} | {fmt(t)} | {pstar(t, h):.3f} |")
    L += ["", "## Bổ sung trên ViQuAD test 4× `[test, bổ sung]` (không phải xác nhận)", "", "| Thiết lập | Giả thuyết | F1: hiệu [CI95] | ACC-LLM: hiệu [CI95] |", "|---|---|---|---|"]
    for st, d in res["supplementary"].items():
        if st == "ratios" or "f1" not in d:
            continue
        for h in ("H-R1", "H-R2a", "H-R2b", "H-S1", "H-S2"):
            a, b = d["f1"].get(h), d.get("acc", {}).get(h)
            L.append(f"| {st} | {h} | {fmt(a)} | {'—' if b is None else fmt(b)} |")
    L += ["", "Ghi chú: M, ME, prompt, bm25_x2 trên ViQuAD test là dự đoán H100 (bf16); Sum, Sum+E, bge-m3, prompt-fbest là fp16 (1080 Ti): so khác thiết bị.", ""]
    L += ["## Bổ sung theo tỉ lệ nén (ViQuAD test)", "", "| Ô | Điều kiện | n | F1 | EM | ACC-LLM |", "|---|---|---|---|---|---|"]
    for cell, row in res["supplementary"].get("ratios", {}).items():
        for k, v in row.items():
            f = lambda x: "—" if x is None else f"{x:.1f}"
            L.append(f"| {cell} | {k} | {v['n']} | {f(v['f1'])} | {f(v['em'])} | {f(v['acc'])} |")
    L += ["", "## Lưu ý (khoảng trống của lượt chạy, ghi cố định)", "",
          "- ViQuAD-Long test bổ sung: Sum, Sum+E, bge-m3 chỉ chạy ở 4× (8× và 16× không cần cho giả thuyết); lượt chạy đầu hết bộ nhớ vì mã giữ embedding của mọi câu hỏi trên GPU, đã sửa (giữ trên CPU) rồi chạy lại hai nửa tập trên hai GPU. Các tệp Sum 8×/16× chỉ có nửa số bài nằm ở `results/icisn/test_extra/long_partial_s1/`, không dùng.",
          "- Phép so ghép cặp H-S1/H-S2 trên ViQuAD test đoạn đơn là khác thiết bị (bf16 H100 so với fp16 1080 Ti).",
          "- Sum tóm tắt dùng ít ngân sách hơn k(r) ở một phần bài Long (xem CHUAN_BI.md §2.1).", ""]
    (ROOT / "docs/icisn/KET_QUA_XAC_NHAN.md").write_text("\n".join(L) + "\n", encoding="utf-8")


DIG = dict(zip("0123456789", "zero one two three four five six seven eight nine".split()))
ALIAS = {"bm25x2": "bmx", "bm25": "bm", "bgem3": "bge", "llmlingua2": "llmlingua"}
STATUS = {"đạt": "pass", "một phần": "partial", "không đạt": "fail"}
HNAME = {"H-R1": "Rone", "H-R2a": "Rtwoa", "H-R2b": "Rtwob", "H-S1": "Sone", "H-S2": "Stwo", "H-R1_prompt_fbest": "Rbest"}


def word(x: str) -> str:
    """macro names hold letters only"""
    x = x.replace("_", "").replace("-", "")
    x = ALIAS.get(x, x)
    return "".join(DIG[c] if c.isdigit() else c for c in x)


def num(x, plus=False) -> str:
    t = f"{abs(x):.1f}"
    return ("$-$" if x < 0 else ("+" if plus else "")) + t


def mac(name: str, val) -> str:
    bs = chr(92)
    return bs + "newcommand{" + bs + name + "}{" + str(val) + "}"


def write_tex(res):
    """Letter-only macros for paper_icisn: cf<S|L><F|A><hyp><D|Lo|Hi|P|Mde|Ok> (tests), cm<S|L><F|A|E><cond> (means),
    cs<cond><F|A> (ViQuAD test single 4x, supplementary), csd<hyp> (its paired differences)."""
    L = ["% generated by scripts/icisn/confirm_numbers.py from results/icisn/confirm/numbers.json"]
    for st, d in res["xquad"].items():
        S = st[0].upper()
        for key, tests in d.items():
            M = "F" if key == "f1" else "A"
            for h, t in tests.items():
                n = f"cf{S}{M}{HNAME.get(h, word(h))}"
                d, lo, hi = t["diff"], t["ci_low"], t["ci_high"]
                if h == "H-R2b":  # tested as router + delta against BM25 2k; the paper reports the raw difference and its CI
                    d, lo, hi = t["raw_diff"], lo - DELTA, hi - DELTA
                L += [mac(n + "D", num(d, True)), mac(n + "Lo", num(lo, True)), mac(n + "Hi", num(hi, True)),
                      mac(n + "Mde", f"{t['mde']:.1f}")]
                if "p_holm" in t:
                    L.append(mac(n + "P", f"{t['p_holm']:.3f}"))
        for h in ("H-R1", "H-R2a", "H-R2b", "H-S1", "H-S2"):
            L.append(mac(f"cf{S}{HNAME[h]}Ok", STATUS[res["verdict"][f"{st}:{h}"]["status"]]))
        L.append(mac(f"cf{S}Nsens", f"{res['sensitivity'][st]['f1']['n']:,}".replace(",", "{,}")))
    for st, tab in res["table"].items():
        S = st[0].upper()
        for cond, v in tab.items():
            if not isinstance(v, dict) or "f1" not in v:
                continue
            for key, M in (("f1", "F"), ("acc", "A"), ("em", "E")):
                if v.get(key) is not None:
                    L.append(mac(f"cm{S}{M}{word(cond)}", f"{v[key]:.1f}"))
        if "router" in tab:
            L.append(mac(f"cm{S}fallback", f"{100 * tab['router']['fallback_share']:.0f}"))
    for cond, v in res["supplementary"].get("ratios", {}).get("single:4", {}).items():
        for key, M in (("f1", "F"), ("acc", "A")):
            if v.get(key) is not None:
                L.append(mac(f"cs{word(cond)}{M}", f"{v[key]:.1f}"))
    for st, pre in (("single", "csd"), ("long", "cld")):
        for h in ("H-S1", "H-S2", "H-R1", "H-R2a", "H-R2b"):
            t = res["supplementary"].get(st, {}).get("f1", {}).get(h)
            if t:
                L.append(mac(f"{pre}{HNAME[h]}", num(t["diff"], True)))
    for cond, v in res["supplementary"].get("ratios", {}).get("long:4", {}).items():
        if v.get("f1") is not None:
            L.append(mac(f"cl{word(cond)}F", f"{v['f1']:.1f}"))
    p = ROOT / "paper_icisn/numbers_icisn.tex"
    p.parent.mkdir(exist_ok=True)
    p.write_text("\n".join(L) + "\n", encoding="utf-8")
    # Vietnamese edition: the same macros with a decimal comma
    import re
    pv = ROOT / "paper_icisn_vi/numbers_icisn.tex"
    pv.parent.mkdir(exist_ok=True)
    pv.write_text(re.sub(r"(?<=\d)\.(?=\d)", ",", "\n".join(L) + "\n"), encoding="utf-8")


if __name__ == "__main__":
    main()
