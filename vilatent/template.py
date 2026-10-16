"""Fixed chat template of each reader (docs/VILATENT.md §Thiết kế thực nghiệm, conventions 1–3).

The template is rendered once per reader with ``enable_thinking=False`` and literal
placeholders, then saved to ``configs/readers/<reader>.json`` (scripts/render_template.py).
Training, the teacher logits, evaluation and every hard baseline read that file, so the text
around the context, including the empty ``<think></think>`` block that Qwen3.5 inserts in
the answer turn, is identical everywhere.

A prompt is assembled from token segments, never by tokenizing one joined string:

  [prefix ids] [context slot] [suffix ids] [target ids]

The context slot holds the memory (⟨mem⟩ m_1 … m_k ⟨/mem⟩), the full context ids (teacher,
full-context reference) or the ids of a compressed text (hard baselines). Answer tokens are
therefore the same ids for the student and the teacher.

The space after "Đoạn văn:" belongs to the context slot, not to the prefix: a text context is
tokenized as " " + context, so its first token is "ĠParis" exactly as when the whole prompt
is tokenized at once (a prefix ending in a lone "Ġ" token followed by "Paris" would show
every method an unnatural seam). ``context_ids`` is the single place where this happens;
the chunks of the writer (budget.chunk_context with ``lead``) give the same ids.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

# User-turn instructions. No system prompt for any reader (same content for every reader).
# The QA instruction is ViWord-C's, so the two projects are comparable.
TASK_PROMPTS = {
    "qa": ("Đọc đoạn văn và trả lời câu hỏi bằng một cụm từ ngắn lấy từ đoạn văn. Chỉ ghi câu trả lời.\n\n"
           "Đoạn văn: {context}\n\nCâu hỏi: {question}\n\nTrả lời:"),
    "continue": "Viết tiếp đoạn văn sau.\n\nĐoạn văn: {context}",
}
CHAT_TEMPLATE_KWARGS = {"enable_thinking": False}
# answers end with the end-of-turn token; stage-1 targets (B) are cut mid-text and do not
ADD_EOS = {"qa": True, "continue": False}


def default_sink_token(tokenizer) -> str:
    """Token prepended to every writer chunk and then dropped: BOS when the reader has one
    (Vistral), else the pad token (Qwen: <|endoftext|>)."""
    return tokenizer.bos_token or tokenizer.pad_token or tokenizer.eos_token


def render_reader_config(reader: str, tokenizer, system_prompt: str | None = None) -> dict:
    prompts = {}
    for task, content in TASK_PROMPTS.items():
        messages = ([{"role": "system", "content": system_prompt}] if system_prompt else [])
        messages.append({"role": "user", "content": content})
        rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                                 **CHAT_TEMPLATE_KWARGS)
        if rendered.count("{context}") != 1:
            raise ValueError(f"{task}: the rendered template must contain {{context}} exactly once")
        prompts[task] = rendered
    return {
        "reader": reader,
        "system_prompt": system_prompt,
        "chat_template_kwargs": CHAT_TEMPLATE_KWARGS,
        "sink_token": default_sink_token(tokenizer),
        "eos_token": tokenizer.eos_token,
        "prompts": prompts,
    }


SLOT_VERSION = 2  # 2: the space before the context is tokenized with the context


def config_hash(cfg: dict) -> str:
    """Identifies a rendered template and how its slot is tokenized: teacher logits and
    checkpoints are only valid for the same hash."""
    keys = ("reader", "system_prompt", "sink_token", "eos_token", "prompts")
    blob = json.dumps({**{k: cfg[k] for k in keys}, "slot_version": SLOT_VERSION}, ensure_ascii=False,
                      sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def load_reader_config(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class ReaderTemplate:
    def __init__(self, cfg: dict, tokenizer):
        self.cfg, self.tokenizer = cfg, tokenizer
        self.hash = config_hash(cfg)
        self.sink_id = self._single_id(cfg["sink_token"])
        self.eos_id = self._single_id(cfg["eos_token"])
        self._prefix, self.lead = {}, {}
        for task, prompt in cfg["prompts"].items():
            before = prompt.split("{context}")[0]
            stripped = before.rstrip(" ")
            self._prefix[task] = self.ids(stripped)
            self.lead[task] = before[len(stripped):]  # " " for "Đoạn văn: {context}"

    def _single_id(self, token: str) -> int:
        ids = self.ids(token)
        if len(ids) != 1:
            raise ValueError(f"{token!r} is not a single token: {ids}")
        return ids[0]

    def ids(self, text: str) -> list[int]:
        return list(self.tokenizer(text, add_special_tokens=False)["input_ids"])

    def prefix_ids(self, task: str) -> list[int]:
        return self._prefix[task]

    def suffix_ids(self, task: str, question: str = "") -> list[int]:
        suffix = self.cfg["prompts"][task].split("{context}")[1]
        return self.ids(suffix.replace("{question}", question))

    def target_ids(self, task: str, target: str) -> list[int]:
        return self.ids(target) + ([self.eos_id] if ADD_EOS[task] else [])

    def slot(self, task: str, text: str) -> str:
        """Text placed in the context slot: the leading space, then the text (nothing if empty)."""
        return self.lead[task] + text if text else ""

    def context_ids(self, task: str, text: str) -> list[int]:
        return self.ids(self.slot(task, text))

    def text_prompt(self, task: str, context: str, question: str = "") -> list[int]:
        """Prompt ids with a text context (teacher, full context, hard baselines)."""
        return self.prefix_ids(task) + self.context_ids(task, context) + self.suffix_ids(task, question)
