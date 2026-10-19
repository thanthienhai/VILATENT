"""The frozen reader: loading, embeddings and greedy decoding from input embeddings.

Every method (memory, full context, hard baselines, no context) goes through the same
``greedy_generate`` on ``inputs_embeds``, so differences between methods cannot come from
two decoding back ends (docs/VILATENT.md §Thiết kế thực nghiệm, convention 4).

Qwen3.5 checkpoints are vision-language checkpoints. ``AutoModelForCausalLM`` maps them to
``Qwen3_5ForCausalLM``, which loads only the language model and skips ``model.visual.*``;
scripts/g0_check.py verifies this and the ``inputs_embeds`` path.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

import torch

# Reader dtype. bfloat16 is the default (H100); GPUs without bf16 (T4) use float16. The writer
# runs under autocast in the same dtype (writer.MemoryWriter).
DTYPES = {"bfloat16": torch.bfloat16, "float16": torch.float16, "float32": torch.float32}
# Reader weights: "none" (G0/G1) or "int4" (bitsandbytes NF4, computing in ``dtype``) to make the
# Kaggle T4 smoke test lighter and fit the 9B reader. int4 numbers are never G0/G1 evidence.
QUANTS = ("none", "int4")


def load_reader(name: str, device: str = "cuda", dtype: torch.dtype | str = torch.bfloat16,
                quant: str = "none", return_loading_info: bool = False):
    """Frozen reader in eval mode. With ``return_loading_info`` also returns the missing and
    unexpected checkpoint keys (scripts/g0_check.py: no weight may stay randomly initialised)."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    dtype = DTYPES[dtype] if isinstance(dtype, str) else dtype
    if quant not in QUANTS:
        raise ValueError(f"quant must be one of {QUANTS}")
    kwargs = {}
    if quant == "int4":  # embeddings and lm_head stay in dtype; the decoder linear layers are NF4
        from transformers import BitsAndBytesConfig

        kwargs["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                                           bnb_4bit_compute_dtype=dtype)
    tokenizer = AutoTokenizer.from_pretrained(name)
    model, info = AutoModelForCausalLM.from_pretrained(name, dtype=dtype, device_map=device,
                                                       output_loading_info=True, **kwargs)
    model.eval()
    model.requires_grad_(False)
    return (model, tokenizer, info) if return_loading_info else (model, tokenizer)


# Gated DeltaNet kernels of Qwen3.5 (scripts/g0_check.py requires the fast ones).
DELTANET_FUNCTIONS = ("torch_chunk_gated_delta_rule", "torch_recurrent_gated_delta_rule", "causal_conv1d_fn",
                      "causal_conv1d_update")


def _implementation(fn) -> str:
    """Module of the function a transformers kernel wrapper calls: transformers ≥ 5.16 resolves
    each kernel at import time (flash-linear-attention, causal-conv1d, else its torch code)."""
    found = []
    while fn is not None:
        found += [c.cell_contents for c in (fn.__closure__ or []) if callable(c.cell_contents)]
        fn = getattr(fn, "__wrapped__", None)
    outside = [getattr(f, "__module__", "") or "" for f in found]
    outside = [mod for mod in outside if not mod.startswith("transformers")]
    return outside[0] if outside else "torch"


def deltanet_kernels() -> dict:
    from transformers.models.qwen3_5 import modeling_qwen3_5 as m

    if hasattr(m, "is_fast_path_available"):  # transformers ≤ 5.12: one flag for all kernels
        return {"fast_deltanet_kernels": bool(m.is_fast_path_available)}
    impl = {name: _implementation(getattr(m, name, None)) for name in DELTANET_FUNCTIONS}
    return {"fast_deltanet_kernels": all(v != "torch" for v in impl.values()), "deltanet_kernels": impl}


def fast_delta_rule() -> bool:
    """The chunked delta rule runs in flash-linear-attention. Its pure-torch fallback computes
    the key l2norm in the input dtype, which overflows in fp16 at padded (zero) positions and
    gives NaN gradients; bf16 and fp32 are not affected."""
    kernels = deltanet_kernels()
    chunk = kernels.get("deltanet_kernels", {}).get("torch_chunk_gated_delta_rule", "torch")
    return kernels["fast_deltanet_kernels"] or chunk != "torch"


def eos_ids(model, template_eos_id: int) -> set[int]:
    ids = {template_eos_id}
    configured = getattr(model.generation_config, "eos_token_id", None)
    if configured is not None:
        ids |= set(configured if isinstance(configured, (list, tuple)) else [configured])
    return ids


def embed_ids(model, ids: list[int]) -> torch.Tensor:
    emb = model.get_input_embeddings()
    return emb(torch.tensor(ids, dtype=torch.long, device=emb.weight.device))


def left_pad(embeds: list[torch.Tensor]) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Stack (T_i, d) sequences with left padding. Returns embeds, attention mask, position ids
    (positions start at 0 on the first real token of every row)."""
    t_max, d = max(e.shape[0] for e in embeds), embeds[0].shape[1]
    x = embeds[0].new_zeros(len(embeds), t_max, d)
    mask = torch.zeros(len(embeds), t_max, dtype=torch.long, device=x.device)
    for i, e in enumerate(embeds):
        x[i, t_max - e.shape[0]:] = e
        mask[i, t_max - e.shape[0]:] = 1
    positions = (mask.cumsum(-1) - 1).clamp(min=0)
    return x, mask, positions


@dataclass
class Generation:
    ids: list[int]
    stopped: bool  # an end-of-turn token was produced within max_new_tokens
    logprobs: list[float]  # log-probability of each generated token under the reader

    @property
    def confidence(self) -> float:
        """Mean log-probability of the answer tokens (end-of-turn included): the signal that
        triggers re-reading the full context in ViLatent-MEF."""
        return sum(self.logprobs) / len(self.logprobs) if self.logprobs else float("-inf")


@torch.no_grad()
def greedy_generate(model, embeds: list[torch.Tensor], max_new_tokens: int,
                    stop_ids: set[int]) -> list[Generation]:
    """Greedy decoding for a batch of prompts given as input embeddings."""
    x, mask, positions = left_pad(embeds)
    def step(logits):
        logp = torch.log_softmax(logits[:, -1].float(), -1)
        nxt = logp.argmax(-1)
        return nxt, logp.gather(-1, nxt[:, None]).squeeze(-1)

    out = model(inputs_embeds=x, attention_mask=mask, position_ids=positions, use_cache=True,
                logits_to_keep=1)
    past, (nxt, lp) = out.past_key_values, step(out.logits)
    generated, logprobs = [[] for _ in embeds], [[] for _ in embeds]
    done = torch.zeros(len(embeds), dtype=torch.bool, device=x.device)
    stop = torch.tensor(sorted(stop_ids), device=x.device)
    for i_step in range(max_new_tokens):
        for i in range(len(embeds)):
            if not done[i]:
                generated[i].append(int(nxt[i]))
                logprobs[i].append(float(lp[i]))
        done |= torch.isin(nxt, stop)
        if bool(done.all()) or i_step == max_new_tokens - 1:
            break
        mask = torch.cat([mask, mask.new_ones(len(embeds), 1)], dim=1)
        positions = positions[:, -1:] + 1
        out = model(input_ids=nxt[:, None], attention_mask=mask, position_ids=positions,
                    past_key_values=past, use_cache=True, logits_to_keep=1)
        past, (nxt, lp) = out.past_key_values, step(out.logits)
    return [Generation(ids=g, stopped=bool(g) and g[-1] in stop_ids, logprobs=p) for g, p in zip(generated, logprobs)]


_THINK = re.compile(r"<think>.*?(</think>|$)", flags=re.S)


def decode(tokenizer, generation: Generation) -> tuple[str, str]:
    """Return ``(raw, clean)``: raw keeps special tokens (to detect a leaked <think> block),
    clean drops special tokens and any thinking block."""
    raw = tokenizer.decode(generation.ids, skip_special_tokens=False)
    clean = _THINK.sub("", tokenizer.decode(generation.ids, skip_special_tokens=True)).strip()
    return raw, clean
