"""Reading modes added after the question-aware review: ME (memory 2r + BM25 sentences in the
same budget), W5 (writer sees the question), the answer confidence and the MEF fallback."""
import math

import pytest
import torch

from test_model import CONTEXT, make_model, qa
from vilatent.data import Example
from vilatent.evaluate import evaluate_vilatent
from vilatent.fallback import choose_tau, combine, curve
from vilatent.reader import embed_ids, greedy_generate

QUESTIONS = [("Ai dời đô ?", "Vua Lý Thái Tổ"), ("Thành phố có diện tích bao nhiêu ?", "3.359 km²")]


def test_me_splits_the_budget_between_memory_and_sentences(reader, tokenizer, template):
    model = make_model(reader, tokenizer, template, ratio=4, mode="ME")
    assert model.writer.ratio == 8 and model.budget_ratio == 4
    p = model.prepare(qa(0, *QUESTIONS[0]))
    k = sum(math.ceil(len(c) / 4) for c in p.chunks)
    k_m = sum(math.ceil(len(c) / 8) for c in p.chunks)
    assert p.budget == k
    assert 0 < len(p.evidence_ids) <= k - k_m
    with torch.no_grad():
        memory = model.encode_memory([p.chunks])[0]
    assert memory.shape[0] - 2 == k_m
    # the sentences sit between ⟨/mem⟩ and the question, as text ids
    seq = model.memory_prompt(p, memory)
    assert seq.shape[0] == len(p.prefix_ids) + k_m + 2 + len(p.evidence_ids) + len(p.suffix_ids)


@pytest.mark.parametrize("factor", [2, 4])
def test_memory_factor_moves_budget_to_text(reader, tokenizer, template, factor):
    torch.manual_seed(0)
    from vilatent.model import ViLatent
    from vilatent.writer import MemoryWriter

    writer = MemoryWriter(reader, tokenizer, n_layers=4, ratio=2 * factor, autocast=False)
    model = ViLatent(reader, tokenizer, template, writer, mode="ME", memory_factor=factor, chunk_tokens=12)
    assert model.budget_ratio == 2
    p = model.prepare(qa(0, *QUESTIONS[0]))
    k_m = sum(math.ceil(len(c) / (2 * factor)) for c in p.chunks)
    assert p.budget == sum(math.ceil(len(c) / 2) for c in p.chunks)
    assert len(p.evidence_ids) <= p.budget - k_m


def test_choose_by_dev_loss(tmp_path):
    import json

    from vilatent.train import choose_by_dev_loss

    for f, loss in ((2, 1.3), (4, 1.1), (8, 1.1)):
        (tmp_path / f"f{f}").mkdir()
        (tmp_path / f"f{f}" / "metrics.jsonl").write_text(
            json.dumps({"event": "start"}) + "\n" + json.dumps({"event": "end", "best_dev_loss": loss}) + "\n")
    chosen, losses = choose_by_dev_loss({f: tmp_path / f"f{f}" for f in (2, 4, 8)})
    assert chosen == 4 and losses[8] == 1.1  # ties go to the smaller factor (more memory)


def test_me_rows_respect_the_budget_and_share_memory(reader, tokenizer, template):
    model = make_model(reader, tokenizer, template, ratio=4, mode="ME")
    rows = evaluate_vilatent(model, [qa(i, q, a) for i, (q, a) in enumerate(QUESTIONS)], batch_size=2)
    assert all(r["used_tokens"] == r["memory_vectors"] + r["evidence_tokens"] <= r["budget"] for r in rows)
    assert all(r["mode"] == "ME" and r["ratio"] == 4 and math.isfinite(r["confidence"]) for r in rows)


def test_w5_memory_depends_on_the_question_and_m_does_not(reader, tokenizer, template):
    m = make_model(reader, tokenizer, template, mode="M")
    w5 = make_model(reader, tokenizer, template, mode="W5")
    a, b = (model.prepare(qa(i, q, ans)) for i, (q, ans) in enumerate(QUESTIONS) for model in [w5])
    with torch.no_grad():
        mem_a, mem_b = w5.encode_memory([a.chunks, b.chunks], [a.question_ids, b.question_ids])
        alone_a = w5.encode_memory([a.chunks], [a.question_ids])[0]
        m_a, m_b = m.encode_memory([a.chunks, b.chunks])
    assert mem_a.shape == mem_b.shape == m_a.shape  # same budget as W0
    assert not torch.allclose(mem_a[1:-1], mem_b[1:-1])
    assert torch.allclose(m_a, m_b)
    assert torch.allclose(mem_a, alone_a, atol=1e-5)  # questions of different lengths in one batch
    assert w5.memory_key(a) != w5.memory_key(b) and m.memory_key(a) == m.memory_key(b)


def test_mode_and_writer_must_agree(reader, tokenizer, template):
    from vilatent.model import ViLatent

    w0 = make_model(reader, tokenizer, template).writer
    with pytest.raises(ValueError):
        ViLatent(reader, tokenizer, template, w0, mode="W5")
    with pytest.raises(ValueError):  # stage 1 has no question: it must run in mode M
        make_model(reader, tokenizer, template, mode="ME").prepare(Example("s", "d", "continue", CONTEXT, target="x"))


def test_confidence_is_the_mean_logprob_of_the_answer(reader, template):
    prompt = template.text_prompt("qa", CONTEXT, "Ai dời đô ?")
    g = greedy_generate(reader, [embed_ids(reader, prompt)], 6, {template.eos_id})[0]
    assert len(g.logprobs) == len(g.ids) and all(lp <= 0 for lp in g.logprobs)
    assert g.confidence == pytest.approx(sum(g.logprobs) / len(g.logprobs))


def rows(f1s, confs, n_tokens=100, used=25):
    return [{"id": f"q{i}", "cluster": "p", "f1": f, "confidence": c, "n_tokens": n_tokens, "used_tokens": used,
             "ratio": 4, "budget": used, "method": "m"} for i, (f, c) in enumerate(zip(f1s, confs))]


def test_fallback_choice_and_accounting():
    me = rows([1.0, 0.0, 1.0, 0.0], [-0.1, -2.0, -0.2, -0.05])
    full = rows([1.0, 1.0, 1.0, 1.0], [0, 0, 0, 0])
    points = curve(me, full)
    assert points[0]["fallback_rate"] == 0 and points[-1]["fallback_rate"] == 1 and points[-1]["f1"] == 100
    chosen = choose_tau(me, full, target=0.75)  # needs 3/4 correct: re-read only the −2.0 answer
    assert chosen["fallback_rate"] == 0.25 and chosen["f1"] == 75
    assert chosen["confident_wrong_rate"] == 0.25  # the wrong answer at −0.05 is not caught
    assert chosen["tau"] == (-2.0 + -0.2) / 2  # midpoint of the dev confidences around the cut
    combined = combine(me, full, chosen["tau"])
    assert [r["fallback"] for r in combined] == [False, True, False, False]
    assert [r["used_tokens"] for r in combined] == [25, 125, 25, 25]
