import math

from vilatent.budget import chunk_context, memory_budget, pack_chunks
from vilatent.text import contains_syllables, has_number, question_overlap, split_sentences, syllables


def sentences(text):
    return [text[a:b] for a, b in split_sentences(text)]


def test_split_basic_and_newlines():
    text = "Hà Nội là thủ đô. Dân số 8,5 triệu người!\nThành phố lớn?  Đúng vậy."
    assert sentences(text) == ["Hà Nội là thủ đô.", "Dân số 8,5 triệu người!", "Thành phố lớn?", "Đúng vậy."]


def test_split_keeps_abbreviations_initials_decimals():
    text = "Ông sống ở TP. Hồ Chí Minh từ năm 1975. PGS.TS. Nguyễn Văn A dạy 3.5 năm. J. K. Rowling viết sách."
    assert sentences(text) == ["Ông sống ở TP. Hồ Chí Minh từ năm 1975.", "PGS.TS. Nguyễn Văn A dạy 3.5 năm.",
                               "J. K. Rowling viết sách."]


def test_split_no_boundary_before_lowercase():
    assert sentences("Các loài cá, chim v.v. và nhiều loài khác.") == ["Các loài cá, chim v.v. và nhiều loài khác."]


def test_syllables():
    assert syllables("Hà Nội, năm 1010!") == ["hà", "nội", "năm", "1010"]


def test_contains_syllables_matches_whole_syllables():
    assert contains_syllables("Đoạn văn đề cập đến loài cây nào?", "cây")
    assert contains_syllables("Ai lãnh đạo Đảng Dân chủ?", "đảng dân chủ")
    assert not contains_syllables("Con cầy hương sống ở đâu?", "cây")
    assert not contains_syllables("Năm 1930 có gì?", "3")
    assert not contains_syllables("Câu hỏi?", "")


def test_has_number():
    for text in ("năm 1943", "60% - 70%", "hai mươi người", "phiên đầu tiên", "khóa X", "thế kỷ XIX"):
        assert has_number(text), text
    for text in ("ATP", "thời trung cổ", "Vitamin C", "Vitamin E", "nhiều giải pháp", "Lý, Bàn, Hoàng"):
        assert not has_number(text), text


def test_question_overlap_uses_the_answer_sentence():
    context = "Hà Nội là thủ đô. Làng gốm Kim Lan thuộc huyện Gia Lâm."
    assert question_overlap("Làng gốm Kim Lan thuộc huyện nào?", context, "huyện Gia Lâm") == 6 / 7
    assert question_overlap("Thủ đô là gì?", context, "Hà Nội") == 3 / 4
    assert question_overlap("Nơi nào?", context, "Gia Lâm") == 0.0
    assert question_overlap("Nơi nào?", context, "đô. Làng") == 0.0  # answer across sentences


def test_pack_chunks_respects_max_and_sentence_ends():
    cuts = [100, 250, 400, 900, 1000]
    bounds = pack_chunks(cuts, 1000, 512)
    assert bounds[0] == (0, 400)  # three sentences fit, the fourth would exceed 512
    assert all(b - a <= 512 for a, b in bounds)
    assert bounds[-1][1] == 1000
    assert all(b in cuts or b - a == 512 for a, b in bounds)  # sentence end, or a hard split


def test_pack_chunks_hard_splits_a_long_sentence():
    bounds = pack_chunks([1200], 1200, 512)
    assert bounds == [(0, 512), (512, 1024), (1024, 1200)]


def test_chunk_context_and_budget(tokenizer):
    text = "Hà Nội là thủ đô của Việt Nam. Thành phố có diện tích 3.359 km². TP. Hồ Chí Minh là thành phố lớn nhất."
    chunked = chunk_context(text, tokenizer, max_tokens=12)
    assert sum(chunked.lengths) == chunked.n_tokens
    assert all(n <= 12 for n in chunked.lengths)
    assert [i for c in chunked.chunks for i in c] == chunked.ids
    assert memory_budget(chunked.lengths, 4) == sum(math.ceil(n / 4) for n in chunked.lengths)
    assert memory_budget([10, 3], 4) == 3 + 1


def test_slot_tokenization_is_shared(tokenizer, template):
    """Chunks, the teacher/full-context prompt and the hard-baseline counter all tokenize the
    context as lead + text; the prefix itself does not end with the space."""
    from vilatent.baselines import TokenCounter

    text = "Hà Nội là thủ đô của Việt Nam. Thành phố có diện tích 3.359 km²."
    assert template.cfg["prompts"]["qa"].split("{context}")[0].endswith("Đoạn văn: ")
    assert template.lead["qa"] == " "
    assert template.prefix_ids("qa") == template.ids(template.cfg["prompts"]["qa"].split("{context}")[0].rstrip(" "))
    chunked = chunk_context(text, tokenizer, lead=template.lead["qa"])
    assert chunked.ids == template.context_ids("qa", text)
    prompt = template.text_prompt("qa", text, "Ai ?")
    assert prompt[len(template.prefix_ids("qa")):][:len(chunked.ids)] == chunked.ids
    counter = TokenCounter(tokenizer, lead=" ")
    assert counter.count(text) == len(chunked.ids) and counter.count("") == 0
    assert counter.offsets(text)[0] == (0, 2)  # "Hà", relative to the text without the lead
    assert template.context_ids("qa", "") == []
