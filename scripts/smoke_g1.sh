#!/usr/bin/env bash
# Smoke test of the whole G1 pipeline at toy scale (e.g. Kaggle 2× T4): every stage of
# scripts/run_g1.sh runs once on a few hundred examples and ~20 optimizer steps, so that
# crashes, shape or path errors and NaN show up before GPU time is spent on G1.
#
# The numbers it produces are NOT G0/G1 evidence: tiny data, 20 steps, fp16 on T4. G0 runs and
# its report is kept, but a G0 failure does not stop the smoke test (G0 on T4 does not count).
# qa_generate is skipped (the iCOMM endpoint is on a private network). With SMOKE_QA=1, the
# auto-generated QA is fetched from the Hub (qa_download, needs an HF_TOKEN that can read the
# private QA_REPO) and its first SMOKE_QA_ROWS rows go through qa_filter; G1 does not use them.
#
# It writes data/, runs/ and results/ like the real pipeline, so it refuses to start where
# they already exist: run it in a fresh copy of the repository.
#
# Usage (repository root, GPU machine):
#   bash scripts/smoke_g1.sh
#   SMOKE_SHORT=1 bash scripts/smoke_g1.sh   # quicker: only checks that every stage runs
#   QUANT=int4 SMOKE_9B=1 bash scripts/smoke_g1.sh   # int4 readers, plus G0 on the 9B (T4)
#   SMOKE_QA=1 HF_TOKEN=... bash scripts/smoke_g1.sh # also qa_download + qa_filter
set -euo pipefail

for d in data runs results; do
  if [ -e "$d" ]; then
    echo "smoke_g1: $d/ exists; run the smoke test in a fresh copy (it would overwrite real files)" >&2
    exit 1
  fi
done

# SMOKE_SHORT=1: a still smaller run (fewer documents, pairs and questions, 16 steps) and no G0,
# when the only question is whether every stage runs through.
SMOKE_SHORT=${SMOKE_SHORT:-0}
if [ "$SMOKE_SHORT" = 1 ]; then
  : "${N_WIKI:=150}" "${N_NEWS:=150}" "${N_PAIRS:=64}" "${N_DEV_PAIRS:=16}"
  # 16 steps: in fp16 the GradScaler skips the first ~9 (overflow at its initial scale), and
  # training fails when no step updated the writer
  : "${TRAIN_ARGS:=--steps 16 --eval-every 8 --effective-batch 4 --micro-batch 2 --dev-limit 8}"
  : "${SMOKE_TRAIN_QA:=64}" "${SMOKE_DEV_QA:=40}" "${SKIP_G0:=1}"
fi
SKIP_G0=${SKIP_G0:-0}

export DTYPE=${DTYPE:-float16}
export GPUS=${GPUS:-"0 1"}
export N_WIKI=${N_WIKI:-300} N_NEWS=${N_NEWS:-300} N_PAIRS=${N_PAIRS:-400} N_DEV_PAIRS=${N_DEV_PAIRS:-40}
export QUANT=${QUANT:-none}   # int4 (bitsandbytes) makes the readers lighter; the 9B fits a T4 only in int4
export G0_READERS=${G0_READERS:-Qwen/Qwen3.5-2B}   # the 9B reader does not fit a 16 GB T4 in fp16
# SMOKE_9B=1 (with QUANT=int4): also G0 on the 9B, without the writer-layer gradients (with them
# one forward + backward does not fit a 16 GB T4 even in int4)
SMOKE_9B=${SMOKE_9B:-0}
export TRAIN_ARGS=${TRAIN_ARGS:-"--steps 20 --eval-every 10 --effective-batch 8 --micro-batch 2 --dev-limit 20"}
export EVAL_ARGS=${EVAL_ARGS:-"--batch-size 8"}
SMOKE_TRAIN_QA=${SMOKE_TRAIN_QA:-400}   # ViQuAD train questions kept
SMOKE_DEV_QA=${SMOKE_DEV_QA:-60}        # questions kept in each of gate, select and ViWord-C dev
SMOKE_QA=${SMOKE_QA:-0}
SMOKE_QA_ROWS=${SMOKE_QA_ROWS:-500}     # auto-generated questions sent through qa_filter
RUN="bash scripts/run_g1.sh"

log() { echo "[$(date '+%F %T')] smoke: $*"; }

$RUN data
log "shrink ViQuAD train to $SMOKE_TRAIN_QA and gate, select, ViWord-C dev to $SMOKE_DEV_QA questions"
# every k-th row, so that the small files keep several articles (swapped memory and the
# article-cluster bootstrap need more than one)
for f in "viquad_train_clean $SMOKE_TRAIN_QA" "viquad_gate $SMOKE_DEV_QA" "viquad_select $SMOKE_DEV_QA" \
         "viquad_viwordc_dev $SMOKE_DEV_QA"; do
  set -- $f
  step=$(( ($(wc -l < "data/tasks/$1.jsonl") + $2 - 1) / $2 ))
  awk -v s="$step" '(NR - 1) % s == 0' "data/tasks/$1.jsonl" | head -n "$2" > "data/tasks/$1.small"
  mv "data/tasks/$1.small" "data/tasks/$1.jsonl"
done

$RUN template
if [ "$SKIP_G0" = 1 ]; then
  log "G0 skipped"
else
  $RUN g0 || log "G0 FAILED (kept in results/g0; on T4 this does not count, continuing)"
  if [ "$SMOKE_9B" = 1 ]; then
    G0_READERS=Qwen/Qwen3.5-9B G0_ARGS=--no-writer-layer-grad $RUN g0 || log "G0 9B FAILED (continuing)"
  fi
fi
$RUN teacher stage1 stage2 select stage2b eval fallback report
if [ "$SMOKE_QA" = 1 ]; then
  $RUN qa_download
  log "shrink the auto-generated QA to its first $SMOKE_QA_ROWS rows"
  head -n "$SMOKE_QA_ROWS" data/qa_gen/qa_raw.jsonl > data/qa_gen/qa_raw.small && mv data/qa_gen/qa_raw.small data/qa_gen/qa_raw.jsonl
  $RUN qa_filter
else
  log "qa_download and qa_filter skipped (SMOKE_QA=1 runs them)"
fi

log "done; G0 report(s) in results/g0, G1 pipeline output in results/g1, filtered QA in data/qa_gen"
