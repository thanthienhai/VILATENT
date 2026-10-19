"""Gate G0: the Qwen3.5 infrastructure works (docs/VILATENT.md §Cổng quyết định, week 1–2).

Checks, for one reader (run it for Qwen3.5-2B and Qwen3.5-9B):
  load        text-only model through AutoModelForCausalLM: no vision weights, no missing
              checkpoint key (no randomly initialised weight), and for Qwen3.5 the
              flash-linear-attention / causal-conv1d kernels must be available
  template    the rendered template exists for this reader; for Qwen3.5 the answer turn
              starts with the empty <think></think> block
  embeds      logits from input_ids == logits from inputs_embeds (the multimodal wrapper is
              not on the path)
  decode      greedy decoding from inputs_embeds == model.generate(input_ids) on one prompt;
              a left-padded batch gives the same answers as one prompt at a time (a mismatch
              there is reported as a warning: bf16 kernels on different shapes can flip a tie)
  backward    loss → reader (frozen, every DeltaNet layer) → memory → writer: gradients on the
              memory, the adapter and the first writer layer are finite and non-zero; also the
              time and peak memory of one forward + backward step (cost estimate)
  first_token norm of the hidden state at position 0 after the writer layers, relative to the
              median of the other positions, with and without the sink token
  llmlingua2  the LLMLingua-2 baseline loads and compresses the sample context within its 4×
              budget (G1 fails without all hard baselines, so a broken install is caught here)

Exit code 1 when a check fails. A JSON report goes to results/g0/<reader>.json.

Usage:
  python scripts/g0_check.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json
  python scripts/g0_check.py ... --dtype float16     # GPUs without bf16 (T4): smoke test only
"""
import argparse
import json
import sys
import time
from pathlib import Path

import torch

from vilatent.baselines import TokenCounter
from vilatent.budget import context_budget
from vilatent.data import Example
from vilatent.evaluate import MAX_NEW_TOKENS
from vilatent.metrics import parse_answer, score_qa
from vilatent.model import ViLatent
from vilatent.reader import DTYPES, embed_ids, greedy_generate, load_reader
from vilatent.template import ReaderTemplate, load_reader_config
from vilatent.writer import MemoryWriter

CONTEXT = ("Hà Nội là thủ đô của nước Cộng hòa xã hội chủ nghĩa Việt Nam. Thành phố nằm ở trung tâm đồng bằng "
           "sông Hồng, có diện tích khoảng 3.359 km² và dân số hơn 8,5 triệu người vào năm 2023. Hà Nội từng là "
           "kinh đô của nhiều triều đại phong kiến, với tên gọi Thăng Long từ năm 1010 dưới thời vua Lý Thái Tổ. "
           "Ngày nay, thành phố là trung tâm chính trị, văn hóa và giáo dục lớn của cả nước.")
QUESTIONS = [("Hà Nội có diện tích khoảng bao nhiêu?", "khoảng 3.359 km²"),
             ("Ai dời đô về Thăng Long?", "vua Lý Thái Tổ"),
             ("Thăng Long có từ năm nào?", "1010")]


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


def check_load(reader, info: dict) -> dict:
    names = [n for n, _ in reader.named_parameters()]
    cfg = reader.config
    out = {"class": type(reader).__name__, "params_b": sum(p.numel() for p in reader.parameters()) / 1e9,
           "vision_params": sum("visual" in n for n in names), "layers": cfg.num_hidden_layers,
           "hidden_size": cfg.hidden_size, "vocab": cfg.vocab_size}
    if getattr(cfg, "layer_types", None):
        out["layer_types"] = {t: cfg.layer_types.count(t) for t in set(cfg.layer_types)}
    if cfg.model_type.startswith("qwen3_5"):
        out.update(deltanet_kernels())
    # a missing key means a randomly initialised weight: decoding would still "work", so the
    # other checks could pass on a broken model
    out["missing_keys"] = list(info.get("missing_keys", []))
    out["unexpected_keys"] = len(info.get("unexpected_keys", []))  # vision tower and MTP head, skipped
    # backward through DeltaNet needs the flash-linear-attention kernels (docs/VILATENT.md); the
    # pure-torch fallback is correct but too slow for the GPU budget, so G0 requires them
    out["pass"] = (out["vision_params"] == 0 and not out["missing_keys"]
                   and out.get("fast_deltanet_kernels", True))
    return out


def check_template(template: ReaderTemplate, model_type: str) -> dict:
    turn = template.cfg["prompts"]["qa"].split("{context}")[1]
    out = {"answer_turn_tail": turn[-40:], "hash": template.hash}
    out["pass"] = ("<think>\n\n</think>" in turn) if model_type.startswith("qwen3_5") else True
    return out


@torch.no_grad()
def check_embeds(reader, ids: list[int]) -> dict:
    x = torch.tensor([ids], device=reader.device)
    a = reader(input_ids=x).logits.float()
    b = reader(inputs_embeds=reader.get_input_embeddings()(x)).logits.float()
    diff = float((a - b).abs().max())
    return {"max_abs_logit_diff": diff, "pass": diff < 1e-3}


@torch.no_grad()
def check_decode(reader, tokenizer, prompts: list[list[int]], stop_ids: set[int]) -> dict:
    n = MAX_NEW_TOKENS["qa"]
    ref = reader.generate(torch.tensor([prompts[0]], device=reader.device), max_new_tokens=n, do_sample=False,
                          eos_token_id=sorted(stop_ids))[0, len(prompts[0]):].tolist()
    ours = greedy_generate(reader, [embed_ids(reader, prompts[0])], n, stop_ids)[0].ids
    single = [greedy_generate(reader, [embed_ids(reader, p)], n, stop_ids)[0].ids for p in prompts]
    batch = [g.ids for g in greedy_generate(reader, [embed_ids(reader, p) for p in prompts], n, stop_ids)]
    return {"generate": tokenizer.decode(ref), "ours": tokenizer.decode(ours),
            "answers": [tokenizer.decode(s) for s in single],
            # sanity of the loaded weights (3 questions, full context; reported, not a gate)
            "full_context_f1": [score_qa(parse_answer(tokenizer.decode(s, skip_special_tokens=True)), [a])["f1"]
                                for s, (_, a) in zip(single, QUESTIONS)],
            "same_as_generate": ref == ours, "batch_equals_single": batch == single,
            "pass": ref == ours, "warning": None if batch == single else "padded batch differs from single prompts"}


def check_backward(model: ViLatent, n_layers: int) -> dict:
    model.reader.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.reader.train()
    model.writer.train()
    batch = [model.prepare(Example(f"g0-{i}", "g0", "qa", CONTEXT, question=q, answers=[a], target=a))
             for i, (q, a) in enumerate(QUESTIONS)]
    torch.cuda.reset_peak_memory_stats() if torch.cuda.is_available() else None
    t0 = time.time()
    memories = model.encode_memory([p.chunks for p in batch])
    for m in memories:
        m.retain_grad()
    seqs = [model.memory_prompt(p, m, with_target=True) for p, m in zip(batch, memories)]
    loss = model.target_loss(seqs, [p.target_ids for p in batch], None, 0.0)["loss"]
    loss.backward()
    seconds = time.time() - t0
    first_layer = [p for p in model.writer.body.layers[0].parameters() if p.requires_grad]

    def ok(grads):
        return all(g is not None and bool(torch.isfinite(g).all()) and float(g.abs().sum()) > 0 for g in grads)

    out = {"loss": float(loss), "memory_grad_ok": ok([m.grad for m in memories]),
           "adapter_grad_ok": ok([model.writer.adapter.weight.grad]),
           "writer_layer0_grad_ok": ok([p.grad for p in first_layer]),
           "writer_layer_types": model.writer.layer_types,
           "step_seconds": seconds,
           "peak_mem_gb": torch.cuda.max_memory_allocated() / 2**30 if torch.cuda.is_available() else None}
    out["pass"] = out["memory_grad_ok"] and out["adapter_grad_ok"] and out["writer_layer0_grad_ok"]
    model.writer.zero_grad(set_to_none=True)
    model.reader.eval()
    return out


@torch.no_grad()
def check_first_token(model: ViLatent, ids: list[int]) -> dict:
    """Hidden-state norm after the writer layers, divided by the median norm of the later
    positions. Descriptive only: it shows whether the sink absorbs the large activation."""
    def norms(seq):
        x = embed_ids(model.reader, seq)[None].float()
        return model.writer.body(inputs_embeds=x).last_hidden_state[0].float().norm(dim=-1)

    plain, sunk = norms(ids), norms([model.template.sink_id] + ids)
    return {"first_token_no_sink": float(plain[0] / plain[1:].median()),
            "sink_token": float(sunk[0] / sunk[1:].median()),
            "first_content_token_after_sink": float(sunk[1] / sunk[2:].median()), "pass": True}


def check_llmlingua(tokenizer, template: ReaderTemplate) -> dict:
    lead = template.lead["qa"]
    _, budget = context_budget(CONTEXT, tokenizer, 4, lead=lead)
    try:
        from vilatent.baselines import LLMLingua2

        text = LLMLingua2().compress(CONTEXT, "", budget, TokenCounter(tokenizer, lead))
    except Exception as e:  # import error, model download, incompatible transformers…
        return {"error": f"{type(e).__name__}: {e}", "pass": False}
    used = TokenCounter(tokenizer, lead).count(text)
    return {"budget": budget, "used_tokens": used, "text": text, "pass": bool(text) and used <= budget}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True)
    ap.add_argument("--reader-config", required=True)
    ap.add_argument("--n-layers", type=int, default=4)
    ap.add_argument("--out-dir", default="results/g0")
    ap.add_argument("--dtype", choices=list(DTYPES), default="bfloat16", help="float16 on GPUs without bf16 (T4)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    reader, tokenizer, info = load_reader(args.reader, dtype=args.dtype, return_loading_info=True)
    template = ReaderTemplate(load_reader_config(args.reader_config), tokenizer)
    writer = MemoryWriter(reader, tokenizer, n_layers=args.n_layers, ratio=4)
    model = ViLatent(reader, tokenizer, template, writer)
    prompts = [template.text_prompt("qa", CONTEXT, q) for q, _ in QUESTIONS]
    context_ids = template.context_ids("qa", CONTEXT)

    report = {"reader": args.reader, "load": check_load(reader, info),
              "template": check_template(template, reader.config.model_type),
              "embeds": check_embeds(reader, prompts[0]),
              "decode": check_decode(reader, tokenizer, prompts, model.stop_ids),
              "backward": check_backward(model, args.n_layers),
              "first_token": check_first_token(model, context_ids),
              "llmlingua2": check_llmlingua(tokenizer, template),
              "dtype": args.dtype, "embedding_norm_mean": writer.emb_norm}
    report["G0_pass"] = all(v["pass"] for v in report.values() if isinstance(v, dict) and "pass" in v)
    out = Path(args.out_dir) / (args.reader.replace("/", "_") + ".json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"G0 {'PASS' if report['G0_pass'] else 'FAIL'} -> {out}")
    sys.exit(0 if report["G0_pass"] else 1)


if __name__ == "__main__":
    main()
