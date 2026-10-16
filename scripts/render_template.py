"""Render the reader's chat template once and save it (docs/VILATENT.md §Thiết kế thực nghiệm,
convention 2). Prints the rendered prompts so the inserted answer-turn text (for Qwen3.5 an
empty ``<think></think>`` block) can be checked by eye; the model card does not document it.

Usage:
  python scripts/render_template.py --reader Qwen/Qwen3.5-2B --out configs/readers/qwen3.5-2b.json
"""
import argparse
import json
import sys
from pathlib import Path

from vilatent.template import config_hash, render_reader_config


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    from transformers import AutoTokenizer

    sys.stdout.reconfigure(encoding="utf-8")
    tokenizer = AutoTokenizer.from_pretrained(args.reader)
    cfg = render_reader_config(args.reader, tokenizer)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    for task, prompt in cfg["prompts"].items():
        print("=" * 30, task, "=" * 30)
        print(prompt)
        print("answer turn starts with:", repr(prompt.split("{context}")[1][-40:]))
    print(f"sink={cfg['sink_token']!r} eos={cfg['eos_token']!r} hash={config_hash(cfg)} -> {args.out}")


if __name__ == "__main__":
    main()
