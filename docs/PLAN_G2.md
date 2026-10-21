# Kế hoạch G2: ablation trên Qwen3.5-2B (tuần 4–6)

Bản nháp ngày 19/10/2026. Kế hoạch này chỉ áp dụng khi **G1 đạt**. Nếu G1 không đạt, đề tài đi theo nhánh F1 (thử W2
thêm một tuần, rồi sang Hướng B) và G2 không chạy. Các điểm ghi "Đề xuất" ở mục 8 chưa được chốt; chủ đề tài quyết
trước khi viết mã phần tương ứng.

## 1. Mục tiêu và cổng

Theo docs/VILATENT.md (lộ trình, khối P2 và G2):

- **Việc của tuần 4–6:** lọc QA sinh tự động, dịch IFEval, tính MDE từ lần thử G1; ablation O-LM với O-AE, số lớp L,
  W1 và tỉ lệ trộn γ, tất cả trên Qwen3.5-2B.
- **Cổng G2:** chốt cấu hình cho tuần 7–9 (Qwen3.5-9B), và accuracy Vi-MQA khi reader đọc kèm memory của một tài liệu
  không liên quan tụt **không quá 2 điểm** so với khi không có memory.
- **Không đạt (F2):** tăng γ hoặc thêm bộ định tuyến kNN theo Cartridges++.

Hai việc G2 **không** quyết định:

- O-LM hay O-AE. Tuần 7–9 huấn luyện cả hai nhánh trên 9B để kiểm định H3 (giả thuyết xác nhận, họ Holm riêng). Ở G2,
  O-AE chỉ cần chạy được, không lỗi, và có λ_AE hợp lý.
- Kết luận cho bất kỳ giả thuyết nào. Mọi số của G2 đo trên dev, một seed, reader 2B; chỉ dùng để chọn cấu hình.

## 2. Đầu vào từ G1

| Từ G1 | Dùng ở G2 |
| --- | --- |
| f* (hệ số memory chọn theo loss dev) | Cấu hình gốc của mọi ablation: ViLatent-ME ở 4× với f*, bộ ghi W0, L = 4, O-LM, γ = 0 |
| `runs/g1_stage1_r{4·f*}/best.pt`, `runs/g1_stage2_me_f{f*}_r4/best.pt` | Điểm gốc O-LM; không chạy lại |
| `results/g1_dev/*.jsonl` (kết quả từng câu) | Tính MDE (mục 4, D5) |
| `sec_per_step`, `peak_mem_gb` của 9 lượt | Chỉnh lại ước lượng GPU ở mục 6 |
| `data/` (corpus, cặp giai đoạn 1, logit thầy, ViQuAD đã lọc) | Dùng lại nguyên vẹn |
| W5, nếu bị dời khỏi G1 vì thiếu GPU | Chạy trong tuần 5 cùng các lượt giai đoạn 2 |

## 3. Những gì đã có

| Phần | Trạng thái |
| --- | --- |
| Số lớp L | `n_layers` là tham số của config; L = 8 chỉ cần file YAML mới (L phải là bội số của 4) |
| O-none | `init_from` để trống thì giai đoạn 2 bắt đầu từ bộ ghi mới |
| MDE, bootstrap cụm, Holm | `vilatent/stats.py` (`mde`, `paired_test`, `holm`) |
| Sinh và lọc QA | `scripts/generate_qa.py`, `scripts/filter_qa.py`. Ngày 21/10/2026 đã chạy thử prompt đầu trên 2.090 đoạn (5.917 câu, giữ ở `data/qa_gen/qa_raw_prompt1.jsonl`); sau khảo sát, prompt được sửa và `filter_qa.py` thêm luật lọc, lấy mẫu câu chép (D1). Ngày 21/10/2026 đã sinh đủ với prompt 3 (19.983 đoạn, 55.480 câu), đẩy lên HF `thanthienhai/vilatent-qa-gen` (private). `filter_qa.py` chưa chạy trên GPU |
| Chống rò rỉ | `scripts/leak_filter.py`, sidecar `.meta.json` |
| Huấn luyện, đánh giá QA, chọn theo loss dev | Dùng chung với G1 |

## 4. Công việc

### Dữ liệu

**D1. QA sinh tự động.** Cụm GPU không gọi được endpoint iCOMM, nên chia làm hai nơi:
`bash scripts/run_g1.sh qa_generate` chạy ở một máy trong mạng iCOMM (chỉ cần CPU và `data/corpus/docs.jsonl`).
`qa_raw.jsonl` và file meta được đẩy lên repo dataset private `thanthienhai/vilatent-qa-gen` trên Hugging Face. Trên
cụm: `HF_TOKEN=<token đọc được repo> bash scripts/run_g1.sh qa_download qa_filter`. `qa_download` tải đúng revision
`QA_REVISION` (mặc định `28e3ac26`, bản prompt 3) và dừng nếu SHA-256 không khớp file meta.

Endpoint `http://172.16.9.11:30049/v1` đo ngày 21/10/2026: khoảng 1,85 request/s, bão hoà từ 16 luồng, nên 20.000
đoạn mất khoảng 3 giờ. Khảo sát 5.917 câu của prompt đầu (so với ViQuAD dev):

| Chỉ số | ViQuAD dev | Prompt đầu |
| --- | --- | --- |
| Đáp án, trung vị số âm tiết | 6 | 3 |
| Câu hỏi chép câu chứa đáp án (≥ 80% âm tiết trùng) | 10,2% (train 10,5%) | 25,3% |
| Đáp án nằm trong câu hỏi | 1,1% | 0,6% |
| Nhãn "số" mà đáp án không có số | – | 3,2% |

Đọc tay 25 câu: 20 tốt, 3 sai nhãn loại, 2 đáp án thiếu cụm. Vì vậy prompt yêu cầu thêm đáp án trọn cụm, đáp án loại
"số" có con số và câu hỏi diễn đạt lại. `filter_qa.py` thêm hai luật (đáp án nằm trong câu hỏi, nhãn "số" không có số)
trước bước kiểm tra hai chiều, và sau đó lấy mẫu câu chép để tỉ lệ bằng ViQuAD train. Chạy thử hai bước này (không có
reader) trên dữ liệu prompt đầu: 206 câu bị luật loại, giữ 500/1.429 câu chép, còn 4.782 câu. Trước khi chạy đủ 20.000
đoạn với prompt mới: chạy thử khoảng 150 đoạn và khảo sát lại như bảng trên.

Hai lượt thử 150 đoạn (cùng đoạn văn, so với prompt đầu):

| Chỉ số | Prompt 1 | Prompt 2 (trọn cụm, diễn đạt lại) | Prompt 3 (câu số chỉ khi đoạn có số, mô tả ≤ 30 âm tiết) | ViQuAD train |
| --- | --- | --- | --- | --- |
| Câu chép câu chứa đáp án | 25,2% | 11,4% | 12,5% | 10,5% |
| Đáp án, phân vị 25/50/75 (âm tiết) | 2/3/5 | 2/3/5 | 2/4/9 | 3/6/14 |
| Đáp án > 15 âm tiết | 0% | 0% | 7,6% | 21,0% |
| Nhãn "số" mà đáp án không có số | 6 | 10 | 4 | – |

Prompt 3 là bản dùng để chạy đủ. Chỉ 7/150 đoạn không có số, nên phần lớn câu "số" sai nhãn vẫn còn và được
`filter_qa.py` loại. Đáp án mô tả dài hơn làm bước kiểm tra hai chiều (F1 ≥ 0,8) khó đạt hơn: cần xem tỉ lệ bị loại
theo loại đáp án.

Chạy đủ với prompt 3 (21/10/2026, 3 giờ 17 phút, không lượt gọi nào lỗi): 19.983 đoạn, 55.480 câu (số / thực thể /
mô tả: 16.050 / 19.952 / 19.478), 6 đoạn không ra câu. Đáp án phân vị 25/50/75 là 2/4/9 âm tiết, 8,2% dài hơn 15
(mô tả: trung vị 11, 23,3% dài hơn 15). Câu chép 10,9%, sát ViQuAD train. Khảo sát này thấy thêm 4,5% câu hỏi nhắc
"đoạn văn" ("Nhân vật chính trong đoạn văn là ai?"), ViQuAD train chỉ có 2 câu; đây cũng là nguồn chính của các câu hỏi
lặp lại giữa các đoạn. `filter_qa.py` thêm luật loại thứ ba cho các câu này. Ba luật loại 5,8% (2.365 câu "đoạn văn",
685 nhãn "số" không có số, 184 câu chứa đáp án), còn 52.246 câu trước bước kiểm tra hai chiều.

Sau khi lọc:

- Đếm tỉ lệ bị loại ở bước kiểm tra hai chiều. Trên 20% là dấu hiệu rủi ro (docs/VILATENT.md, bảng rủi ro): một người
  kiểm 200 mẫu, giảm tỉ trọng dữ liệu sinh.
- Kiểm phân bố ba loại đáp án (số, thực thể, mô tả).
- Việc dùng QA sinh trong huấn luyện ở G2 là câu hỏi Q12 (mục 8).

**D2. Vi-MQA (VMLU).**

- Kiểm tra giấy phép trước khi tải (docs/VILATENT.md ghi "Cần kiểm tra giấy phép").
- Kiểm tra các split và **tập nào có nhãn công khai**. Nếu nhãn của tập test chỉ chấm qua leaderboard, G2 dùng tập
  có nhãn (valid/dev), và cỡ mẫu nhỏ làm MDE lớn (xem Q9).
- `scripts/prepare_vimqa.py` ghi `data/tasks/vimqa_<split>.jsonl` dạng `{id, cluster, question, choices, answer,
  subject}`; `cluster` là câu hỏi, vì các câu không chung đoạn văn.
- Ghép memory lạ: mỗi câu Vi-MQA nhận một đoạn văn không liên quan, cố định bằng seed (Q8).

**D3. IFEval-vi.**

- Chọn từ 541 prompt của IFEval những loại chỉ dẫn có bộ kiểm tra không phụ thuộc ngôn ngữ: định dạng (JSON, gạch đầu
  dòng, tiêu đề, số đoạn), từ khoá (có, không có, số lần xuất hiện), mở đầu và kết thúc bằng một cụm cố định, không
  dùng dấu phẩy. Bỏ các loại đếm "từ" (tiếng Việt không có ranh giới từ bằng dấu cách) và các loại về chữ hoa của tiếng
  Anh.
- Dịch bằng iCOMM 27B; một người rà toàn bộ bản dịch, nhất là từ khoá phải khớp với tham số của bộ kiểm tra.
- `vilatent/ifeval.py`: bộ kiểm tra strict cho các loại đã chọn, viết lại tối giản theo mã gốc của IFEval.
- Ở G2 chỉ báo cáo, không dùng làm cổng.

**D4. Dữ liệu trộn γ.**

- Mỗi mẫu: câu hỏi của đoạn X ghép với memory của đoạn Y (Y ≠ X, khác bài), cùng một số chỉ dẫn chung (nguồn: Q6).
- Đích là câu trả lời greedy của chính reader khi **không có memory** (`enable_thinking=False`, template cố định);
  logit thầy cũng lấy từ reader không có memory. Không cần gán nhãn.
- `scripts/make_offcontext.py` ghi `data/offctx/{train,dev}.jsonl`; `scripts/precompute_teacher.py` thêm chế độ
  không có ngữ cảnh.
- Chạy `leak_filter.py` trên dữ liệu này với tập đánh giá là ViQuAD dev/test và Vi-MQA.

**D5. MDE.** `scripts/mde_report.py` đọc kết quả từng câu của G1, tính sai số chuẩn của chênh lệch cặp (ViLatent-ME
trừ mốc cứng tốt nhất) bằng bootstrap theo cụm đoạn, rồi suy ra MDE cho ViQuAD test (2.653 câu / 557 đoạn) và MLQA
tiếng Việt (5.495 câu). Nếu MDE của MLQA lớn hơn 2 F1, H2 hạ xuống phân tích mô tả (không chạy TOST), và điều này
được ghi lại ngay ở G2.

### Mã

**C1. O-AE.** Giai đoạn 1 thêm mục tiêu tái tạo: reader đọc memory của đoạn A rồi sinh lại nguyên văn A.

- Template thêm tác vụ `reconstruct` ("Chép lại nguyên văn đoạn văn sau.\n\nĐoạn văn: {context}"), đích là A.
- Loss tái tạo chỉ có CE, không KL (thầy đọc A rồi chép lại A gần như chắc chắn, KL không mang thêm tín hiệu).
- Trộn với mục tiêu tiếp nối theo Q4; thêm `objective: lm | ae` và `lambda_ae` vào `TrainConfig`.
- Đích A dài tới 1.024 token nên bước O-AE đắt hơn; đo `sec_per_step` ở smoke test.

**C2. Template không làm hỏng sản phẩm của G1.** `config_hash` hiện băm toàn bộ `prompts`, nên thêm tác vụ mới
(`reconstruct`, `mcq`, `instruct`) sẽ đổi hash và làm checkpoint cùng logit thầy của G1 bị từ chối. Cách xử lý theo
Q10. Việc này phải làm trước C1, C4, C5.

**C3. W1: gộp theo ranh giới âm tiết hoặc từ.**

- `budget.py`: hàm cắt mỗi khúc thành nhóm theo ranh giới (âm tiết theo dấu cách, hoặc từ theo VnCoreNLP: Q5), mỗi
  nhóm g đơn vị; g chọn trên train sao cho số token trung bình mỗi nhóm ≈ r.
- `writer.py`: gộp trung bình theo `segment_ids` bằng `scatter_reduce`, thay cho `mean_pool` cửa sổ cố định. Số
  memory mỗi mẫu thay đổi; phần pad và mask đã có sẵn ở `target_loss`.
- Ngân sách: k của mỗi mẫu là số nhóm; mốc nén cứng nhận đúng k token của mẫu đó; báo cáo tỉ lệ nén thực tế (trung
  bình n/k).
- ME với W1: phần câu gốc là k − k_m với k_m là số nhóm ở hệ số f (Q5).
- Test: khi mọi nhóm đúng r token, kết quả phải trùng `mean_pool`.

**C4. Trộn γ vào giai đoạn 2.**

- `train.py`: mỗi micro-batch lấy mẫu ngoài tài liệu với xác suất sao cho khoảng γ số token có giám sát đến từ
  `data/offctx/train.jsonl`; `TrainConfig` thêm `offcontext`, `teacher_offcontext`, `gamma`.
- Loss dev giữ nguyên trên ViQuAD dev (để so được với γ = 0), và log thêm loss dev riêng trên `data/offctx/dev.jsonl`.

**C5. Đánh giá ngoài tài liệu.** `scripts/evaluate_offcontext.py`:

- Vi-MQA: accuracy khi không có memory (mốc) và khi có memory lạ, với ViLatent-M và ViLatent-ME (ME chọn câu gốc
  bằng BM25 theo câu hỏi trắc nghiệm, đúng như khi triển khai). Cách chấm theo Q7.
- IFEval-vi: strict accuracy, cùng ba điều kiện; giải mã greedy, `max_new_tokens` cố định cho mọi phương pháp.
- Tỉ lệ câu trả lời không đọc được < 2%, như ở QA.
- Kết quả từng câu ra `results/g2_dev/offctx_*.jsonl`, cùng định dạng cột với `vilatent/evaluate.py`.

**C6. Báo cáo G2.** `scripts/g2_report.py`:

- Bảng ablation: loss dev giai đoạn 2, F1/EM ViQuAD dev ở 4×, chênh lệch so với cấu hình gốc kèm CI 95% bootstrap theo
  đoạn, tỉ lệ không đọc được.
- Bảng ngoài tài liệu: Vi-MQA (không memory, M, ME) kèm chênh lệch và CI bootstrap theo câu; IFEval-vi.
- Cấu hình được chốt theo quy tắc ở Q3, in `G2_pass` và `G2: PASS/FAIL`, ghi `results/g2_dev/g2.json`.

**C7. Pipeline và tài liệu vận hành.**

- `configs/g2/*.yaml` (mục 5), `scripts/run_g2.sh` theo cùng kiểu với `run_g1.sh` (các bước `data`, `teacher`,
  `stage1`, `stage2`, `eval`, `report`; lượt độc lập chia qua `GPUS`).
- `scripts/smoke_g2.sh` có `SMOKE_SHORT=1`, chạy thử trên Kaggle 2× T4 (fp16) trước khi gửi đội vận hành.
- `docs/RUN_G2.md` theo khung của `docs/RUN_G0_G1.md`.
- Test CPU với Qwen3.5 tí hon cho C1, C3, C4, C5 và bộ kiểm tra IFEval.

## 5. Ma trận thí nghiệm

Mọi lượt: Qwen3.5-2B, ngân sách 4×, ViLatent-ME với f* của G1, seed 0, giai đoạn 1 và 2 cùng số bước như G1 (Q1).
Mỗi ablation đổi **một** yếu tố so với cấu hình gốc.

| Lượt | Đổi so với gốc | Giai đoạn 1 mới (bộ ghi r·f*) | Giai đoạn 2 mới |
| --- | --- | --- | --- |
| Gốc (O-LM, L = 4, W0, γ = 0) | — | dùng lại G1 | dùng lại G1 |
| O-AE | Mục tiêu giai đoạn 1 | 1 | 1 |
| O-none | Bỏ giai đoạn 1 | — | 1 |
| L = 8 | Số lớp bộ ghi | 1 | 1 |
| W1 | Gộp theo ranh giới | 1 | 1 |
| γ = 1%, 5%, 10% | Trộn ngoài tài liệu | — | 3 |
| Cấu hình chốt | Gộp các lựa chọn thắng (nếu khác gốc) | 0–1 | 1 |
| W5 (nếu dời từ G1) | — | dùng lại G1 | 1 |

Tổng: 3–4 lượt giai đoạn 1 và 8–9 lượt giai đoạn 2. Mỗi lượt giai đoạn 2 được đánh giá trên ViQuAD dev (1.175 câu) và
Vi-MQA; IFEval-vi chỉ chạy cho cấu hình gốc, các lượt γ và cấu hình chốt.

## 6. Ước lượng GPU

Ngoại suy từ ước lượng của G1 (chưa có số đo H100); chỉnh lại khi có `sec_per_step` của G1.

| Phần | Ước lượng (giờ H100) |
| --- | --- |
| Giai đoạn 1: O-AE (đích dài, 1,5–2 lần một bước O-LM), L = 8, W1 | 3–5 |
| Giai đoạn 2: 8–9 lượt | 2–5 |
| Sinh đích và logit thầy cho dữ liệu γ | 0,5–1 |
| Đánh giá: ViQuAD dev, Vi-MQA, IFEval-vi | 2–4 |
| Smoke test trên máy chạy | 0,5 |
| **Tổng** | **khoảng 8–16 giờ** (gấp đôi nếu Q1 chọn giai đoạn 1 dài 5.000 bước) |

Phần sinh QA và dịch IFEval chạy trên endpoint iCOMM, không tốn GPU của cụm.

## 7. Lịch

| Thời gian | Việc | Cần GPU cụm |
| --- | --- | --- |
| Tuần 3, trong lúc chờ G1 | Chốt các câu hỏi ở mục 8; kiểm giấy phép và nhãn VMLU; viết D2, D3 (chọn và dịch IFEval), D5 (chạy được ngay khi có kết quả G1) | Không |
| Tuần 4 | C2 trước, rồi C1, C3, C4, C5; D4; test CPU; smoke trên Kaggle T4; viết `docs/RUN_G2.md` | Không |
| Tuần 5 | Đội vận hành chạy smoke bf16, giai đoạn 1 (3 lượt), giai đoạn 2 (7–8 lượt), đánh giá | Có |
| Tuần 6 | Lượt cấu hình chốt và đánh giá ngoài tài liệu của nó; `g2_report.py`; quyết định G2 | Có |

Nếu G2 không đạt: thử γ lớn hơn (ví dụ 20%) trong tuần 6; bộ định tuyến kNN là việc mới, cần một kế hoạch riêng và
sẽ lùi tuần 7–9.

## 8. Các câu hỏi cần chốt

| # | Câu hỏi | Đề xuất |
| --- | --- | --- |
| Q1 | Số bước giai đoạn 1 ở G2: giữ 2.500 như G1 hay dùng mức đầy đủ 5.000–10.000 của docs/VILATENT.md? | Giữ 2.500, để so trực tiếp với gốc của G1 và dùng lại checkpoint; mức đầy đủ để dành cho 9B |
| Q2 | Ablation chỉ ở 4× hay cả 8×, 16×? | Chỉ 4× (cùng ngân sách với G1); 8× và 16× chạy ở 9B |
| Q3 | Quy tắc chốt cấu hình | L và W1 chọn theo loss dev giai đoạn 2 trên ViQuAD (như cách chọn f ở G1, không chọn theo F1 dev để G3 không bị lạc quan); γ là giá trị nhỏ nhất đạt tiêu chí Vi-MQA; O-AE không chọn (cả hai nhánh lên 9B) |
| Q4 | O-AE trộn với O-LM thế nào? | Mỗi mẫu giai đoạn 1 nhận ngẫu nhiên một trong hai mục tiêu, tỉ lệ 50 : 50, λ_AE = 1; chi phí mỗi bước gần như cũ. Cách khác: cộng cả hai loss trên mỗi mẫu (chi phí gấp đôi) |
| Q5 | W1: ranh giới âm tiết hay từ (VnCoreNLP, cần Java)? ME có dùng W1 không? | Âm tiết theo dấu cách (không thêm phụ thuộc); thử ở ME vì đó là hệ chính |
| Q6 | Nguồn "chỉ dẫn chung" trong dữ liệu γ | Chỉ dùng câu hỏi ViQuAD của đoạn khác ở lần này; nếu thêm chỉ dẫn chung thì lấy từ một bộ dữ liệu chỉ dẫn tiếng Việt có giấy phép rõ, không lấy từ VMLU hay IFEval |
| Q7 | Chấm Vi-MQA bằng cách nào? | So log-prob của các nhãn A/B/C/D ở token trả lời đầu tiên: tất định, không có câu trả lời không đọc được. Cách khác: sinh greedy rồi tách nhãn |
| Q8 | Memory lạ lấy từ đâu? | Một đoạn ViQuAD dev ngẫu nhiên khác bài, cố định bằng seed 0, nén ở 4× |
| Q9 | Tiêu chí G2 tính bằng ước lượng điểm hay cận CI? | Ước lượng điểm của mức tụt ≤ 2 điểm, kèm CI 95% và MDE. Với vài trăm câu có nhãn, cận trên CI ≤ 2 gần như không thể đạt |
| Q10 | Giữ hash template của G1 khi thêm tác vụ mới | Băm theo từng tác vụ: checkpoint và logit thầy kiểm hash của đúng tác vụ chúng dùng. Cách khác: một file cấu hình template riêng cho G2 |
| Q11 | Số seed ở G2 | Một seed; ba seed dành cho 9B |
| Q12 | Có đưa QA sinh tự động vào giai đoạn 2 ở G2 không? | Chỉ lọc và kiểm chất lượng ở G2; quyết định trộn khi lên 9B, sau khi biết tỉ lệ loại |

## 9. Ngoài phạm vi G2

W2 (chỉ thuộc nhánh F1), W4 (QA nhiều tài liệu), LongLLMLingua, ICAE, ViWord-C và mốc tóm tắt, MLQA/SQuAD/Belebele,
LLM trọng tài và Cohen κ, đo TTFT/FLOPs, phân tích H4, Vistral. Các phần này thuộc tuần 7–11.
