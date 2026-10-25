"""Changes of the review of 22/10/2026: article split, leak index, BM25 parameters, p-value."""
import random

import numpy as np
import pytest

from vilatent.baselines import build_baseline, load_bm25_params
from vilatent.data import split_viquad_train
from vilatent.leak import LeakIndex
from vilatent.stats import paired_test


def rows_of_articles(sizes: dict[str, int], per_passage: int = 2) -> list[dict]:
    rows = []
    for title, n in sizes.items():
        for i in range(n):
            rows.append({"id": f"{title}-{i}", "title": title, "cluster": f"{title}-p{i // per_passage}",
                         "context": f"{title} {i // per_passage}", "question": "?", "answers": ["x"]})
    return rows


def test_split_is_by_article_and_keeps_the_viwordc_sample():
    sizes = {f"a{i}": n for i, n in enumerate([6, 8, 10, 4, 12, 40, 6, 8, 10, 6])}
    rows = rows_of_articles(sizes)
    splits, held = split_viquad_train(rows, n_viwordc_passages=5, gate_questions=14, select_questions=8,
                                      max_article_questions=20, seed=0)
    titles = {name: {r["title"] for r in rs} for name, rs in splits.items()}
    assert not titles["gate"] & titles["train"] and not titles["select"] & titles["train"]
    assert not titles["gate"] & titles["select"] and "a5" not in titles["gate"] | titles["select"]  # 40 > 20
    assert len(splits["gate"]) >= 14 and len(splits["select"]) >= 8
    # ViWord-C's dev: the same passage sample as before the change, kept out of train
    passages = sorted({r["cluster"] for r in rows})
    expected = set(random.Random(0).sample(passages, 5))
    assert {r["cluster"] for r in splits["viwordc_dev"]} == expected
    assert not {r["cluster"] for r in splits["train"]} & expected
    assert sorted(held["gate"]) == sorted(titles["gate"])


def test_leak_index_finds_13_syllable_overlaps():
    evaluation = "một hai ba bốn năm sáu bảy tám chín mười mười một mười hai mười ba mười bốn"
    index = LeakIndex([evaluation])
    assert index.leaks("trước đó " + " ".join(evaluation.split()[2:15]) + " sau đó")
    assert not index.leaks(" ".join(evaluation.split()[:12]))  # 12 syllables: no 13-gram in common
    with pytest.raises(ValueError):
        LeakIndex(["quá ngắn"])


def test_bm25_baseline_needs_its_tuned_parameters(tmp_path):
    with pytest.raises(ValueError):
        build_baseline("bm25")
    path = tmp_path / "bm25.json"
    path.write_text('{"k1": 0.9, "b": 0.3, "grid": []}', encoding="utf-8")
    params = load_bm25_params(path)
    selector = build_baseline("bm25", bm25=params)
    # a file without units was tuned on syllables (G1); the paper re-tunes on pyvi words
    assert params == {"k1": 0.9, "b": 0.3, "units": "syllable"} and (selector.k1, selector.b) == (0.9, 0.3)
    path.write_text('{"k1": 1.2, "b": 0.5, "units": "word"}', encoding="utf-8")
    assert build_baseline("bm25", bm25=load_bm25_params(path)).units == "word"


def test_one_sided_p_value_is_centred_on_the_null():
    rng = np.random.default_rng(0)
    clusters = [f"p{i // 4}" for i in range(400)]
    noise = rng.normal(0.0, 1.0, 400)
    big = paired_test(noise + 1.0, np.zeros(400), clusters, n_boot=2000)
    null = paired_test(noise - noise.mean(), np.zeros(400), clusters, n_boot=2000)
    assert big["p_one_sided"] < 0.01
    assert 0.3 < null["p_one_sided"] < 0.7
