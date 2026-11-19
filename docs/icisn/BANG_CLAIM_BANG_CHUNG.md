# Bảng claim | bằng chứng | trạng thái (bài ICISN, bản sau Giai đoạn 7)

Nguồn số: ViQuAD = `paper/numbers.tex` (`scripts/paper_numbers.py`); XQuAD-vi = `paper_icisn/numbers_icisn.tex`
(`scripts/icisn/confirm_numbers.py`, từ `results/icisn/confirm/numbers.json`, đầy đủ ở `docs/icisn/KET_QUA_XAC_NHAN.md`).
Đăng ký trước: `PREREG_JUDGE.md`, `PREREG_CONFIRM.md` (SHA trong file `.sha256` cạnh chúng).

| # | Claim trong bài | Bằng chứng | Trạng thái |
|---|---|---|---|
| 1 | Quy tắc đăng ký trước (RQ1) không đạt: trên ViQuAD-Long 4×, ME hòa prompt học được | Bảng 1; `diff.test.long.4.me-prompt` (+0,43 F1, CI [−1,43; +2,18]); ACC-LLM cùng kết luận (−0,41 [−2,34; +1,48], `KET_QUA_JUDGE.md` §3) | supported |
| 2 | ME hơn bộ nén cứng tốt nhất (PhoBERT) ở ViQuAD-Long 4× | Bảng 1 (`diff…me-phobert`) | supported (F1); phần lớn do tinh chỉnh tác vụ, vì memory hoán đổi vẫn hơn PhoBERT |
| 3 | Ở đoạn đơn, memory (M, ME) cao hơn văn bản cùng ngân sách | Bảng 1 | supported; kèm điều kiện: prompt đặt ở f=2, và ME/M thấp hơn PhoBERT/BM25 ở EM |
| 4 | H-R1: memory bù ở nơi bộ chọn câu hụt đáp án, cả đoạn đơn và Long | Hình 2: +38,7 [34,2; 43,2] và +24,6 [16,6; 32,8] F1; ACC-LLM +46,0 và +27,4; Holm đạt cả hai độ đo | supported (với prompt ở f=2) |
| 5 | H-R1 phụ thuộc prompt đối chứng | Prompt ở f=8: +10,3 [5,2; 15,5] (đoạn đơn), −1,7 [−10,8; +7,2] (Long) | supported; gắn nhãn thăm dò, ngoài họ Holm |
| 6 | H-R2a: router hơn M | Hình 2: +2,9 và +15,2 F1; ACC +3,5 và +16,6; Holm đạt | supported |
| 7 | H-R2b: router không kém BM25 2k (δ=2) | Đoạn đơn: +0,0 [−2,3; +2,6], cận dưới < −2, ACC −2,2 → **không đạt**; Long: +4,9 [2,9; 6,9] đạt | **không được nêu như một kết quả dương ở đoạn đơn** (bài nêu rõ) |
| 8 | H-S1/H-S2: memory hơn tóm tắt không theo câu hỏi cùng ngân sách | Hình 2: M−Sum +23,2/+23,9; ME−Sum+E +18,7/+7,7; cả hai độ đo; bổ sung ViQuAD-Long (không Holm, M/ME khác thiết bị): M−Sum +28,4, ME−Sum+E +8,6 F1 | supported, với hạn chế: Sum do mô hình lớn hơn viết, Sum dùng 82% ngân sách ở ViQuAD-Long |
| 9 | Loại 6 đoạn trùng corpus giai đoạn 1 không đổi kết luận | `KET_QUA_XAC_NHAN.md`, mục độ nhạy | supported (chỉ F1) |
| 10 | Kết luận về văn bản rất dài | Chỉ ViQuAD-Long (19 bài); XQuAD-Long trung vị ~1 000 token | bài nêu rõ giới hạn; không rút từ XQuAD-vi |
| 11 | "Memory đáng giá khi tài liệu ngắn hoặc bộ chọn câu dễ hụt; tài liệu dài thì tinh chỉnh reader trên câu chọn" | Gộp 1–8 | supported ở mức khuyến nghị thực hành, **không** phải kết luận nhân quả |
| 12 | Không có tuyên bố tiết kiệm thời gian/chi phí | Không có trong bài; ME không nhanh hơn toàn văn (419 vs 417 ms) | supported |
| 13 | Điều **không** có: LongLLMLingua, bộ truy hồi đoạn dày, tái lập nén mềm đã công bố | Bài ghi ở Hạn chế | needs evidence / không tuyên bố |

## Tự rà theo 5 chiều

- **Đóng góp:** đóng góp chính là phép so sánh có kiểm soát cùng kết quả âm được báo cáo; không phải một phương pháp mới thắng. Rủi ro: người phản biện coi là "phủ định".
- **Văn phong:** bài rút từ ~10 trang xuống 7; phần Phương pháp bỏ hai phương trình (gộp pooling vào chữ, bỏ công thức loss) để vừa trang.
- **Thực nghiệm:** một seed, một reader, một ngôn ngữ; 19 bài test ViQuAD; XQuAD-vi 48 bài; CI theo bài.
- **Đánh giá đầy đủ:** F1, EM (chỉ ở ViQuAD), ACC-LLM (κ=0,90 với 60 nhãn do một người soát). Hình 2 chỉ vẽ F1 và CI; ACC-LLM (điểm và CI) nằm ở `KET_QUA_XAC_NHAN.md`.
- **Thiết kế phương pháp:** Sum viết bởi mô hình lớn hơn; người chấm cùng họ với người viết tóm tắt; prompt đối chứng chưa tinh chỉnh lr.
