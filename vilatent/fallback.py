"""ViLatent-MEF: re-reading when ME is not sure (H7; checklist A6, revision of 25/10/2026).

Cascade (the MEF of the paper), one threshold τ for stages 1 and 2:

  1. ViLatent-ME answers with k(r) reader positions. The answer is accepted if it is verbatim in
     the evidence sentences (answer-in-evidence, AiE: its syllables occur contiguously there)
     AND the mean log-probability of its tokens (end-of-turn included) is at least τ.
  2. Otherwise the reader answers from BM25 sentences with a budget of 2k(r) tokens (cumulative
     cost k + 2k), accepted under the same two checks (AiE against that text).
  3. Otherwise it reads the full context (cumulative cost k + 2k + n).

The log-prob-only fallback of G1 (ME, then the full context when the confidence is below τ) is
kept as the second curve of the figure. τ is chosen on select at f*: the smallest τ (the
cheapest point: cost never decreases with τ) whose F1 reaches ``target`` × full-context F1;
every τ between two consecutive confidences gives the same result, so the midpoint is used, and
it is applied unchanged to gate and test.

"Confident but wrong" = accepted before the full context with F1 < 0.5; the AiE check and τ
cannot catch these. Calibration: ECE over 10 equal-width bins of confidence exp(mean log-prob),
correct = F1 ≥ 0.5.
"""
from __future__ import annotations

import math

import numpy as np

WRONG_F1 = 0.5


def align(*row_lists: list[dict]) -> list[tuple[dict, ...]]:
    """Rows of several methods on the same questions, in the order of the first list."""
    first = row_lists[0]
    indexed = [{r["id"]: r for r in rows} for rows in row_lists[1:]]
    for rows, index in zip(row_lists[1:], indexed):
        missing = [r["id"] for r in first if r["id"] not in index]
        if missing or len(index) != len(first):
            raise ValueError(f"rows of {rows[0]['method']} and {first[0]['method']} are not the same questions "
                             f"(e.g. {missing[:3]})")
    return [(r, *(index[r["id"]] for index in indexed)) for r in first]


def accepted(row: dict, tau: float, use_aie: bool) -> bool:
    return row["confidence"] >= tau and (not use_aie or bool(row["aie"]))


def cascade(me_rows: list[dict], bm_rows: list[dict], full_rows: list[dict], tau: float,
            method: str = "vilatent_mef") -> list[dict]:
    """Rows of the three-stage cascade at threshold τ (``bm_rows``: BM25 at 2k(r))."""
    rows = []
    for me, bm, full in align(me_rows, bm_rows, full_rows):
        if accepted(me, tau, True):
            stage, src, cost = 1, me, me["used_tokens"]
        elif accepted(bm, tau, True):
            stage, src, cost = 2, bm, me["used_tokens"] + bm["used_tokens"]
        else:
            stage, src, cost = 3, full, me["used_tokens"] + bm["used_tokens"] + full["n_tokens"]
        rows.append({**src, "method": method, "ratio": me["ratio"], "budget": me["budget"], "stage": stage,
                     "used_tokens": cost, "me_confidence": me["confidence"], "me_aie": me["aie"]})
    return rows


def logprob_fallback(me_rows: list[dict], full_rows: list[dict], tau: float,
                     method: str = "vilatent_mef_logprob") -> list[dict]:
    """Rows of the G1 fallback: ME, or the full context when ME's confidence is below τ."""
    rows = []
    for me, full in align(me_rows, full_rows):
        back = me["confidence"] < tau
        src = full if back else me
        rows.append({**src, "method": method, "ratio": me["ratio"], "budget": me["budget"], "stage": 3 if back else 1,
                     "used_tokens": me["used_tokens"] + (full["n_tokens"] if back else 0),
                     "me_confidence": me["confidence"], "me_aie": me["aie"]})
    return rows


def thresholds(*confidences: np.ndarray) -> list[float]:
    """−∞, the midpoints between consecutive distinct confidences, +∞: one τ per distinct outcome."""
    levels = sorted(set(np.concatenate(confidences).tolist()) - {-math.inf})
    return [-math.inf] + [(a + b) / 2 for a, b in zip(levels, levels[1:])] + [math.inf]


def _arrays(rows: list[dict]) -> dict[str, np.ndarray]:
    return {"conf": np.array([r["confidence"] for r in rows], dtype=float),
            "aie": np.array([bool(r["aie"]) for r in rows]), "f1": np.array([r["f1"] for r in rows], dtype=float),
            "used": np.array([r["used_tokens"] for r in rows], dtype=float),
            "n": np.array([r["n_tokens"] for r in rows], dtype=float)}


def curve(me_rows: list[dict], full_rows: list[dict], bm_rows: list[dict] | None = None) -> list[dict]:
    """One operating point per τ: the cascade when ``bm_rows`` is given, else the log-prob-only
    fallback. Same numbers as cascade()/logprob_fallback(), computed with arrays."""
    triples = align(*([me_rows, full_rows] + ([bm_rows] if bm_rows else [])))
    me, full = _arrays([t[0] for t in triples]), _arrays([t[1] for t in triples])
    bm = _arrays([t[2] for t in triples]) if bm_rows else None
    full_f1 = 100 * full["f1"].mean()
    points = []
    for tau in thresholds(me["conf"], *([bm["conf"]] if bm else [])):
        if bm is None:
            s1 = me["conf"] >= tau
            s2 = np.zeros_like(s1)
            cost = me["used"] + (~s1) * full["n"]
        else:
            s1 = (me["conf"] >= tau) & me["aie"]
            s2 = ~s1 & (bm["conf"] >= tau) & bm["aie"]
            cost = me["used"] + (~s1) * bm["used"] + (~s1 & ~s2) * full["n"]
        s3 = ~s1 & ~s2
        f1 = np.where(s1, me["f1"], np.where(s2, bm["f1"] if bm else 0.0, full["f1"]))
        points.append({"tau": tau, "f1": float(100 * f1.mean()),
                       "retention_vs_full": float(f1.mean() * 100 / full_f1) if full_f1 else None,
                       "stage1_rate": float(s1.mean()), "stage2_rate": float(s2.mean()),
                       "fallback_rate": float(s3.mean()), "mean_tokens": float(cost.mean()),
                       "confident_wrong_rate": float(((s1 | s2) & (f1 < WRONG_F1)).mean())})
    return points


def choose_tau(points: list[dict], full_f1: float, target: float = 0.95) -> dict:
    """The cheapest point (smallest τ) with F1 ≥ target × full-context F1. τ = +∞ (always the
    full context) reaches the full-context F1, so a point always exists."""
    for point in points:
        if point["f1"] >= target * full_f1 - 1e-9:
            return {**point, "target": target, "full_f1": full_f1}
    raise AssertionError("unreachable: always reading the full context gives the full-context F1")


def operating_point(rows: list[dict], full_f1: float) -> dict:
    n = len(rows)
    f1 = 100 * sum(r["f1"] for r in rows) / n
    return {"f1": f1, "retention_vs_full": f1 / full_f1 if full_f1 else None,
            **{f"stage{s}_rate": sum(r["stage"] == s for r in rows) / n for s in (1, 2)},
            "fallback_rate": sum(r["stage"] == 3 for r in rows) / n,
            "mean_tokens": sum(r["used_tokens"] for r in rows) / n,
            "confident_wrong_rate": sum(r["stage"] < 3 and r["f1"] < WRONG_F1 for r in rows) / n}


def ece(rows: list[dict], bins: int = 10) -> dict:
    """Expected calibration error of the answer confidence exp(mean log-prob) against
    correctness (F1 ≥ 0.5), with ``bins`` equal-width bins; also the per-bin table."""
    conf = np.exp(np.array([r["confidence"] for r in rows], dtype=float))
    correct = np.array([r["f1"] >= WRONG_F1 for r in rows], dtype=float)
    which = np.minimum((conf * bins).astype(int), bins - 1)
    table, total = [], 0.0
    for b in range(bins):
        sel = which == b
        if sel.any():
            gap = abs(correct[sel].mean() - conf[sel].mean())
            total += sel.mean() * gap
            table.append({"bin": b, "n": int(sel.sum()), "confidence": float(conf[sel].mean()),
                          "accuracy": float(correct[sel].mean())})
    return {"ece": float(total), "accuracy": float(correct.mean()), "mean_confidence": float(conf.mean()),
            "bins": table}
