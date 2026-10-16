"""ViLatent-MEF: read the full context again when the ME answer is not confident (H7,
docs/VILATENT.md §Kiến trúc, "Đọc theo câu hỏi").

A question falls back when the mean log-probability of its ME answer is below τ. Its cost is
the ME budget already spent plus the full context. τ is chosen on dev as the smallest fallback
(the smallest τ) whose F1 reaches ``target`` × full-context F1, then fixed for test.

"Confident but wrong" = a question that did not fall back and has F1 < 0.5; the mechanism cannot
catch these, so their share is reported.
"""
from __future__ import annotations

import math

import numpy as np

WRONG_F1 = 0.5


def _paired(me_rows: list[dict], full_rows: list[dict]) -> list[tuple[dict, dict]]:
    full = {r["id"]: r for r in full_rows}
    missing = [r["id"] for r in me_rows if r["id"] not in full]
    if missing or len(full) != len(me_rows):
        raise ValueError(f"ME and full-context rows are not the same questions (e.g. {missing[:3]})")
    return [(r, full[r["id"]]) for r in me_rows]


def combine(me_rows: list[dict], full_rows: list[dict], tau: float, method: str = "vilatent_mef") -> list[dict]:
    rows = []
    for me, full in _paired(me_rows, full_rows):
        back = me["confidence"] < tau
        src = full if back else me
        rows.append({**src, "method": method, "ratio": me["ratio"], "budget": me["budget"], "fallback": back,
                     "used_tokens": me["used_tokens"] + (full["n_tokens"] if back else 0),
                     "me_confidence": me["confidence"]})
    return rows


def operating_point(rows: list[dict], full_f1: float) -> dict:
    n = len(rows)
    f1 = 100 * sum(r["f1"] for r in rows) / n
    return {"f1": f1, "retention_vs_full": f1 / full_f1 if full_f1 else None,
            "fallback_rate": sum(r["fallback"] for r in rows) / n,
            "mean_tokens": sum(r["used_tokens"] for r in rows) / n,
            "confident_wrong_rate": sum((not r["fallback"]) and r["f1"] < WRONG_F1 for r in rows) / n}


def curve(me_rows: list[dict], full_rows: list[dict]) -> list[dict]:
    """One point per distinct threshold, from no fallback (τ = −∞) to always (τ = +∞); the
    same numbers as ``operating_point(combine(...))``, computed with arrays."""
    pairs = _paired(me_rows, full_rows)
    conf = np.array([me["confidence"] for me, _ in pairs], dtype=float)
    f1_me = np.array([me["f1"] for me, _ in pairs])
    f1_full = np.array([full["f1"] for _, full in pairs])
    used_me = np.array([me["used_tokens"] for me, _ in pairs], dtype=float)
    n_full = np.array([full["n_tokens"] for _, full in pairs], dtype=float)
    full_f1 = 100 * f1_full.mean()
    points = []
    for t in [-math.inf] + sorted(set(conf.tolist())) + [math.inf]:
        back = conf < t
        f1 = 100 * np.where(back, f1_full, f1_me).mean()
        points.append({"tau": t, "f1": float(f1), "retention_vs_full": float(f1 / full_f1) if full_f1 else None,
                       "fallback_rate": float(back.mean()), "mean_tokens": float((used_me + back * n_full).mean()),
                       "confident_wrong_rate": float(((~back) & (f1_me < WRONG_F1)).mean())})
    return points


def choose_tau(me_rows: list[dict], full_rows: list[dict], target: float = 0.95) -> dict:
    """Smallest τ (fewest fallbacks) whose F1 ≥ target × full-context F1. τ = +∞ (always
    re-read) always qualifies, so a point always exists."""
    full_f1 = 100 * sum(r["f1"] for r in full_rows) / len(full_rows)
    for point in curve(me_rows, full_rows):
        if point["f1"] >= target * full_f1:
            return {**point, "target": target, "full_f1": full_f1}
    raise AssertionError("unreachable: always re-reading gives the full-context F1")
