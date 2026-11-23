#!/usr/bin/env bash
# PREREG_MORONG trên H100 (bf16). Hàng đợi động: mỗi GPU nhận job kế tiếp còn trống (claim bằng mkdir).
# Hai bộ job (chọn bằng SET):
#   SET=text    (mặc định; ĐÃ CHẠY XONG 2026-11-23, tag icisn-h100-v1) : `full`, `bm25_x2` trên P1. Không cần checkpoint.
#   SET=memctl  (lượt 2, phép kiểm soát nội dung bộ nhớ của M, giả thuyết C1)         : `m_swap` rồi `m_intact`.
#                MORE=1 thêm `m_zero`, `m_shuf` (thứ yếu, ngoài họ Holm). Cần checkpoint runs/paper/stage2_mem (xem tài liệu).
#   XCHECK=1 (SET=text) thêm m_intact và me_intact để đối chiếu fp16/bf16 (không dùng nữa; giữ cho tái lập).
# Dùng:  SET=memctl GPUS="0 1" bash scripts/icisn/run_h100.sh                       # chạy thật, hai GPU
#        SET=memctl GPUS="0" bash scripts/icisn/run_h100.sh                         # một GPU (RAM máy chủ < 128 GiB)
#        SET=memctl GPUS="0" LIMIT=12 OUT=results/icisn_h100_smoke_memctl/p1 bash scripts/icisn/run_h100.sh   # thử nhanh
# Chạy lại sau gián đoạn: xóa thư mục claim (rm -rf logs/h100/claim_<SET>); --skip-existing bỏ qua ô đã xong.
set -u
cd "$(dirname "$0")/../.."
GPUS=${GPUS:-"0 1"}; LIMIT=${LIMIT:-}; SET=${SET:-text}
OUT=${OUT:-$([ "$SET" = memctl ] && echo results/icisn_h100_memctl/p1 || echo results/icisn_h100/p1)}
CLAIM=logs/h100/claim_$SET; [ -n "$LIMIT" ] && CLAIM=logs/h100/claim_smoke_$SET
mkdir -p logs/h100 "$OUT" "$CLAIM"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True PYTHONIOENCODING=utf-8 VILATENT_MAX_CHUNKS=8
# KHÔNG đặt VILATENT_CHUNK_SDPA (chỉ cần cho 1080 Ti/T4). KHÔNG đổi cờ dưới đây: giữ bằng các lượt 1080 Ti.
MEM=vilatent:runs/paper/stage2_mem/best.pt
L=; [ -n "$LIMIT" ] && L="--limit $LIMIT"
# tên|các --methods   (job quan trọng trước)
case "$SET" in
  text)   JOBS=("full|full" "bm25_x2|bm25_x2")
          [ "${XCHECK:-0}" = "1" ] && JOBS+=("m_intact|$MEM,f=1" "me_intact|$MEM,f=2") ;;
  memctl) JOBS=("m_swap|$MEM,f=1,swap=0" "m_intact|$MEM,f=1")
          [ "${MORE:-0}" = "1" ] && JOBS+=("m_zero|$MEM,f=1,zero=1" "m_shuf|$MEM,f=1,shuf=0") ;;
  *) echo "SET phải là text hoặc memctl"; exit 2 ;;
esac
if [ "$SET" = memctl ] && [ ! -s runs/paper/stage2_mem/best.pt ]; then echo "THIẾU runs/paper/stage2_mem/best.pt"; exit 3; fi
worker() {
  local gpu=$1
  for j in "${JOBS[@]}"; do
    name=${j%%|*}; spec=${j#*|}
    mkdir "$CLAIM/$name" 2>/dev/null || continue
    echo "[$(date +%F\ %T)] gpu$gpu start $name"
    CUDA_VISIBLE_DEVICES=$gpu python scripts/evaluate.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
      --dtype bfloat16 --quant none --data data/icisn/longctx_p1.jsonl --ratios 4 --out-dir "$OUT" --selector runs/paper/selector \
      --max-batch-tokens 3000 --batch-size 4 --skip-existing $L --methods "$spec" > "logs/h100/${SET}_$name.log" 2>&1
    rc=$?
    echo "[$(date +%F\ %T)] gpu$gpu done $name rc=$rc $(grep -aE 'OutOfMemory|Traceback|Killed' "logs/h100/${SET}_$name.log" | tail -1 | cut -c1-120)"
  done
}
for g in $GPUS; do worker "$g" & done
wait
echo QUEUE_DONE
