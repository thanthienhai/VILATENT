#!/usr/bin/env bash
# G2.1: Sum variants v1..v3 on ViQuAD select (single and Long), 4x. Usage: bash select_sum.sh <gpu> <mbt>
gpu=$1; mbt=${2:-3000}
export CUDA_VISIBLE_DEVICES=$gpu PYTHONIOENCODING=utf-8 HF_HUB_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
cd ~/vilatent_mlqa
for kind in single long; do
  data=data/tasks/viquad_select.jsonl; [ $kind = long ] && data=data/tasks/viquad_long_select.jsonl
  for v in v1 v2 v3; do
    echo "[$(date +%T)] $kind $v"
    .venv/bin/python scripts/evaluate.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
      --dtype float16 --data $data --ratios 4 --out-dir results/icisn_select/$kind --max-batch-tokens $mbt --batch-size 8 \
      --skip-existing --methods sum:$v:data/icisn/summaries/select_$v.json 2>&1 | grep -vE "it/s\]|fast path"
  done
done
echo QUEUE_DONE
