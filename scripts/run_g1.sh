#!/usr/bin/env bash
# G0 + G1 pipeline, one stage at a time (docs/RUN_G0_G1.md):
#   bash scripts/run_g1.sh data template g0          # week 1–2
#   bash scripts/run_g1.sh qa_gen                     # background job (teacher endpoint)
#   bash scripts/run_g1.sh teacher stage1 stage2 eval select fallback report   # week 3
# Each stage reads only the files written by the previous ones.
# Independent runs (teacher files, stage 1, stage 2, evaluation) are spread over the GPUs in GPUS.
# The size variables below exist for scripts/smoke_g1.sh; leave them at their defaults for G1.
set -euo pipefail

READER=${READER:-Qwen/Qwen3.5-2B}
READER_9B=${READER_9B:-Qwen/Qwen3.5-9B}
SLUG=${SLUG:-qwen3.5-2b}
RATIO=${RATIO:-4}
TEACHER_URL=${TEACHER_URL:-http://172.16.9.11:30048/v1}
TEACHER_MODEL=${TEACHER_MODEL:-icmodel/icom-model-llm-ic-v3.8-27b}
N_PAIRS=${N_PAIRS:-96000}
N_DEV_PAIRS=${N_DEV_PAIRS:-1000}
N_WIKI=${N_WIKI:-200000}
N_NEWS=${N_NEWS:-200000}
DTYPE=${DTYPE:-bfloat16}        # float16 on GPUs without bf16 (T4)
QUANT=${QUANT:-none}            # int4: lighter reader for the T4 smoke test only (never for G0/G1)
GPUS=${GPUS:-0}                 # e.g. "0 1": independent runs go round-robin to these GPUs
G0_READERS=${G0_READERS:-"$READER $READER_9B"}
G0_ARGS=${G0_ARGS:-}            # extra scripts/g0_check.py arguments (smoke test, 9B on a T4)
TRAIN_ARGS=${TRAIN_ARGS:-}      # extra scripts/train.py arguments (smoke test: --steps …)
EVAL_ARGS=${EVAL_ARGS:-}        # extra scripts/evaluate.py arguments (smoke test: --batch-size …)
EVAL_FILES="data/tasks/viquad_dev.jsonl data/tasks/viquad_test.jsonl"
CFG=configs/readers/$SLUG.json
TEACHER_DIR=data/teacher/$SLUG
export PYTHONIOENCODING=utf-8

log() { echo "[$(date '+%F %T')] $*"; }

# Run the given commands with one queue per GPU (command i goes to GPU i mod n); fails if any fails.
# After a failure, the rest of that GPU's queue is skipped and each skipped command is logged.
on_gpus() {
  local gpus=($GPUS) n g i pids=() status=0
  n=${#gpus[@]}
  for ((g = 0; g < n; g++)); do
    (
      for ((i = g + 1; i <= $#; i += n)); do
        log "GPU ${gpus[$g]}: ${!i}"
        if ! CUDA_VISIBLE_DEVICES=${gpus[$g]} bash -c "${!i}"; then
          for ((i += n; i <= $#; i += n)); do log "GPU ${gpus[$g]}: skipped (an earlier run on this GPU failed): ${!i}"; done
          exit 1
        fi
      done
    ) &
    pids+=($!)
  done
  for pid in "${pids[@]}"; do wait "$pid" || status=1; done
  return $status
}

reader_cfg() {
  case "$1" in
    "$READER") echo "$CFG" ;;
    "$READER_9B") echo configs/readers/qwen3.5-9b.json ;;
    *) echo "no reader config for $1" >&2; return 1 ;;
  esac
}

stage_data() {
  log "ViQuAD 2.0 (ViWord-C split) and leak-filtered train"
  python scripts/prepare_viquad.py --out-dir data/tasks
  python scripts/leak_filter.py --input data/tasks/viquad_train.jsonl --eval-files $EVAL_FILES \
    --out data/tasks/viquad_train_clean.jsonl
  log "stage-1 corpus (Wikipedia + BKAINewsCorpus) and (A, B) pairs"
  python scripts/build_corpus.py --eval-files $EVAL_FILES --n-wiki "$N_WIKI" --n-news "$N_NEWS" \
    --out data/corpus/docs.jsonl
  python scripts/make_pairs.py --docs data/corpus/docs.jsonl --reader "$READER" --n-train "$N_PAIRS" \
    --n-dev "$N_DEV_PAIRS" --out-dir data/stage1
}

stage_template() {
  log "render the fixed chat templates"
  python scripts/render_template.py --reader "$READER" --out "$CFG"
  python scripts/render_template.py --reader "$READER_9B" --out configs/readers/qwen3.5-9b.json
}

stage_g0() {
  for r in $G0_READERS; do
    log "G0 on $r"
    python scripts/g0_check.py --reader "$r" --reader-config "$(reader_cfg "$r")" --dtype "$DTYPE" \
      --quant "$QUANT" $G0_ARGS
  done
}

stage_qa_gen() {
  log "auto-generated QA with the teacher, then the two-way check with $READER"
  python scripts/generate_qa.py --docs data/corpus/docs.jsonl --base-url "$TEACHER_URL" --model "$TEACHER_MODEL" \
    --out data/qa_gen/qa_raw.jsonl
  local gpus=($GPUS)
  local qa_gpu=${QA_GPU:-${gpus[${#gpus[@]} - 1]}}  # runs in the background: keep it off the GPUs of G1
  log "two-way check on GPU $qa_gpu"
  CUDA_VISIBLE_DEVICES=$qa_gpu python scripts/filter_qa.py --input data/qa_gen/qa_raw.jsonl --reader "$READER" \
    --reader-config "$CFG" --eval-files $EVAL_FILES --out data/qa_gen/qa_clean.jsonl --dtype "$DTYPE" --quant "$QUANT"
}

stage_teacher() {
  local jobs=() pair
  for pair in "data/stage1/pairs_train.jsonl continue pairs_train" "data/stage1/pairs_dev.jsonl continue pairs_dev" \
              "data/tasks/viquad_train_clean.jsonl qa viquad_train" "data/tasks/viquad_dev.jsonl qa viquad_dev"; do
    set -- $pair
    jobs+=("python scripts/precompute_teacher.py --reader $READER --reader-config $CFG --data $1 --task $2 --out $TEACHER_DIR/$3.pt --dtype $DTYPE --quant $QUANT")
  done
  log "teacher logits for the stage-1 pairs and ViQuAD train/dev"
  on_gpus "${jobs[@]}"
}

# Stage-1 writers: 4x (ViLatent-M, W5) and 8x/16x/32x (ViLatent-ME with f = 2, 4, 8 at a 4x budget).
# The configs are written for RATIO=4.
train_cmd() { echo "python scripts/train.py --config configs/g1/$1.yaml --dtype $DTYPE --quant $QUANT $TRAIN_ARGS"; }
stage_stage1() {
  on_gpus "$(train_cmd stage1_r4)" "$(train_cmd stage1_r8)" "$(train_cmd stage1_r16)" "$(train_cmd stage1_r32)"
}
stage_stage2() {
  # the three ME runs are needed for the gate; M and W5 are reported alongside
  on_gpus "$(train_cmd stage2_me_f2)" "$(train_cmd stage2_me_f4)" "$(train_cmd stage2_me_f8)" \
          "$(train_cmd stage2_m)" "$(train_cmd stage2_w5)"
}

stage_eval() {
  log "ViQuAD dev at ${RATIO}x: references, hard baselines, ViLatent-ME (f = 2, 4, 8), -M, W5"
  local eval="python scripts/evaluate.py --reader $READER --reader-config $CFG --data data/tasks/viquad_dev.jsonl"
  eval+=" --ratios $RATIO --out-dir results/g1_dev --dtype $DTYPE --quant $QUANT $EVAL_ARGS --methods"
  local ckpt="runs/g1_stage2_%s_r${RATIO}/best.pt" soft="" run
  for run in me_f2 me_f4 me_f8 m w5; do soft+=" vilatent:$(printf "$ckpt" "$run")"; done
  on_gpus "$eval full none truncation lead bm25 llmlingua2" "$eval$soft"
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
