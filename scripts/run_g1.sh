#!/usr/bin/env bash
# G0 + G1 pipeline, one stage at a time (docs/RUN_G0_G1.md):
#   bash scripts/run_g1.sh data template g0          # week 1–2
#   bash scripts/run_g1.sh qa_gen                     # background job (teacher endpoint)
#   bash scripts/run_g1.sh teacher stage1 stage2 eval select fallback report   # week 3
# Each stage reads only the files written by the previous ones.
set -euo pipefail

READER=${READER:-Qwen/Qwen3.5-2B}
READER_9B=${READER_9B:-Qwen/Qwen3.5-9B}
SLUG=${SLUG:-qwen3.5-2b}
RATIO=${RATIO:-4}
TEACHER_URL=${TEACHER_URL:-http://172.16.9.11:30048/v1}
TEACHER_MODEL=${TEACHER_MODEL:-icmodel/icom-model-llm-ic-v3.8-27b}
N_PAIRS=${N_PAIRS:-96000}
EVAL_FILES="data/tasks/viquad_dev.jsonl data/tasks/viquad_test.jsonl"
CFG=configs/readers/$SLUG.json
TEACHER_DIR=data/teacher/$SLUG
export PYTHONIOENCODING=utf-8

log() { echo "[$(date '+%F %T')] $*"; }

stage_data() {
  log "ViQuAD 2.0 (ViWord-C split) and leak-filtered train"
  python scripts/prepare_viquad.py --out-dir data/tasks
  python scripts/leak_filter.py --input data/tasks/viquad_train.jsonl --eval-files $EVAL_FILES \
    --out data/tasks/viquad_train_clean.jsonl
  log "stage-1 corpus (Wikipedia + BKAINewsCorpus) and (A, B) pairs"
  python scripts/build_corpus.py --eval-files $EVAL_FILES --out data/corpus/docs.jsonl
  python scripts/make_pairs.py --docs data/corpus/docs.jsonl --reader "$READER" --n-train "$N_PAIRS" \
    --out-dir data/stage1
}

stage_template() {
  log "render the fixed chat templates"
  python scripts/render_template.py --reader "$READER" --out "$CFG"
  python scripts/render_template.py --reader "$READER_9B" --out configs/readers/qwen3.5-9b.json
}

stage_g0() {
  log "G0 on $READER and $READER_9B"
  python scripts/g0_check.py --reader "$READER" --reader-config "$CFG"
  python scripts/g0_check.py --reader "$READER_9B" --reader-config configs/readers/qwen3.5-9b.json
}

stage_qa_gen() {
  log "auto-generated QA with the teacher, then the two-way check with $READER"
  python scripts/generate_qa.py --docs data/corpus/docs.jsonl --base-url "$TEACHER_URL" --model "$TEACHER_MODEL" \
    --out data/qa_gen/qa_raw.jsonl
  python scripts/filter_qa.py --input data/qa_gen/qa_raw.jsonl --reader "$READER" --reader-config "$CFG" \
    --eval-files $EVAL_FILES --out data/qa_gen/qa_clean.jsonl
}

stage_teacher() {
  for pair in "data/stage1/pairs_train.jsonl continue pairs_train" "data/stage1/pairs_dev.jsonl continue pairs_dev" \
              "data/tasks/viquad_train_clean.jsonl qa viquad_train" "data/tasks/viquad_dev.jsonl qa viquad_dev"; do
    set -- $pair
    log "teacher logits: $1"
    python scripts/precompute_teacher.py --reader "$READER" --reader-config "$CFG" --data "$1" --task "$2" \
      --out "$TEACHER_DIR/$3.pt"
  done
}

# Stage-1 writers: 4x (ViLatent-M, W5) and 8x/16x/32x (ViLatent-ME with f = 2, 4, 8 at a 4x budget).
# The configs are written for RATIO=4.
stage_stage1() {
  for r in 4 8 16 32; do python scripts/train.py --config "configs/g1/stage1_r$r.yaml"; done
}
stage_stage2() {
  for f in 2 4 8; do python scripts/train.py --config "configs/g1/stage2_me_f$f.yaml"; done  # needed for the gate
  python scripts/train.py --config configs/g1/stage2_m.yaml
  python scripts/train.py --config configs/g1/stage2_w5.yaml
}

stage_eval() {
  log "ViQuAD dev at ${RATIO}x: references, hard baselines, ViLatent-ME (f = 2, 4, 8), -M, W5"
  python scripts/evaluate.py --reader "$READER" --reader-config "$CFG" --data data/tasks/viquad_dev.jsonl \
    --ratios "$RATIO" --methods full none truncation lead bm25 llmlingua2 \
    "vilatent:runs/g1_stage2_me_f2_r${RATIO}/best.pt" "vilatent:runs/g1_stage2_me_f4_r${RATIO}/best.pt" \
    "vilatent:runs/g1_stage2_me_f8_r${RATIO}/best.pt" "vilatent:runs/g1_stage2_m_r${RATIO}/best.pt" \
    "vilatent:runs/g1_stage2_w5_r${RATIO}/best.pt" --out-dir results/g1_dev
}

# ViLatent-ME: memory factor f chosen on stage-2 dev loss (not on dev F1, which the gate uses)
stage_select() { python scripts/select_me.py --ratio "$RATIO" --results-dir results/g1_dev; }

# ViLatent-MEF: choose tau on dev (smallest re-reading that keeps >= 95% of full-context F1)
stage_fallback() { python scripts/fallback_report.py --results-dir results/g1_dev --ratio "$RATIO"; }

stage_report() { python scripts/g1_report.py --results-dir results/g1_dev --ratio "$RATIO"; }

for stage in "$@"; do
  log "=== $stage"
  "stage_$stage"
  log "=== $stage done"
done
