import json
import tempfile
from pathlib import Path

from vilatent.baselines import Summary, SummaryPlusE, TokenCounter, context_key
from vilatent.budget import chunk_context, memory_budget

CONTEXT = ("Hà Nội là thủ đô của Việt Nam . Thành phố có diện tích 3.359 km² và dân số 8,5 triệu người . "
           "TP. Hồ Chí Minh là thành phố lớn nhất . Vua Lý Thái Tổ dời đô năm 1010 . " * 4)
SUMMARY = "Hà Nội là thủ đô . TP. Hồ Chí Minh lớn nhất . Vua Lý Thái Tổ dời đô . " * 4


def write(_):
    p = Path(tempfile.mkdtemp()) / "s.json"
    p.write_text(json.dumps({"summaries": {context_key(CONTEXT): SUMMARY}}), encoding="utf-8")
    return str(p)


def test_summary_is_cut_to_the_budget(tokenizer):
    counter = TokenCounter(tokenizer, " ")
    out = Summary(write(None)).compress(CONTEXT, "q", 20, counter)
    assert 0 < counter.count(out) <= 20 and SUMMARY.startswith(out)


def test_sum_plus_e_fills_memory_share_with_summary_and_rest_with_bm25(tokenizer):
    counter = TokenCounter(tokenizer, " ")
    lengths = chunk_context(CONTEXT, tokenizer, 512, lead=" ").lengths
    ratio = 2
    k, k_mem = memory_budget(lengths, ratio), memory_budget(lengths, ratio * 2)
    b = SummaryPlusE(write(None), {"k1": 1.5, "b": 0.75, "units": "syllable"}, factor=2)
    b.set_ratio(ratio)
    out = b.compress(CONTEXT, "Vua Lý Thái Tổ dời đô năm nào ?", k, counter)
    assert counter.count(out) <= k
    assert out.startswith(b.compress.__self__.summary(CONTEXT)[:5])
    assert "1010" in out  # the BM25 evidence found the sentence with the answer
    assert k_mem < k


def test_perturb_memories_zero_and_shuffle_keep_shape_and_ends():
    import torch

    from vilatent.evaluate import perturb_memories

    memory = {"a": torch.arange(24, dtype=torch.float32).reshape(8, 3) + 1, "b": torch.randn(6, 3)}
    zero = perturb_memories(memory, "zero")
    shuf = perturb_memories(memory, "shuffle", seed=3)
    for out in (zero, shuf):
        for k, m in memory.items():
            assert out[k].shape == m.shape
            assert torch.equal(out[k][:1], m[:1]) and torch.equal(out[k][-1:], m[-1:])
    assert all(float(zero[k][1:-1].abs().sum()) == 0.0 for k in memory)
    for k, m in memory.items():  # same vectors, different order, deterministic in the seed
        assert sorted(shuf[k][1:-1].flatten().tolist()) == sorted(m[1:-1].flatten().tolist())
    assert not torch.equal(shuf["a"][1:-1], memory["a"][1:-1])
    again = perturb_memories(memory, "shuffle", seed=3)
    assert all(torch.equal(again[k], shuf[k]) for k in memory)
    try:
        perturb_memories(memory, "other")
    except ValueError:
        pass
    else:
        raise AssertionError("an unknown mode must raise")
