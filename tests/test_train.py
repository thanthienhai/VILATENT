"""End-to-end: teacher file → train() for a few steps → best.pt that evaluates (tiny reader, CPU)."""
import dataclasses
import json
import random

import pytest
import torch

import vilatent.train as T
from conftest import make_reader
from vilatent.data import load_examples, multi_passage_rows, read_jsonl, write_jsonl
from vilatent.teacher import compute_teacher, load_teacher, save_teacher
from vilatent.template import ReaderTemplate, render_reader_config

CONTEXT = "Hà Nội là thủ đô của Việt Nam. Thành phố có diện tích 3.359 km² và dân số 8,5 triệu người."
OTHER = "Vua Lý Thái Tổ dời đô năm 1010."
ROWS = [{"id": f"viquad-0001-000{1 + i % 2}-000{i}", "cluster": f"p{i % 2}", "title": "Hà Nội",
         "context": CONTEXT if i % 2 == 0 else OTHER, "question": q, "answers": [a]}
        for i, (q, a) in enumerate([("Thủ đô của Việt Nam ?", "Hà Nội"), ("Ai dời đô ?", "Vua Lý Thái Tổ"),
                                    ("diện tích bao nhiêu ?", "3.359 km²"), ("năm bao nhiêu ?", "1010")])]


def test_sampler_mixes_pools_and_pairs():
    sampler = T.Sampler(list("abcd"), list("XYZ"), 0.3, [(4, 1), (8, 2)], seed=0)
    batch = [x for _ in range(500) for x in sampler.batch(4)]
    share = sum(ex in "XYZ" for ex, _, _ in batch) / len(batch)
    assert 0.25 < share < 0.35 and {(r, f) for _, r, f in batch} == {(4, 1), (8, 2)}
    assert T.dev_items(list("abc"), [(4, 1), (8, 2)]) == [("a", 4, 1), ("b", 8, 2), ("c", 4, 1)]
    with pytest.raises(ValueError):
        T.Sampler(list("ab"), [], 0.3, [(4, 1)], seed=0)


def test_train_multi_rate_and_variants(tokenizer, tmp_path, monkeypatch):
    reader = make_reader(len(tokenizer))
    cfg_path = tmp_path / "reader.json"
    cfg_path.write_text(json.dumps(render_reader_config("tiny", tokenizer)), encoding="utf-8")
    template = ReaderTemplate(json.loads(cfg_path.read_text(encoding="utf-8")), tokenizer)
    data, multi = tmp_path / "qa.jsonl", tmp_path / "multi.jsonl"
    write_jsonl(data, ROWS)
    write_jsonl(multi, multi_passage_rows(ROWS, seed=0))
    assert all(r["n_passages"] == 2 and "\n\n" in r["context"] and r["id"].startswith("multi-")
               for r in read_jsonl(multi))
    teacher, teacher_multi = tmp_path / "teacher.pt", tmp_path / "teacher_multi.pt"
    for src, out in ((data, teacher), (multi, teacher_multi)):
        save_teacher(out, compute_teacher(reader, template, load_examples(src, "qa")), template, 20, str(src))
    assert set(load_teacher(teacher, template)) == {r["id"] for r in ROWS}

    monkeypatch.setattr(T, "load_reader", lambda name, **kwargs: (reader, tokenizer))
    bm25 = tmp_path / "bm25.json"
    bm25.write_text(json.dumps({"k1": 1.2, "b": 0.5, "units": "word"}), encoding="utf-8")
    random.seed(0)
    # stage-1-like run: f = 1 only, several pooling ratios
    stage1 = T.TrainConfig(reader="tiny", reader_config=str(cfg_path), task="qa", train=str(data), dev=str(data),
                           out_dir=str(tmp_path / "s1"), teacher_train=str(teacher), teacher_dev=str(teacher),
                           ratios=[4, 8], memory_factors=[1], steps=2, effective_batch=4, micro_batch=2,
                           eval_every=1, chunk_tokens=8, bm25_config=str(bm25))
    best = T.train(stage1)
    events = [json.loads(line) for line in open(tmp_path / "s1" / "metrics.jsonl", encoding="utf-8")]
    assert events[0]["event"] == "start" and events[-1]["event"] == "end"
    assert [e["event"] for e in events].count("eval") == 2
    assert torch.load(best, weights_only=False)["pairs"] == [(4, 1), (8, 1)]

    # stage 2: M and ME in one run, 30% multi-passage windows, combined dev loss
    cfg = dataclasses.replace(stage1, out_dir=str(tmp_path / "s2"), init_from=str(best), ratios=[2, 4],
                              memory_factors=[1, 2], max_pool=8, train_multi=str(multi), dev_multi=str(multi),
                              teacher_train_multi=str(teacher_multi), teacher_dev_multi=str(teacher_multi),
                              multi_share=0.3)
    with pytest.raises(ValueError, match="ρ"):  # ρ = 2 was never trained in stage 1
        T.train(cfg)
    cfg = dataclasses.replace(cfg, ratios=[4], memory_factors=[1, 2])
    s2 = T.train(cfg)
    ckpt = torch.load(s2, weights_only=False)
    assert ckpt["pairs"] == [(4, 1), (4, 2)] and ckpt["bm25"] == {"k1": 1.2, "b": 0.5, "units": "word"}
    ev = [json.loads(line) for line in open(tmp_path / "s2" / "metrics.jsonl", encoding="utf-8")]
    last = [e for e in ev if e["event"] == "eval"][-1]
    assert last["dev_loss"] == pytest.approx(0.7 * last["dev_single_loss"] + 0.3 * last["dev_multi_loss"])
    with pytest.raises(ValueError, match="teacher"):  # multi-passage samples need their teacher
        T.train(dataclasses.replace(cfg, teacher_train_multi=None, out_dir=str(tmp_path / "bad")))

    # ViLatent-Q from the stage-1 writer; the frozen writer and the prompt control from scratch
    q = T.train(dataclasses.replace(stage1, sees_question=True, init_from=str(best), ratios=[4],
                                    out_dir=str(tmp_path / "q"), steps=1))
    assert torch.load(q, weights_only=False)["writer_config"]["sees_question"]
    with pytest.raises(ValueError, match="memory only"):
        T.train(dataclasses.replace(cfg, sees_question=True, out_dir=str(tmp_path / "bad2"), steps=1))
    frozen = T.train(dataclasses.replace(cfg, freeze_writer=True, init_from=None, out_dir=str(tmp_path / "fz"),
                                         steps=1))
    from vilatent.model import load_vilatent
    from vilatent.writer import MemoryWriter, PromptWriter

    loaded = load_vilatent(frozen, reader, tokenizer, template)
    assert isinstance(loaded.writer, MemoryWriter) and loaded.writer.frozen
    fresh = MemoryWriter(reader, tokenizer, 4)
    for p, ref in zip(loaded.writer.body.layers.parameters(), fresh.body.layers.parameters()):
        assert torch.equal(p, ref)  # the copied layers did not move
    with pytest.raises(ValueError, match="from scratch"):
        T.train(dataclasses.replace(cfg, writer="prompt", out_dir=str(tmp_path / "bad3"), steps=1))
    prompt = T.train(dataclasses.replace(cfg, writer="prompt", init_from=None, out_dir=str(tmp_path / "pe"),
                                         steps=1, lr_adapter=1e-3))
    loaded = load_vilatent(prompt, reader, tokenizer, template)
    assert isinstance(loaded.writer, PromptWriter) and loaded.writer.n_prompt == 2  # ceil(8 / 4)
    assert loaded.pairs == [(4, 1), (4, 2)]
