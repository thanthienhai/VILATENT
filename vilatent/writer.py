"""The W0 writer (docs/VILATENT.md §Kiến trúc ViLatent, items 1–4).

    chunk ids ──► [sink] + chunk ──► L bottom layers of the reader (trainable copy)
              ──► drop the sink ──► mean of every ρ tokens ──► RMSNorm × s ──► adapter W (d×d)

* Multi-rate (revision of 25/10/2026): the hidden states h_t do not depend on the pooling ratio
  ρ, so one writer serves every ρ. ρ is an argument of ``forward`` (one value per chunk); W and
  s are shared by all ratios. Training samples ρ per example (vilatent.train).
* ``frozen`` (the LatentPress-style baseline, checklist A23): the copied layers are not trained,
  only s, W and the boundary embeddings.

* The body is a copy of the reader's L bottom decoder layers, built as the reader's own text
  model class with ``num_hidden_layers = L``, so rotary embeddings, masks and the Gated
  DeltaNet layers behave exactly as in the reader. Its final norm is replaced by the
  identity: the writer outputs raw hidden states. The reader itself is never modified.
* Each chunk runs independently, with a fixed sink token prepended; the sink's hidden state
  is dropped, so the large activation of the first position does not enter any group.
* W5 only (``sees_question``): the question tokens sit between the sink and the chunk, and
  their hidden states are dropped too; pooling, budget and parameters are those of W0.
* RMSNorm with a learned scalar scale ``s``, initialised so that the mean L2 norm of the
  memory equals the mean L2 norm of the reader's input embeddings (W = I at the start).
* Trainable weights are kept in fp32; the forward pass runs under autocast in the reader's
  dtype (bf16 by default, fp16 on GPUs without bf16 such as the T4; none for an fp32 reader).
"""
from __future__ import annotations

import copy
import math
import random

import torch
from torch import nn


def pool_rows(h: torch.Tensor, lengths: torch.Tensor, ratios: list[int]) -> list[torch.Tensor]:
    """mean_pool with one ratio per row of ``h``."""
    out = [None] * h.shape[0]
    for ratio in sorted(set(ratios)):
        idx = [i for i, r in enumerate(ratios) if r == ratio]
        sel = torch.tensor(idx, device=h.device)
        for i, pooled in zip(idx, mean_pool(h[sel], lengths[sel], ratio)):
            out[i] = pooled
    return out


def mean_pool(h: torch.Tensor, lengths: torch.Tensor, ratio: int) -> list[torch.Tensor]:
    """Mean of every ``ratio`` consecutive tokens of each row of ``h`` (C, T, d), using only the
    first ``lengths[i]`` tokens of row i. Row i gives ceil(lengths[i] / ratio) vectors; the
    last group may hold fewer than ``ratio`` tokens."""
    c, t, d = h.shape
    g = math.ceil(t / ratio)
    valid = torch.arange(g * ratio, device=h.device)[None, :] < lengths[:, None]  # (C, g·r)
    h = nn.functional.pad(h, (0, 0, 0, g * ratio - t)) * valid[..., None].to(h.dtype)
    sums = h.view(c, g, ratio, d).sum(2)
    counts = valid.view(c, g, ratio).sum(2).clamp(min=1)
    means = sums / counts[..., None].to(sums.dtype)
    n_groups = (lengths + ratio - 1) // ratio
    return [means[i, : int(n_groups[i])] for i in range(c)]


def bottom_layers_state(base, n_layers: int) -> dict[str, torch.Tensor]:
    """State dict of the first ``n_layers`` decoder layers of the reader's text model. Linear
    layers of a reader loaded in int4 (bitsandbytes, smoke test only) are dequantized, so the
    writer always starts as a plain floating-point copy."""
    def in_bottom(key: str) -> bool:
        return key.startswith("layers.") and int(key.split(".")[1]) < n_layers

    state = {k: v for k, v in base.state_dict().items() if in_bottom(k)}
    for name, module in base.named_modules():
        weight = getattr(module, "weight", None)
        if in_bottom(name) and hasattr(weight, "quant_state"):  # bitsandbytes Params4bit
            from bitsandbytes.functional import dequantize_4bit

            key = f"{name}.weight"  # drop the packed weight and its quantization state
            state = {k: v for k, v in state.items() if k != key and not k.startswith(key + ".")}
            state[key] = dequantize_4bit(weight.data, weight.quant_state)
    return state


def mean_embedding_norm(reader) -> float:
    weight = reader.get_input_embeddings().weight
    return float(weight.float().norm(dim=-1).mean())


def text_embedding(reader, tokenizer, text: str) -> torch.Tensor:
    ids = tokenizer(text, add_special_tokens=False)["input_ids"]
    weight = reader.get_input_embeddings().weight
    return weight[torch.tensor(ids, device=weight.device)].float().mean(0)


class MemoryWriter(nn.Module):
    def __init__(self, reader, tokenizer, n_layers: int = 4, lora_rank: int = 0, sees_question: bool = False,
                 frozen: bool = False, autocast: bool = True):
        super().__init__()
        base = reader.model  # the reader's text model (Qwen3_5TextModel, MistralModel, Qwen2Model…)
        cfg = copy.deepcopy(base.config)
        layer_types = getattr(cfg, "layer_types", None)
        if layer_types is not None:
            if "full_attention" in layer_types and "full_attention" not in layer_types[:n_layers]:
                raise ValueError(f"L={n_layers}: the writer must contain at least one attention layer "
                                 f"(layer types {layer_types[:n_layers]})")
            cfg.layer_types = list(layer_types[:n_layers])
        cfg.num_hidden_layers = n_layers
        cfg.vocab_size, cfg.pad_token_id = 1, None  # the writer always receives inputs_embeds

        body = type(base)(cfg)
        missing, unexpected = body.load_state_dict(bottom_layers_state(base, n_layers), strict=False)
        if unexpected or any(k.startswith("layers.") for k in missing):
            raise RuntimeError(f"writer copy failed: missing={missing} unexpected={unexpected}")
        body.norm = nn.Identity()
        self.body = body.float()
        if frozen and lora_rank:
            raise ValueError("a frozen writer has no LoRA")
        self.frozen = frozen
        if frozen:
            self.body.requires_grad_(False)

        d = cfg.hidden_size
        self.n_layers, self.lora_rank, self.autocast = n_layers, lora_rank, autocast
        self.sees_question = sees_question  # W5: [sink][question][chunk]; W0: [sink][chunk]
        self.layer_types = list(cfg.layer_types) if layer_types is not None else ["full_attention"] * n_layers
        self.autocast_dtype = reader.get_input_embeddings().weight.dtype
        self.emb_norm = mean_embedding_norm(reader)
        self.scale = nn.Parameter(torch.tensor(self.emb_norm / math.sqrt(d)))
        self.adapter = nn.Linear(d, d, bias=False)
        with torch.no_grad():
            self.adapter.weight.copy_(torch.eye(d))
        self.mem_start = nn.Parameter(text_embedding(reader, tokenizer, "«"))
        self.mem_end = nn.Parameter(text_embedding(reader, tokenizer, "»"))
        self.eps = cfg.rms_norm_eps
        if lora_rank > 0:
            self._add_lora(lora_rank)
        self.to(reader.get_input_embeddings().weight.device)

    def _add_lora(self, rank: int) -> None:
        """Freeze the copied layers and train LoRA adapters on all their linear maps instead."""
        from peft import LoraConfig, inject_adapter_in_model

        targets = sorted({name.split(".")[-1] for name, m in self.body.named_modules()
                          if isinstance(m, nn.Linear)})
        self.body.requires_grad_(False)
        self.body = inject_adapter_in_model(LoraConfig(r=rank, lora_alpha=2 * rank, target_modules=targets),
                                            self.body)

    def config(self) -> dict:
        return {"n_layers": self.n_layers, "lora_rank": self.lora_rank, "sees_question": self.sees_question,
                "frozen": self.frozen}

    def shape_config(self) -> dict:
        """The settings that fix the parameter shapes: a W0 stage-1 checkpoint can start a W5
        writer (seeing the question adds no parameter)."""
        return {"n_layers": self.n_layers, "lora_rank": self.lora_rank}

    def param_groups(self, lr_adapter: float, lr_writer: float) -> list[dict]:
        """Adapter, scale and boundary embeddings at lr_adapter; writer layers at lr_writer
        (none when frozen)."""
        head = [self.scale, self.mem_start, self.mem_end, *self.adapter.parameters()]
        body = [p for p in self.body.parameters() if p.requires_grad]
        return [{"params": head, "lr": lr_adapter}] + ([{"params": body, "lr": lr_writer}] if body else [])

    def checked_params(self) -> list[tuple[str, torch.Tensor]]:
        """Parameters whose gradient must be finite and non-zero after the first step: the adapter and
        the scale, and a weight matrix of the first copied layer, so a gradient that does not reach the
        writer layers (the adapter alone would still train) is caught. Not checked when the layers are
        frozen; the LoRA A matrices are skipped (their gradient is 0 while B is 0)."""
        checked = [("adapter", self.adapter.weight), ("scale", self.scale)]
        first = [(f"layer0.{name}", p) for name, p in self.body.layers[0].named_parameters()
                 if p.requires_grad and p.ndim >= 2 and "lora_A" not in name]
        return checked + first[:1]

    def normalize(self, x: torch.Tensor) -> torch.Tensor:
        x = x.float()
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps) * self.scale

    def forward(self, chunk_embeds: torch.Tensor, starts: torch.Tensor, lengths: torch.Tensor,
                ratios: list[int]) -> list[torch.Tensor]:
        """``chunk_embeds`` (C, T, d): reader embeddings of [sink] (+ question, W5) + chunk,
        right-padded. ``starts`` (C,): position of the first chunk token (1 for W0, 1 + question
        length for W5); everything before it is dropped. ``lengths`` (C,): number of chunk
        tokens. ``ratios``: pooling ratio ρ of every chunk. Returns one (ceil(n_i / ρ_i), d)
        memory tensor per chunk."""
        total = starts + lengths
        mask = (torch.arange(chunk_embeds.shape[1], device=lengths.device)[None, :] < total[:, None]).long()
        device_type = chunk_embeds.device.type
        enabled = self.autocast and self.autocast_dtype in (torch.bfloat16, torch.float16)
        with torch.autocast(device_type, dtype=self.autocast_dtype, enabled=enabled):
            with torch.set_grad_enabled(torch.is_grad_enabled() and not self.frozen):
                h = self.body(inputs_embeds=chunk_embeds.float(), attention_mask=mask,
                              use_cache=False).last_hidden_state
            # keep only the chunk positions of every row: h[i, starts[i] : starts[i] + lengths[i]]
            idx = (starts[:, None] + torch.arange(int(lengths.max()), device=h.device)[None, :]).clamp(
                max=h.shape[1] - 1)
            h = h.gather(1, idx[..., None].expand(-1, -1, h.shape[-1]))
            pooled = pool_rows(h, lengths, ratios)
            sizes = [p.shape[0] for p in pooled]
            memory = self.adapter(self.normalize(torch.cat(pooled)))
        return list(memory.split(sizes))


def prompt_init_ids(texts: list[str], tokenizer, n: int, seed: int = 0, n_texts: int = 500) -> list[int]:
    """``n`` reader token ids drawn (seeded) from the tokens of up to ``n_texts`` training
    contexts: the initial vectors of a PromptWriter are embeddings of ordinary Vietnamese tokens."""
    rng = random.Random(seed)
    pool = [t for text in rng.sample(texts, min(n_texts, len(texts)))
            for t in tokenizer(text, add_special_tokens=False)["input_ids"]]
    return [rng.choice(pool) for _ in range(n)]


class PromptWriter(nn.Module):
    """Control for ViLatent-ME (review of 22/10/2026): the memory is replaced by learned vectors
    that do not depend on the context. A chunk of n tokens pooled at ρ receives the first
    ceil(n / ρ) vectors of one learned table (ceil(chunk_tokens / min_ratio) vectors, so it
    serves every ratio of a multi-rate run), so the reader gets exactly the vector count, the
    boundary embeddings and the BM25 sentences of ME, and the same training (CE + λ·KL).
    What this control learns is the answer style of the training set, not the context, so
    ME minus this control is what the memory content adds (a condition of gate G1).

    It has the interface of MemoryWriter (forward, config, param_groups, mem_start/mem_end);
    the vectors start as embeddings of tokens of training contexts (prompt_init_ids)."""

    def __init__(self, reader, tokenizer, min_ratio: int, chunk_tokens: int, init_ids: list[int] | None = None):
        super().__init__()
        weight = reader.get_input_embeddings().weight
        self.min_ratio, self.chunk_tokens = min_ratio, chunk_tokens
        self.n_prompt = math.ceil(chunk_tokens / min_ratio)  # the most vectors one chunk can need
        self.sees_question = False
        self.emb_norm = mean_embedding_norm(reader)
        init = (weight[torch.tensor(init_ids, device=weight.device)].float() if init_ids is not None
                else torch.zeros(self.n_prompt, weight.shape[1]))
        if init.shape[0] != self.n_prompt:
            raise ValueError(f"PromptWriter needs {self.n_prompt} initial ids, got {init.shape[0]}")
        self.prompt = nn.Parameter(init.clone())
        self.mem_start = nn.Parameter(text_embedding(reader, tokenizer, "«"))
        self.mem_end = nn.Parameter(text_embedding(reader, tokenizer, "»"))
        self.to(weight.device)

    def config(self) -> dict:
        return {"kind": "prompt", "min_ratio": self.min_ratio, "chunk_tokens": self.chunk_tokens}

    def shape_config(self) -> dict:
        return self.config()

    def param_groups(self, lr_adapter: float, lr_writer: float) -> list[dict]:
        """Every parameter is a vector in the reader's embedding space: all at lr_adapter."""
        return [{"params": [self.prompt, self.mem_start, self.mem_end], "lr": lr_adapter}]

    def checked_params(self) -> list[tuple[str, torch.Tensor]]:
        return [("prompt", self.prompt)]

    def forward(self, chunk_embeds: torch.Tensor, starts: torch.Tensor, lengths: torch.Tensor,
                ratios: list[int]) -> list[torch.Tensor]:
        """Same signature as MemoryWriter.forward; only ``lengths`` and ``ratios`` are used."""
        groups = [math.ceil(int(n) / r) for n, r in zip(lengths.tolist(), ratios)]
        if max(groups) > self.n_prompt:
            raise ValueError(f"a chunk needs {max(groups)} vectors, the prompt has {self.n_prompt}")
        return [self.prompt[:g] for g in groups]


def build_writer(reader, tokenizer, config: dict, init_ids: list[int] | None = None) -> nn.Module:
    """Writer of a checkpoint's ``writer_config``: a PromptWriter when ``kind`` is "prompt",
    else the MemoryWriter (W0/W5)."""
    config = dict(config)
    if config.pop("kind", "layers") == "prompt":
        return PromptWriter(reader, tokenizer, init_ids=init_ids, **config)
    return MemoryWriter(reader, tokenizer, **config)
