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
