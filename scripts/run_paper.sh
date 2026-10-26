#!/usr/bin/env bash
# Paper pipeline (ACIIDS 2027; checklist of 25/10/2026, docs/RUN_PAPER.md), one stage at a time:
#   bash scripts/run_paper.sh data template g0                     # data, fixed templates, kernel check (B1, B4)
#   bash scripts/run_paper.sh tune_bm25 selector aie                # T4 is enough: BM25 k1/b, PhoBERT (B3, B5)
#   bash scripts/run_paper.sh teacher stage1 stage2                 # H100 (B6, B8, B9, B10, B13)
#   bash scripts/run_paper.sh baselines                             # H100, can run during training (B7)
#   bash scripts/run_paper.sh eval_select choose eval_gate decide   # H100 (B12)
#   bash scripts/run_paper.sh test                                  # ONCE, after decide (B14)
#   optional: stage2_q (B17), stage2_seed2 (B15) before eval_select; figures after test
# Splits (whole Wikipedia articles): train; select (every choice: BM25 k1/b, selector checkpoint,
# stage-2 checkpoint, f*, τ); gate (only the pre-specified decision rule, ViQuAD-Long at 4x); test
# (official validation, read once by the `test` stage). Two settings: single passages ("single") and
# ViQuAD-Long ("long": the whole article). Metrics for the paper come from H100 (bf16) only; T4 runs
# (DTYPE=float16) are for debugging.
# Independent runs are spread over the GPUs in GPUS ("0 1": H100 #1 and #2).
# The size variables below exist for scripts/smoke_paper.sh; leave them at their defaults otherwise.
set -euo pipefail

READER=${READER:-Qwen/Qwen3.5-2B}
READER_9B=${READER_9B:-Qwen/Qwen3.5-9B}
SLUG=${SLUG:-qwen3.5-2b}
RATIOS=${RATIOS:-"4 8 16"}
N_PAIRS=${N_PAIRS:-96000}
N_DEV_PAIRS=${N_DEV_PAIRS:-1000}
N_WIKI=${N_WIKI:-200000}
N_NEWS=${N_NEWS:-200000}
DTYPE=${DTYPE:-bfloat16}        # float16 on GPUs without bf16 (T4)
QUANT=${QUANT:-none}            # int4: lighter reader for the T4 smoke test only
GPUS=${GPUS:-0}                 # e.g. "0 1": independent runs go round-robin to these GPUs
G0_READERS=${G0_READERS:-"$READER"}
G0_ARGS=${G0_ARGS:-}
TRAIN_ARGS=${TRAIN_ARGS:-}      # extra scripts/train.py arguments (smoke test: --steps …)
EVAL_ARGS=${EVAL_ARGS:-}        # extra scripts/evaluate.py arguments (smoke test, T4: --max-batch-tokens …)
SELECTOR_ARGS=${SELECTOR_ARGS:-}
LATENCY_ARGS=${LATENCY_ARGS:-}
TASKS=data/tasks
EVAL_EXT="data/eval_ext/mlqa_vi_dev.jsonl data/eval_ext/mlqa_vi_test.jsonl data/eval_ext/belebele_vi.jsonl
  data/eval_ext/vietnews_dev.jsonl data/eval_ext/vietnews_test.jsonl"
EVAL_FILES="$TASKS/viquad_gate.jsonl $TASKS/viquad_select.jsonl $TASKS/viquad_viwordc_dev.jsonl
  $TASKS/viquad_test.jsonl $EVAL_EXT"
CFG=configs/readers/$SLUG.json
TEACHER_DIR=data/teacher/$SLUG
RES=results/paper
RUNS=runs/paper
SELECTOR=$RUNS/selector
CHOICES=$RES/select/choices.json
export PYTHONIOENCODING=utf-8

log() { echo "[$(date '+%F %T')] $*"; }

# Run the given commands with one queue per GPU (command i goes to GPU i mod n); fails if any fails.
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

# file of a setting on a split: single -> viquad_<split>.jsonl, long -> viquad_long_<split>.jsonl
task_file() { if [ "$2" = long ]; then echo "$TASKS/viquad_long_$1.jsonl"; else echo "$TASKS/viquad_$1.jsonl"; fi; }

# a value of choices.json: setting, ratio, key
choice() { python -c 'import json, sys; print(json.load(open(sys.argv[1]))["settings"][sys.argv[2]][sys.argv[3]][sys.argv[4]])' \
  "$CHOICES" "$1" "$2" "$3"; }

# BM25 of the paper: pyvi words without question words, tuned on select (stage tune_bm25)
require_word_bm25() {
  python -c 'import sys; from vilatent.baselines import load_bm25_params
sys.exit(0 if load_bm25_params("configs/bm25.json")["units"] == "word" else
         "configs/bm25.json is not tuned for pyvi words yet: run the tune_bm25 stage first")'
}

ev() { echo "python scripts/evaluate.py --reader $READER --reader-config $CFG --dtype $DTYPE --quant $QUANT --selector $SELECTOR --skip-existing $EVAL_ARGS"; }

stage_data() {
  log "ViQuAD 2.0 split by article, contexts of the later evaluation sets, leak-filtered train"
  python scripts/prepare_viquad.py --out-dir $TASKS
  python scripts/prepare_external_eval.py --out-dir data/eval_ext
  python scripts/leak_filter.py --input $TASKS/viquad_train.jsonl --eval-files $EVAL_FILES \
    --out $TASKS/viquad_train_clean.jsonl
  log "ViQuAD-Long (gate, select, test) and multi-passage windows (train, select)"
  python scripts/build_long.py --tasks-dir $TASKS --reader "$READER"
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

stage_g0() {  # B1: Gated DeltaNet kernels, inputs_embeds, backward, decoding (also on a T4 with DTYPE=float16)
  local r
  for r in $G0_READERS; do
    log "G0 on $r"
    python scripts/g0_check.py --reader "$r" --reader-config "$CFG" --dtype "$DTYPE" --quant "$QUANT" \
      --out-dir results/g0 $G0_ARGS
  done
}

stage_tune_bm25() {
  # configs/bm25.json was tuned on words and committed on 26/10/2026 (6cc889a, Kaggle T4); a rerun (e.g. in bf16
  # on an H100) would overwrite it with other values. Only the smoke test reruns it, with FORCE_TUNE=1.
  if python -c 'import sys; from vilatent.baselines import load_bm25_params
sys.exit(0 if load_bm25_params("configs/bm25.json")["units"] == "word" else 1)' && [ "${FORCE_TUNE:-0}" != 1 ]; then
    log "tune_bm25: configs/bm25.json is already tuned on words (committed); skipped"
    return 0
  fi
  log "BM25 on pyvi words without question words: k1, b on select (single passages, 4x)"
  python scripts/tune_bm25.py --reader "$READER" --reader-config "$CFG" --data $TASKS/viquad_select.jsonl \
    --ratio 4 --units word --out configs/bm25.json --dtype "$DTYPE" --quant "$QUANT"
}

stage_selector() {
  log "PhoBERT sentence selector (trained hard baseline)"
  python scripts/train_selector.py --train $TASKS/viquad_train_clean.jsonl --dev $TASKS/viquad_select.jsonl \
    --out-dir $SELECTOR --dtype "$DTYPE" $SELECTOR_ARGS
}

stage_aie() {  # B3: is the gold answer still in the selected text? (CPU, select only)
  require_word_bm25
  python scripts/answer_in_evidence.py --reader "$READER" --ratios $RATIOS \
    --data $TASKS/viquad_select.jsonl $TASKS/viquad_long_select.jsonl --out $RES/select/answer_in_evidence.json
}

stage_teacher() {  # B6
  local jobs=() pair
  for pair in "data/stage1/pairs_train.jsonl continue pairs_train" "data/stage1/pairs_dev.jsonl continue pairs_dev" \
              "$TASKS/viquad_train_clean.jsonl qa viquad_train" "$TASKS/viquad_select.jsonl qa viquad_select" \
              "$TASKS/viquad_train_multi.jsonl qa viquad_train_multi" "$TASKS/viquad_select_multi.jsonl qa viquad_select_multi"; do
    set -- $pair
    jobs+=("python scripts/precompute_teacher.py --reader $READER --reader-config $CFG --data $1 --task $2 --out $TEACHER_DIR/$3.pt --dtype $DTYPE --quant $QUANT")
  done
  log "teacher logits: stage-1 pairs, ViQuAD train/select, multi-passage train/select"
  on_gpus "${jobs[@]}"
}

train_cmd() { echo "python scripts/train.py --config configs/paper/$1.yaml --dtype $DTYPE --quant $QUANT $TRAIN_ARGS"; }

stage_stage1() { on_gpus "$(train_cmd stage1)"; }  # B8: one multi-rate writer

stage_stage2() {  # B9 (ME/M), B10 (prompt control), B13 (frozen writer)
  require_word_bm25
  on_gpus "$(train_cmd stage2_mem)" "$(train_cmd stage2_prompt)" "$(train_cmd stage2_frozen)"
}

stage_stage2_q() { on_gpus "$(train_cmd stage2_q)"; }  # B17, if time permits

stage_stage2_seed2() {  # B15, if time permits: second seed of ME/M and of the control
  on_gpus "$(train_cmd stage2_mem) --seed 1 --out-dir $RUNS/stage2_mem_s1" \
          "$(train_cmd stage2_prompt) --seed 1 --out-dir $RUNS/stage2_prompt_s1"
}

# B7: hard baselines and references, every ratio, select and gate, both settings (no training needed)
stage_baselines() {
  require_word_bm25
  local jobs=() split setting
  for split in select gate; do
    for setting in long single; do
      jobs+=("$(ev) --data $(task_file $split $setting) --ratios $RATIOS --out-dir $RES/$split/$setting --methods full none truncation lead bm25 bm25_x2 phobert llmlingua2")
    done
  done
  on_gpus "${jobs[@]}"
}

# the trained methods of a split, every ratio and f (f* is chosen afterwards); optional runs if present
soft_methods() {
  local m="vilatent:$RUNS/stage2_mem/best.pt vilatent:$RUNS/stage2_prompt/best.pt vilatent:$RUNS/stage2_frozen/best.pt"
  [ -f $RUNS/stage2_mem_s1/best.pt ] && m+=" vilatent:$RUNS/stage2_mem_s1/best.pt,tag=s1"
  [ -f $RUNS/stage2_prompt_s1/best.pt ] && m+=" vilatent:$RUNS/stage2_prompt_s1/best.pt,tag=s1"
  echo "$m"
}

stage_eval_select() {  # B12, first half: everything f* and τ are chosen from
  local jobs=() setting
  for setting in long single; do
    jobs+=("$(ev) --data $(task_file select $setting) --ratios $RATIOS --out-dir $RES/select/$setting --methods $(soft_methods)")
  done
  on_gpus "${jobs[@]}"
}

stage_choose() {  # f* by select F1, then the cascade τ at f*, per setting and ratio
  python scripts/choose_f.py --select-dir $RES/select --ratios $RATIOS --out $CHOICES
  local setting r
  for setting in long single; do
    for r in $RATIOS; do
      python scripts/cascade_report.py --results-dir $RES/select/$setting --setting $setting --ratio $r \
        --choices $CHOICES --choose
    done
  done
}

# gate and test: the same soft methods, the swapped-memory control at 4x (every f), ViLatent-Q at 4x
eval_soft_jobs() {
  local split=$1 setting q=""
  [ -f $RUNS/stage2_q/best.pt ] && q=" vilatent:$RUNS/stage2_q/best.pt"
  for setting in long single; do
    echo "$(ev) --data $(task_file $split $setting) --ratios $RATIOS --out-dir $RES/$split/$setting --methods $(soft_methods)"
    echo "$(ev) --data $(task_file $split $setting) --ratios 4 --out-dir $RES/$split/$setting --methods vilatent:$RUNS/stage2_mem/best.pt,swap=0$q"
  done
}

reports() {  # cascade (τ from select), report of every setting and ratio, of one split
  local split=$1 setting r
  for setting in long single; do
    for r in $RATIOS; do
      python scripts/cascade_report.py --results-dir $RES/$split/$setting --setting $setting --ratio $r --choices $CHOICES
      python scripts/paper_report.py --results-dir $RES/$split/$setting --setting $setting --ratio $r --choices $CHOICES
    done
  done
}

stage_eval_gate() {
  local jobs=()
  mapfile -t jobs < <(eval_soft_jobs gate)
  on_gpus "${jobs[@]}"
}

# the pre-specified rule: gate, ViQuAD-Long, 4x (its line is the last of the log)
stage_decide() {
  reports gate
  python scripts/paper_report.py --results-dir $RES/gate/long --setting long --ratio 4 --choices $CHOICES --decide
}

# B14: ViQuAD test, read ONCE, after the decision, with every choice fixed on select. TEST_RESUME=1
# continues an interrupted run (finished files are not evaluated again); ask the project owner first.
stage_test() {
  local out=$RES/test jobs=() setting
  if [ ! -f "$RES/gate/decision.json" ]; then
    log "test: no $RES/gate/decision.json; the test set is read only after the decision"
    return 1
  fi
  if [ -n "$(ls -A "$out" 2>/dev/null)" ] && [ "${TEST_RESUME:-0}" != 1 ]; then
    log "test: $out is not empty; the test set is read once (ask the project owner before resuming or deleting)"
    return 1
  fi
  log "ViQuAD test (single and Long), read once"
  for setting in long single; do
    jobs+=("$(ev) --data $(task_file test $setting) --ratios $RATIOS --out-dir $out/$setting --methods full none truncation lead bm25 bm25_x2 phobert llmlingua2")
  done
  mapfile -t -O ${#jobs[@]} jobs < <(eval_soft_jobs test)
  on_gpus "${jobs[@]}"
  reports test
  python scripts/position_report.py --results-dir $out/long --ratio 4
  for setting in long single; do
    python scripts/latency.py --reader "$READER" --reader-config "$CFG" --data "$(task_file test $setting)" \
      --checkpoint $RUNS/stage2_mem/best.pt --ratio 4 --factor "$(choice $setting 4 f_star)" --selector $SELECTOR \
      --llmlingua --cascade $out/$setting/cascade_r4.json --dtype "$DTYPE" --out $out/latency_$setting.json $LATENCY_ARGS
  done
}

stage_figures() {
  python scripts/paper_figures.py --results-dir $RES/test/long --choices $CHOICES --ratios $RATIOS \
    --out paper/figures/curves.tex
}

# Auto-generated QA, not used by the paper (stage-2 data of G2), kept from the G1 pipeline. The GPU
# cluster cannot reach the teacher endpoint, so generation runs elsewhere and its output is on the Hub:
#   bash scripts/run_paper.sh qa_generate            # machine inside the iCOMM network, CPU only
#   bash scripts/run_paper.sh qa_download qa_filter  # GPU cluster; needs an HF_TOKEN that can read QA_REPO
TEACHER_URL=${TEACHER_URL:-http://172.16.9.11:30049/v1}
TEACHER_MODEL=${TEACHER_MODEL:-icmodel/icom-model-llm-ic-v3.8-27b}
QA_REPO=${QA_REPO:-thanthienhai/vilatent-qa-gen}
QA_REVISION=${QA_REVISION:-28e3ac26c3d0289d4b38b7366f6df3b8d08a937b}  # prompt 3, 19,983 paragraphs (21/10/2026)

stage_qa_generate() {
  log "auto-generated QA with the teacher at $TEACHER_URL (no GPU)"
  python scripts/generate_qa.py --docs data/corpus/docs.jsonl --base-url "$TEACHER_URL" --model "$TEACHER_MODEL" \
    --out data/qa_gen/qa_raw.jsonl
}

stage_qa_download() {
  log "auto-generated QA from $QA_REPO at revision $QA_REVISION"
  hf download "$QA_REPO" qa_raw.jsonl qa_raw.jsonl.meta.json --repo-type dataset --revision "$QA_REVISION" \
    --local-dir data/qa_gen
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

for stage in "$@"; do
  log "=== $stage"
  "stage_$stage"
  log "=== $stage done"
done
