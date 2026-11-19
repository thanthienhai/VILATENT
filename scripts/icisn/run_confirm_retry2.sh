#!/usr/bin/env bash
# Usage: bash run_confirm_retry2.sh <gpu> <a|s0|s1>   a: XQuAD-Long text conditions; s0/s1: shard of ViQuAD-Long test (sum, sumE, bgem3)
gpu=$1; q=$2
export CUDA_VISIBLE_DEVICES=$gpu PYTHONIOENCODING=utf-8 HF_HUB_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
cd ~/vilatent_mlqa
SUM=data/icisn/summaries
ev() { data=$1; out=$2; ratios=$3; bs=$4; shift 4
  echo "[$(date +%F\ %T)] $out r=$ratios bs=$bs :: $*"
  .venv/bin/python scripts/evaluate.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
    --dtype float16 --data $data --ratios $ratios --out-dir $out --selector runs/paper/selector \
    --max-batch-tokens 2000 --batch-size $bs --skip-existing --methods "$@" 2>&1 | grep -E "OutOfMemory|Error|Traceback"
  echo "[$(date +%F\ %T)] rc=${PIPESTATUS[0]}"; }
if [ $q = a ]; then
  while pgrep -f "methods llmlingua2" >/dev/null; do sleep 20; done
  L=data/icisn/xquad_vi_long.jsonl
  for m in bm25 bm25_x2 truncation lead none phobert bgem3 llmlingua2 full; do ev $L results/icisn_xquad/long 4 1 $m; done
else
  T=data/icisn/viquad_long_test_$q.jsonl
  for m in sum:v1:$SUM/final_viquad_test_v1.json sumE:v1:$SUM/final_viquad_test_v1.json,f=2 bgem3; do ev $T results/icisn_test/long_$q "4 8 16" 1 $m; done
fi
echo QUEUE_DONE
