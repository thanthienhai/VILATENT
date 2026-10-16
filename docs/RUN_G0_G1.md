# Hướng dẫn chạy G0 và G1

Lộ trình theo `docs/VILATENT.md` §Cổng quyết định và lộ trình. Mỗi giai đoạn của `scripts/run_g1.sh` chỉ đọc file do
giai đoạn trước ghi ra, nên có thể chạy các giai đoạn trên những máy khác nhau. Thời gian ghi dưới đây là ước
lượng, phải đo lại ở G0.

## 0. Chuẩn bị (máy Linux có GPU, khuyến nghị H100 80 GB)

```bash
git clone <repo> && cd VILATENT
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,model,data,baselines,teacher,kernels]"
pytest -q                                   # 34 test CPU phải pass
huggingface-cli login                       # nếu cần (Qwen3.5 không gated)
```

Biến môi trường dùng trong `scripts/run_g1.sh`: `READER` (mặc định `Qwen/Qwen3.5-2B`), `READER_9B`, `SLUG`, `RATIO`
(mặc định 4), `TEACHER_URL`, `TEACHER_MODEL` (endpoint iCOMM 27B dạng OpenAI), `N_PAIRS` (mặc định 96.000 cặp
giai đoạn 1).

## 1. Tuần 1–2: dữ liệu, template, G0

```bash
bash scripts/run_g1.sh data template g0
```

| Bước | Sinh ra | Kiểm tra |
| --- | --- | --- |
| `data` | `data/tasks/viquad_{train,dev,test}.jsonl`, `viquad_train_clean.jsonl`, `data/corpus/docs.jsonl`, `data/stage1/pairs_{train,dev}.jsonl`, kèm `*.meta.json` | dev 1.175 câu / 250 đoạn, test 2.653 / 557 (trùng split ViWord-C); `docs.jsonl.meta.json` ghi số bài bị loại theo tiêu đề và theo n-gram |
| `template` | `configs/readers/qwen3.5-{2b,9b}.json` | lượt trả lời bắt đầu bằng `<think>\n\n</think>\n\n`. **Commit hai file này**: checkpoint và logit thầy gắn với hash của template |
| `g0` | `results/g0/Qwen_Qwen3.5-{2B,9B}.json` | `G0_pass: true` cho cả hai reader |

G0 gồm các kiểm tra sau:

- nạp mô hình chỉ phần ngôn ngữ (`vision_params = 0`) và không thiếu key nào của checkpoint (`missing_keys` rỗng; nếu thiếu, trọng số đó bị khởi tạo ngẫu nhiên mà các kiểm tra khác vẫn có thể pass);
- `fast_deltanet_kernels` phải là `true` (điều kiện để qua G0);
- logit từ `input_ids` trùng logit từ `inputs_embeds`;
- giải mã greedy từ `inputs_embeds` trùng `model.generate`; `full_context_f1` của 3 câu mẫu chỉ để kiểm tra trọng số có hợp lý (không dùng làm cổng);
- gradient về memory, adapter và lớp đầu của bộ ghi hữu hạn và khác 0 sau khi đi qua mọi lớp DeltaNet;
- thời gian và bộ nhớ đỉnh của một bước forward + backward;
- chuẩn trạng thái ẩn của token đầu chuỗi, so khi có và không có token mồi.

Nếu `decode.warning` báo batch có padding lệch với từng câu riêng lẻ, hãy gửi lại file JSON. Lỗi này không làm G0
trượt, nhưng cần xem xét trước G1.

**G0 không đạt:** dừng lại, gửi `results/g0/*.json` cùng log lỗi. Phương án dự phòng là Qwen2.5-1.5B và 7B với
L = 2 (`docs/VILATENT.md`), nhưng chỉ đổi khi chủ đề tài đồng ý.

Chạy ngầm ngay từ tuần 1 (cần endpoint thầy; script tự tiếp tục được nếu bị ngắt):

```bash
nohup bash scripts/run_g1.sh qa_gen > qa_gen.log 2>&1 &
```

Script in tỉ lệ loại ở bước kiểm tra hai chiều. Nếu tỉ lệ này vượt 20%, cần cho người kiểm tra 200 mẫu (bảng rủi
ro). G1 không dùng dữ liệu này; nó dành cho tuần 4–6.

## 2. Tuần 3: G1 trên Qwen3.5-2B ở 4×

```bash
bash scripts/run_g1.sh teacher stage1 stage2 eval select fallback report
```

| Bước | Việc | Sinh ra |
| --- | --- | --- |
| `teacher` | top-20 log-prob của thầy trên cặp giai đoạn 1 và ViQuAD train/dev (dùng chung cho mọi cấu hình) | `data/teacher/qwen3.5-2b/*.pt` |
| `stage1` | O-LM rút gọn, 2.500 bước × batch 32, bốn bộ ghi: 4× (cho M, W5) và 8×, 16×, 32× (cho ME với f = 2, 4, 8) | `runs/g1_stage1_r{4,8,16,32}/{best.pt,metrics.jsonl,config.json}` |
| `stage2` | chưng cất theo đáp án trên ViQuAD train, 2.000 bước, năm lượt: ME f = 2, 4, 8 (câu gốc BM25 có trong đầu vào), M, W5 | `runs/g1_stage2_{me_f2,me_f4,me_f8,m,w5}_r4/…` |
| `eval` | full, none, truncation, lead, bm25, llmlingua2 và năm cấu hình ViLatent trên ViQuAD dev | `results/g1_dev/*.jsonl`, `*.summary.json` |
| `select` | chọn f của ME theo loss dev giai đoạn 2 (không theo F1 dev) | `results/g1_dev/me_choice_r4.json`, `vilatent_me_r4.jsonl` |
| `fallback` | MEF: đường đánh đổi và ngưỡng τ nhỏ nhất đạt ≥ 95% F1 toàn văn | `results/g1_dev/mef_{curve,tau}_r4.json`, `vilatent_mef_r4.jsonl` |
| `report` | ME so với mốc cứng tốt nhất (cả theo từng nhóm có và không dùng câu hỏi), bootstrap theo đoạn, MDE; W5 − M và ME − M (mô tả) | `results/g1_dev/g1_report_r4.json` |

Thứ tự ưu tiên khi thiếu GPU: ba lượt ME là bắt buộc cho cổng; W5 có thể dời sang tuần 4–6; f = 8 có thể bỏ
(bảng rủi ro trong `docs/VILATENT.md`). Hỏi chủ đề tài trước khi bỏ lượt nào.

Trong khi huấn luyện, theo dõi `runs/*/metrics.jsonl`. Mỗi dòng `train` ghi `loss`, `ce`, `kl`, `mem_norm` (chuẩn
của memory) cạnh `emb_norm` (chuẩn embedding), `grad_norm`, `sec_per_step` và `peak_mem_gb`. Nhân `sec_per_step`
với số bước để có số giờ H100 thực tế, con số mà tài liệu yêu cầu đo lại ở tuần đầu. Ở bước đầu tiên, vòng huấn
luyện tự dừng nếu gradient về bộ ghi không hữu hạn hoặc bằng 0.

**Tiêu chí G1, cố định trước khi chạy:** trên ViQuAD dev ở 4×, F1 của ViLatent-ME (f chọn theo loss dev) trừ F1 của mốc cứng tốt nhất phải
≥ 3 điểm, **và** cận dưới CI 95% (bootstrap theo đoạn văn) phải > 0. Ngoài ra, tỉ lệ câu trả lời không đọc được
phải dưới 2% với mọi phương pháp.

Sau khi chạy xong, gửi lại:

```bash
tar czf g1.tgz results/g0 results/g1_dev runs/*/metrics.jsonl runs/*/config.json data/*/*.meta.json data/qa_gen/*.meta.json
```

**G1 không đạt:** thử W2 thêm một tuần, rồi chuyển sang Hướng B (`docs/VILATENT.md`). Không chạy reader 9B khi chưa
qua G1. Tập test không được dùng ở G0 hay G1.
