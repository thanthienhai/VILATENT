"""OpenAI-compatible LLM client for the ICISN study: many threads, sqlite cache, model chosen per call.

It reuses the credentials loader of the pilot client (vi-pilot/llm_client.py, which reads its own .env);
this file never reads, prints or copies the key. Cache key = (model, messages, max_tokens, temperature, extra_body).
"""
import hashlib, importlib.util, json, random, sqlite3, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PILOT = "C:/Users/PC/Coding/some-research/llm/context-compress/context-research/vi-pilot/llm_client.py"
EXTRA = {  # thinking OFF, per model family (checked 2026-11-07: 4 completion tokens, no reasoning tokens)
    "DeepSeek-V4.1-Flash": {"chat_template_kwargs": {"thinking": False}},
    "Qwen3.8-27B": {"chat_template_kwargs": {"enable_thinking": False}},
}
_client = None
_lock = threading.Lock()


def client():
    global _client
    if _client is None:
        sp = importlib.util.spec_from_file_location("pilot_llm_client", PILOT)
        m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
        _client = m._client()
    return _client


class Cache:
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False, timeout=60)
        self.db.execute("create table if not exists c (k text primary key, v text)")
        self.db.commit()

    def get(self, k):
        with _lock:
            r = self.db.execute("select v from c where k=?", (k,)).fetchone()
        return json.loads(r[0]) if r else None

    def put(self, k, v):
        with _lock:
            self.db.execute("insert or replace into c values (?,?)", (k, json.dumps(v, ensure_ascii=False)))
            self.db.commit()


RPM = {"DeepSeek-V4.1-Flash": 140, "Qwen3.8-27B": 90}  # provider limits: 150 / 100 requests per minute (observed 2026-11-07)
_next = {}


def _throttle(model):
    with _lock:
        now = time.time(); t = max(_next.get(model, 0), now); _next[model] = t + 60.0 / RPM[model]
    if t > now: time.sleep(t - now)


STATS = {"live": 0, "cached": 0, "failures": 0, "prompt_tokens": 0, "completion_tokens": 0}


def chat(cache, model, messages, max_tokens=8, temperature=0.0, retries=6):
    extra = EXTRA[model]
    k = hashlib.sha256(json.dumps([model, messages, max_tokens, temperature, extra], ensure_ascii=False,
                                  sort_keys=True).encode()).hexdigest()
    hit = cache.get(k)
    if hit is not None:
        with _lock: STATS["cached"] += 1
        return hit
    err = None
    for a in range(retries):
        try:
            _throttle(model)
            r = client().chat.completions.create(model=model, messages=messages, max_tokens=max_tokens,
                                                 temperature=temperature, extra_body=extra)
            rec = {"content": r.choices[0].message.content or "", "finish": r.choices[0].finish_reason,
                   "model_returned": getattr(r, "model", None)}
            with _lock:
                STATS["live"] += 1
                STATS["prompt_tokens"] += r.usage.prompt_tokens or 0
                STATS["completion_tokens"] += r.usage.completion_tokens or 0
            cache.put(k, rec)
            return rec
        except Exception as e:  # rate limit, 5xx, timeouts: back off and retry
            err = e
            time.sleep(61 if "429" in str(e) else min(60, 2 ** a) + random.random())
    with _lock: STATS["failures"] += 1
    raise RuntimeError(f"LLM call failed: {type(err).__name__}: {str(err)[:200]}")


def map_threads(fn, items, workers=24):
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(fn, items))
