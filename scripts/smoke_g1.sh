#!/usr/bin/env bash
# Smoke test of the whole G1 pipeline at toy scale (e.g. Kaggle 2× T4): every stage of
# scripts/run_g1.sh runs once on a few hundred examples and ~10 optimizer steps, so that
# crashes, shape or path errors and NaN show up before GPU time is spent on G1.
#
# The numbers it produces are NOT G0/G1 evidence: tiny data, 10 steps, fp16 on T4. G0 runs and
# its report is kept, but a G0 failure does not stop the smoke test (G0 on T4 does not count).
# qa_gen is skipped (the iCOMM endpoint is on a private network).
#
# It writes data/, runs/ and results/ like the real pipeline, so it refuses to start where
# they already exist: run it in a fresh copy of the repository.
#
# Usage (repository root, GPU machine):
#   bash scripts/smoke_g1.sh
#   SMOKE_SHORT=1 bash scripts/smoke_g1.sh   # quicker: only checks that every stage runs
set -euo pipefail

for d in data runs results; do
  if [ -e "$d" ]; then
    echo "smoke_g1: $d/ exists; run the smoke test in a fresh copy (it would overwrite real files)" >&2
    exit 1
  fi
done

# SMOKE_SHORT=1: a still smaller run (fewer documents, pairs and questions, 4 steps) and no G0,
# when the only question is whether every stage runs through.
SMOKE_SHORT=${SMOKE_SHORT:-0}
if [ "$SMOKE_SHORT" = 1 ]; then
  : "${N_WIKI:=150}" "${N_NEWS:=150}" "${N_PAIRS:=64}" "${N_DEV_PAIRS:=16}"
  : "${TRAIN_ARGS:=--steps 4 --eval-every 2 --effective-batch 4 --micro-batch 2 --dev-limit 8}"
  : "${SMOKE_TRAIN_QA:=64}" "${SMOKE_DEV_QA:=24}" "${SKIP_G0:=1}"
fi
SKIP_G0=${SKIP_G0:-0}

export DTYPE=${DTYPE:-float16}
export GPUS=${GPUS:-"0 1"}
export N_WIKI=${N_WIKI:-300} N_NEWS=${N_NEWS:-300} N_PAIRS=${N_PAIRS:-400} N_DEV_PAIRS=${N_DEV_PAIRS:-40}
export G0_READERS=${G0_READERS:-Qwen/Qwen3.5-2B}   # the 9B reader does not fit a 16 GB T4
export TRAIN_ARGS=${TRAIN_ARGS:-"--steps 10 --eval-every 5 --effective-batch 8 --micro-batch 2 --dev-limit 20"}
export EVAL_ARGS=${EVAL_ARGS:-"--batch-size 8"}
SMOKE_TRAIN_QA=${SMOKE_TRAIN_QA:-400}   # ViQuAD train questions kept
SMOKE_DEV_QA=${SMOKE_DEV_QA:-60}        # ViQuAD dev questions kept (whole passages come first in the file)
RUN="bash scripts/run_g1.sh"

log() { echo "[$(date '+%F %T')] smoke: $*"; }

$RUN data
log "shrink ViQuAD train to $SMOKE_TRAIN_QA and dev to $SMOKE_DEV_QA questions"
for f in "viquad_train_clean $SMOKE_TRAIN_QA" "viquad_dev $SMOKE_DEV_QA"; do
  set -- $f
  head -n "$2" "data/tasks/$1.jsonl" > "data/tasks/$1.small" && mv "data/tasks/$1.small" "data/tasks/$1.jsonl"
done

$RUN template
if [ "$SKIP_G0" = 1 ]; then
  log "G0 skipped"
else
  $RUN g0 || log "G0 FAILED (kept in results/g0; on T4 this does not count, continuing)"
fi
$RUN teacher stage1 stage2 eval select fallback report

log "done; G0 report(s) in results/g0, G1 pipeline output in results/g1_dev"
