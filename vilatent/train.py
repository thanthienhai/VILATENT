"""Training loop for stage 1 (task "continue") and stage 2 (task "qa"), docs/VILATENT.md
§Chiến lược huấn luyện, revised 25/10/2026 for the multi-rate writer.

Every training example gets its own (r, f), drawn uniformly from the pairs of ``ratios`` ×
``memory_factors`` with r·f ≤ ``max_pool`` (vilatent.model.allowed_pairs):

  stage 1   f = 1, ρ = r ∈ {4, 8, 16, 32}: one writer for every pooling ratio
  stage 2   r ∈ {4, 8, 16}, f ∈ {1, 2, 4, 8} (f = 1 is ViLatent-M, f ≥ 2 ViLatent-ME with the BM25
            sentences in the reader input, as at evaluation): one checkpoint for M and ME at every
            ratio; f is chosen at inference
  Q         stage 2 with ``sees_question`` (the writer reads the question), r = 4, f = 1, from
            the stage-1 writer (seeing the question adds no parameter)

``multi_share`` of the stage-2 examples (checklist A22: 30%) come from ``train_multi``: windows
of 2–8 passages of one training article (vilatent.data.multi_passage_rows), so the reader also
learns to read long memory sequences. The dev loss is measured on ``dev`` and ``dev_multi``
with a fixed (r, f) per dev example (the pairs in turn) and combined with the same shares; the
checkpoint with the lowest combined dev loss (CE + λ·KL) is kept.

Writers: ``layers`` (the copied bottom layers, trained at lr_writer, or frozen with
``freeze_writer``: the LatentPress-style baseline that trains only the adapter, the scale and the
boundary embeddings) or ``prompt`` (control "learned prompt + BM25": context-independent vectors
trained from scratch on the same data and loss). Pairs with f ≥ 2 read the BM25 parameters from
``bm25_config`` (configs/bm25.json, tuned for the bm25 baseline) and store them in the checkpoint.

Only the writer is trained; gradients flow back through the frozen reader. AdamW with two
learning rates (adapter 1e-4, writer layers 2e-5), no weight decay, gradient norm clipped at 1.0,
3% linear warmup then linear decay to 0. With ``dtype: float16`` (GPUs without bf16, e.g. the T4)
the loss is scaled (torch GradScaler) so that small gradients coming back through the fp16 reader
do not underflow.

Every run writes ``config.json``, ``metrics.jsonl`` (one JSON line per log or eval event) and
``best.pt`` into ``out_dir``.
"""
from __future__ import annotations

import json
import math
import random
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import torch

from .baselines import load_bm25_params
from .data import load_examples
from .model import MAX_POOL, ViLatent, allowed_pairs
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
    train_multi: str | None = None  # stage 2: multi-passage samples (scripts/build_long.py)
    dev_multi: str | None = None
    teacher_train_multi: str | None = None
    teacher_dev_multi: str | None = None
    multi_share: float = 0.0  # share of training examples drawn from train_multi (0.3; 0.15 if short on time)
    init_from: str | None = None  # stage-1 best.pt to start stage 2 from (O-LM); None = O-none
    writer: str = "layers"  # layers (copied bottom layers) or prompt (control: learned vectors that ignore the context)
    sees_question: bool = False  # ViLatent-Q (W5): the writer reads [sink][question][chunk]
    freeze_writer: bool = False  # frozen-writer baseline: train only adapter, scale, boundary embeddings
    bm25_config: str = "configs/bm25.json"  # tuned k1, b, units of the BM25 sentences (pairs with f >= 2)
    ratios: list[int] = field(default_factory=lambda: [4])  # r (stage 1: the pooling ratio)
    memory_factors: list[int] = field(default_factory=lambda: [1])  # f; 1 = memory only
    max_pool: int = MAX_POOL  # only pairs with r·f <= max_pool
    n_layers: int = 4
    lora_rank: int = 0  # 0: train the copied layers; > 0: LoRA on them
    chunk_tokens: int = 512
    lambda_kl: float = 1.0
    lr_adapter: float = 1e-4
    lr_writer: float = 2e-5
    weight_decay: float = 0.0
    max_grad_norm: float = 1.0
    warmup_frac: float = 0.03
    steps: int = 4000  # optimizer steps
    effective_batch: int = 32
    micro_batch: int = 4
    eval_every: int = 250
    dev_limit: int | None = None  # per dev file
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

    def pairs(self) -> list[tuple[int, int]]:
        return allowed_pairs(self.ratios, self.memory_factors, self.max_pool)


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


def index_stream(n: int, rng: random.Random):
    """Endless stream of indices into n examples, a new permutation every epoch."""
    if n == 0:
        raise ValueError("no training examples")
    while True:
        order = list(range(n))
        rng.shuffle(order)
        yield from order


class Sampler:
    """Micro-batches of (example, r, f): each example comes from the multi-passage pool with
    probability ``multi_share`` and gets a pair drawn uniformly from ``pairs``."""

    def __init__(self, single: list, multi: list, multi_share: float, pairs: list, seed: int):
        if multi_share > 0 and not multi:
            raise ValueError("multi_share > 0 needs train_multi")
        self.rng = random.Random(seed)
        self.single, self.multi, self.share, self.pairs = single, multi, multi_share, pairs
        self.streams = (index_stream(len(single), random.Random(seed + 1)),
                        index_stream(len(multi), random.Random(seed + 2)) if multi else None)

    def batch(self, size: int) -> list[tuple]:
        out = []
        for _ in range(size):
            from_multi = self.rng.random() < self.share
            pool = self.multi if from_multi else self.single
            ex = pool[next(self.streams[1 if from_multi else 0])]
            out.append((ex, *self.rng.choice(self.pairs)))
        return out


def dev_items(examples: list, pairs: list) -> list[tuple]:
    """Fixed (r, f) per dev example: the pairs in turn, so the dev loss is comparable across evals."""
    return [(ex, *pairs[i % len(pairs)]) for i, ex in enumerate(examples)]


def teacher_for(records: dict | None, batch) -> list | None:
    if records is None:
        return None
    return [(records[p.example.id]["ids"], records[p.example.id]["logp"]) for p in batch]


@torch.no_grad()
def dev_loss(model: ViLatent, dev: list[tuple], teacher: dict | None, cfg: TrainConfig) -> dict[str, float]:
    """Mean losses over ``dev`` items (example, r, f), weighted by example."""
    model.writer.eval()
    model.reader.eval()
    sums, n = {}, 0
    for start in range(0, len(dev), cfg.micro_batch):
        batch = [model.prepare(ex, r, f) for ex, r, f in dev[start:start + cfg.micro_batch]]
        out = model.loss(batch, teacher_for(teacher, batch), cfg.lambda_kl)
        for k, v in out.items():
            sums[k] = sums.get(k, 0.0) + float(v) * len(batch)
        n += len(batch)
    model.writer.train()
    model.reader.train()
    return {k: v / n for k, v in sums.items()}


def best_dev_loss(run_dir: str | Path) -> float:
    """Lowest dev loss of a finished run (the ``end`` event of its metrics.jsonl)."""
    with open(Path(run_dir) / "metrics.jsonl", encoding="utf-8") as f:
        ends = [row for row in map(json.loads, f) if row.get("event") == "end"]
    if not ends:
        raise ValueError(f"{run_dir} has not finished (no end event)")
    return float(ends[-1]["best_dev_loss"])


def check_gradients(writer) -> None:
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


def load_teachers(paths: list[str | None], template: ReaderTemplate) -> dict:
    records = {}
    for path in paths:
        if path:
            records.update(load_teacher(path, template))
    return records


def build_train_writer(cfg: TrainConfig, reader, tokenizer, train_ex: list, pairs: list):
    if cfg.writer == "prompt":
        if cfg.init_from or cfg.sees_question or cfg.freeze_writer:
            raise ValueError("the prompt control starts from scratch (no init_from) and has no writer layers")
        min_ratio = min(r * f for r, f in pairs)
        n_prompt = math.ceil(cfg.chunk_tokens / min_ratio)
        return PromptWriter(reader, tokenizer, min_ratio, cfg.chunk_tokens,
                            prompt_init_ids([ex.context for ex in train_ex], tokenizer, n_prompt, cfg.seed))
    if cfg.writer == "layers":
        if cfg.freeze_writer and cfg.init_from:
            raise ValueError("the frozen-writer baseline starts from the reader's own layers (no init_from)")
        if cfg.sees_question and any(f > 1 for _, f in pairs):
            raise ValueError("ViLatent-Q reads memory only: memory_factors must be [1]")
        return MemoryWriter(reader, tokenizer, cfg.n_layers, cfg.lora_rank, sees_question=cfg.sees_question,
                            frozen=cfg.freeze_writer)
    raise ValueError(f"unknown writer {cfg.writer!r}")


def train(cfg: TrainConfig) -> Path:
    out_dir = Path(cfg.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "best.pt").unlink(missing_ok=True)  # a rerun must not leave the previous run's checkpoint
    (out_dir / "config.json").write_text(json.dumps(asdict(cfg), indent=2, ensure_ascii=False), encoding="utf-8")
    set_seed(cfg.seed)
    if cfg.effective_batch % cfg.micro_batch:
        raise ValueError("effective_batch must be a multiple of micro_batch")
    accum = cfg.effective_batch // cfg.micro_batch
    pairs = cfg.pairs()
    if cfg.task == "continue" and any(f > 1 for _, f in pairs):
        raise ValueError("stage 1 has no question: memory_factors must be [1]")

    reader, tokenizer = load_reader(cfg.reader, dtype=cfg.dtype, quant=cfg.quant)
    if cfg.dtype == "float16" and reader.config.model_type.startswith("qwen3_5") and not fast_delta_rule():
        raise RuntimeError("float16 training of Qwen3.5 needs the flash-linear-attention DeltaNet kernel: "
                           "the pure-torch fallback gives NaN gradients in fp16 (pip install flash-linear-attention)")
    template = ReaderTemplate(load_reader_config(cfg.reader_config), tokenizer)
    if template.cfg["reader"] != cfg.reader:
        raise ValueError(f"{cfg.reader_config} was rendered for {template.cfg['reader']}, not {cfg.reader}")
    train_ex = load_examples(cfg.train, cfg.task)
    train_multi = load_examples(cfg.train_multi, cfg.task) if cfg.train_multi and cfg.multi_share > 0 else []
    dev_single = dev_items(load_examples(cfg.dev, cfg.task, cfg.dev_limit), pairs)
    dev_multi = (dev_items(load_examples(cfg.dev_multi, cfg.task, cfg.dev_limit), pairs)
                 if cfg.dev_multi and cfg.multi_share > 0 else [])
    writer = build_train_writer(cfg, reader, tokenizer, train_ex, pairs)
    if cfg.init_from:
        ckpt = torch.load(cfg.init_from, map_location="cpu", weights_only=False)
        shape = {k: ckpt["writer_config"].get(k) for k in writer.shape_config()}
        if shape != writer.shape_config() or ckpt["template_hash"] != template.hash:
            raise ValueError(f"{cfg.init_from}: writer {shape} or template differs from this run "
                             f"({writer.shape_config()})")
        trained = {r * f for r, f in ckpt.get("pairs") or []}
        if trained and not {r * f for r, f in pairs} <= trained:
            raise ValueError(f"{cfg.init_from} was trained at ρ {sorted(trained)}; this run pools at "
                             f"{sorted({r * f for r, f in pairs})}")
        writer.load_state_dict(ckpt["state_dict"])
    needs_bm25 = any(f > 1 for _, f in pairs)
    model = ViLatent(reader, tokenizer, template, writer, chunk_tokens=cfg.chunk_tokens,
                     bm25=load_bm25_params(cfg.bm25_config) if needs_bm25 else None, pairs=pairs)
    teacher_train = teacher_dev = None
    if cfg.lambda_kl > 0:
        if not (cfg.teacher_train and cfg.teacher_dev):
            raise ValueError("lambda_kl > 0 needs teacher_train and teacher_dev")
        if train_multi and not (cfg.teacher_train_multi and cfg.teacher_dev_multi):
            raise ValueError("multi-passage samples need teacher_train_multi and teacher_dev_multi")
        teacher_train = load_teachers([cfg.teacher_train, cfg.teacher_train_multi if train_multi else None], template)
        teacher_dev = load_teachers([cfg.teacher_dev, cfg.teacher_dev_multi if dev_multi else None], template)
        missing = ([ex.id for ex in train_ex + train_multi if ex.id not in teacher_train]
                   + [ex.id for ex, *_ in dev_single + dev_multi if ex.id not in teacher_dev])
        if missing:
            raise ValueError(f"{len(missing)} examples have no teacher, e.g. {missing[:3]}")

    if cfg.gradient_checkpointing:
        kwargs = {"gradient_checkpointing_kwargs": {"use_reentrant": False}}
        reader.gradient_checkpointing_enable(**kwargs)
        if hasattr(writer, "body") and not cfg.freeze_writer:
            writer.body.gradient_checkpointing_enable(**kwargs)
    reader.train()  # only to activate gradient checkpointing; the reader has no dropout and stays frozen
    writer.train()
    optimizer = torch.optim.AdamW(writer.param_groups(cfg.lr_adapter, cfg.lr_writer), weight_decay=cfg.weight_decay)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda(round(cfg.warmup_frac * cfg.steps), cfg.steps))
    trainable = [p for g in optimizer.param_groups for p in g["params"]]
    fp16 = cfg.dtype == "float16"
    scaler = torch.amp.GradScaler(enabled=fp16)
    share = cfg.multi_share if dev_multi else 0.0

    def eval_dev() -> dict[str, float]:
        single = dev_loss(model, dev_single, teacher_dev, cfg)
        out = {f"dev_single_{k}": v for k, v in single.items()}
        out["dev_loss"] = single["loss"]
        if dev_multi:
            multi = dev_loss(model, dev_multi, teacher_dev, cfg)
            out.update({f"dev_multi_{k}": v for k, v in multi.items()})
            out["dev_loss"] = (1 - share) * single["loss"] + share * multi["loss"]
        return out

    log = MetricsLog(out_dir / "metrics.jsonl")
    log.write(event="start", n_train=len(train_ex), n_train_multi=len(train_multi), n_dev=len(dev_single),
              n_dev_multi=len(dev_multi), pairs=pairs, accum=accum, dtype=cfg.dtype, quant=cfg.quant,
              trainable_params=sum(p.numel() for p in trainable), emb_norm=writer.emb_norm)
    sampler = Sampler(train_ex, train_multi, cfg.multi_share, pairs, cfg.seed)
    best, t0, checked = float("inf"), time.time(), False
    # recent speed: steps since the last train log, eval time excluded (the cumulative mean
    # sec_per_step is inflated by the first step, which compiles the kernels)
    t_recent, step_recent = t0, 0
    for step in range(cfg.steps):
        stats = {}
        for _ in range(accum):
            batch = [model.prepare(ex, r, f) for ex, r, f in sampler.batch(cfg.micro_batch)]
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
            dev = eval_dev()
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
