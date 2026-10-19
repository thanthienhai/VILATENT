# Hướng dẫn chạy G0 và G1 (cho đội vận hành GPU)

Tài liệu này dành cho người chạy máy GPU. Mục tiêu là chạy hai cổng đầu của đề tài trên Qwen3.5 (`docs/VILATENT.md`
§Cổng quyết định và lộ trình) và gửi kết quả về cho chủ đề tài. Người chạy không cần hiểu phương pháp. Chỉ cần làm
đúng thứ tự, kiểm tra kết quả theo từng bảng và dừng lại ở những chỗ ghi **Dừng**.

- **G0, tuần 1–2:** kiểm tra hạ tầng Qwen3.5 (đọc `inputs_embeds`, lan truyền ngược qua Gated DeltaNet, giải mã)
  trên Qwen3.5-2B và 9B.
- **G1, tuần 3:** huấn luyện bộ ghi trên Qwen3.5-2B và so với các mốc nén cứng trên ViQuAD dev ở tỉ lệ nén 4×.
  Chỉ chạy G1 khi G0 đạt.

Nguyên tắc chung:

- Chạy đúng commit được giao. Mỗi file `.meta.json` ghi lại `git_commit`, nên đừng sửa code trên máy chạy. Nếu cần
  sửa, báo chủ đề tài để có commit mới.
- Không đổi file trong `configs/` và không đổi tiêu chí của cổng.
- Không dùng tập test (`data/tasks/viquad_test.jsonl`) ở G0 hay G1. Các script G1 chỉ đọc dev.
- Muốn bỏ hay cắt bớt lượt chạy nào, phải hỏi chủ đề tài trước.
- Mọi lệnh chạy ở thư mục gốc của repo.

## 0. Yêu cầu máy

| Hạng mục | Yêu cầu |
| --- | --- |
| GPU | GPU có bf16, khuyến nghị H100 80 GB. 1 GPU là đủ. Nếu có nhiều GPU, đặt `GPUS="0 1 …"` để các lượt độc lập chạy song song, mỗi lượt trên một GPU |
| Hệ điều hành | Linux, có CUDA toolkit (`nvcc`) khớp với bản CUDA của torch, để build `causal-conv1d` |
| Đĩa | Nên có ≥ 100 GB trống (ước lượng): bộ nhớ đệm Hugging Face khoảng 30 GB (Qwen3.5-2B và 9B, xlm-roberta-large của LLMLingua-2, Wikipedia tiếng Việt); `data/` vài GB (logit thầy của cặp giai đoạn 1 khoảng 1,5 GB); `runs/` khoảng 1 GB mỗi checkpoint × 9 |
| RAM | ≥ 32 GB |
| Mạng | Truy cập được Hugging Face Hub (mô hình và dataset). Bước `qa_gen` cần thêm endpoint thầy iCOMM `http://172.16.9.11:30048/v1` trong mạng nội bộ |

Môi trường đã chạy thử toàn bộ luồng (Kaggle, 2× T4, fp16, quy mô nhỏ): Python 3.13, torch 2.11.0+cu128,
transformers 5.16.1, flash-linear-attention 0.5.2, causal-conv1d 1.7.0, datasets 4.8.5. Ngày 19/10/2026, G0 đạt trên
cả 2B và 9B ở đó với reader int4 (9B không tính gradient lớp bộ ghi vì T4 không đủ bộ nhớ). **Chưa** chạy thử trên
bf16 và H100, nên bước 2 bên dưới là bắt buộc.

## 1. Cài đặt

```bash
git clone https://github.com/thanthienhai/VILATENT.git && cd VILATENT
git checkout <commit hoặc nhánh được giao>
python -m venv .venv && source .venv/bin/activate
# transformers ghim ở 5.16.1: G0 nhận diện kernel DeltaNet theo cách của 5.12 và 5.16 (5.13–5.15 chưa kiểm)
pip install -e ".[dev,model,data,baselines,teacher]" "transformers==5.16.1" flash-linear-attention
# causal-conv1d phải build từ source; 9.0 là kiến trúc của H100 (A100: 8.0). Mất một lúc.
TORCH_CUDA_ARCH_LIST=9.0 MAX_JOBS=8 pip install --no-build-isolation causal-conv1d
python -c "import torch, transformers, fla, causal_conv1d; print(torch.__version__, transformers.__version__, torch.cuda.is_available())"
pytest -q                                   # 36 passed (chạy trên CPU)
export HF_TOKEN=...                         # không bắt buộc (Qwen3.5 không gated), nhưng tránh bị giới hạn tốc độ tải
mkdir -p logs
```

Các lệnh chạy lâu nên để trong `tmux` hoặc `screen` và ghi log bằng `tee`, như các ví dụ bên dưới. `logs/` không đưa
lên git.

## 2. Thử nhanh trên máy chạy (khoảng 15 phút, bắt buộc)

Việc này kiểm tra đường bf16 trên đúng máy sẽ chạy G1. Chạy trong **một bản sao riêng** của repo, vì script ghi
`data/`, `runs/`, `results/` và từ chối chạy nếu các thư mục này đã có:

```bash
git clone . ../VILATENT-smoke && cd ../VILATENT-smoke
# PYTHONPATH: dùng mã của bản sao, không phải bản cài editable trỏ về repo chính
PYTHONPATH=$PWD DTYPE=bfloat16 GPUS="0" SMOKE_SHORT=1 bash scripts/smoke_g1.sh 2>&1 | tee ../VILATENT/logs/smoke.log
cd ../VILATENT
```

Với nhiều GPU, đặt `GPUS="0 1"` cho nhanh hơn.

`SMOKE_SHORT=1` chạy mọi giai đoạn của G1 (trừ G0 và `qa_gen`) với vài chục mẫu và 16 bước huấn luyện. Kết quả đạt khi:

- Dòng cuối của log là `smoke: done; …`, và lệnh trả về exit 0.
- `results/g1_dev/g1_report_r4.json` có mặt, kèm một bảng 13 phương pháp trong log.

Dòng `G1: FAIL` ở cuối bảng là **bình thường**: với 16 bước, bộ ghi chưa học được gì. Số liệu của lượt thử không có
giá trị làm bằng chứng. Nếu lệnh dừng với lỗi: **Dừng**, gửi `logs/smoke.log`. Chạy xong thì xoá `../VILATENT-smoke`.

## 3. Tuần 1–2: dữ liệu, template, G0

```bash
bash scripts/run_g1.sh data template g0 2>&1 | tee -a logs/g0.log
```

| Bước | Sinh ra | Kiểm tra |
| --- | --- | --- |
| `data` | `data/tasks/viquad_{train,dev,test}.jsonl`, `viquad_train_clean.jsonl`, `data/corpus/docs.jsonl`, `data/stage1/pairs_{train,dev}.jsonl`, mỗi file kèm `*.meta.json` | <ul><li>Log in `viquad dev: 1175 answerable questions, 250 passages` và `viquad test: 2653 …, 557 passages` (trùng split ViWord-C)</li><li>Lọc rò rỉ in `{"n_input": 18063, "kept": …, "dropped": …}`</li><li>`docs.jsonl.meta.json` ghi số bài bị loại theo tiêu đề và theo n-gram</li><li>`pairs_train.jsonl` có 96.000 dòng, `pairs_dev.jsonl` có 1.000 dòng</li></ul> |
| `template` | `configs/readers/qwen3.5-{2b,9b}.json` | <ul><li>Lượt trả lời bắt đầu bằng `<think>\n\n</think>\n\n`</li><li>`git diff configs/readers` phải rỗng. Nếu khác, nghĩa là thư viện đã render template khác bản đã commit: ghi lại khác biệt và báo chủ đề tài trước khi sang G1, vì logit thầy và checkpoint gắn với hash của template</li></ul> |
| `g0` | `results/g0/Qwen_Qwen3.5-2B.json`, `results/g0/Qwen_Qwen3.5-9B.json` | `G0_pass: true` cho cả hai reader |

Bước `data` duyệt toàn bộ Wikipedia tiếng Việt (1,29 triệu bài) và một phần BKAINewsCorpus. Chỉ khoảng 147 nghìn bài
Wikipedia dài từ 1.500 ký tự trở lên, nên `docs.jsonl` có ít hơn 200.000 bài Wikipedia là **bình thường**: script
lấy hết các bài đủ dài.

G0 gồm các kiểm tra sau (mỗi mục là một khoá trong file JSON):

- `load`: nạp chỉ phần ngôn ngữ (`vision_params = 0`) và không thiếu key nào của checkpoint (`missing_keys` rỗng).
  Thiếu key thì trọng số đó bị khởi tạo ngẫu nhiên, trong khi các kiểm tra khác vẫn có thể pass.
- `load.fast_deltanet_kernels` phải là `true`. `load.deltanet_kernels` cho biết từng kernel đang dùng `fla…`,
  `causal_conv1d…` hay `torch`. Có mục nào là `torch` thì chưa cài đủ kernel (mục 1).
- `embeds`: logit từ `input_ids` trùng logit từ `inputs_embeds`.
- `decode`: giải mã greedy từ `inputs_embeds` trùng `model.generate`. `full_context_f1` của 3 câu mẫu chỉ để kiểm
  tra trọng số có hợp lý, không dùng làm cổng.
- `backward`: gradient về memory, adapter và lớp đầu của bộ ghi hữu hạn và khác 0 sau khi đi qua mọi lớp DeltaNet.
  Mục này cũng ghi thời gian (`step_seconds`) và bộ nhớ đỉnh (`peak_mem_gb`) của một bước. Lần đầu có thể chậm vì
  Triton biên dịch kernel.
- `first_token`: chuẩn trạng thái ẩn của token đầu chuỗi, so khi có và không có token mồi.
- `llmlingua2`: mốc LLMLingua-2 nạp được và nén một đoạn mẫu trong ngân sách 4×. G1 trượt nếu thiếu một mốc cứng,
  nên lỗi cài đặt `llmlingua` phải lộ ra ngay ở đây.

Nếu `decode.warning` báo batch có padding lệch với chạy từng câu, hãy gửi file JSON. Lỗi này không làm G0 trượt,
nhưng cần được xem trước G1.

Khi một reader không đạt, `g0_check.py` trả về exit 1 và `run_g1.sh` dừng ngay. Vì vậy, nếu 2B trượt thì 9B không
được kiểm tra; muốn kiểm tra riêng 9B thì chạy `G0_READERS=Qwen/Qwen3.5-9B bash scripts/run_g1.sh g0`.

**G0 không đạt: Dừng.** Gửi `results/g0/*.json` cùng `logs/g0.log`. Phương án dự phòng (Qwen2.5-1.5B và 7B với
L = 2) chỉ được dùng khi chủ đề tài đồng ý.

### Chạy ngầm từ tuần 1: QA sinh tự động

G1 **không** dùng dữ liệu này (nó dành cho tuần 4–6), nhưng nên chạy ngầm ngay từ tuần 1. Bước này cần endpoint thầy,
và script tự chạy tiếp được nếu bị ngắt:

```bash
QA_GPU=1 nohup bash scripts/run_g1.sh qa_gen > logs/qa_gen.log 2>&1 &
```

Cuối bước, `filter_qa` nạp reader lên GPU `QA_GPU` (mặc định là GPU cuối trong `GPUS`). Khi G1 chạy cùng lúc, đặt
`QA_GPU` là một GPU mà G1 không dùng. Nếu chỉ có 1 GPU, chạy `qa_gen` sau khi G1 xong.

Bước này chưa từng chạy thử, vì endpoint chỉ có trong mạng nội bộ. Nếu lỗi, gửi `logs/qa_gen.log`; việc này không
chặn G1. Cuối bước, script in tỉ lệ câu bị loại ở bước kiểm tra hai chiều. Nếu tỉ lệ vượt 20%, cần người kiểm tra
200 mẫu (bảng rủi ro trong `docs/VILATENT.md`).

## 4. Tuần 3: G1 trên Qwen3.5-2B ở 4×

Chỉ chạy khi cả hai file G0 có `G0_pass: true`.

```bash
GPUS="0" bash scripts/run_g1.sh teacher stage1 stage2 eval select fallback report 2>&1 | tee -a logs/g1.log
```

Với nhiều GPU, ví dụ `GPUS="0 1 2 3"`. Có thể chạy từng bước một (ví dụ `… run_g1.sh teacher`, rồi
`… run_g1.sh stage1`, …), vì mỗi bước chỉ đọc file do bước trước ghi ra.

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `teacher` | top-20 log-prob của thầy trên cặp giai đoạn 1 và ViQuAD train/dev (dùng chung cho mọi cấu hình) | `data/teacher/qwen3.5-2b/{pairs_train,pairs_dev,viquad_train,viquad_dev}.pt` |
| `stage1` | O-LM rút gọn, 2.500 bước × batch 32, bốn bộ ghi: 4× (cho M, W5) và 8×, 16×, 32× (cho ME với f = 2, 4, 8) | `runs/g1_stage1_r{4,8,16,32}/{best.pt,metrics.jsonl,config.json}` |
| `stage2` | chưng cất theo đáp án trên ViQuAD train, 2.000 bước, năm lượt: ME f = 2, 4, 8 (có câu gốc BM25 trong đầu vào), M, W5 | `runs/g1_stage2_{me_f2,me_f4,me_f8,m,w5}_r4/…` |
| `eval` | full, none, truncation, lead, bm25, llmlingua2 và năm cấu hình ViLatent trên ViQuAD dev | `results/g1_dev/*.jsonl`, `*.summary.json` |
| `select` | chọn f của ME theo loss dev giai đoạn 2 (không theo F1 dev) | `results/g1_dev/me_choice_r4.json`, `vilatent_me_r4.jsonl` |
| `fallback` | MEF: đường đánh đổi và ngưỡng τ nhỏ nhất đạt ≥ 95% F1 toàn văn | `results/g1_dev/mef_{curve,tau}_r4.json`, `vilatent_mef_r4.jsonl` |
| `report` | ME so với mốc cứng tốt nhất (cả trong từng nhóm có và không dùng câu hỏi), bootstrap theo đoạn, MDE; W5 − M và ME − M (mô tả) | `results/g1_dev/g1_report_r4.json` và một bảng trong log |

### Theo dõi khi huấn luyện

Mỗi lượt ghi `runs/<tên>/metrics.jsonl`, mỗi sự kiện một dòng JSON. Xem nhanh:

```bash
tail -n 3 runs/*/metrics.jsonl
```

- Dòng `train` (mỗi 10 bước) có `loss`, `ce`, `kl`, `grad_norm`, `mem_norm` (chuẩn của memory) cạnh `emb_norm` (chuẩn
  embedding), `sec_per_step` và `peak_mem_gb`. `loss` phải hữu hạn. `mem_norm` không nên lệch `emb_norm` nhiều bậc.
- Dòng `eval` (mỗi 250 bước) có `dev_loss`. `best: true` nghĩa là `best.pt` vừa được ghi lại.
- Dòng `end` ghi `best_dev_loss` và số giờ đã chạy.

**Báo sớm thời gian chạy.** Khoảng 30 phút sau khi `stage1` bắt đầu, gửi `sec_per_step` và `peak_mem_gb` của từng
lượt đang chạy. Số giờ H100 của G1 ≈ `sec_per_step` × số bước, cộng dồn qua 9 lượt. Tài liệu đề tài yêu cầu đo lại
con số này. Nếu quá ngân sách GPU, chủ đề tài sẽ quyết định cắt lượt nào (thứ tự ưu tiên: ba lượt ME là bắt buộc;
W5 có thể dời sang tuần 4–6; f = 8 có thể bỏ).

Ở bước đầu tiên, vòng huấn luyện tự kiểm tra gradient về bộ ghi và dừng với lỗi nếu gradient không hữu hạn hoặc bằng
0. Các cảnh báo sau là bình thường và có thể bỏ qua:

- `You are sending unauthenticated requests to the HF Hub`: chưa đặt `HF_TOKEN`.
- `Converting a tensor with requires_grad=True to a scalar`: phát ra từ chỗ ghi log loss.

Huấn luyện **không có chế độ chạy tiếp**. Nếu một lượt bị ngắt, chạy lại đúng lệnh của lượt đó. Lệnh được in trong log
ở dòng `GPU <n>: python scripts/train.py --config …`. Lượt mới xoá `best.pt` cũ và ghi lại `metrics.jsonl` từ đầu. Các
lượt `stage2` cần `best.pt` của lượt `stage1` tương ứng.

Khi một lượt lỗi, các lượt xếp sau nó trên **cùng GPU** không chạy, và log in dòng `GPU <n>: skipped (an earlier run on
this GPU failed): …` cho từng lượt bị bỏ. Phải chạy lại cả lượt lỗi lẫn các lượt bị bỏ, hoặc chạy lại cả bước.

### Tiêu chí G1 (cố định trước khi chạy)

Trên ViQuAD dev ở 4×, G1 đạt khi thoả cả ba điều kiện:

1. F1 của ViLatent-ME (f chọn theo loss dev) trừ F1 của mốc cứng tốt nhất ≥ 3 điểm.
2. Cận dưới CI 95% (bootstrap theo đoạn văn) > 0.
3. Tỉ lệ câu trả lời không đọc được dưới 2% với ViLatent-ME và cả bốn mốc cứng. Với các phương pháp còn lại (full,
   none, M, W5, MEF, các f khác), tỉ lệ này chỉ được báo cáo kèm cảnh báo.

Kết quả nằm ở `G1_pass` trong `results/g1_dev/g1_report_r4.json`, và ở dòng `G1: PASS` hoặc `G1: FAIL` cuối log.
Người chạy không cần diễn giải kết quả. Chỉ cần gửi về.

**G1 không đạt:** không chạy gì thêm, gửi kết quả. Chủ đề tài sẽ quyết định thử W2 hay chuyển sang Hướng B
(`docs/VILATENT.md`). Không chạy reader 9B khi chưa qua G1.

## 5. Gửi kết quả

```bash
tar czf vilatent_g0_g1.tgz logs results/g0 results/g1_dev runs/*/metrics.jsonl runs/*/config.json data/*/*.meta.json
```

Gói này nhỏ (vài MB). Kèm thêm:

- Kết quả của `git rev-parse HEAD` và `pip freeze`.
- Kết quả của `nvidia-smi --query-gpu=name,memory.total --format=csv`.

Giữ lại trên máy chạy (không xoá) `runs/*/best.pt` và `data/`, vì tuần 4–6 dùng lại chúng. Chỉ gửi đi khi được yêu
cầu, vì dung lượng khoảng chục GB.

## 6. Sự cố thường gặp

| Triệu chứng | Nguyên nhân thường gặp | Cách xử lý |
| --- | --- | --- |
| `fast_deltanet_kernels: false`; trong `deltanet_kernels` có mục là `torch` | thiếu `flash-linear-attention` hoặc `causal-conv1d`, hoặc bản build không khớp torch | cài lại theo mục 1, kiểm tra `python -c "import fla, causal_conv1d"`, rồi chạy lại `run_g1.sh g0` |
| Build `causal-conv1d` lỗi | không có `nvcc`, hoặc `TORCH_CUDA_ARCH_LIST` sai | cài CUDA toolkit khớp với `torch.version.cuda`; đặt đúng kiến trúc GPU |
| `smoke_g1: data/ exists` | chạy thử trong repo chính | chạy trong bản sao riêng (mục 2) |
| `CUDA out of memory` khi huấn luyện | micro-batch 8 không vừa GPU | giữ nguyên batch hiệu dụng và giảm micro-batch: `TRAIN_ARGS="--micro-batch 4" bash scripts/run_g1.sh stage1 …`; ghi lại trong báo cáo |
| `gradient check failed on the writer …` ở bước đầu (với fp16: `gradients still not finite after 20 steps`) | lỗi số học hoặc lỗi cài đặt | **Dừng**, gửi `logs/` và `runs/<tên>/metrics.jsonl` |
| `only N wiki pairs for M wanted: build a larger corpus` | corpus quá ít bài đủ dài | **Dừng**, gửi `data/corpus/docs.jsonl.meta.json` |
| `N examples have no teacher` | dữ liệu đã thay đổi sau khi chạy `teacher` | chạy lại `run_g1.sh teacher` rồi các bước sau |
| `… was trained with another reader template`, `template differs` hoặc `teacher computed with another template` | `configs/readers/*.json` bị render lại sau khi đã tính logit thầy hoặc đã huấn luyện | khôi phục bằng `git checkout configs/readers`, hoặc chạy lại từ `teacher`; báo chủ đề tài |
| Một bước in xong kết quả nhưng tiến trình không thoát, không dùng CPU | lỗi treo khi thoát sau khi đọc dataset dạng streaming (đã sửa trong `build_corpus.py`) | nếu gặp lại ở bước nào, ghi tên bước, dừng bằng Ctrl+C, rồi báo chủ đề tài |
| Tải Hugging Face chậm hoặc lỗi 429 | giới hạn tốc độ khi chưa đăng nhập | đặt `HF_TOKEN` |

Trên GPU không có bf16 (ví dụ T4), đặt `DTYPE=float16`: reader chạy fp16, bộ ghi dùng autocast fp16 và loss được
scale bằng GradScaler. Khoảng 10 bước đầu bị bỏ qua là bình thường, vì GradScaler đang tìm hệ số scale. Kết quả fp16
chỉ dùng để thử đường chạy, không dùng làm bằng chứng cho G0 hay G1.

## Phụ lục: biến môi trường của `scripts/run_g1.sh`

| Biến | Mặc định | Ý nghĩa |
| --- | --- | --- |
| `GPUS` | `0` | danh sách GPU. Các lượt độc lập (logit thầy, bốn lượt giai đoạn 1, năm lượt giai đoạn 2, hai nhóm đánh giá) chia vòng tròn cho các GPU này |
| `DTYPE` | `bfloat16` | `float16` chỉ dùng cho GPU không có bf16 |
| `READER`, `READER_9B`, `SLUG`, `RATIO` | `Qwen/Qwen3.5-2B`, `Qwen/Qwen3.5-9B`, `qwen3.5-2b`, `4` | không đổi cho G0 và G1 |
| `TEACHER_URL`, `TEACHER_MODEL` | endpoint iCOMM 27B | chỉ dùng cho `qa_gen` |
| `N_PAIRS`, `N_DEV_PAIRS`, `N_WIKI`, `N_NEWS` | 96.000, 1.000, 200.000, 200.000 | cỡ dữ liệu giai đoạn 1; giữ mặc định |
| `G0_READERS` | cả hai reader | reader được kiểm tra ở G0 (mục 3) |
| `TRAIN_ARGS`, `EVAL_ARGS` | rỗng | dành cho `scripts/smoke_g1.sh`. Ngoài lượt thử, `TRAIN_ARGS` chỉ dùng để giảm micro-batch khi thiếu bộ nhớ |
| `QUANT`, `G0_ARGS`, `SMOKE_9B` | `none`, rỗng, `0` | chỉ cho lượt thử trên Kaggle T4 (reader int4; G0 của 9B không tính gradient lớp bộ ghi). **Không dùng trên cụm**: kết quả int4 không phải bằng chứng cho G0/G1 |
