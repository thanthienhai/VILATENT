#!/usr/bin/env bash
# usage: run_longctx_rest.sh <gpu> <p1|p2>: M+ME then prompt f2+f8 on one set (log logs/icisn_lc_rest_<set>.log)
cd ~/vilatent_mlqa
for c in only_M only_PRO; do bash scripts/icisn/run_longctx.sh $1 $2 $c; done > logs/icisn_lc_rest_$2.log 2>&1
echo ALL_DONE > logs/icisn_lc_rest_$2.done
