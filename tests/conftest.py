"""CPU fixtures: a word-level tokenizer with a Qwen-like chat template and a tiny random
Qwen3.5 reader (3 Gated DeltaNet layers + 1 attention layer, ×2). No download, no GPU."""
import pytest

TEMPLATE = (
    "{% for m in messages %}<|im_start|>{{ m['role'] }}\n{{ m['content'] }}<|im_end|>\n{% endfor %}"
    "{% if add_generation_prompt %}<|im_start|>assistant\n"
    "{% if enable_thinking is defined and enable_thinking is false %}<think>\n\n</think>\n\n{% endif %}{% endif %}"
)
SPECIAL = ["<|endoftext|>", "<|im_start|>", "<|im_end|>", "<think>", "</think>", "[UNK]"]
CORPUS = (
    "Hà Nội là thủ đô của Việt Nam . Thành phố có diện tích 3.359 km² và dân số 8,5 triệu người . "
    "TP. Hồ Chí Minh là thành phố lớn nhất . Đọc đoạn văn và trả lời câu hỏi bằng một cụm từ ngắn lấy từ "
    "đoạn văn . Chỉ ghi câu trả lời : Câu hỏi Trả lời Viết tiếp đoạn văn sau user assistant { context } "
    "{ question } « » ? ! , Vua vua Lý Thái Tổ dời đô năm 1010 Ai bao nhiêu"
)


def make_tokenizer():
    from tokenizers import Tokenizer, models, pre_tokenizers
    from transformers import PreTrainedTokenizerFast

    words = sorted(set(CORPUS.split()) | set("{}.,:?!«»"))
    vocab = {tok: i for i, tok in enumerate(SPECIAL + words)}
    backend = Tokenizer(models.WordLevel(vocab, unk_token="[UNK]"))
    backend.pre_tokenizer = pre_tokenizers.Sequence([pre_tokenizers.WhitespaceSplit(),
                                                     pre_tokenizers.Punctuation()])
    tok = PreTrainedTokenizerFast(tokenizer_object=backend, unk_token="[UNK]", pad_token="<|endoftext|>",
                                  eos_token="<|im_end|>")
    tok.add_special_tokens({"additional_special_tokens": SPECIAL[1:5]})
    tok.chat_template = TEMPLATE
    return tok


def make_reader(vocab_size: int):
    import torch
    from transformers import Qwen3_5ForCausalLM, Qwen3_5TextConfig

    torch.manual_seed(0)
    cfg = Qwen3_5TextConfig(
        vocab_size=vocab_size, hidden_size=64, intermediate_size=128, num_hidden_layers=8,
        num_attention_heads=4, num_key_value_heads=2, head_dim=16, linear_key_head_dim=16,
        linear_value_head_dim=16, linear_num_key_heads=2, linear_num_value_heads=4,
        layer_types=["linear_attention"] * 3 + ["full_attention"] + ["linear_attention"] * 3 + ["full_attention"],
        eos_token_id=2, pad_token_id=0)
    model = Qwen3_5ForCausalLM(cfg).float().eval()
    model.requires_grad_(False)
    return model


@pytest.fixture(scope="session")
def tokenizer():
    return make_tokenizer()


@pytest.fixture(scope="session")
def reader(tokenizer):
    return make_reader(len(tokenizer))


@pytest.fixture(scope="session")
def template(tokenizer):
    from vilatent.template import ReaderTemplate, render_reader_config

    return ReaderTemplate(render_reader_config("tiny", tokenizer), tokenizer)
