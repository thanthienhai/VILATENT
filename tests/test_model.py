"""W0 writer, reader input, losses and decoding on a tiny random Qwen3.5 (CPU, fp32)."""
import math

import pytest
import torch

from vilatent.baselines import Full, Truncation
from vilatent.data import Example
from vilatent.evaluate import evaluate_text, evaluate_vilatent
from vilatent.model import ViLatent, load_vilatent
from vilatent.reader import embed_ids, greedy_generate
from vilatent.teacher import compute_teacher
from vilatent.writer import MemoryWriter, mean_pool

CONTEXT = ("Hà Nội là thủ đô của Việt Nam. Thành phố có diện tích 3.359 km² và dân số 8,5 triệu người. "
           "Vua Lý Thái Tổ dời đô năm 1010.")


def make_model(reader, tokenizer, template, ratio=4, chunk_tokens=12, mode="M"):
    """``ratio`` is the budget ratio r; the writer pools 2r tokens in ME."""
    torch.manual_seed(0)
    writer = MemoryWriter(reader, tokenizer, n_layers=4, ratio=2 * ratio if mode == "ME" else ratio,
                          sees_question=mode == "W5", autocast=False)
    return ViLatent(reader, tokenizer, template, writer, mode=mode, chunk_tokens=chunk_tokens)


def qa(i=0, q="Ai dời đô ?", a="vua Lý Thái Tổ", context=CONTEXT):
    return Example(f"q{i}", "p0", "qa", context, question=q, answers=[a], target=a)


def test_writer_copies_bottom_layers_and_needs_attention(reader, tokenizer):
    writer = MemoryWriter(reader, tokenizer, n_layers=4, autocast=False)
    for (name, p), (_, q) in zip(writer.body.layers.named_parameters(), reader.model.layers[:4].named_parameters()):
        assert torch.equal(p, q.float()), name
    assert writer.layer_types == ["linear_attention"] * 3 + ["full_attention"]
    assert not any(p.requires_grad for p in reader.parameters())
    with pytest.raises(ValueError):
        MemoryWriter(reader, tokenizer, n_layers=2)


def test_mean_pool():
    h = torch.arange(2 * 6 * 1, dtype=torch.float).view(2, 6, 1)
    out = mean_pool(h, torch.tensor([6, 3]), 4)
    assert [o.shape[0] for o in out] == [2, 1]
    assert out[0][:, 0].tolist() == [1.5, 4.5] and out[1][:, 0].tolist() == [7.0]


def test_memory_size_norm_and_padding_invariance(reader, tokenizer, template):
    model = make_model(reader, tokenizer, template)
    p = model.prepare(qa())
    assert len(p.chunks) > 1
    with torch.no_grad():
        alone = model.encode_memory([p.chunks])[0]
        short = model.encode_memory([[p.chunks[0][:3]]])[0]
        both = model.encode_memory([p.chunks, [p.chunks[0][:3]]])
    assert alone.shape[0] == model.budget(p) + 2 == sum(math.ceil(len(c) / 4) for c in p.chunks) + 2
    assert torch.allclose(both[0], alone, atol=1e-5) and torch.allclose(both[1], short, atol=1e-5)
    norms = alone[1:-1].norm(dim=-1)  # W = I at init: memory norm = mean embedding norm
    assert torch.allclose(norms, torch.full_like(norms, model.writer.emb_norm), rtol=1e-2)


def test_gradients_reach_the_writer(reader, tokenizer, template):
    model = make_model(reader, tokenizer, template)
    batch = [model.prepare(qa(0)), model.prepare(qa(1, "Thành phố có diện tích bao nhiêu ?", "3.359 km²"))]
    out = model.loss(batch, None, 0.0)
    out["loss"].backward()
    for p in (model.writer.adapter.weight, model.writer.scale, model.writer.mem_start,
              next(model.writer.body.layers[0].linear_attn.parameters())):
        assert p.grad is not None and torch.isfinite(p.grad).all() and p.grad.abs().sum() > 0
    assert all(p.grad is None for p in reader.parameters())


def test_teacher_matches_student_on_full_context(reader, tokenizer, template):
    """The KL is ~0 when the student reads exactly what the teacher read."""
    model = make_model(reader, tokenizer, template)
    ex = qa()
    teacher = compute_teacher(reader, template, [ex], k=20, batch_size=1)[ex.id]
    target = template.target_ids("qa", ex.target)
    seq = embed_ids(reader, template.text_prompt("qa", ex.context, ex.question) + target)
    with torch.no_grad():
        out = model.target_loss([seq], [target], [(teacher["ids"], teacher["logp"])], 1.0)
    assert float(out["kl"]) < 1e-3
    assert abs(float(out["ce"]) - teacher["nll"]) < 1e-3


def test_greedy_generate_padding_and_reference(reader, tokenizer, template):
    prompts = [template.text_prompt("qa", CONTEXT, q) for q in ("Ai dời đô ?", "bao nhiêu ?")]
    prompts.append(template.text_prompt("qa", "Hà Nội", "Ai ?"))
    stop = {template.eos_id}
    single = [greedy_generate(reader, [embed_ids(reader, p)], 8, stop)[0].ids for p in prompts]
    batch = [g.ids for g in greedy_generate(reader, [embed_ids(reader, p) for p in prompts], 8, stop)]
    assert batch == single
    ref = reader.generate(torch.tensor([prompts[0]]), max_new_tokens=8, do_sample=False,
                          eos_token_id=sorted(stop))[0, len(prompts[0]):].tolist()
    assert ref == single[0]


def test_evaluation_paths_and_checkpoint(reader, tokenizer, template, tmp_path):
    model = make_model(reader, tokenizer, template)
    examples = [qa(0), qa(1, "Thành phố có diện tích bao nhiêu ?", "3.359 km²")]
    soft = evaluate_vilatent(model, examples, batch_size=2)
    assert {r["budget"] for r in soft} == {model.budget(model.prepare(examples[0]))}
    assert all(r["used_tokens"] == r["budget"] for r in soft)
    hard = evaluate_text(reader, tokenizer, template, Truncation(), examples, 4, chunk_tokens=12, batch_size=2)
    assert all(r["used_tokens"] <= r["budget"] == soft[0]["budget"] for r in hard)
    full = evaluate_text(reader, tokenizer, template, Full(), examples, None, batch_size=2)
    assert all(r["budget"] is None and r["used_tokens"] == r["n_tokens"] for r in full)

    model.save(tmp_path / "w.pt")
    loaded = load_vilatent(tmp_path / "w.pt", reader, tokenizer, template)
    loaded.writer.autocast = False
    with torch.no_grad():
        a = model.encode_memory([model.prepare(examples[0]).chunks])[0]
        b = loaded.encode_memory([loaded.prepare(examples[0]).chunks])[0]
    assert torch.allclose(a, b)
