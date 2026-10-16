"""Train a writer (stage 1 or stage 2) from a YAML config; command-line values override it.

Usage:
  python scripts/train.py --config configs/g1/stage1.yaml
  python scripts/train.py --config configs/g1/stage2.yaml --init-from runs/g1_stage1_r4/best.pt
"""
import argparse

from vilatent.train import TrainConfig, train


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out-dir")
    ap.add_argument("--init-from")
    ap.add_argument("--ratio", type=int)
    ap.add_argument("--mode", choices=["M", "ME", "W5"])
    ap.add_argument("--steps", type=int)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--micro-batch", type=int)
    args = ap.parse_args()
    cfg = TrainConfig.from_yaml(args.config, out_dir=args.out_dir, init_from=args.init_from, ratio=args.ratio,
                                mode=args.mode,
                                steps=args.steps, seed=args.seed, micro_batch=args.micro_batch)
    print(train(cfg))


if __name__ == "__main__":
    main()
