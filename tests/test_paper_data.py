"""Revision of 25/10/2026: pyvi BM25 without question words, sentence packing, ViQuAD-Long and the
multi-passage windows, token-based generation batches."""
import pytest

from vilatent.baselines import BM25Sentences, TokenCounter, bm25_scores, pack_sentences
from vilatent.data import article_passages, long_rows, multi_passage_rows, position_bin
from vilatent.evaluate import length_batches
from vilatent.text import query_words, words


def row(article: int, paragraph: int, question: int, context: str, answer: str = "x", title: str = "A") -> dict:
    return {"id": f"viquad-{article:04d}-{paragraph:04d}-{question:04d}", "cluster": f"p{paragraph}",
            "title": title, "context": context, "question": "?", "answers": [answer]}


def test_words_and_question_words():
    assert words("Thủ đô của Việt Nam là thành phố nào?") == ["thủ_đô", "của", "việt_nam", "là", "thành_phố", "nào"]
    assert query_words("Thủ đô của Việt Nam là thành phố nào?") == ["thủ_đô", "của", "việt_nam", "là", "thành_phố"]
    assert "bao_nhiêu" not in query_words("Dân số có bao nhiêu người?")


def test_word_bm25_ignores_question_words():
    sentences = ["Ai cũng thích lễ hội nào đó.", "Lý Thái Tổ dời đô về Thăng Long."]
    word = bm25_scores("Ai dời đô?", sentences)
    syl = bm25_scores("Ai dời đô?", sentences, units="syllable")
    assert word[1] > 0 and word[0] == 0  # "ai" is a question word, removed from the query
    assert syl[0] > 0  # the G1 syllable selector matched "ai"


def test_pack_sentences_respects_budget_and_order(tokenizer):
    counter = TokenCounter(tokenizer)
    sentences = ["Hà Nội là thủ đô của Việt Nam .", "Thành phố có diện tích 3.359 km² .", "Vua Lý Thái Tổ dời đô năm 1010 ."]
    for budget in range(0, 30):
        out = pack_sentences(sentences, [0.1, 2.0, 1.0], budget, counter, positive_only=False)
        assert counter.count(out) <= budget
        kept = [s for s in sentences if s in out]
        assert kept == [s for s in sentences if s in kept]  # original order
    whole = counter.count(sentences[1])
    assert pack_sentences(sentences, [0.1, 2.0, 1.0], whole, counter, False) == sentences[1]
    # positive_only: a zero-score sentence is never packed whole; its budget goes to the best head
    out = pack_sentences(sentences, [0.0, 0.0, 1.0], counter.count(sentences[0]), counter, True)
    assert out.startswith("Vua")


def test_long_rows_join_the_article_in_json_order():
    rows = [row(1, 2, 1, "Đoạn hai .", "hai"), row(1, 1, 1, "Đoạn một .", "một"), row(1, 2, 2, "Đoạn hai .", "Đoạn"),
            row(1, 3, 1, "Đoạn ba .", "ba")]
    passages = article_passages(rows)
    assert passages == {"A": ["Đoạn một .", "Đoạn hai .", "Đoạn ba ."]}
    out = long_rows(rows, passages)
    assert all(r["context"] == "Đoạn một .\n\nĐoạn hai .\n\nĐoạn ba ." for r in out)
    assert [r["passage_index"] for r in out] == [1, 0, 1, 2] and out[0]["n_passages"] == 3
    assert [r["position"] for r in out] == ["middle", "beginning", "middle", "end"]
    # bins on the passage centre (i + 0.5) / n
    assert [position_bin(i, 7) for i in range(7)] == ["beginning"] * 2 + ["middle"] * 3 + ["end"] * 2


def test_multi_passage_windows_contain_the_question_passage():
    rows = [row(1, p, 1, f"Đoạn {p} .", str(p)) for p in range(1, 11)] + [row(2, 1, 1, "Một đoạn .", title="B")]
    out = multi_passage_rows(rows, seed=0)
    assert len(out) == 10  # article B has a single passage: no window
    for r in out:
        parts = r["context"].split("\n\n")
        assert 2 <= r["n_passages"] == len(parts) <= 8
        assert parts[r["passage_index"]] == f"Đoạn {r['answers'][0]} ."
        numbers = [int(p.split()[1]) for p in parts]
        assert numbers == list(range(numbers[0], numbers[0] + len(numbers)))  # contiguous, in order
        assert r["id"].startswith("multi-")
    assert multi_passage_rows(rows, seed=0) == out  # seeded


def test_length_batches_cap_padded_tokens():
    batches = length_batches([10, 5000, 20, 9000, 30], batch_size=8, max_batch_tokens=10_000)
    assert sorted(i for b in batches for i in b) == [0, 1, 2, 3, 4]
    lengths = [10, 5000, 20, 9000, 30]
    for b in batches:
        assert len(b) == 1 or len(b) * max(lengths[i] for i in b) <= 10_000
    assert length_batches([1, 2, 3], 2, None) == [[0, 1], [2]]


def test_bm25_selector_on_a_long_context(tokenizer):
    counter = TokenCounter(tokenizer)
    context = "\n\n".join(["Hà Nội là thủ đô của Việt Nam ."] * 30 + ["Vua Lý Thái Tổ dời đô năm 1010 ."])
    out = BM25Sentences(units="word").compress(context, "Vua Lý Thái Tổ dời đô năm nào ?", 9, counter)
    assert out.startswith("Vua Lý Thái Tổ") and counter.count(out) <= 9


@pytest.mark.parametrize("units", ["word", "syllable"])
def test_bm25_units_both_run(tokenizer, units):
    out = BM25Sentences(units=units).compress("Hà Nội là thủ đô . Vua dời đô năm 1010 .", "Ai dời đô ?", 5,
                                              TokenCounter(tokenizer))
    assert out
