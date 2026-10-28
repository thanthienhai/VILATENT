"""Hub bundles (vilatent.hub): file lists, manifests and the checks of a download, without the network."""
import pytest

from vilatent.hub import build_manifest, bundle_files, check_files, conflicts


def make_tree(root):
    for path, text in {"data/tasks/viquad_gate.jsonl": "{}\n", "data/tasks/viquad_gate.jsonl.meta.json": "{}",
                       "data/tasks/viquad_long_stats.json": "{}", "data/stage1/pairs_dev.jsonl": "{}\n",
                       "data/corpus/docs.jsonl": "{}\n", "data/corpus/docs.jsonl.gz": "x",
                       "data/eval_ext/raw/MLQA_V1.zip": "x", "data/teacher/qwen/pairs_dev.pt": "t",
                       "data/qa_gen/qa_raw.jsonl": "{}\n", "runs/paper/selector/selector.json": "{}",
                       "runs/paper/selector/model.safetensors": "w", "runs/paper/stage1/best.pt": "w"}.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")


def test_bundles_hold_only_the_built_files(tmp_path):
    make_tree(tmp_path)
    assert bundle_files(tmp_path, "data") == [
        "data/corpus/docs.jsonl", "data/stage1/pairs_dev.jsonl", "data/tasks/viquad_gate.jsonl",
        "data/tasks/viquad_gate.jsonl.meta.json", "data/tasks/viquad_long_stats.json"]
    assert bundle_files(tmp_path, "teacher") == ["data/teacher/qwen/pairs_dev.pt"]
    assert bundle_files(tmp_path, "selector") == ["runs/paper/selector/model.safetensors", "runs/paper/selector/selector.json"]
    with pytest.raises(FileNotFoundError):
        bundle_files(tmp_path / "empty", "data")


def test_manifest_checks_and_conflicts(tmp_path):
    make_tree(tmp_path)
    manifest = build_manifest(tmp_path, "data")
    assert check_files(tmp_path, manifest) == [] and conflicts(tmp_path, manifest) == []
    (tmp_path / "data/stage1/pairs_dev.jsonl").unlink()  # missing: to download, not a conflict
    (tmp_path / "data/tasks/viquad_gate.jsonl").write_text("{} changed\n", encoding="utf-8")  # differs: a conflict
    assert check_files(tmp_path, manifest) == ["data/stage1/pairs_dev.jsonl", "data/tasks/viquad_gate.jsonl"]
    assert conflicts(tmp_path, manifest) == ["data/tasks/viquad_gate.jsonl"]
