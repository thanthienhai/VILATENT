#!/usr/bin/env bash
# Waits for >= 9500 MiB free on the GPU (it is shared with other jobs), runs the missing conditions, retries on OOM.
gpu=$1
cd ~/vilatent_mlqa
free() { nvidia-smi -i $gpu --query-gpu=memory.free --format=csv,noheader,nounits; }
for s in p2 p1; do
  for cond in M PRO; do
    if [ $cond = M ]; then chk=vilatent_me_f2_r4.jsonl; else chk=prompt_bm25_f8_r4.jsonl; fi
    n=0
    while [ ! -s results/icisn_longctx/$s/$chk ] && [ $n -lt 60 ]; do
      until [ "$(free)" -ge 9500 ]; do sleep 120; done
      n=$((n+1)); echo "[$(date +%F\ %T)] $s $cond attempt $n free=$(free)"
      bash scripts/icisn/run_longctx.sh $gpu $s only_$cond 2>&1 | tail -3
    done
  done
done
echo ALL_DONE > logs/icisn_lc_retry.done
