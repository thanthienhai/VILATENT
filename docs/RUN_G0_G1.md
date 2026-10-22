# Hướng dẫn chạy G0 và G1 (cho đội vận hành GPU)

Tài liệu này dành cho người chạy máy GPU. Mục tiêu là chạy hai cổng đầu của đề tài trên Qwen3.5 (`docs/VILATENT.md`
§Cổng quyết định và lộ trình) và gửi kết quả về cho chủ đề tài. Người chạy không cần hiểu phương pháp. Chỉ cần làm
đúng thứ tự, kiểm tra kết quả theo từng bảng và dừng lại ở những chỗ ghi **Dừng**.

- **G0:** kiểm tra hạ tầng Qwen3.5 (đọc `inputs_embeds`, lan truyền ngược qua Gated DeltaNet, giải mã)
  trên Qwen3.5-2B và 9B.
- **G1:** huấn luyện bộ ghi trên Qwen3.5-2B và so với các mốc nén cứng trên ViQuAD gate (các bài Wikipedia tách
  khỏi train) ở tỉ lệ nén 4×. Chỉ chạy G1 khi G0 đạt.
- **Sau G1:** lọc bộ QA sinh tự động bằng Qwen3.5-2B, khoảng 1,5–2 giờ trên một GPU.

Nguyên tắc chung:

- Chạy đúng commit được giao. Mỗi file `.meta.json` ghi lại `git_commit`, nên đừng sửa code trên máy chạy. Nếu cần
  sửa, báo chủ đề tài để có commit mới.
- Không đổi file trong `configs/` và không đổi tiêu chí của cổng.
- Không dùng tập test (`data/tasks/viquad_test.jsonl`) ở G0 hay G1; các bước lọc rò rỉ chỉ đọc phần ngữ cảnh của nó.
  Các script G1 đánh giá trên ViQuAD gate, select và dev của ViWord-C.
- Muốn bỏ hay cắt bớt lượt chạy nào, phải hỏi chủ đề tài trước.
- Mọi lệnh chạy ở thư mục gốc của repo.

## 0. Yêu cầu máy

| Hạng mục | Yêu cầu |
| --- | --- |
| GPU | GPU có bf16, khuyến nghị H100 80 GB. 1 GPU là đủ. Nếu có nhiều GPU, đặt `GPUS="0 1 …"` để các lượt độc lập chạy song song, mỗi lượt trên một GPU |
| Hệ điều hành | Linux, có CUDA toolkit (`nvcc`) khớp với bản CUDA của torch, để build `causal-conv1d` |
| Đĩa | Nên có ≥ 100 GB trống (ước lượng): bộ nhớ đệm Hugging Face khoảng 30 GB (Qwen3.5-2B và 9B, xlm-roberta-large của LLMLingua-2, Wikipedia tiếng Việt); `data/` vài GB (logit thầy của cặp giai đoạn 1 khoảng 1,5 GB); `runs/` khoảng 1 GB mỗi checkpoint × 9 |
| RAM | ≥ 32 GB |
| Mạng | Truy cập được Hugging Face Hub (mô hình và dataset, kể cả repo private `thanthienhai/vilatent-qa-gen` ở mục 5) và `dl.fbaipublicfiles.com` (file MLQA, 76 MB, chỉ để lọc rò rỉ). Không cần endpoint iCOMM: cụm không gọi nó |

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
pytest -q                                   # 46 passed (chạy trên CPU)
export HF_TOKEN=...                         # bắt buộc: token chủ đề tài cấp, đọc được repo private thanthienhai/vilatent-qa-gen
mkdir -p logs
```

`HF_TOKEN` cần cho bước lọc QA (mục 5) và cho phần QA của lượt thử ở mục 2. G0 và G1 không cần nó (Qwen3.5 không
gated), nhưng có token thì tải mô hình không bị giới hạn tốc độ. Không ghi token vào file trong repo.

Trên image container đã có sẵn torch trong một venv riêng (ví dụ `/opt/venv` của image `dynamo-lmcache-runtime`, torch
2.13.0+cu130, nvcc 13.0), `python -m venv --system-site-packages` không thấy torch đó. Khi ấy cài thẳng vào venv của
image và ghim torch đúng bản của image, để causal-conv1d build cùng bản CUDA. Cách này đã chạy được ngày 22/10/2026
(G0 đạt trên H100, bf16):

```bash
echo "torch==$(/opt/venv/bin/python -c 'import torch; print(torch.__version__.split("+")[0])')" > /tmp/constraints.txt
uv pip install --python /opt/venv/bin/python -c /tmp/constraints.txt -e ".[dev,model,data,baselines,teacher]" \
  "transformers==5.16.1" flash-linear-attention
TORCH_CUDA_ARCH_LIST=9.0 MAX_JOBS=24 uv pip install --python /opt/venv/bin/python -c /tmp/constraints.txt \
  --no-build-isolation causal-conv1d
```

Các lệnh chạy lâu nên để trong `tmux` hoặc `screen` và ghi log bằng `tee`, như các ví dụ bên dưới. `logs/` không đưa
lên git.

## 2. Thử nhanh trên máy chạy (khoảng 15 phút, bắt buộc)

Việc này kiểm tra đường bf16 trên đúng máy sẽ chạy G1. Chạy trong **một bản sao riêng** của repo, vì script ghi
`data/`, `runs/`, `results/` và từ chối chạy nếu các thư mục này đã có:

```bash
git clone . ../VILATENT-smoke && cd ../VILATENT-smoke
# PYTHONPATH: dùng mã của bản sao, không phải bản cài editable trỏ về repo chính
PYTHONPATH=$PWD DTYPE=bfloat16 GPUS="0" SMOKE_SHORT=1 SMOKE_QA=1 bash scripts/smoke_g1.sh 2>&1 | tee ../VILATENT/logs/smoke.log
cd ../VILATENT
```

Với nhiều GPU, đặt `GPUS="0 1"` cho nhanh hơn.

`SMOKE_SHORT=1` chạy mọi giai đoạn của G1 (trừ G0) với vài chục mẫu và 16 bước huấn luyện. `SMOKE_QA=1` chạy thêm
bước tải và lọc QA của mục 5 trên 500 câu, để kiểm tra sớm `HF_TOKEN`. Kết quả đạt khi:

- Dòng cuối của log là `smoke: done; …`, và lệnh trả về exit 0.
- `results/g1/gate/g1_report_r4.json` có mặt, kèm một bảng các phương pháp trong log (ViWord-C dev trước, ViQuAD gate
  sau).
- Log có một khối JSON với `"n_input": 500`, rồi đến dòng `=== qa_filter done`.

Dòng `G1: FAIL` ở cuối bảng là **bình thường**: với 16 bước, bộ ghi chưa học được gì. Dòng `WARNING: …% rejected by
the reader` sau khối JSON của QA cũng không phải lỗi. Số liệu của lượt thử không có
giá trị làm bằng chứng. Nếu lệnh dừng với lỗi: **Dừng**, gửi `logs/smoke.log`. Chạy xong thì xoá `../VILATENT-smoke`.

## 3. Dữ liệu, template, G0

```bash
bash scripts/run_g1.sh data template g0 2>&1 | tee -a logs/g0.log
```

| Bước | Sinh ra | Kiểm tra |
| --- | --- | --- |
| `data` | `data/tasks/viquad_{train,gate,select,viwordc_dev,test}.jsonl`, `viquad_train_clean.jsonl`, `data/eval_ext/*.jsonl` (MLQA-vi, Belebele-vi, VietNews: chỉ để lọc rò rỉ), `data/corpus/docs.jsonl` và `docs.dropped.jsonl`, `data/stage1/pairs_{train,dev}.jsonl`, mỗi file kèm `*.meta.json` | <ul><li>Log in `viquad train: 16318 …`, `viquad gate: 1228 answerable questions, 244 passages, 16 articles`, `viquad select: 621 …, 125 passages, 6 articles`, `viquad viwordc_dev: 1175 …, 250 passages` và `viquad test: 2653 …, 557 passages, 19 articles`</li><li>`mlqa vi test: 4795 paragraphs`, `belebele vi: 488 passages`, `vietnews test: 22498 articles`</li><li>Lọc rò rỉ in `{"n_input": 16318, "kept": 15706, "dropped": 612}`</li><li>`docs.jsonl.meta.json` ghi số bài bị loại theo tiêu đề và theo n-gram</li><li>`pairs_train.jsonl` có 96.000 dòng, `pairs_dev.jsonl` có 1.000 dòng</li></ul> |
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

Không chạy `qa_generate` trên cụm: câu hỏi đã được sinh ở ngoài cụm (cụm không gọi được endpoint iCOMM). Không cần
gửi corpus đi.

## 4. G1 trên Qwen3.5-2B ở 4×

Chỉ chạy khi cả hai file G0 có `G0_pass: true`.

```bash
GPUS="0" bash scripts/run_g1.sh teacher stage1 stage2 select stage2b eval fallback report 2>&1 | tee -a logs/g1.log
```

Với nhiều GPU, ví dụ `GPUS="0 1 2 3"`. Có thể chạy từng bước một (ví dụ `… run_g1.sh teacher`, rồi
`… run_g1.sh stage1`, …), vì mỗi bước chỉ đọc file do bước trước ghi ra.

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `teacher` | top-20 log-prob của thầy trên cặp giai đoạn 1 và ViQuAD train/select (dùng chung cho mọi cấu hình) | `data/teacher/qwen3.5-2b/{pairs_train,pairs_dev,viquad_train,viquad_select}.pt` |
| `stage1` | O-LM rút gọn, 2.500 bước × batch 32, bốn bộ ghi: 4× (cho M, W5) và 8×, 16×, 32× (cho ME với f = 2, 4, 8) | `runs/g1_stage1_r{4,8,16,32}/{best.pt,metrics.jsonl,config.json}` |
| `stage2` | chưng cất theo đáp án trên ViQuAD train, 2.000 bước, năm lượt: ME f = 2, 4, 8 (có câu gốc BM25 trong đầu vào), M, W5; checkpoint chọn theo loss trên ViQuAD select | `runs/g1_stage2_{me_f2,me_f4,me_f8,m,w5}_r4/…` |
| `select` | chọn f* của ME theo loss giai đoạn 2 trên ViQuAD select (không theo F1 nào) | `results/g1/me_choice_r4.json` |
| `stage2b` | ở f*: ME với seed 1, và đối chứng "prompt học được + BM25" với lr 1e-4 và 1e-3 (ba lượt), rồi chọn lr của đối chứng theo loss trên select | `runs/g1_stage2_me_f*_s1_r4/…`, `runs/g1_stage2_prompt_f*_lr{1e-4,1e-3}_r4/…`, `results/g1/pe_choice_r4.json` |
| `eval` | ViQuAD gate: full, none, truncation, lead, bm25, llmlingua2, ME f = 2, 4, 8 (thêm bản đổi memory), ME f* seed 1, M, W5, đối chứng. ViQuAD select: full và ME f*. Dev của ViWord-C (bảng phụ): tham chiếu, mốc cứng, ME f*, M, W5 | `results/g1/{gate,select,viwordc}/*.jsonl`, `*.summary.json` |
| `fallback` | MEF: chọn τ nhỏ nhất đạt ≥ 95% F1 toàn văn trên select, rồi áp nguyên cho gate và dev của ViWord-C | `results/g1/select/mef_{curve,tau}_r4.json`, `vilatent_mef_r4.jsonl` trong từng thư mục |
| `report` | bảng phụ trên dev của ViWord-C, rồi quyết định G1 trên gate: ME so với mốc cứng tốt nhất và với đối chứng, bootstrap theo seed × đoạn, thêm CI theo bài, MDE, các cặp mô tả | `results/g1/viwordc/report_r4.json`, `results/g1/gate/g1_report_r4.json` và hai bảng trong log |

### Theo dõi khi huấn luyện

Mỗi lượt ghi `runs/<tên>/metrics.jsonl`, mỗi sự kiện một dòng JSON. Xem nhanh:

```bash
tail -n 3 runs/*/metrics.jsonl
```

- Dòng `train` (mỗi 10 bước) có `loss`, `ce`, `kl`, `grad_norm`, `mem_norm` (chuẩn của memory) cạnh `emb_norm` (chuẩn
  embedding), `sec_per_step` (trung bình từ bước 1, bị bước đầu biên dịch kernel kéo lên), `sec_per_step_recent` (tốc
  độ của các bước kể từ dòng `train` trước, không tính thời gian eval) và `peak_mem_gb`. `loss` phải hữu hạn.
  `mem_norm` không nên lệch `emb_norm` nhiều bậc. `grad_norm` lớn (hàng chục đến hàng trăm, nhất là ở M và W5) là
  bình thường vì gradient được cắt về 1,0; điều cần xem là `dev_loss` giảm dần.
- Dòng `eval` (mỗi 250 bước) có `dev_loss`. `best: true` nghĩa là `best.pt` vừa được ghi lại.
- Dòng `end` ghi `best_dev_loss` và số giờ đã chạy.

**Báo sớm thời gian chạy.** Khoảng 30 phút sau khi `stage1` bắt đầu, gửi `sec_per_step_recent` và `peak_mem_gb` của
từng lượt đang chạy. Số giờ H100 của G1 ≈ `sec_per_step_recent` × số bước, cộng dồn qua 12 lượt (lượt thử ngày
22/10/2026 ở micro-batch 8: khoảng 1 s/bước, tổng phần huấn luyện khoảng 7 giờ GPU). Không tự cắt lượt nào: nếu quá
ngân sách GPU, chủ đề tài sẽ báo lượt cần bỏ.

Ở bước đầu tiên, vòng huấn luyện tự kiểm tra gradient về bộ ghi và dừng với lỗi nếu gradient không hữu hạn hoặc bằng
0. Các cảnh báo sau là bình thường và có thể bỏ qua:

- `You are sending unauthenticated requests to the HF Hub`: chưa đặt `HF_TOKEN`.
- `TileLang begins to compile kernel`: flash-linear-attention biên dịch kernel ở bước đầu.

Huấn luyện **không có chế độ chạy tiếp**. Nếu một lượt bị ngắt, chạy lại đúng lệnh của lượt đó. Lệnh được in trong log
ở dòng `GPU <n>: python scripts/train.py --config …`. Lượt mới xoá `best.pt` cũ và ghi lại `metrics.jsonl` từ đầu. Các
lượt `stage2` cần `best.pt` của lượt `stage1` tương ứng.

Khi một lượt lỗi, các lượt xếp sau nó trên **cùng GPU** không chạy, và log in dòng `GPU <n>: skipped (an earlier run on
this GPU failed): …` cho từng lượt bị bỏ. Phải chạy lại cả lượt lỗi lẫn các lượt bị bỏ, hoặc chạy lại cả bước.

### Tiêu chí G1 (cố định trước khi chạy)

Trên ViQuAD gate ở 4× (sửa ngày 22/10/2026), với ViLatent-ME là f* (chọn theo loss trên select) gộp hai seed, G1
đạt khi thoả cả ba điều kiện:

1. F1 của ViLatent-ME trừ F1 của mốc cứng tốt nhất ≥ 3 điểm, và cận dưới CI 95% (bootstrap theo seed × đoạn văn) > 0.
2. Cận dưới CI 95% của F1 ViLatent-ME trừ F1 đối chứng "prompt học được + BM25" > 0.
3. Tỉ lệ câu trả lời không đọc được dưới 2% với ViLatent-ME và mốc cứng tốt nhất. Với các phương pháp còn lại, tỉ
   lệ này chỉ được báo cáo kèm cảnh báo.

Kết quả nằm ở `G1_pass` (và từng điều kiện ở `conditions`) trong `results/g1/gate/g1_report_r4.json`, và ở dòng
`G1: PASS` hoặc `G1: FAIL` cuối log.
Người chạy không cần diễn giải kết quả. Chỉ cần gửi về.

**G1 không đạt:** chỉ chạy thêm mục 5 (lọc QA), rồi gửi kết quả và chờ chủ đề tài báo bước tiếp theo. Không chạy
reader 9B khi chưa qua G1.

## 5. Sau G1: lọc QA sinh tự động (khoảng 1,5–2 giờ)

G1 không dùng bộ QA này. Chạy sau khi G1 xong, dù G1 đạt hay không:

```bash
bash scripts/run_g1.sh qa_download qa_filter 2>&1 | tee -a logs/qa_filter.log
```

| Bước | Việc | Sinh ra | Kiểm tra |
| --- | --- | --- | --- |
| `qa_download` | tải `qa_raw.jsonl` (57 MB) và file meta từ repo private, đúng revision `QA_REVISION`, rồi so SHA-256 | `data/qa_gen/qa_raw.jsonl`, `qa_raw.jsonl.meta.json` | không có dòng `does not match its meta sha256` |
| `qa_filter` | bỏ câu sinh từ bài bị loại khỏi corpus và câu trùng n-gram với tập đánh giá, luật lọc, rồi Qwen3.5-2B đọc đoạn văn đầy đủ và trả lời từng câu (khoảng 52 nghìn câu, một GPU), giữ câu đạt F1 ≥ 0,8. Cần `data/corpus/docs.dropped.jsonl` của bước `data` | `data/qa_gen/qa_clean.jsonl`, `qa_clean.jsonl.meta.json` | log in một khối JSON có `"n_input": 55480`, `"leaked"` và `"kept"` |

Thời gian ngoại suy từ lượt thử trên H100 ngày 22/10/2026 (478 câu trong 71 giây, kể cả nạp mô hình). `qa_filter` chỉ dùng một GPU, dù `GPUS` có nhiều GPU. Nếu log in `WARNING:
…% rejected by the reader (> 20%)` thì **không phải lỗi**, cứ gửi kết quả về: chủ đề tài sẽ xử lý theo bảng rủi ro.

## 6. Gửi kết quả

```bash
tar czf vilatent_g0_g1.tgz logs results/g0 results/g1 runs/*/metrics.jsonl runs/*/config.json data/*/*.meta.json
```

Gói này nhỏ (vài MB) và đã gồm thống kê lọc QA (`data/qa_gen/qa_clean.jsonl.meta.json`). Kèm thêm:

- Kết quả của `git rev-parse HEAD` và `pip freeze`.
- Kết quả của `nvidia-smi --query-gpu=name,memory.total --format=csv`.

Giữ lại trên máy chạy (không xoá) `runs/*/best.pt` và `data/` (kể cả `data/qa_gen/qa_clean.jsonl`), vì các bước
sau dùng lại chúng. Chỉ gửi đi khi được yêu cầu, vì dung lượng khoảng chục GB.

## 7. Sự cố thường gặp

| Triệu chứng | Nguyên nhân thường gặp | Cách xử lý |
| --- | --- | --- |
| `fast_deltanet_kernels: false`; trong `deltanet_kernels` có mục là `torch` | thiếu `flash-linear-attention` hoặc `causal-conv1d`, hoặc bản build không khớp torch | cài lại theo mục 1, kiểm tra `python -c "import fla, causal_conv1d"`, rồi chạy lại `run_g1.sh g0` |
| Build `causal-conv1d` lỗi | không có `nvcc`, hoặc `TORCH_CUDA_ARCH_LIST` sai | cài CUDA toolkit khớp với `torch.version.cuda`; đặt đúng kiến trúc GPU |
| `smoke_g1: data/ exists` | chạy thử trong repo chính | chạy trong bản sao riêng (mục 2) |
| `CUDA out of memory` khi huấn luyện | micro-batch 32 không vừa GPU (trên H100 80 GB ước tính khoảng 20 GB) | giữ nguyên batch hiệu dụng và giảm micro-batch: `TRAIN_ARGS="--micro-batch 16" bash scripts/run_g1.sh stage1 …`; ghi lại trong báo cáo |
| `gradient check failed on the writer …` ở bước đầu (với fp16: `gradients still not finite after 20 steps` hoặc `no step out of N had finite gradients`), hoặc `dev loss was never finite` | lỗi số học hoặc lỗi cài đặt | **Dừng**, gửi `logs/` và `runs/<tên>/metrics.jsonl` |
| `only N wiki pairs for M wanted: build a larger corpus` | corpus quá ít bài đủ dài | **Dừng**, gửi `data/corpus/docs.jsonl.meta.json` |
| `N examples have no teacher` | dữ liệu đã thay đổi sau khi chạy `teacher` | chạy lại `run_g1.sh teacher` rồi các bước sau |
| `… was trained with BM25 {…}, not those of configs/bm25.json` | `configs/bm25.json` bị sửa sau khi huấn luyện ME | khôi phục bằng `git checkout configs/bm25.json`; file này đã được dò sẵn trước G1, không chạy lại `tune_bm25.py` trên cụm |
| `… was trained with another reader template`, `template differs` hoặc `teacher computed with another template` | `configs/readers/*.json` bị render lại sau khi đã tính logit thầy hoặc đã huấn luyện | khôi phục bằng `git checkout configs/readers`, hoặc chạy lại từ `teacher`; báo chủ đề tài |
| Một bước in xong kết quả nhưng tiến trình không thoát, không dùng CPU | lỗi treo khi thoát sau khi đọc dataset dạng streaming (đã sửa trong `build_corpus.py`) | nếu gặp lại ở bước nào, ghi tên bước, dừng bằng Ctrl+C, rồi báo chủ đề tài |
| Tải Hugging Face chậm hoặc lỗi 429 | giới hạn tốc độ khi chưa đăng nhập | đặt `HF_TOKEN` |
| `qa_download` lỗi 401, 403, 404 hoặc `Repository Not Found` | chưa đặt `HF_TOKEN`, hoặc token không đọc được repo private | xin chủ đề tài token có quyền đọc `thanthienhai/vilatent-qa-gen`, rồi chạy lại `run_g1.sh qa_download qa_filter` |
| `qa_raw.jsonl does not match its meta sha256` | file tải về hỏng hoặc sai revision | **Dừng**, gửi `logs/qa_filter.log` |

Trên GPU không có bf16 (ví dụ T4), đặt `DTYPE=float16`: reader chạy fp16, bộ ghi dùng autocast fp16 và loss được
scale bằng GradScaler. Khoảng 10 bước đầu bị bỏ qua là bình thường, vì GradScaler đang tìm hệ số scale. Kết quả fp16
chỉ dùng để thử đường chạy, không dùng làm bằng chứng cho G0 hay G1.

## Phụ lục: biến môi trường của `scripts/run_g1.sh`

| Biến | Mặc định | Ý nghĩa |
| --- | --- | --- |
| `GPUS` | `0` | danh sách GPU. Các lượt độc lập (logit thầy, bốn lượt giai đoạn 1, năm lượt giai đoạn 2, hai nhóm đánh giá) chia vòng tròn cho các GPU này |
| `DTYPE` | `bfloat16` | `float16` chỉ dùng cho GPU không có bf16 |
| `READER`, `READER_9B`, `SLUG`, `RATIO` | `Qwen/Qwen3.5-2B`, `Qwen/Qwen3.5-9B`, `qwen3.5-2b`, `4` | không đổi cho G0 và G1 |
| `TEACHER_URL`, `TEACHER_MODEL` | endpoint iCOMM 27B | chỉ dùng cho `qa_generate`, chạy ngoài cụm |
| `QA_REPO`, `QA_REVISION` | `thanthienhai/vilatent-qa-gen`, `28e3ac26…` | repo HF private chứa QA sinh tự động, cho `qa_download` (mục 5). Cần `HF_TOKEN` có quyền đọc repo này; giữ mặc định |
| `SMOKE_QA`, `SMOKE_QA_ROWS` | `0`, `500` | `SMOKE_QA=1` (mục 2): `smoke_g1.sh` chạy thêm `qa_download` và `qa_filter` trên 500 câu đầu (cần `HF_TOKEN` như trên) |
| `N_PAIRS`, `N_DEV_PAIRS`, `N_WIKI`, `N_NEWS` | 96.000, 1.000, 200.000, 200.000 | cỡ dữ liệu giai đoạn 1; giữ mặc định |
| `G0_READERS` | cả hai reader | reader được kiểm tra ở G0 (mục 3) |
| `TRAIN_ARGS`, `EVAL_ARGS` | rỗng | dành cho `scripts/smoke_g1.sh`. Ngoài lượt thử, `TRAIN_ARGS` chỉ dùng để giảm micro-batch khi thiếu bộ nhớ |
| `QUANT`, `G0_ARGS`, `SMOKE_9B` | `none`, rỗng, `0` | chỉ cho lượt thử trên Kaggle T4 (reader int4; G0 của 9B không tính gradient lớp bộ ghi). **Không dùng trên cụm**: kết quả int4 không phải bằng chứng cho G0/G1 |
