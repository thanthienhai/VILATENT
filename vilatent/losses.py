"""Training loss: CE on the target tokens + λ·KL(teacher ‖ student) on the same tokens
(docs/VILATENT.md §Chiến lược huấn luyện, L_2).

The teacher (the frozen reader reading the full context) is stored as its top-K log
probabilities per target token. The KL is taken over K + 1 bins: the K teacher tokens and
one "rest" bin with the remaining mass, for both distributions, so both sum to 1 and the
KL stays finite (no NaN when the top-K mass is ~1).
"""
from __future__ import annotations

import torch

_MAX_LOG = -1e-7  # cap on log(top-K mass), so that log(1 − mass) stays finite


def log1mexp(x: torch.Tensor) -> torch.Tensor:
    """log(1 − exp(x)) for x < 0, numerically stable."""
    x = x.clamp(max=_MAX_LOG)
    return torch.where(x > -0.6931, torch.log(-torch.expm1(x)), torch.log1p(-torch.exp(x)))


def topk_kl(student_logp: torch.Tensor, teacher_ids: torch.Tensor, teacher_logp: torch.Tensor) -> torch.Tensor:
    """Per-token KL(teacher ‖ student) over the teacher's top-K tokens plus a rest bin.

    student_logp (N, V) log-softmax of the student; teacher_ids, teacher_logp (N, K)."""
    s_top = student_logp.gather(-1, teacher_ids)
    t_top = teacher_logp.float()
    s_rest = log1mexp(torch.logsumexp(s_top, -1))
    t_rest = log1mexp(torch.logsumexp(t_top, -1))
    t = torch.cat([t_top, t_rest[:, None]], -1)
    s = torch.cat([s_top, s_rest[:, None]], -1)
    return (t.exp() * (t - s)).sum(-1)


def ce_kl_loss(logits: torch.Tensor, targets: torch.Tensor, teacher_ids: torch.Tensor | None,
               teacher_logp: torch.Tensor | None, lambda_kl: float) -> dict[str, torch.Tensor]:
    """``logits`` (N, V) at the positions that predict the N target tokens ``targets`` (N,).
    Token-level means over the batch."""
    logp = torch.log_softmax(logits.float(), -1)
    ce = -logp.gather(-1, targets[:, None]).squeeze(-1).mean()
    out = {"ce": ce, "loss": ce}
    if teacher_ids is not None and lambda_kl > 0:
        kl = topk_kl(logp, teacher_ids, teacher_logp).mean()
        out["kl"] = kl
        out["loss"] = ce + lambda_kl * kl
    return out
