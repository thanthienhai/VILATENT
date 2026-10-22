#!/usr/bin/env bash
# G0 + G1 pipeline, one stage at a time (docs/RUN_G0_G1.md):
#   bash scripts/run_g1.sh data template g0          # week 1–2
#   bash scripts/run_g1.sh teacher stage1 stage2 select stage2b eval fallback report   # week 3
# ViQuAD splits (review of 22/10/2026): train; gate (whole articles, only for the G1 decision);
# select (other whole articles: checkpoints, f*, the control's learning rate, τ); viwordc_dev
# (ViWord-C's dev, same articles as train: auxiliary table only); test (never read at G1, only
# its contexts for the leak filters). configs/bm25.json (k1, b) was tuned on select beforehand.
# Auto-generated QA (not used by G1; for weeks 4–6). The GPU cluster cannot reach the teacher
# endpoint, so generation runs elsewhere and its output is published on the Hugging Face Hub:
#   bash scripts/run_g1.sh qa_generate               # machine inside the iCOMM network, CPU only
#   bash scripts/run_g1.sh qa_download qa_filter     # GPU cluster; needs an HF_TOKEN that can read QA_REPO
# Each stage reads only the files written by the previous ones.
# Independent runs (teacher files, stage 1, stage 2, evaluation) are spread over the GPUs in GPUS.
# The size variables below exist for scripts/smoke_g1.sh; leave them at their defaults for G1.
set -euo pipefail

READER=${READER:-Qwen/Qwen3.5-2B}
READER_9B=${READER_9B:-Qwen/Qwen3.5-9B}
SLUG=${SLUG:-qwen3.5-2b}
RATIO=${RATIO:-4}
TEACHER_URL=${TEACHER_URL:-http://172.16.9.11:30049/v1}
TEACHER_MODEL=${TEACHER_MODEL:-icmodel/icom-model-llm-ic-v3.8-27b}
QA_REPO=${QA_REPO:-thanthienhai/vilatent-qa-gen}   # private dataset repo with qa_raw.jsonl and its meta
QA_REVISION=${QA_REVISION:-28e3ac26c3d0289d4b38b7366f6df3b8d08a937b}  # prompt 3, 19,983 paragraphs (21/10/2026)
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
TASKS=data/tasks
EVAL_EXT="data/eval_ext/mlqa_vi_dev.jsonl data/eval_ext/mlqa_vi_test.jsonl data/eval_ext/belebele_vi.jsonl
  data/eval_ext/vietnews_dev.jsonl data/eval_ext/vietnews_test.jsonl"
# every evaluation file, for the leak filters (training text must not overlap any of them)
EVAL_FILES="$TASKS/viquad_gate.jsonl $TASKS/viquad_select.jsonl $TASKS/viquad_viwordc_dev.jsonl
  $TASKS/viquad_test.jsonl $EVAL_EXT"
CFG=configs/readers/$SLUG.json
TEACHER_DIR=data/teacher/$SLUG
RES=results/g1
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
  log "ViQuAD 2.0 split by article, contexts of the later evaluation sets, leak-filtered train"
  python scripts/prepare_viquad.py --out-dir $TASKS
  python scripts/prepare_external_eval.py --out-dir data/eval_ext
  python scripts/leak_filter.py --input $TASKS/viquad_train.jsonl --eval-files $EVAL_FILES \
    --out $TASKS/viquad_train_clean.jsonl
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

stage_qa_generate() {
  log "auto-generated QA with the teacher at $TEACHER_URL (no GPU)"
  python scripts/generate_qa.py --docs data/corpus/docs.jsonl --base-url "$TEACHER_URL" --model "$TEACHER_MODEL" \
    --out data/qa_gen/qa_raw.jsonl
}

stage_qa_download() {
  log "auto-generated QA from $QA_REPO at revision $QA_REVISION"
  hf download "$QA_REPO" qa_raw.jsonl qa_raw.jsonl.meta.json --repo-type dataset --revision "$QA_REVISION"     --local-dir data/qa_gen
  python -c 'import json, sys; from vilatent.data import sha256_file
meta = json.load(open("data/qa_gen/qa_raw.jsonl.meta.json", encoding="utf-8"))
sys.exit(0 if sha256_file("data/qa_gen/qa_raw.jsonl") == meta["sha256"] else "qa_raw.jsonl does not match its meta sha256")'
}

stage_qa_filter() {
  log "two-way check of the auto-generated QA with $READER"
  python scripts/filter_qa.py --input data/qa_gen/qa_raw.jsonl --reader "$READER" --reader-config "$CFG" \
    --eval-files $EVAL_FILES --dropped-docs data/corpus/docs.dropped.jsonl --out data/qa_gen/qa_clean.jsonl \
    --dtype "$DTYPE" --quant "$QUANT"
}

stage_teacher() {
  local jobs=() pair
  for pair in "data/stage1/pairs_train.jsonl continue pairs_train" "data/stage1/pairs_dev.jsonl continue pairs_dev" \
              "$TASKS/viquad_train_clean.jsonl qa viquad_train" "$TASKS/viquad_select.jsonl qa viquad_select"; do
    set -- $pair
    jobs+=("python scripts/precompute_teacher.py --reader $READER --reader-config $CFG --data $1 --task $2 --out $TEACHER_DIR/$3.pt --dtype $DTYPE --quant $QUANT")
  done
  log "teacher logits for the stage-1 pairs and ViQuAD train/select"
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

# a value of a choice file written by scripts/choose_by_loss.py
choice() { python -c 'import json, sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$1" "$2"; }

# ViLatent-ME: memory factor f* chosen on the select dev loss of the three ME runs (not on any F1)
stage_select() {
  python scripts/choose_by_loss.py --key memory_factor --out $RES/me_choice_r$RATIO.json \
    $(for f in 2 4 8; do echo "$f=runs/g1_stage2_me_f${f}_r$RATIO"; done)
}

# At f*: ME with seed 1 (the gate pools two seeds) and the learned-prompt control at lr 1e-4 and
# 1e-3; the control's learning rate is then chosen on the select dev loss.
stage_stage2b() {
  local f pe
  f=$(choice $RES/me_choice_r$RATIO.json memory_factor)
  pe="$(train_cmd stage2_prompt) --memory-factor $f"
  on_gpus "$(train_cmd stage2_me_f$f) --seed 1 --out-dir runs/g1_stage2_me_f${f}_s1_r$RATIO" \
          "$pe --lr-adapter 1e-4 --out-dir runs/g1_stage2_prompt_f${f}_lr1e-4_r$RATIO" \
          "$pe --lr-adapter 1e-3 --out-dir runs/g1_stage2_prompt_f${f}_lr1e-3_r$RATIO"
  python scripts/choose_by_loss.py --key lr_adapter --out $RES/pe_choice_r$RATIO.json \
    "1e-4=runs/g1_stage2_prompt_f${f}_lr1e-4_r$RATIO" "1e-3=runs/g1_stage2_prompt_f${f}_lr1e-3_r$RATIO"
}

# gate: every method; ME at f = 2, 4, 8 with own and with swapped memory; ME f* seed 1; the control.
# select: full and ME f* (for τ). viwordc_dev (auxiliary): references, hard baselines, ME f*, M, W5.
stage_eval() {
  local f me m w5 ev gate soft swap g
  f=$(choice $RES/me_choice_r$RATIO.json memory_factor)
  me="vilatent:runs/g1_stage2_me_f${f}_r$RATIO/best.pt"
  m="vilatent:runs/g1_stage2_m_r$RATIO/best.pt"
  w5="vilatent:runs/g1_stage2_w5_r$RATIO/best.pt"
  ev="python scripts/evaluate.py --reader $READER --reader-config $CFG --ratios $RATIO --dtype $DTYPE --quant $QUANT"
  ev+=" $EVAL_ARGS"
  gate="$ev --data $TASKS/viquad_gate.jsonl --out-dir $RES/gate --methods"
  soft=" $m $w5 vilatent:runs/g1_stage2_me_f${f}_s1_r$RATIO/best.pt,name=vilatent_me_f${f}_s1"
  soft+=" vilatent:$(choice $RES/pe_choice_r$RATIO.json run)/best.pt"
  swap=""
  for g in 2 4 8; do
    soft+=" vilatent:runs/g1_stage2_me_f${g}_r$RATIO/best.pt"
    swap+=" vilatent:runs/g1_stage2_me_f${g}_r$RATIO/best.pt,swap=0"
  done
  log "ViQuAD gate, select and ViWord-C dev at ${RATIO}x (f* = $f)"
  on_gpus "$gate full none truncation lead bm25 llmlingua2" "$gate$soft" "$gate$swap" \
          "$ev --data $TASKS/viquad_select.jsonl --out-dir $RES/select --methods full $me" \
          "$ev --data $TASKS/viquad_viwordc_dev.jsonl --out-dir $RES/viwordc --methods full none truncation lead bm25 llmlingua2 $me $m $w5"
}

# ViLatent-MEF: τ chosen on select (smallest re-reading that keeps >= 95% of full-context F1), then
# applied unchanged to gate and ViWord-C dev
stage_fallback() {
  local f d
  f=$(choice $RES/me_choice_r$RATIO.json memory_factor)
  python scripts/fallback_report.py --results-dir $RES/select --ratio "$RATIO" --me vilatent_me_f$f
  for d in gate viwordc; do
    python scripts/fallback_report.py --results-dir $RES/$d --ratio "$RATIO" --me vilatent_me_f$f \
      --tau-file $RES/select/mef_tau_r$RATIO.json
  done
}

# the auxiliary ViWord-C table first, the gate decision last (the last line of the log)
stage_report() {
  python scripts/g1_report.py --results-dir $RES/viwordc --choices-dir $RES --ratio "$RATIO"
  python scripts/g1_report.py --results-dir $RES/gate --choices-dir $RES --ratio "$RATIO" --gate
}

for stage in "$@"; do
  log "=== $stage"
  "stage_$stage"
  log "=== $stage done"
done
