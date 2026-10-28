import unicodedata

import numpy as np
import torch

from vilatent.losses import ce_kl_loss, topk_kl
from vilatent.metrics import is_repetitive, is_unreadable, qa_em, qa_f1, score_qa
from vilatent.stats import bootstrap_mean, holm, mde, paired_test


def test_topk_kl_zero_for_identical_and_finite_for_peaked():
    logits = torch.randn(5, 50)
    logp = torch.log_softmax(logits, -1)
    top = logp.topk(20, -1)
    assert torch.allclose(topk_kl(logp, top.indices, top.values), torch.zeros(5), atol=1e-5)
    peaked = torch.full((2, 50), -60.0)
    peaked[:, 0] = 0.0
    peaked = torch.log_softmax(peaked, -1)
    t = peaked.topk(20, -1)
    kl = topk_kl(torch.log_softmax(torch.randn(2, 50), -1), t.indices, t.values)
    assert torch.isfinite(kl).all() and (kl > 0).all()


def test_ce_kl_loss_combines():
    logits = torch.randn(4, 30)
    targets = torch.tensor([1, 2, 3, 4])
    top = torch.log_softmax(torch.randn(4, 30), -1).topk(20, -1)
    out = ce_kl_loss(logits, targets, top.indices, top.values, lambda_kl=0.5)
    assert torch.isclose(out["loss"], out["ce"] + 0.5 * out["kl"])
    assert "kl" not in ce_kl_loss(logits, targets, None, None, 1.0)


def test_qa_metrics():
    assert qa_f1("vua Lý Thái Tổ", "Lý Thái Tổ") == 2 * (3 / 4) * 1 / (3 / 4 + 1)
    assert qa_em("Lý Thái Tổ.", "lý thái tổ") == 1.0
    assert score_qa("1010", ["năm 1010", "1010"])["em"] == 1.0
    assert is_unreadable("<think>x", stopped=True) and is_unreadable("ok", stopped=False)
    assert not is_unreadable("ok", stopped=True)
    assert is_repetitive("a b c a b c a b c") and not is_repetitive("Hà Nội")
    assert qa_em("", "…") == 0.0  # an empty answer never matches, even a gold made of punctuation
    nfd = unicodedata.normalize("NFD", "Hà Nội")
    assert qa_em(nfd, "Hà Nội") == 1.0 and qa_f1(nfd, "Hà Nội") == 1.0
    assert abs(mde(1.0) - (1.960 + 0.842)) < 1e-9  # two-sided α = 0.05, as the gates' 95% CI


def test_paired_test_and_clusters():
    rng = np.random.default_rng(0)
    clusters = [f"p{i // 4}" for i in range(400)]
    a = rng.normal(1.0, 1.0, 400)
    b = a - 0.5
    out = paired_test(a, b, clusters, n_boot=2000)
    assert abs(out["diff"] - 0.5) < 1e-9 and out["ci_low"] <= 0.5 <= out["ci_high"]
    assert out["n_clusters"] == 100 and mde(out["se"]) >= 0


def test_bootstrap_seeds_share_cluster_draws():
    values = [1.0, 0.0, 1.0, 0.0]
    boot = bootstrap_mean(values, ["a", "b", "a", "b"], seeds=[0, 0, 1, 1], n_boot=500)
    assert set(np.round(boot, 6)) <= {0.0, 0.5, 1.0}


def test_holm():
    adjusted = holm({"x": 0.01, "y": 0.04, "z": 0.03})
    assert adjusted == {"x": 0.03, "z": 0.06, "y": 0.06}


def _row(i, **kw):
    row = dict(id=i, method="m", ratio=4, cluster="c", title="t", f1=1.0, em=1.0, unreadable=False,
               repetitive=False, prediction="a b", used_tokens=10, n_tokens=40, budget=10, aie=None, confidence=-0.1)
    return {**row, **kw}


def test_aie_rate_and_summary_of_cascade_rows():
    from vilatent.evaluate import summarize
    from vilatent.fallback import cascade
    from vilatent.metrics import aie_rate

    assert aie_rate([_row("1")]) is None
    assert aie_rate([_row("1", aie=True), _row("2", aie=False), _row("3")]) == 0.5  # rows without the check are left out

    me = [_row("1", aie=True, evidence_tokens=4), _row("2", aie=False, evidence_tokens=6),
          _row("3", aie=False, evidence_tokens=4)]
    bm = [_row("1", aie=True), _row("2", aie=False), _row("3", aie=False)]
    rows = cascade(me, bm, [_row("1"), _row("2"), _row("3")], tau=-1.0)
    assert [r["stage"] for r in rows] == [1, 3, 3]
    for ordered in (rows, rows[::-1]):  # the summary does not depend on which row comes first
        summary = summarize(ordered)
        assert summary["aie_rate"] == 1.0  # the only row with the check holds the answer
        assert "budget_use" not in summary and "actual_ratio" not in summary  # used_tokens is a cumulative cost
        assert summary["mean_used_tokens"] == sum(r["used_tokens"] for r in rows) / 3
    plain = summarize([_row("1", aie=True), _row("2", aie=False)])  # non-cascade rows keep both
    assert plain["aie_rate"] == 0.5 and plain["budget_use"] == 1.0 and plain["actual_ratio"] == 4.0
