from vilatent.baselines import BM25Sentences, LeadSentences, TokenCounter, Truncation, bm25_scores, fit_head

TEXT = ("Hà Nội là thủ đô của Việt Nam. Thành phố có diện tích 3.359 km² và dân số 8,5 triệu người. "
        "Vua Lý Thái Tổ dời đô năm 1010.")


def test_truncation_keeps_head_within_budget(tokenizer):
    counter = TokenCounter(tokenizer)
    for budget in (1, 5, 9, 100):
        out = Truncation().compress(TEXT, "", budget, counter)
        assert counter.count(out) <= budget
        assert TEXT.startswith(out)
    assert fit_head(TEXT, 0, counter) == ""


def test_lead_keeps_only_whole_sentences(tokenizer):
    counter = TokenCounter(tokenizer)
    first = "Hà Nội là thủ đô của Việt Nam."
    budget = counter.count(first) + 3  # not enough for the second sentence
    assert LeadSentences().compress(TEXT, "", budget, counter) == first
    assert LeadSentences().compress(TEXT, "", 2, counter) == ""


def test_bm25_prefers_the_relevant_sentence_and_fills(tokenizer):
    counter = TokenCounter(tokenizer)
    scores = bm25_scores("Ai dời đô năm 1010 ?", [s for s in TEXT.split(". ")])
    assert max(range(3), key=lambda i: scores[i]) == 2
    budget = counter.count("Vua Lý Thái Tổ dời đô năm 1010.") + 4
    out = BM25Sentences().compress(TEXT, "Ai dời đô năm 1010 ?", budget, counter)
    assert "Vua Lý Thái Tổ dời đô năm 1010." in out
    assert counter.count(out) <= budget
    assert counter.count(out) > budget - 4  # the rest of the budget was filled


def test_bm25_never_packs_a_sentence_without_question_syllables(tokenizer):
    counter = TokenCounter(tokenizer)
    text = ("Trời hôm nay đẹp. Vua Lý Thái Tổ dời đô từ Hoa Lư về Đại La vào mùa thu năm 1010 "
            "và đổi tên thành Thăng Long.")
    budget = counter.count("Trời hôm nay đẹp.") + 1  # the unrelated sentence would fit whole
    out = BM25Sentences().compress(text, "Ai dời đô năm 1010 ?", budget, counter)
    assert out.startswith("Vua")  # the whole budget goes to the head of the relevant sentence
    assert counter.count(out) <= budget


def test_bm25_fill_cuts_at_reader_tokens(tokenizer):
    counter = TokenCounter(tokenizer)
    text = "Năm 1010, vua Lý Thái Tổ dời đô về Thăng Long."
    for budget in range(1, counter.count(text)):
        out = BM25Sentences().compress(text, "Năm nào dời đô ?", budget, counter)
        assert counter.count(out) <= budget
        assert counter.count(out) >= budget - 1  # no multi-token word left out whole
