#!/usr/bin/env bash
# Pha ngu canh rat dai (sau khi PREREG_LONGCTX khoa). Usage: bash run_longctx.sh <gpu> <p1|p2> [limit]
gpu=$1; set_=$2; lim=${3:-}; only=
case $lim in only_*) only=$lim; lim=;; esac
export VILATENT_MAX_CHUNKS=8 VILATENT_CHUNK_SDPA=1 CUDA_VISIBLE_DEVICES=$gpu PYTHONIOENCODING=utf-8 HF_HUB_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
cd ~/vilatent_mlqa
MEM=vilatent:runs/paper/stage2_mem/best.pt,f=1+2
PRO=vilatent:runs/paper/stage2_prompt/best.pt,f=2+8
out=results/icisn_longctx/$set_; [ -n "$lim" ] && out=results/icisn_longctx_smoke/$set_ && L="--limit $lim"
ev() {
  echo "[$(date +%F\ %T)] $out :: $*"
  .venv/bin/python scripts/evaluate.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json     --dtype float16 --data data/icisn/longctx_$set_.jsonl --ratios 4 --out-dir $out --selector runs/paper/selector     --max-batch-tokens 3000 --batch-size 4 --skip-existing $L --methods "$@" 2>&1 | grep -E "OutOfMemory|Error|Traceback"
  echo "[$(date +%F\ %T)] rc=${PIPESTATUS[0]}"
}
case $only in
  only_M) ev $MEM;;
  only_PRO) ev $PRO;;
  *) ev phobert; ev $MEM; ev $PRO;;
esac
echo QUEUE_DONE
