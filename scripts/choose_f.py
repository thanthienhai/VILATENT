"""Choose the memory factor f* of ViLatent-ME on ViQuAD select (decision of 25/10/2026).

With the multi-rate writer, f is an inference-time choice of one checkpoint. For every setting
(long, single) and budget ratio r, f* is the f ≥ 2 with the highest select F1 among the
evaluated ``vilatent_me_f<f>_r<r>`` (ties: the smaller f, i.e. more memory). The frozen-writer
baseline gets its own f* the same way (``frozen_me_f<f>``); the learned-prompt control is read at
ME's f*, since it must differ from ME only in the memory content. select is article-disjoint
from gate and test, so neither the decision rule nor the test table is biased by the choice.

scripts/cascade_report.py --choose then adds the cascade thresholds τ to the same file.

Usage:
  python scripts/choose_f.py --select-dir results/paper/select --out results/paper/select/choices.json
"""
import argparse
import json
import re
from pathlib import Path


def best_factor(d: Path, prefix: str, ratio: int) -> dict | None:
    f1 = {}
    for path in d.glob(f"{prefix}_f*_r{ratio}.summary.json"):
        match = re.fullmatch(rf"{prefix}_f(\d+)_r{ratio}\.summary\.json", path.name)
        if match:
            f1[int(match.group(1))] = json.loads(path.read_text(encoding="utf-8"))["f1"]
    if not f1:
        return None
    best = max(sorted(f1), key=lambda f: f1[f])  # max keeps the first (smallest f) of equal values
    return {"f_star": best, "select_f1": {str(f): f1[f] for f in sorted(f1)}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--select-dir", required=True)
    ap.add_argument("--settings", nargs="+", default=["long", "single"])
    ap.add_argument("--ratios", type=int, nargs="+", default=[4, 8, 16])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    choices = {"criterion": "highest select F1 among f >= 2 (ties: smaller f)", "settings": {}}
    for setting in args.settings:
        d = Path(args.select_dir) / setting
        for r in args.ratios:
            me = best_factor(d, "vilatent_me", r)
            if me is None:
                raise SystemExit(f"no vilatent_me_f*_r{r}.summary.json in {d}")
            frozen = best_factor(d, "frozen_me", r)
            choices["settings"].setdefault(setting, {})[str(r)] = {
                **me, "frozen_f_star": frozen["f_star"] if frozen else None,
                "frozen_select_f1": frozen["select_f1"] if frozen else None}
            print(f"{setting} r={r}: f* = {me['f_star']} (select F1 {me['select_f1']})"
                  + (f", frozen f* = {frozen['f_star']}" if frozen else ""))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(choices, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
