"""Reading with the question: ME (memory at r·f + BM25 sentences in the same budget), ViLatent-Q
(writer sees the question), the answer confidence, and the cascade / log-prob fallback of MEF."""
import math

import pytest
import torch

from test_model import BM25, CONTEXT, make_model, qa
from vilatent.data import Example
from vilatent.evaluate import evaluate_vilatent
from vilatent.fallback import cascade, choose_tau, curve, ece, logprob_fallback, operating_point
from vilatent.model import allowed_pairs
from vilatent.reader import embed_ids, greedy_generate

QUESTIONS = [("Ai dời đô ?", "Vua Lý Thái Tổ"), ("Thành phố có diện tích bao nhiêu ?", "3.359 km²")]


def test_allowed_pairs_keep_rho_within_stage_one():
    pairs = allowed_pairs([4, 8, 16], [1, 2, 4, 8])
    assert pairs == [(4, 1), (4, 2), (4, 4), (4, 8), (8, 1), (8, 2), (8, 4), (16, 1), (16, 2)]
    assert all(r * f <= 32 for r, f in pairs)


@pytest.mark.parametrize("factor", [2, 4])
def test_me_splits_the_budget_between_memory_and_sentences(reader, tokenizer, template, factor):
    model = make_model(reader, tokenizer, template)
    p = model.prepare(qa(0, *QUESTIONS[0]), 2, factor)
    assert p.pool == 2 * factor
    k = sum(math.ceil(len(c) / 2) for c in p.chunks)
    k_m = sum(math.ceil(len(c) / (2 * factor)) for c in p.chunks)
    assert p.budget == k
    assert 0 < len(p.evidence_ids) <= k - k_m and p.evidence
    with torch.no_grad():
        memory = model.encode_memory([p])[0]
    assert memory.shape[0] - 2 == k_m
    # the sentences sit between ⟨/mem⟩ and the question, as text ids
    seq = model.memory_prompt(p, memory)
    assert seq.shape[0] == len(p.prefix_ids) + k_m + 2 + len(p.evidence_ids) + len(p.suffix_ids)
    # f = 1 is ViLatent-M: no evidence, the whole budget in memory
    m = model.prepare(qa(0, *QUESTIONS[0]), 2, 1)
    assert m.evidence_ids == [] and m.pool == 2


def test_me_rows_respect_the_budget_and_share_memory(reader, tokenizer, template):
    model = make_model(reader, tokenizer, template)
    rows = evaluate_vilatent(model, [qa(i, q, a) for i, (q, a) in enumerate(QUESTIONS)], 4, 2, batch_size=2)
    assert all(r["used_tokens"] == r["memory_vectors"] + r["evidence_tokens"] <= r["budget"] for r in rows)
    assert all(r["factor"] == 2 and r["pool"] == 8 and r["ratio"] == 4 and math.isfinite(r["confidence"])
               for r in rows)
    assert all(isinstance(r["aie"], bool) for r in rows)  # answer-in-evidence for the cascade
    m_rows = evaluate_vilatent(model, [qa(0, *QUESTIONS[0])], 4, 1, batch_size=2)
    assert m_rows[0]["aie"] is None and m_rows[0]["evidence_tokens"] == 0


def test_q_memory_depends_on_the_question_and_m_does_not(reader, tokenizer, template):
    m = make_model(reader, tokenizer, template)
    q = make_model(reader, tokenizer, template, sees_question=True)
    a, b = (q.prepare(qa(i, question, ans), 4) for i, (question, ans) in enumerate(QUESTIONS))
    with torch.no_grad():
        mem_a, mem_b = q.encode_memory([a, b])
        alone_a = q.encode_memory([a])[0]
        m_a, m_b = m.encode_memory([m.prepare(qa(i, question, ans), 4) for i, (question, ans) in enumerate(QUESTIONS)])
    assert mem_a.shape == mem_b.shape == m_a.shape  # same budget as W0
    assert not torch.allclose(mem_a[1:-1], mem_b[1:-1])
    assert torch.allclose(m_a, m_b)
    assert torch.allclose(mem_a, alone_a, atol=1e-5)  # questions of different lengths in one batch
    assert q.memory_key(a) != q.memory_key(b)
    with pytest.raises(ValueError):  # Q reads memory only
        q.prepare(qa(0), 4, 2)


def test_evidence_needs_a_question_and_bm25(reader, tokenizer, template):
    from vilatent.model import ViLatent

    model = make_model(reader, tokenizer, template)
    with pytest.raises(ValueError):  # stage 1 has no question
        model.prepare(Example("s", "d", "continue", CONTEXT, target="x"), 4, 2)
    no_bm25 = ViLatent(reader, tokenizer, template, model.writer, chunk_tokens=12)
    with pytest.raises(ValueError, match="BM25"):
        no_bm25.prepare(qa(0), 4, 2)


def test_swapped_memory_comes_from_another_article_with_the_same_size():
    from vilatent.evaluate import swap_memories

    def mem(k, v):  # ⟨mem⟩ + k vectors of value v + ⟨/mem⟩
        return torch.cat([torch.zeros(1, 2), torch.full((k, 2), float(v)), torch.ones(1, 2)])

    memory = {"a1": mem(3, 1), "a2": mem(3, 2), "b1": mem(3, 3), "b2": mem(5, 4), "c1": mem(2, 5)}
    info = {"a1": ("A", 3), "a2": ("A", 3), "b1": ("B", 3), "b2": ("B", 5), "c1": ("C", 2)}
    swapped, donors = swap_memories(memory, info, seed=0)
    for key, (title, k_m) in info.items():
        assert info[donors[key]][0] != title and swapped[key].shape == memory[key].shape
        assert torch.equal(swapped[key][[0, -1]], memory[key][[0, -1]])  # own boundaries
    assert donors["a1"] == "b1" and donors["c1"] in ("a1", "a2", "b1")  # same size first, then the smallest larger
    # no other article has 5 vectors: the longest donor (a1, 3 vectors) is repeated to 5
    assert donors["b2"] == "a1" and torch.equal(swapped["b2"][1:-1], torch.full((5, 2), 1.0))
    assert swap_memories(memory, info, seed=0)[1] == donors  # seeded


def test_me_rows_with_swapped_memory(reader, tokenizer, template):
    model = make_model(reader, tokenizer, template)
    other = "TP. Hồ Chí Minh là thành phố lớn nhất. Hà Nội có dân số 8,5 triệu người."
    examples = [qa(0, *QUESTIONS[0]), qa(1, *QUESTIONS[1]),
                Example("q2", "p1", "qa", other, question="Ai ?", answers=["Hà Nội"], target="Hà Nội")]
    own = {r["id"]: r for r in evaluate_vilatent(model, examples, 4, 2, batch_size=2)}
    swapped = evaluate_vilatent(model, examples, 4, 2, batch_size=2, swap_seed=0)
    assert {r["memory_from"] for r in swapped if r["cluster"] == "p0"} == {"p1"}
    assert all(r["used_tokens"] == own[r["id"]]["used_tokens"] for r in swapped)


def test_prompt_writer_ignores_the_context(reader, tokenizer, template):
    from vilatent.model import ViLatent
    from vilatent.writer import PromptWriter, build_writer, prompt_init_ids

    ids = prompt_init_ids([CONTEXT], tokenizer, n=3, seed=0)
    writer = PromptWriter(reader, tokenizer, min_ratio=4, chunk_tokens=12, init_ids=ids)
    model = ViLatent(reader, tokenizer, template, writer, chunk_tokens=12, bm25=BM25)
    a = model.prepare(qa(0, *QUESTIONS[0]), 4, 2)
    b = model.prepare(qa(1, *QUESTIONS[0], context="Hà Nội là thủ đô ."), 4, 2)
    mem_a, mem_b = model.encode_memory([a, b])
    assert mem_a.shape[0] - 2 == sum(math.ceil(len(c) / 8) for c in a.chunks)  # the ME vector count
    assert torch.equal(mem_a[:mem_b.shape[0] - 1], mem_b[:-1])  # same vectors, whatever the context
    model.loss([a, b], None, 0.0)["loss"].backward()
    assert writer.prompt.grad is not None and writer.prompt.grad.abs().sum() > 0
    rebuilt = build_writer(reader, tokenizer, writer.config())
    assert isinstance(rebuilt, PromptWriter) and rebuilt.prompt.shape == writer.prompt.shape


def test_frozen_writer_trains_only_the_head(reader, tokenizer, template):
    model = make_model(reader, tokenizer, template, frozen=True)
    groups = model.writer.param_groups(1e-4, 2e-5)
    assert len(groups) == 1 and not any(p.requires_grad for p in model.writer.body.parameters())
    out = model.loss([model.prepare(qa(0), 4), model.prepare(qa(1, *QUESTIONS[1]), 4, 2)], None, 0.0)
    out["loss"].backward()
    assert model.writer.adapter.weight.grad.abs().sum() > 0 and model.writer.scale.grad is not None
    assert all(p.grad is None for p in model.writer.body.parameters())
    assert torch.equal(model.writer.adapter.weight.detach(), torch.eye(model.writer.adapter.weight.shape[0]))


def test_confidence_is_the_mean_logprob_of_the_answer(reader, template):
    prompt = template.text_prompt("qa", CONTEXT, "Ai dời đô ?")
    g = greedy_generate(reader, [embed_ids(reader, prompt)], 6, {template.eos_id})[0]
    assert len(g.logprobs) == len(g.ids) and all(lp <= 0 for lp in g.logprobs)
    assert g.confidence == pytest.approx(sum(g.logprobs) / len(g.logprobs))


def rows(f1s, confs, aie=None, n_tokens=100, used=25, method="m"):
    aie = aie or [True] * len(f1s)
    return [{"id": f"q{i}", "cluster": "p", "f1": f, "confidence": c, "aie": a, "n_tokens": n_tokens,
             "used_tokens": used, "ratio": 4, "budget": used, "method": method}
            for i, (f, c, a) in enumerate(zip(f1s, confs, aie))]


def test_logprob_fallback_choice_and_accounting():
    me = rows([1.0, 0.0, 1.0, 0.0], [-0.1, -2.0, -0.2, -0.05])
    full = rows([1.0, 1.0, 1.0, 1.0], [0, 0, 0, 0], method="full")
    points = curve(me, full)
    assert points[0]["fallback_rate"] == 0 and points[-1]["fallback_rate"] == 1 and points[-1]["f1"] == 100
    chosen = choose_tau(points, 100.0, target=0.75)  # needs 3/4 correct: re-read only the −2.0 answer
    assert chosen["fallback_rate"] == 0.25 and chosen["f1"] == 75
    assert chosen["confident_wrong_rate"] == 0.25  # the wrong answer at −0.05 is not caught
    assert chosen["tau"] == (-2.0 + -0.2) / 2  # midpoint of the dev confidences around the cut
    combined = logprob_fallback(me, full, chosen["tau"])
    assert [r["stage"] for r in combined] == [1, 3, 1, 1]
    assert [r["used_tokens"] for r in combined] == [25, 125, 25, 25]


def test_cascade_stages_costs_and_curve_agree():
    # q0: ME right and in evidence; q1: ME not in evidence, BM25 at 2k right; q2: both fail -> full
    me = rows([1.0, 1.0, 0.0], [-0.1, -0.1, -3.0], aie=[True, False, True], used=25)
    bm = rows([0.0, 1.0, 0.0], [-0.5, -0.2, -0.1], aie=[True, True, False], used=50, method="bm25_x2")
    full = rows([1.0, 1.0, 1.0], [0, 0, 0], method="full")
    out = cascade(me, bm, full, tau=-1.0)
    assert [r["stage"] for r in out] == [1, 2, 3]
    assert [r["used_tokens"] for r in out] == [25, 75, 175]  # k, k + 2k, k + 2k + n
    assert [r["f1"] for r in out] == [1.0, 1.0, 1.0]
    point = operating_point(out, 100.0)
    same = [p for p in curve(me, full, bm) if p["tau"] < -0.5 and p["tau"] > -3.0]
    assert same and all(p["f1"] == point["f1"] and p["mean_tokens"] == point["mean_tokens"] for p in same)
    assert same[0]["stage1_rate"] == pytest.approx(1 / 3) and same[0]["stage2_rate"] == pytest.approx(1 / 3)


def test_ece():
    rows_ = [{"confidence": math.log(0.9), "f1": 1.0}] * 9 + [{"confidence": math.log(0.9), "f1": 0.0}]
    assert ece(rows_)["ece"] == pytest.approx(0.0, abs=1e-9)  # 90% confident, 90% right
    rows_ = [{"confidence": math.log(0.95), "f1": 0.0}] * 4
    assert ece(rows_)["ece"] == pytest.approx(0.95)
