#!/usr/bin/env bash
# Phase 4 (after PREREG_CONFIRM is locked). Usage: bash run_confirm.sh <gpu> <queue: q0|q1>
# q0: XQuAD-vi 4x (single, Long) then ViQuAD-Long test extras. q1: ViQuAD single test extras + prompt at its best f.
# Resumable (--skip-existing). Logs in logs/icisn_confirm_<queue>.log.
gpu=$1; q=$2
export CUDA_VISIBLE_DEVICES=$gpu PYTHONIOENCODING=utf-8 HF_HUB_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
cd ~/vilatent_mlqa
SUM=data/icisn/summaries
ev() { # data out ratios methods...
  data=$1; out=$2; ratios=$3; shift 3
  echo "[$(date +%F\ %T)] $out r=$ratios :: $*"
  .venv/bin/python scripts/evaluate.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
    --dtype float16 --data $data --ratios $ratios --out-dir $out --selector runs/paper/selector \
    --max-batch-tokens 3000 --batch-size 4 --skip-existing --methods "$@" 2>&1 | grep -E "OutOfMemory|Error|Traceback"
  echo "[$(date +%F\ %T)] rc=${PIPESTATUS[0]}"
}
MEM=vilatent:runs/paper/stage2_mem/best.pt,f=1+2
PRO=vilatent:runs/paper/stage2_prompt/best.pt,f=2+8
if [ $q = q0 ]; then
  for s in single long; do
    d=data/icisn/xquad_vi_$s.jsonl; o=results/icisn_xquad/$s
    ev $d $o 4 full none truncation lead bm25 bm25_x2 phobert llmlingua2 bgem3
    ev $d $o 4 sum:v1:$SUM/final_xquad_v1.json sumE:v1:$SUM/final_xquad_v1.json,f=2
    ev $d $o 4 $MEM $PRO
  done
  ev data/tasks/viquad_long_test.jsonl results/icisn_test/long "4 8 16" bgem3 sum:v1:$SUM/final_viquad_test_v1.json sumE:v1:$SUM/final_viquad_test_v1.json,f=2
else
  for r in 4 8 16; do
    ev data/tasks/viquad_test.jsonl results/icisn_test/single $r bgem3 sum:v1:$SUM/final_viquad_test_v1.json sumE:v1:$SUM/final_viquad_test_v1.json,f=2
  done
  ev data/tasks/viquad_test.jsonl results/icisn_test/single 4 vilatent:runs/paper/stage2_prompt/best.pt,f=8
  ev data/tasks/viquad_test.jsonl results/icisn_test/single 8 vilatent:runs/paper/stage2_prompt/best.pt,f=4
fi
echo QUEUE_DONE
