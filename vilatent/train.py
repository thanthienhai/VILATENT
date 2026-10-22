"""Training loop for stage 1 (task "continue") and stage 2 (task "qa"), docs/VILATENT.md
§Chiến lược huấn luyện.

Modes (vilatent.model): stage 1 always runs in mode M (no question); stage 2 runs in M, ME
(the BM25 sentences are in the reader input, as at evaluation; the writer pools r·f tokens and
starts from a stage-1 writer at r·f) or W5 (the writer sees the question; it starts from the
stage-1 W0 writer at r, since seeing the question adds no parameter).

The control "learned prompt + BM25" (``writer: prompt``) runs in mode ME with a
writer.PromptWriter: context-independent vectors trained from scratch on the same data and loss.
ME (and the control) reads the BM25 parameters from ``bm25_config`` (configs/bm25.json, the
values tuned for the bm25 baseline) and stores them in the checkpoint.

Only the writer (copied layers or their LoRA, RMSNorm scale, adapter, boundary embeddings) is
trained; gradients flow back through the frozen reader. AdamW with two learning rates
(adapter 1e-4, writer layers 2e-5), no weight decay, gradient norm clipped at 1.0, 3% linear
warmup then linear decay to 0. The checkpoint with the lowest dev loss (CE + λ·KL) is kept.
With ``dtype: float16`` (GPUs without bf16, e.g. the T4) the loss is scaled (torch GradScaler)
so that small gradients coming back through the fp16 reader do not underflow.

Every run writes ``config.json``, ``metrics.jsonl`` (one JSON line per log or eval event) and
``best.pt`` into ``out_dir``.
"""
from __future__ import annotations

import json
import math
import random
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import torch

from .baselines import load_bm25_params
from .data import load_examples
from .model import ViLatent, writer_ratio
from .reader import fast_delta_rule, load_reader
from .teacher import load_teacher
from .template import ReaderTemplate, load_reader_config
from .writer import MemoryWriter, PromptWriter, prompt_init_ids


@dataclass
class TrainConfig:
    reader: str
    reader_config: str  # configs/readers/<reader>.json (scripts/render_template.py)
    task: str  # "continue" (stage 1) or "qa" (stage 2)
    train: str
    dev: str
    out_dir: str
    teacher_train: str | None = None  # required when lambda_kl > 0
    teacher_dev: str | None = None
    init_from: str | None = None  # stage-1 best.pt to start stage 2 from (O-LM); None = O-none
    mode: str = "M"  # M, ME (memory at r·f + BM25 sentences, stage 2 only) or W5 (writer sees the question)
    writer: str = "layers"  # layers (W0/W5 writer) or prompt (control: learned vectors that ignore the context)
    bm25_config: str = "configs/bm25.json"  # tuned k1, b of the BM25 sentences (ME only)
    ratio: int = 4  # budget ratio r; the writer pools r·f tokens in ME
    memory_factor: int = 2  # f in ME: 2, 4 or 8, chosen on the select dev loss (scripts/choose_by_loss.py)
    n_layers: int = 4
    lora_rank: int = 0  # 0: train the copied layers; > 0: LoRA on them
    chunk_tokens: int = 512
    lambda_kl: float = 1.0
    lr_adapter: float = 1e-4
    lr_writer: float = 2e-5
    weight_decay: float = 0.0
    max_grad_norm: float = 1.0
    warmup_frac: float = 0.03
    steps: int = 2000  # optimizer steps
    effective_batch: int = 32
    micro_batch: int = 4
    eval_every: int = 250
    dev_limit: int | None = None
    log_every: int = 10
    seed: int = 0
    gradient_checkpointing: bool = True
    dtype: str = "bfloat16"  # reader dtype and writer autocast: bfloat16, float16 (T4) or float32
    quant: str = "none"  # reader weights: none, or int4 for the T4 smoke test only (vilatent.reader)

    @classmethod
    def from_yaml(cls, path: str, **overrides) -> "TrainConfig":
        import yaml

        with open(path, encoding="utf-8") as f:
            values = yaml.safe_load(f) or {}
        values.update({k: v for k, v in overrides.items() if v is not None})
        return cls(**values)


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


class MetricsLog:
    def __init__(self, path: Path):
        self.f = open(path, "w", encoding="utf-8")  # no resume: a rerun starts a fresh log

    def write(self, **row) -> None:
        row = {k: (float(v) if isinstance(v, torch.Tensor) else v) for k, v in row.items()}
        self.f.write(json.dumps(row, ensure_ascii=False) + "\n")
        self.f.flush()
        print(json.dumps(row, ensure_ascii=False))


def lr_lambda(warmup: int, total: int):
    def f(step: int) -> float:
        if step < warmup:
            return (step + 1) / warmup
        return max(0.0, (total - step) / max(1, total - warmup))
    return f


def batches(n: int, size: int, seed: int):
    """Endless stream of index batches, a new permutation every epoch."""
    if n < size:
        raise ValueError(f"{n} training examples is fewer than one micro-batch of {size}")
    rng = random.Random(seed)
    while True:
        order = list(range(n))
        rng.shuffle(order)
        for start in range(0, n - size + 1, size):
            yield order[start:start + size]


def teacher_for(records: dict | None, batch) -> list | None:
    if records is None:
        return None
    return [(records[p.example.id]["ids"], records[p.example.id]["logp"]) for p in batch]


@torch.no_grad()
def dev_loss(model: ViLatent, dev, teacher: dict | None, cfg: TrainConfig) -> dict[str, float]:
    model.writer.eval()
    model.reader.eval()
    sums, n = {}, 0
    for start in range(0, len(dev), cfg.micro_batch):
        batch = [model.prepare(ex) for ex in dev[start:start + cfg.micro_batch]]
        out = model.loss(batch, teacher_for(teacher, batch), cfg.lambda_kl)
        for k, v in out.items():
            sums[k] = sums.get(k, 0.0) + float(v) * len(batch)
        n += len(batch)
    model.writer.train()
    model.reader.train()
    return {f"dev_{k}": v / n for k, v in sums.items()}


def best_dev_loss(run_dir: str | Path) -> float:
    """Lowest dev loss of a finished run (the ``end`` event of its metrics.jsonl)."""
    with open(Path(run_dir) / "metrics.jsonl", encoding="utf-8") as f:
        ends = [row for row in map(json.loads, f) if row.get("event") == "end"]
    if not ends:
        raise ValueError(f"{run_dir} has not finished (no end event)")
    return float(ends[-1]["best_dev_loss"])


def choose_by_dev_loss(runs: dict) -> tuple:
    """Key of the run with the lowest dev loss (CE + λ·KL on the same answers and the same
    teacher, so runs with different memory factors are comparable); ties go to the first key.
    The dev set of stage 2 is ViQuAD select, disjoint by article from ViQuAD gate, on which the
    G1 gate is measured, so the choice does not bias the gate."""
    losses = {key: best_dev_loss(path) for key, path in runs.items()}
    return min(losses, key=lambda key: losses[key]), losses


def check_gradients(writer: MemoryWriter) -> None:
    """After the first backward pass: gradients reaching the writer (through every reader
    layer, including the DeltaNet ones) must be finite and non-zero."""
    for name, p in writer.checked_params():
        if p.grad is None or not torch.isfinite(p.grad).all() or p.grad.abs().sum() == 0:
            raise RuntimeError(f"gradient check failed on the writer {name}: {p.grad}")


def grads_finite(params) -> bool:
    return all(p.grad is None or bool(torch.isfinite(p.grad).all()) for p in params)


# fp16 only: the first steps may overflow at the initial loss scale and are skipped by the
# GradScaler; the gradient check runs on the first step with finite gradients, within this many
MAX_SKIPPED_STEPS = 20


def train(cfg: TrainConfig) -> Path:
    out_dir = Path(cfg.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "best.pt").unlink(missing_ok=True)  # a rerun must not leave the previous run's checkpoint
    (out_dir / "config.json").write_text(json.dumps(asdict(cfg), indent=2, ensure_ascii=False), encoding="utf-8")
    set_seed(cfg.seed)
    if cfg.effective_batch % cfg.micro_batch:
        raise ValueError("effective_batch must be a multiple of micro_batch")
    accum = cfg.effective_batch // cfg.micro_batch

    reader, tokenizer = load_reader(cfg.reader, dtype=cfg.dtype, quant=cfg.quant)
    if cfg.dtype == "float16" and reader.config.model_type.startswith("qwen3_5") and not fast_delta_rule():
        raise RuntimeError("float16 training of Qwen3.5 needs the flash-linear-attention DeltaNet kernel: "
                           "the pure-torch fallback gives NaN gradients in fp16 (pip install flash-linear-attention)")
    template = ReaderTemplate(load_reader_config(cfg.reader_config), tokenizer)
    if template.cfg["reader"] != cfg.reader:
        raise ValueError(f"{cfg.reader_config} was rendered for {template.cfg['reader']}, not {cfg.reader}")
    train_ex = load_examples(cfg.train, cfg.task)
    dev_ex = load_examples(cfg.dev, cfg.task, cfg.dev_limit)
    ratio = writer_ratio(cfg.mode, cfg.ratio, cfg.memory_factor)
    if cfg.writer == "prompt":
        if cfg.mode != "ME" or cfg.init_from:
            raise ValueError("the prompt control runs in mode ME and starts from scratch (no init_from)")
        n_prompt = math.ceil(cfg.chunk_tokens / ratio)
        writer = PromptWriter(reader, tokenizer, ratio, cfg.chunk_tokens,
                              prompt_init_ids([ex.context for ex in train_ex], tokenizer, n_prompt, cfg.seed))
    elif cfg.writer == "layers":
        writer = MemoryWriter(reader, tokenizer, cfg.n_layers, ratio, cfg.lora_rank, sees_question=cfg.mode == "W5")
    else:
        raise ValueError(f"unknown writer {cfg.writer!r}")
    if cfg.init_from:
        ckpt = torch.load(cfg.init_from, map_location="cpu", weights_only=False)
        shape = {k: ckpt["writer_config"][k] for k in writer.shape_config()}
        if shape != writer.shape_config() or ckpt["template_hash"] != template.hash:
            raise ValueError(f"{cfg.init_from}: writer {shape} or template differs from this run "
                             f"({writer.shape_config()}); ME at r needs a stage-1 writer at r·f")
        writer.load_state_dict(ckpt["state_dict"])
    model = ViLatent(reader, tokenizer, template, writer, mode=cfg.mode, memory_factor=cfg.memory_factor,
                     chunk_tokens=cfg.chunk_tokens,
                     bm25=load_bm25_params(cfg.bm25_config) if cfg.mode == "ME" else None)
    teacher_train = teacher_dev = None
    if cfg.lambda_kl > 0:
        if not (cfg.teacher_train and cfg.teacher_dev):
            raise ValueError("lambda_kl > 0 needs teacher_train and teacher_dev")
        teacher_train = load_teacher(cfg.teacher_train, template)
        teacher_dev = load_teacher(cfg.teacher_dev, template)
        missing = ([ex.id for ex in train_ex if ex.id not in teacher_train]
                   + [ex.id for ex in dev_ex if ex.id not in teacher_dev])
        if missing:
            raise ValueError(f"{len(missing)} examples have no teacher, e.g. {missing[:3]}")

    if cfg.gradient_checkpointing:
        kwargs = {"gradient_checkpointing_kwargs": {"use_reentrant": False}}
        reader.gradient_checkpointing_enable(**kwargs)
        if hasattr(writer, "body"):
            writer.body.gradient_checkpointing_enable(**kwargs)
    reader.train()  # only to activate gradient checkpointing; the reader has no dropout and stays frozen
    writer.train()
    optimizer = torch.optim.AdamW(writer.param_groups(cfg.lr_adapter, cfg.lr_writer), weight_decay=cfg.weight_decay)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda(round(cfg.warmup_frac * cfg.steps), cfg.steps))
    trainable = [p for g in optimizer.param_groups for p in g["params"]]
    fp16 = cfg.dtype == "float16"
    scaler = torch.amp.GradScaler(enabled=fp16)

    log = MetricsLog(out_dir / "metrics.jsonl")
    log.write(event="start", n_train=len(train_ex), n_dev=len(dev_ex), accum=accum, dtype=cfg.dtype,
              quant=cfg.quant, trainable_params=sum(p.numel() for p in trainable), emb_norm=writer.emb_norm)
    stream = batches(len(train_ex), cfg.micro_batch, cfg.seed)
    best, t0, checked = float("inf"), time.time(), False
    # recent speed: steps since the last train log, eval time excluded (the cumulative mean
    # sec_per_step is inflated by the first step, which compiles the kernels)
    t_recent, step_recent = t0, 0
    for step in range(cfg.steps):
        stats = {}
        for _ in range(accum):
            batch = [model.prepare(train_ex[i]) for i in next(stream)]
            out = model.loss(batch, teacher_for(teacher_train, batch), cfg.lambda_kl)
            scaler.scale(out["loss"] / accum).backward()
            for k, v in out.items():
                stats[k] = stats.get(k, 0.0) + float(v.detach()) / accum
        scaler.unscale_(optimizer)
        if not checked:
            if fp16 and not grads_finite(trainable):
                if step + 1 >= MAX_SKIPPED_STEPS:
                    raise RuntimeError(f"fp16: gradients still not finite after {step + 1} steps")
            else:
                check_gradients(writer)
                checked = True
        grad_norm = torch.nn.utils.clip_grad_norm_(trainable, cfg.max_grad_norm)
        scaler.step(optimizer)  # skipped (fp16) when a gradient is not finite
        scaler.update()
        scheduler.step()
        optimizer.zero_grad(set_to_none=True)

        if step % cfg.log_every == 0 or step == cfg.steps - 1:
            now = time.time()
            log.write(event="train", step=step + 1, lr_adapter=scheduler.get_last_lr()[0],
                      grad_norm=grad_norm, scale=writer.scale.detach() if hasattr(writer, "scale") else None,
                      emb_norm=writer.emb_norm,
                      loss_scale=scaler.get_scale() if fp16 else 1.0,
                      sec_per_step=(now - t0) / (step + 1),
                      sec_per_step_recent=(now - t_recent) / (step + 1 - step_recent),
                      peak_mem_gb=torch.cuda.max_memory_allocated() / 2**30 if torch.cuda.is_available() else 0,
                      **stats)
            t_recent, step_recent = now, step + 1
        if (step + 1) % cfg.eval_every == 0 or step == cfg.steps - 1:
            dev = dev_loss(model, dev_ex, teacher_dev, cfg)
            improved = dev["dev_loss"] < best
            if improved:
                best = dev["dev_loss"]
                model.save(out_dir / "best.pt", extra={"step": step + 1, **dev})
            log.write(event="eval", step=step + 1, best=improved, **dev)
            t_recent, step_recent = time.time(), step + 1
    if not checked:  # fp16: every step was skipped, so the writer was never updated
        raise RuntimeError(f"fp16: no step out of {cfg.steps} had finite gradients; the writer was not trained")
    if best == float("inf"):
        raise RuntimeError("dev loss was never finite: no checkpoint written")
    log.write(event="end", best_dev_loss=best, hours=(time.time() - t0) / 3600)
    return out_dir / "best.pt"
