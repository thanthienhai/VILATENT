#!/usr/bin/env bash
# Smoke test of the whole paper pipeline at toy scale (Kaggle 2x T4, fp16; checklist B1, B2): every
# stage of scripts/run_paper.sh runs once on ~50 training questions, a few dozen evaluation questions
# and ~16 optimizer steps, so that crashes, shape or path errors and NaN show up before H100 time is
# spent. The numbers it produces are NOT results (tiny data, 16 steps, fp16 on T4).
#
# It writes data/, runs/, results/ and configs/bm25.json like the real pipeline, so it refuses to start
# where data/, runs/ or results/ already exist: run it in a fresh copy of the repository.
#
# Usage (repository root, GPU machine):
#   bash scripts/smoke_paper.sh
#   SMOKE_G0=1 bash scripts/smoke_paper.sh   # also the G0 kernel check on the T4 (B1)
set -euo pipefail

for d in data runs results; do
  if [ -e "$d" ]; then
    echo "smoke_paper: $d/ exists; run the smoke test in a fresh copy (it would overwrite real files)" >&2
    exit 1
  fi
done

export DTYPE=${DTYPE:-float16}
export GPUS=${GPUS:-"0 1"}
export N_WIKI=${N_WIKI:-150} N_NEWS=${N_NEWS:-150} N_PAIRS=${N_PAIRS:-64} N_DEV_PAIRS=${N_DEV_PAIRS:-16}
export QUANT=${QUANT:-none}
# 16 steps: in fp16 the GradScaler skips the first ~9 (overflow at its initial scale), and training
# fails when no step updated the writer
export TRAIN_ARGS=${TRAIN_ARGS:-"--steps 16 --eval-every 8 --effective-batch 4 --micro-batch 2 --dev-limit 8"}
export EVAL_ARGS=${EVAL_ARGS:-"--batch-size 8 --max-batch-tokens 12000"}
export SELECTOR_ARGS=${SELECTOR_ARGS:-"--limit 50 --epochs 1 --eval-every 20"}
export LATENCY_ARGS=${LATENCY_ARGS:-"--docs 2 --questions-per-doc 2"}
SMOKE_TRAIN_QA=${SMOKE_TRAIN_QA:-50}   # ViQuAD train questions kept (and their multi-passage windows)
SMOKE_DEV_QA=${SMOKE_DEV_QA:-30}       # questions kept in each of gate, select and test (both settings)
SMOKE_G0=${SMOKE_G0:-0}
RUN="bash scripts/run_paper.sh"

log() { echo "[$(date '+%F %T')] smoke: $*"; }

$RUN data
log "shrink ViQuAD train to $SMOKE_TRAIN_QA and gate, select, test to $SMOKE_DEV_QA questions (both settings)"
# every k-th row, so that the small files keep several articles (swapped memory and the article
# bootstrap need more than one); the multi-passage and Long files keep the rows of the same questions
keep() {  # file, n: keep every k-th row of data/tasks/<file>.jsonl, at most n rows
  local f=data/tasks/$1.jsonl step
  step=$(( ($(wc -l < "$f") + $2 - 1) / $2 ))
  awk -v s="$step" '(NR - 1) % s == 0' "$f" | head -n "$2" > "$f.small" && mv "$f.small" "$f"
}
same_ids() {  # file, reference: keep the rows of data/tasks/<file>.jsonl whose id (without "multi-") is in the reference
  python - "$1" "$2" <<'PY'
import json, sys
ref = {json.loads(l)["id"] for l in open(f"data/tasks/{sys.argv[2]}.jsonl", encoding="utf-8")}
path = f"data/tasks/{sys.argv[1]}.jsonl"
rows = [l for l in open(path, encoding="utf-8") if json.loads(l)["id"].removeprefix("multi-") in ref]
open(path, "w", encoding="utf-8").writelines(rows)
PY
}
keep viquad_train_clean "$SMOKE_TRAIN_QA"
same_ids viquad_train_multi viquad_train_clean
for split in gate select test; do
  keep "viquad_$split" "$SMOKE_DEV_QA"
  same_ids "viquad_long_$split" "viquad_$split"
done
same_ids viquad_select_multi viquad_select

$RUN template
if [ "$SMOKE_G0" = 1 ]; then
  $RUN g0 || log "G0 FAILED (kept in results/g0; on T4 this does not count, continuing)"
fi
$RUN tune_bm25 selector aie teacher stage1 stage2 stage2_q baselines eval_select choose eval_gate decide test figures
log "done; results in results/paper (decision: results/paper/gate/decision.json), figures in paper/figures/curves.tex"
