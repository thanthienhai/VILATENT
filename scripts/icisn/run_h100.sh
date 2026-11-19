#!/usr/bin/env bash
# PREREG_MORONG trên H100 (bf16), PHẠM VI THU HẸP (bản 2, 2026-11-18): chỉ phần 1080 Ti không làm được hoặc đã mất:
#   `full` và `bm25_x2` trên P1 (533 câu); tùy chọn XCHECK=1 thêm ViLatent M và ME nguyên vẹn để đối chiếu fp16 (1080 Ti) với bf16 (H100).
# Các điều kiện kiểm soát bộ nhớ (swap/zero/shuf) KHÔNG chạy ở đây: chạy trên 1080 Ti như đã đăng ký.
# Hàng đợi động: mỗi GPU nhận job kế tiếp còn trống (claim bằng mkdir), chạy được với số GPU bất kỳ.
# Dùng:  GPUS="0 1" bash scripts/icisn/run_h100.sh                     # chạy thật
#        GPUS="0" LIMIT=12 OUT=results/icisn_h100_smoke/p1 bash scripts/icisn/run_h100.sh   # thử nhanh (không dùng làm kết quả)
#        XCHECK=1 GPUS="0 1" bash scripts/icisn/run_h100.sh             # thêm hai job đối chiếu bf16
# Chạy lại sau gián đoạn: xóa thư mục claim (rm -rf logs/h100/claim); --skip-existing bỏ qua ô đã xong.
set -u
cd "$(dirname "$0")/../.."
GPUS=${GPUS:-"0 1"}; LIMIT=${LIMIT:-}; OUT=${OUT:-results/icisn_h100/p1}
CLAIM=logs/h100/claim; [ -n "$LIMIT" ] && CLAIM=logs/h100/claim_smoke
mkdir -p logs/h100 "$OUT" "$CLAIM"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True PYTHONIOENCODING=utf-8 VILATENT_MAX_CHUNKS=8
# KHÔNG đặt VILATENT_CHUNK_SDPA (chỉ cần cho 1080 Ti/T4). KHÔNG đổi cờ dưới đây: giữ bằng các lượt 1080 Ti.
MEM=vilatent:runs/paper/stage2_mem/best.pt
L=; [ -n "$LIMIT" ] && L="--limit $LIMIT"
# tên|các --methods   (job nặng trước)
JOBS=(
"full|full"
"bm25_x2|bm25_x2"
)
[ "${XCHECK:-0}" = "1" ] && JOBS+=("m_intact|$MEM,f=1" "me_intact|$MEM,f=2")
worker() {
  local gpu=$1
  for j in "${JOBS[@]}"; do
    name=${j%%|*}; spec=${j#*|}
    mkdir "$CLAIM/$name" 2>/dev/null || continue
    echo "[$(date +%F\ %T)] gpu$gpu start $name"
    CUDA_VISIBLE_DEVICES=$gpu python scripts/evaluate.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
      --dtype bfloat16 --quant none --data data/icisn/longctx_p1.jsonl --ratios 4 --out-dir "$OUT" --selector runs/paper/selector \
      --max-batch-tokens 3000 --batch-size 4 --skip-existing $L --methods "$spec" > "logs/h100/$name.log" 2>&1
    rc=$?
    echo "[$(date +%F\ %T)] gpu$gpu done $name rc=$rc $(grep -aE 'OutOfMemory|Traceback|Killed' "logs/h100/$name.log" | tail -1 | cut -c1-120)"
  done
}
for g in $GPUS; do worker "$g" & done
wait
echo QUEUE_DONE
