"""Choose the ME memory factor f ∈ {2, 4, 8} by dev loss and expose it as ``vilatent_me``.

The three stage-2 ME runs are compared by their lowest dev loss (CE + λ·KL on ViQuAD dev),
the same criterion that picks checkpoints. Their dev F1 is not used, so the G1 gate, which is
measured on dev F1, is not biased by the choice. The rows of the chosen run are copied to
``vilatent_me_r<r>.jsonl`` (the name g1_report.py gates on and fallback_report.py reads); the
rows of all three stay in the folder and are reported.

Usage:
  python scripts/select_me.py --ratio 4 --results-dir results/g1_dev
"""
import argparse
import json
import shutil
from pathlib import Path

from vilatent.train import choose_by_dev_loss

FACTORS = (2, 4, 8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratio", type=int, default=4)
    ap.add_argument("--runs", default="runs/g1_stage2_me_f{f}_r{r}", help="run folder pattern")
    ap.add_argument("--results-dir", required=True)
    args = ap.parse_args()

    runs = {f: args.runs.format(f=f, r=args.ratio) for f in FACTORS}
    chosen, losses = choose_by_dev_loss(runs)
    d = Path(args.results_dir)
    src = d / f"vilatent_me_f{chosen}_r{args.ratio}"
    for ext in (".jsonl", ".summary.json"):
        shutil.copyfile(f"{src}{ext}", d / f"vilatent_me_r{args.ratio}{ext}")
    choice = {"memory_factor": chosen, "memory_ratio": chosen * args.ratio, "dev_loss": losses,
              "criterion": "lowest stage-2 dev loss (CE + lambda*KL)", "runs": runs}
    (d / f"me_choice_r{args.ratio}.json").write_text(json.dumps(choice, indent=2), encoding="utf-8")
    print(json.dumps(choice, indent=2))


if __name__ == "__main__":
    main()
