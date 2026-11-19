#!/usr/bin/env bash
# WP1 (PREREG_MORONG): memory-content controls on P1, 4x. Usage: bash run_morong.sh <gpu> [limit] -- <spec> [<spec> ...]
# spec = <f>:<mode>   with f in {1 (M), 2 (ME)} and mode in {swap, zero, shuf}. Runs sequentially, --skip-existing.
gpu=$1; shift; lim=
[ "$1" != "--" ] && { lim=$1; shift; }; shift
export VILATENT_MAX_CHUNKS=8 VILATENT_CHUNK_SDPA=1 CUDA_VISIBLE_DEVICES=$gpu PYTHONIOENCODING=utf-8 HF_HUB_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
cd ~/vilatent_mlqa; mkdir -p logs
out=results/icisn_morong/p1; L=
[ -n "$lim" ] && out=results/icisn_morong_smoke/p1 && L="--limit $lim"
for sp in "$@"; do
  f=${sp%%:*}; mode=${sp##*:}
  case $mode in swap) o="swap=0";; zero) o="zero=1";; shuf) o="shuf=0";; *) echo "bad mode $mode"; continue;; esac
  echo "[$(date +%F\ %T)] gpu$gpu f=$f $o -> $out"
  .venv/bin/python scripts/evaluate.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json --dtype float16 \
    --data data/icisn/longctx_p1.jsonl --ratios 4 --out-dir $out --max-batch-tokens 3000 --batch-size 4 --skip-existing $L \
    --methods vilatent:runs/paper/stage2_mem/best.pt,f=$f,$o > logs/icisn_morong_${f}_${mode}.log 2>&1
  echo "[$(date +%F\ %T)] gpu$gpu f=$f $mode rc=$? $(grep -aE 'OutOfMemory|Traceback' logs/icisn_morong_${f}_${mode}.log | tail -1 | cut -c1-160)"
done
echo QUEUE_DONE gpu$gpu
