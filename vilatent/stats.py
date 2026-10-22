"""Paired comparisons with a cluster bootstrap (docs/VILATENT.md §Thiết kế thực nghiệm, "Thống kê").

Several questions share one passage, so the bootstrap resamples passages (clusters), not
questions. With several training seeds evaluated on the same questions, a replicate draws
seeds with replacement and ONE set of clusters, applied to every drawn seed: drawing
clusters independently per seed would treat the seeds as independent samples of passages
and give intervals that are too narrow (the LACC bootstrap error, fixed in ViWord-C).
"""
from __future__ import annotations

import numpy as np

Z_TWO_SIDED = {0.05: 1.960, 0.01: 2.576}
Z_POWER = {0.8: 0.842, 0.9: 1.282}


def bootstrap_mean(values, clusters: list, seeds: list | None = None, n_boot: int = 10_000,
                   seed: int = 0) -> np.ndarray:
    """Bootstrap distribution of the row-level mean, resampling seeds × clusters."""
    values = np.asarray(values, dtype=float)
    seeds = [0] * len(values) if seeds is None else seeds
    if not (len(values) == len(clusters) == len(seeds)):
        raise ValueError("values, clusters and seeds must have the same length")
    seed_ids, cluster_ids = list(dict.fromkeys(seeds)), list(dict.fromkeys(clusters))
    if len(cluster_ids) < 2:
        raise ValueError("the cluster bootstrap needs at least 2 clusters")
    s_index = {s: i for i, s in enumerate(seed_ids)}
    c_index = {c: i for i, c in enumerate(cluster_ids)}
    sums = np.zeros((len(seed_ids), len(cluster_ids)))
    sizes = np.zeros_like(sums)
    for v, c, s in zip(values, clusters, seeds):
        sums[s_index[s], c_index[c]] += v
        sizes[s_index[s], c_index[c]] += 1

    rng = np.random.default_rng(seed)
    n_s, n_c = len(seed_ids), len(cluster_ids)
    out = np.empty(n_boot)
    step = max(1, 2_000_000 // n_c)
    for start in range(0, n_boot, step):
        k = min(step, n_boot - start)
        seed_w = np.zeros((k, n_s))
        np.add.at(seed_w, (np.repeat(np.arange(k), n_s), rng.integers(0, n_s, k * n_s)), 1)
        clus_w = np.zeros((k, n_c))
        np.add.at(clus_w, (np.repeat(np.arange(k), n_c), rng.integers(0, n_c, k * n_c)), 1)
        num = np.einsum("bs,sc,bc->b", seed_w, sums, clus_w)
        den = np.einsum("bs,sc,bc->b", seed_w, sizes, clus_w)
        out[start:start + k] = num / den
    return out


def paired_test(a, b, clusters: list, seeds: list | None = None, n_boot: int = 10_000,
                seed: int = 0) -> dict:
    """Mean difference a − b on the same rows, its 95% percentile CI, and the one-sided
    bootstrap p-value for H1: a > b. The p-value comes from the bootstrap distribution shifted
    to the null (mean 0): the share of centered bootstrap means at least as large as the
    observed difference (Efron & Tibshirani 1993, §16.4). The share of bootstrap means ≤ 0
    used before is not a p-value under H0."""
    diff = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    boot = bootstrap_mean(diff, clusters, seeds, n_boot, seed)
    observed = float(diff.mean())
    return {"diff": observed, "ci_low": float(np.percentile(boot, 2.5)),
            "ci_high": float(np.percentile(boot, 97.5)), "p_one_sided": float(((boot - observed) >= observed).mean()),
            "se": float(boot.std()), "n": int(len(diff)), "n_clusters": len(set(clusters))}


def mde(se: float, alpha: float = 0.05, power: float = 0.8) -> float:
    """Minimum detectable effect of a two-sided test at level ``alpha`` (as the gates' 95% CI),
    normal approximation."""
    return (Z_TWO_SIDED[alpha] + Z_POWER[power]) * se


def holm(p_values: dict[str, float]) -> dict[str, float]:
    """Holm–Bonferroni adjusted p-values."""
    order = sorted(p_values, key=p_values.get)
    adjusted, running = {}, 0.0
    for rank, key in enumerate(order):
        running = max(running, min(1.0, (len(order) - rank) * p_values[key]))
        adjusted[key] = running
    return adjusted
