"""End-to-end: teacher file → train() for a few steps → best.pt that evaluates (tiny reader, CPU)."""
import dataclasses
import json

import pytest
import torch

import vilatent.train as T
from conftest import make_reader
from vilatent.data import load_examples, write_jsonl
from vilatent.teacher import compute_teacher, load_teacher, save_teacher
from vilatent.template import ReaderTemplate, render_reader_config

CONTEXT = "Hà Nội là thủ đô của Việt Nam. Thành phố có diện tích 3.359 km² và dân số 8,5 triệu người."
ROWS = [{"id": f"q{i}", "cluster": f"p{i % 2}", "context": CONTEXT, "question": q, "answers": [a]}
        for i, (q, a) in enumerate([("Thủ đô của Việt Nam ?", "Hà Nội"), ("bao nhiêu người ?", "8,5 triệu"),
                                    ("diện tích bao nhiêu ?", "3.359 km²"), ("Ai ?", "Hà Nội")])]


def test_train_two_steps(tokenizer, tmp_path, monkeypatch):
    reader = make_reader(len(tokenizer))
    cfg_path = tmp_path / "reader.json"
    cfg_path.write_text(json.dumps(render_reader_config("tiny", tokenizer)), encoding="utf-8")
    template = ReaderTemplate(json.loads(cfg_path.read_text(encoding="utf-8")), tokenizer)
    data = tmp_path / "qa.jsonl"
    write_jsonl(data, ROWS)
    teacher = tmp_path / "teacher.pt"
    save_teacher(teacher, compute_teacher(reader, template, load_examples(data, "qa")), template, 20, str(data))
    assert set(load_teacher(teacher, template)) == {r["id"] for r in ROWS}

    monkeypatch.setattr(T, "load_reader", lambda name, **kwargs: (reader, tokenizer))
    bm25 = tmp_path / "bm25.json"
    bm25.write_text(json.dumps({"k1": 1.2, "b": 0.5}), encoding="utf-8")
    cfg = T.TrainConfig(reader="tiny", reader_config=str(cfg_path), task="qa", train=str(data), dev=str(data),
                        out_dir=str(tmp_path / "run"), teacher_train=str(teacher), teacher_dev=str(teacher),
                        steps=2, effective_batch=4, micro_batch=2, eval_every=1, chunk_tokens=8,
                        bm25_config=str(bm25))
    best = T.train(cfg)
    assert best.exists()
    events = [json.loads(line)["event"] for line in open(tmp_path / "run" / "metrics.jsonl", encoding="utf-8")]
    assert events[0] == "start" and events[-1] == "end" and events.count("eval") == 2

    # W5 starts from the W0 writer at the same ratio (seeing the question adds no parameter)
    w5 = T.train(dataclasses.replace(cfg, mode="W5", init_from=str(best), out_dir=str(tmp_path / "w5"), steps=1))
    assert torch.load(w5, weights_only=False)["mode"] == "W5"
    # ME at r = 4 with f = 2 pools 8 tokens: it cannot start from a writer at 4
    with pytest.raises(ValueError, match="r·f"):
        T.train(dataclasses.replace(cfg, mode="ME", init_from=str(best), out_dir=str(tmp_path / "bad"), steps=1))
    me = T.train(dataclasses.replace(cfg, mode="ME", out_dir=str(tmp_path / "me"), steps=1))
    ckpt = torch.load(me, weights_only=False)
    assert ckpt["mode"] == "ME" and ckpt["writer_config"]["ratio"] == 8
    assert ckpt["bm25"] == {"k1": 1.2, "b": 0.5}  # the tuned values travel with the checkpoint
    # the learned-prompt control: mode ME, from scratch, loaded back as a PromptWriter
    with pytest.raises(ValueError, match="from scratch"):
        T.train(dataclasses.replace(cfg, mode="ME", writer="prompt", init_from=str(best), steps=1,
                                    out_dir=str(tmp_path / "bad2")))
    prompt = T.train(dataclasses.replace(cfg, mode="ME", writer="prompt", out_dir=str(tmp_path / "pe"), steps=1,
                                         lr_adapter=1e-3))
    from vilatent.model import load_vilatent
    from vilatent.writer import PromptWriter

    loaded = load_vilatent(prompt, reader, tokenizer, template)
    assert isinstance(loaded.writer, PromptWriter) and loaded.mode == "ME" and loaded.bm25 == {"k1": 1.2, "b": 0.5}
