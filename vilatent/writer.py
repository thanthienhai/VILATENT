"""The W0 writer (docs/VILATENT.md §Kiến trúc ViLatent, items 1–4).

    chunk ids ──► [sink] + chunk ──► L bottom layers of the reader (trainable copy)
              ──► drop the sink ──► mean of every r tokens ──► RMSNorm × s ──► adapter W (d×d)

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
* Trainable weights are kept in fp32; the forward pass runs under bf16 autocast.
"""
from __future__ import annotations

import copy
import math

import torch
from torch import nn


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


def mean_embedding_norm(reader) -> float:
    weight = reader.get_input_embeddings().weight
    return float(weight.float().norm(dim=-1).mean())


def text_embedding(reader, tokenizer, text: str) -> torch.Tensor:
    ids = tokenizer(text, add_special_tokens=False)["input_ids"]
    weight = reader.get_input_embeddings().weight
    return weight[torch.tensor(ids, device=weight.device)].float().mean(0)


class MemoryWriter(nn.Module):
    def __init__(self, reader, tokenizer, n_layers: int = 4, ratio: int = 4, lora_rank: int = 0,
                 sees_question: bool = False, autocast: bool = True):
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
        layers = {k: v for k, v in base.state_dict().items()
                  if k.startswith("layers.") and int(k.split(".")[1]) < n_layers}
        missing, unexpected = body.load_state_dict(layers, strict=False)
        if unexpected or any(k.startswith("layers.") for k in missing):
            raise RuntimeError(f"writer copy failed: missing={missing} unexpected={unexpected}")
        body.norm = nn.Identity()
        self.body = body.float()

        d = cfg.hidden_size
        self.n_layers, self.ratio, self.lora_rank, self.autocast = n_layers, ratio, lora_rank, autocast
        self.sees_question = sees_question  # W5: [sink][question][chunk]; W0: [sink][chunk]
        self.layer_types = list(cfg.layer_types) if layer_types is not None else ["full_attention"] * n_layers
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
        return {"n_layers": self.n_layers, "ratio": self.ratio, "lora_rank": self.lora_rank,
                "sees_question": self.sees_question}

    def shape_config(self) -> dict:
        """The settings that fix the parameter shapes: a W0 stage-1 checkpoint can start a W5
        writer (seeing the question adds no parameter)."""
        return {"n_layers": self.n_layers, "ratio": self.ratio, "lora_rank": self.lora_rank}

    def param_groups(self, lr_adapter: float, lr_writer: float) -> list[dict]:
        """Adapter, scale and boundary embeddings at lr_adapter; writer layers at lr_writer."""
        head = [self.scale, self.mem_start, self.mem_end, *self.adapter.parameters()]
        body = [p for p in self.body.parameters() if p.requires_grad]
        return [{"params": head, "lr": lr_adapter}, {"params": body, "lr": lr_writer}]

    def normalize(self, x: torch.Tensor) -> torch.Tensor:
        x = x.float()
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps) * self.scale

    def forward(self, chunk_embeds: torch.Tensor, starts: torch.Tensor, lengths: torch.Tensor) -> list[torch.Tensor]:
        """``chunk_embeds`` (C, T, d): reader embeddings of [sink] (+ question, W5) + chunk,
        right-padded. ``starts`` (C,): position of the first chunk token (1 for W0, 1 + question
        length for W5); everything before it is dropped. ``lengths`` (C,): number of chunk
        tokens. Returns one (ceil(n_i / r), d) memory tensor per chunk."""
        total = starts + lengths
        mask = (torch.arange(chunk_embeds.shape[1], device=lengths.device)[None, :] < total[:, None]).long()
        device_type = chunk_embeds.device.type
        with torch.autocast(device_type, dtype=torch.bfloat16, enabled=self.autocast):
            h = self.body(inputs_embeds=chunk_embeds.float(), attention_mask=mask,
                          use_cache=False).last_hidden_state
            # keep only the chunk positions of every row: h[i, starts[i] : starts[i] + lengths[i]]
            idx = (starts[:, None] + torch.arange(int(lengths.max()), device=h.device)[None, :]).clamp(
                max=h.shape[1] - 1)
            h = h.gather(1, idx[..., None].expand(-1, -1, h.shape[-1]))
            pooled = mean_pool(h, lengths, self.ratio)
            sizes = [p.shape[0] for p in pooled]
            memory = self.adapter(self.normalize(torch.cat(pooled)))
        return list(memory.split(sizes))
