"""Choose among finished stage-2 runs by their lowest dev loss (CE + λ·KL on ViQuAD select).

G1 uses it twice, before any evaluation:
  * the ME memory factor f ∈ {2, 4, 8} (same answers and same teacher, so the losses compare);
  * the learning rate of the learned-prompt control (1e-4 or 1e-3, at f*).
Neither uses an F1, and the select split is disjoint from the gate split, so the gate (F1 on
ViQuAD gate) is not biased by these choices. Ties go to the first candidate.

Usage:
  python scripts/choose_by_loss.py --key memory_factor --out results/g1/me_choice_r4.json \
      2=runs/g1_stage2_me_f2_r4 4=runs/g1_stage2_me_f4_r4 8=runs/g1_stage2_me_f8_r4
"""
import argparse
import json
from pathlib import Path

from vilatent.train import choose_by_dev_loss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True, help="name of the chosen value in the output JSON")
    ap.add_argument("--out", required=True)
    ap.add_argument("candidates", nargs="+", help="value=run_dir, in order of preference for ties")
    args = ap.parse_args()

    runs = dict(c.split("=", 1) for c in args.candidates)
    chosen, losses = choose_by_dev_loss(runs)
    choice = {args.key: chosen, "run": runs[chosen], "dev_loss": losses,
              "criterion": "lowest stage-2 dev loss (CE + lambda*KL) on ViQuAD select", "runs": runs}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(choice, indent=2), encoding="utf-8")
    print(json.dumps(choice, indent=2))


if __name__ == "__main__":
    main()
