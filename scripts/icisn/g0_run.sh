#!/usr/bin/env bash
# G0.2/0.3: re-run M and ME(f=2) at 4x on 200 first test questions (fp16, GTX 1080 Ti). Usage: bash g0_run.sh <gpu> <mbt>
gpu=$1; mbt=${2:-3000}
export CUDA_VISIBLE_DEVICES=$gpu PYTHONIOENCODING=utf-8 HF_HUB_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
cd ~/vilatent_mlqa
for kind in ${KINDS:-single long}; do
  data=data/icisn_g0/viquad_${kind/single/}test200.jsonl; [ $kind = long ] && data=data/icisn_g0/viquad_long_test200.jsonl
  [ $kind = single ] && data=data/icisn_g0/viquad_test200.jsonl
  echo "[$(date +%T)] $kind start"
  .venv/bin/python scripts/icisn/g0_wrap.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
    --dtype float16 --data $data --ratios 4 --out-dir results/icisn_g0/$kind --selector runs/paper/selector \
    --max-batch-tokens $mbt --batch-size ${BS:-8} --skip-existing --methods vilatent:runs/paper/stage2_mem/best.pt,f=1+2 2>&1 | grep -vE "it/s\]|fast path"
  echo "[$(date +%T)] $kind done"
done
echo QUEUE_DONE
