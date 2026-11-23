#!/usr/bin/env bash
# PREREG_MORONG trên H100 (bf16). Hàng đợi động: mỗi GPU nhận job kế tiếp còn trống (claim bằng mkdir).
# Hai bộ job (chọn bằng SET):
#   SET=text    (mặc định; ĐÃ CHẠY XONG 2026-11-23) : `full`, `bm25_x2` trên P1. Không cần checkpoint.
#   SET=memctl  (lượt 2, phép kiểm soát nội dung bộ nhớ của M, giả thuyết C1)  : `m_swap` rồi `m_intact`.
#                MORE=1 thêm `m_zero`, `m_shuf` (thứ yếu, ngoài họ Holm). Cần checkpoint runs/paper/stage2_mem.
#   XCHECK=1 (SET=text) thêm m_intact và me_intact để đối chiếu fp16/bf16 (không dùng nữa; giữ cho tái lập).
# Dùng:  SET=memctl GPUS="0 1" bash scripts/icisn/run_h100.sh                       # chạy thật
#        python scripts/icisn/make_smoke_p1.py && SET=memctl GPUS="0" DATA=data/icisn/longctx_p1_smoke.jsonl OUT=results/icisn_h100_smoke_memctl/p1 bash scripts/icisn/run_h100.sh   # thử nhanh (12 câu, 3 bài, đủ 16k/32k/64k)
# Đảm bảo chạy đủ: (1) RAM dùng được < 200 GiB thì tự chạy tuần tự trên một GPU (FORCE_PARALLEL=1 để bỏ qua);
#   (2) ô thiếu hoặc sai n thì tự thử lại tối đa 2 lần trên GPU đầu tiên (--skip-existing giữ ô đã xong);
#   (3) chạy lại cùng lệnh sau gián đoạn là đủ (hàng đợi tự khởi tạo lại);
#   (4) kết thúc in RESULT_COMPLETE (exit 0) hoặc RESULT_INCOMPLETE (exit 1) kèm tên ô thiếu.
set -u
cd "$(dirname "$0")/../.."
GPUS=${GPUS:-"0 1"}; LIMIT=${LIMIT:-}; SET=${SET:-text}
P1=data/icisn/longctx_p1.jsonl; P1_SHA=52e01c31cc0097660d900e6ce7bcaa1e525c83b0758df567f7cd97b34eca20fc
DATA=${DATA:-$P1}   # DATA=data/icisn/longctx_p1_smoke.jsonl chỉ cho thử nhanh (tạo bằng scripts/icisn/make_smoke_p1.py)
OUT=${OUT:-$([ "$SET" = memctl ] && echo results/icisn_h100_memctl/p1 || echo results/icisn_h100/p1)}
CLAIM=logs/h100/claim_$SET; [ -n "$LIMIT" ] && CLAIM=logs/h100/claim_smoke_$SET
case "$SET" in text|memctl) ;; *) echo "SET phải là text hoặc memctl"; exit 2 ;; esac
rm -rf "$CLAIM"   # mỗi lần gọi bắt đầu lại hàng đợi; ô đã xong được --skip-existing bỏ qua
mkdir -p logs/h100 "$OUT" "$CLAIM"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True PYTHONIOENCODING=utf-8 VILATENT_MAX_CHUNKS=8
# KHÔNG đặt VILATENT_CHUNK_SDPA (chỉ cần cho 1080 Ti/T4). KHÔNG đổi cờ dưới đây: giữ bằng các lượt 1080 Ti.
MEM=vilatent:runs/paper/stage2_mem/best.pt
L=; [ -n "$LIMIT" ] && L="--limit $LIMIT"
# tên|các --methods   (job quan trọng trước)
case "$SET" in
  text)   JOBS=("full|full" "bm25_x2|bm25_x2")
          [ "${XCHECK:-0}" = "1" ] && JOBS+=("m_intact|$MEM,f=1" "me_intact|$MEM,f=2")
          NEED=(full bm25_x2_r4) ;;
  memctl) JOBS=("m_swap|$MEM,f=1,swap=0" "m_intact|$MEM,f=1")
          NEED=(vilatent_m_swap_r4 vilatent_m_r4)
          [ "${MORE:-0}" = "1" ] && { JOBS+=("m_zero|$MEM,f=1,zero=1" "m_shuf|$MEM,f=1,shuf=0"); NEED+=(vilatent_m_zero_r4 vilatent_m_shuf_r4); } ;;
esac
if [ "$SET" = memctl ] && [ ! -s runs/paper/stage2_mem/best.pt ]; then echo "THIẾU runs/paper/stage2_mem/best.pt"; exit 3; fi
[ -s "$DATA" ] || { echo "THIẾU $DATA"; exit 3; }
if [ "$DATA" = "$P1" ]; then   # lượt chạy thật: bắt buộc đúng tệp đã đăng ký
  [ "$(sha256sum "$P1" | cut -d' ' -f1)" = "$P1_SHA" ] || { echo "SAI SHA-256 của $P1 (cần $P1_SHA): dừng."; exit 4; }
elif [ "$OUT" = "results/icisn_h100_memctl/p1" ] || [ "$OUT" = "results/icisn_h100/p1" ]; then
  echo "DATA khác tệp đăng ký thì OUT phải là thư mục thử, không được ghi vào thư mục kết quả chính."; exit 4
fi
EXPECT_N=${LIMIT:-$(grep -c . "$DATA")}

# RAM dùng được thật sự = min(giới hạn cgroup, MemTotal), GiB. Mỗi tiến trình M có thể dùng 45-50 GB (ngoại suy từ 1080 Ti, chưa đo).
mem_gib() {
  local tot lim; tot=$(awk '/MemTotal/{print int($2/1048576)}' /proc/meminfo)
  lim=$(cat /sys/fs/cgroup/memory.max 2>/dev/null || cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null || echo max)
  case "$lim" in max|"") echo "$tot" ;; *) lim=$((lim/1073741824)); if [ "$lim" -lt "$tot" ]; then echo "$lim"; else echo "$tot"; fi ;; esac
}
RAM=$(mem_gib); NG=$(echo $GPUS | wc -w)
if [ "$SET" = memctl ] && [ "$NG" -gt 1 ] && [ "$RAM" -lt 200 ] && [ "${FORCE_PARALLEL:-0}" != 1 ]; then
  echo "!! RAM dùng được ${RAM} GiB < 200 GiB: hai tiến trình M song song có thể bị giết. Chạy tuần tự trên GPU đầu tiên."
  GPUS=${GPUS%% *}
fi
echo "RAM dùng được: ${RAM} GiB; GPU dùng: $GPUS; bộ: $SET; n kỳ vọng: $EXPECT_N"

missing() {  # tên ô còn thiếu hoặc sai n
  OUT="$OUT" EXPECT_N="$EXPECT_N" python - "${NEED[@]}" <<'PYEOF'
import os, sys, json
d, n = os.environ["OUT"], int(os.environ["EXPECT_N"])
for k in sys.argv[1:]:
    f = f"{d}/{k}.summary.json"
    if not os.path.exists(f) or json.load(open(f)).get("n") != n: print(k)
PYEOF
}
worker() {
  local gpu=$1 name spec rc lg before
  for j in "${JOBS[@]}"; do
    name=${j%%|*}; spec=${j#*|}
    mkdir "$CLAIM/$name" 2>/dev/null || continue
    lg="logs/h100/${SET}_$name.log"; if [ -f "$lg" ]; then before=$(wc -l < "$lg"); else before=0; fi
    echo "[$(date +%F\ %T)] gpu$gpu start $name"
    CUDA_VISIBLE_DEVICES=$gpu python scripts/evaluate.py --reader Qwen/Qwen3.5-2B --reader-config configs/readers/qwen3.5-2b.json \
      --dtype bfloat16 --quant none --data "$DATA" --ratios 4 --out-dir "$OUT" --selector runs/paper/selector \
      --max-batch-tokens 3000 --batch-size 4 --skip-existing $L --methods "$spec" >> "$lg" 2>&1
    rc=$?
    echo "[$(date +%F\ %T)] gpu$gpu done $name rc=$rc $(tail -n +$((before+1)) "$lg" | grep -aE 'OutOfMemory|Traceback|Killed' | tail -1 | cut -c1-120)"
  done
}
# RSS đỉnh của tiến trình evaluate.py (MiB), ghi mỗi 15 giây, để báo lại cho chủ đề tài
( while true; do ps -eo rss,args 2>/dev/null | awk '/scripts\/evaluate.py/ && !/awk/ {if ($1>m) m=$1} END{printf "%s %d MiB\n", strftime("%T"), m/1024}' >> "logs/h100/rss_$SET.log"; sleep 15; done ) &
SAMPLER=$!
trap 'kill $SAMPLER 2>/dev/null' EXIT

PIDS=()
for g in $GPUS; do worker "$g" & PIDS+=($!); done
wait "${PIDS[@]}"   # chỉ chờ các worker, không chờ vòng lấy mẫu RSS
# còn ô thiếu (bị giết, lỗi tạm): thử lại tuần tự trên GPU đầu tiên, tối đa 2 lần
G0=${GPUS%% *}
for attempt in 1 2; do
  M=$(missing); [ -z "$M" ] && break
  echo "!! thiếu hoặc sai n: $(echo $M | tr '\n' ' ') -> thử lại lần $attempt trên gpu$G0"
  rm -rf "$CLAIM"; mkdir -p "$CLAIM"
  worker "$G0"
done
M=$(missing)
if [ -z "$M" ]; then echo "RESULT_COMPLETE set=$SET n=$EXPECT_N dir=$OUT"; echo QUEUE_DONE; exit 0
else echo "RESULT_INCOMPLETE set=$SET thiếu: $(echo $M | tr '\n' ' ') (xem logs/h100/${SET}_*.log)"; echo QUEUE_DONE; exit 1; fi
