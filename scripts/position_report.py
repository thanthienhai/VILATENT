"""F1 by the position of the answer's passage within the article, on ViQuAD-Long (checklist A25/B16).

Every ViQuAD-Long row carries ``position``: the third of the article (beginning, middle, end) that
holds the question's passage (vilatent.data.position_bin, on passage index / passage count). For
every method of --results-dir at --ratio (and the full / no-context references) this prints and
writes the question count and the mean F1 of each third.

Usage:
  python scripts/position_report.py --results-dir results/paper/test/long --ratio 4
"""
import argparse
import json
from pathlib import Path

from vilatent.data import read_jsonl

BINS = ("beginning", "middle", "end")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--ratio", type=int, default=4)
    args = ap.parse_args()

    d, r = Path(args.results_dir), args.ratio
    paths = sorted(d.glob(f"*_r{r}.jsonl")) + [d / m for m in ("full.jsonl", "none.jsonl") if (d / m).exists()]
    report = {"ratio": r, "bins": "third of the article holding the answer passage", "methods": {}}
    for path in paths:
        rows = read_jsonl(path)
        if "position" not in rows[0]:
            raise SystemExit(f"{path}: rows have no position (not a ViQuAD-Long file?)")
        out = {}
        for b in BINS:
            sel = [x for x in rows if x["position"] == b]
            out[b] = {"n": len(sel), "f1": 100 * sum(x["f1"] for x in sel) / len(sel) if sel else None}
        report["methods"][rows[0]["method"]] = out
        print(f"{rows[0]['method']:<28}" + "  ".join(
            f"{b} {out[b]['f1']:.1f} (n={out[b]['n']})" if out[b]["f1"] is not None else f"{b} -" for b in BINS))
    (d / f"positions_r{r}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
