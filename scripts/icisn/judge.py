"""LLM judge (ACC-LLM) following docs/icisn/PREREG_JUDGE.md. judge_v1 prompt in docs/icisn/judge_prompt.json."""
import hashlib, json, re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import llm

ROOT = Path(__file__).resolve().parents[2]
P = json.loads((ROOT / "docs/icisn/judge_prompt.json").read_text(encoding="utf-8"))
PRIMARY, SECONDARY = "DeepSeek-V4.1-Flash", "Qwen3.8-27B"


def check_lock():
    """Refuse to run if the preregistration files changed since they were hashed."""
    want = dict(l.split()[::-1] for l in (ROOT / "docs/icisn/PREREG_JUDGE.sha256").read_text().splitlines() if l.strip())
    for name in ("PREREG_JUDGE.md", "judge_prompt.json"):
        got = hashlib.sha256((ROOT / "docs/icisn" / name).read_bytes()).hexdigest()
        if want["*" + name] != got:
            raise SystemExit(f"{name} changed after the lock")


def uniq(xs):
    return list(dict.fromkeys(xs))


def messages(question, golds, pred):
    gold = "\n".join("- " + g for g in uniq(golds))
    return [{"role": "system", "content": P["system"]},
            {"role": "user", "content": P["user_template"].format(question=question, gold=gold,
                                                                   prediction=pred[:P["prediction_max_chars"]])}]


def parse(text):
    t = re.sub(r"[^A-ZĐÀ-Ỹ]", "", unicodedata.normalize("NFC", text.strip()).upper())
    if t.startswith("ĐÚNG") or t.startswith("DUNG") or t.startswith("ĐUNG"):
        return 1
    if t.startswith("SAI"):
        return 0
    return None


def rule(pred, unreadable):
    if not any(ch.isalnum() for ch in pred or ""):
        return "rule_empty"
    if unreadable:
        return "rule_unreadable"
    return None


def judge_one(cache, model, question, golds, pred):
    rec = llm.chat(cache, model, messages(question, golds, pred), max_tokens=P["max_tokens"], temperature=P["temperature"])
    return parse(rec["content"]), rec["content"]
