#!/usr/bin/env bash
# P1 then P2 sequentially on one GPU (1080 Ti has too little memory for two jobs at 64k).
bash scripts/icisn/run_longctx.sh $1 p1 > logs/icisn_lc_p1c.log 2>&1
bash scripts/icisn/run_longctx.sh $1 p2 > logs/icisn_lc_p2c.log 2>&1
echo ALL_DONE > logs/icisn_lc_all.done
