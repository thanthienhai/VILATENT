# Xem trước P2 (câu hỏi sinh bằng LLM trên bài Wikipedia dài); mẫu nhỏ, chưa chạy mô hình đọc

- 4 bài, 8 cửa sổ mỗi bài, mô hình sinh Qwen3.8-27B, mô hình kiểm DeepSeek-V4.1-Flash.
- Trạng thái: answer_length=40, answer_not_verbatim=9, check_disagrees=53, kept=500, question_refers_to_text=22

**Bài:** Chiến dịch Krym (1944) (10,215 âm tiết), cửa sổ ở 54% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sư đoàn bộ binh 50 đã để lại đơn vị nào rút về Lũy Thổ Nhĩ Kỳ?  
**Đáp án sinh:** Trung đoàn 121  
**Kiểm:** Trung đoàn 121 (F1 1.0)  
**Cửa sổ (rút gọn):** Sư đoàn bộ binh 50 để lại Trung đoàn 121 rút về Lũy Thổ Nhĩ Kỳ, lấy thị trấn Bak (???) là trung tâm phòng ngự. Sư đoàn bộ binh 98 để lại Trung đoàn bộ binh 289 phòng thủ sau lưng Sư đoàn bộ binh 50. Sư đoàn bộ binh sơn chiến 3 (Romania) được điều ra phòng thủ khu vực mỏ đá Ak Monai. Sư đoàn bộ binh 6 (Romania) thay Trung đoàn bộ binh 290 phòng thủ …

**Bài:** Chiến dịch Krym (1944) (10,215 âm tiết), cửa sổ ở 59% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn bộ binh 16 và Lữ đoàn xe tăng 63 đã đánh chiếm thành phố nào vào ngày 13 tháng 4?  
**Đáp án sinh:** Feodosiya  
**Kiểm:** Feodosiya (F1 1.0)  
**Cửa sổ (rút gọn):** Trong khi đó, các lực lượng Romania luôn được lệnh phải ở lại để cản hậu. Ngày 12 tháng 4, Quân đoàn bộ binh sơn chiến 3 (Liên Xô) với sự yểm hộ của các trung đoàn xe tăng 85 và 244 đã đánh thiệt hại nặng Sư đoàn bộ binh sơn chiến 3 (Romania) ở mỏ đá Ak Monai và chiếm lĩnh các chốt phòng thủ. Tàn quân Romania bỏ chạy về Simferopol. Ngày 13 tháng 4,…

**Bài:** Chiến dịch Krym (1944) (10,215 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Tập đoàn quân 17 của Đức đã buộc phải rút lui khỏi thảo nguyên Kuban qua eo biển nào vào tháng 10 năm 1943?  
**Đáp án sinh:** eo biển Kerch-Taman  
**Kiểm:** Kerch-Taman (F1 0.5)  
**Cửa sổ (rút gọn):** Tháng 10 năm 1943, Tập đoàn quân 17 (Đức) đã buộc phải rút lui khỏi thảo nguyên Kuban qua eo biển Kerch-Taman. Cuối năm 1943, Hồng quân đẩy lùi Cụm tập đoàn quân Nam (Đức) khỏi miền nam Ukraina. Tháng 11 năm 1943, Phương diện quân Ukraina 4 (Liên Xô) hoàn thành Chiến dịch tấn công Nikopol-Krivoi Rog, tiến đến bờ Đông sông Dniepr, chia cắt và cô lập…

**Bài:** Chiến dịch Krym (1944) (10,215 âm tiết), cửa sổ ở 36% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Sư đoàn bộ binh 336 của tướng Wolf Hagemann bao gồm những đơn vị nào?  
**Đáp án sinh:** các trung đoàn bộ binh 685, 686, 687; Trung đoàn pháo binh 336, 1 tiểu đoàn xe tăng, 1 trung đoàn pháo chống tăng, 1 tiểu đoàn bộ binh cơ giới, các tiểu đoàn trinh sát, công binh  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Sư đoàn bộ binh 19 (Romania) Quân đoàn bộ binh sơn chiến 49 của tướng Rudolf Konrad. Sư đoàn bộ binh 336 của tướng Wolf Hagemann gồm các trung đoàn bộ binh 685, 686, 687; Trung đoàn pháo binh 336, 1 tiểu đoàn xe tăng, 1 trung đoàn pháo chống tăng, 1 tiểu đoàn bộ binh cơ giới, các tiểu đoàn trinh sát, công binh. Sư đoàn bộ binh 370 của tướng Fritz B…

**Bài:** Chiến dịch Krym (1944) (10,215 âm tiết), cửa sổ ở 71% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào đầu tháng 5 năm 1944, tướng Karl Allmendinger chỉ còn lại bao nhiêu sư đoàn Đức và Romania để phòng thủ Sevastopol?  
**Đáp án sinh:** 5 sư đoàn Đức và 3 sư đoàn Romania  
**Kiểm:** 5 sư đoàn Đức và 3 sư đoàn Romania (F1 1.0)  
**Cửa sổ (rút gọn):** Tập đoàn quân độc lập Duyên Hải khép vòng vây trên bộ phía Tây Nam Sevastopol, từ Novo Shuly qua Kamary (???) đến Balaklava. Trên biển, Phân hạm đội Bắc Biển Đen đã phong tỏa tất cả các con đường biển quan trọng ra vào Sevastopol từ ngoài khơi Lyubimovka qua mũi Khersonet đến mũi Feolent ở phía Nam. Giai đoạn 3: Giải phóng Sevastopol Đầu tháng 5 nă…

**Bài:** Chiến dịch Krym (1944) (10,215 âm tiết), cửa sổ ở 68% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người được Hitler đề bạt làm tư lệnh Tập đoàn quân 17 sau khi cách chức tướng Erwin Jaenecke?  
**Đáp án sinh:** tướng Karl Allmendinger  
**Kiểm:** tướng Karl Allmendinger (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 19 tháng 4, Tập đoàn quân 51 (Liên Xô) đã vượt qua tất cả các cụm chốt của quân Đức dọc theo đường cao tốc Simferopol - Sevastopol, lần lượt đánh chiếm điểm cao Chernaya (???) và Fediukhinykh (???). Ngày 21 tháng 4, Quân đoàn bộ binh cận vệ 1 và Quân đoàn xe tăng 19 hợp lực tiêu diệt cụm quân Đức-Romania tại thung lũng Inkerman và đánh chiếm đ…

**Bài:** Chiến dịch Krym (1944) (10,215 âm tiết), cửa sổ ở 56% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn bộ binh cận vệ 11 đã chiếm được trung tâm phòng ngự tiền tiêu nào của quân Đức ở phía Đông Kerch vào 4 giờ sáng ngày 11 tháng 4?  
**Đáp án sinh:** Bak  
**Kiểm:** Bak (F1 1.0)  
**Cửa sổ (rút gọn):** Quân Đức cũng thả khói mù để che giấu các hoạt động chuyển quân. Không cho quân Đức yên ổn rút lui, 22 giờ đêm 10 tháng 4, Quân đoàn bộ binh cận vệ 11 phát động tấn công. 4 giờ sáng ngày 11 tháng 4, quân đoàn này đã chiếm được Bak, trung tâm phòng ngự tiền tiêu của quân Đức ở phía Đông Kerch và các thị trấn Kara Sedzheyt (???), Adzhi Mandy (???), K…

**Bài:** Chiến dịch Krym (1944) (10,215 âm tiết), cửa sổ ở 42% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào lúc 10 giờ 30 phút sáng ngày 8 tháng 4, đơn vị nào đã đồng loạt nhả đạn?  
**Đáp án sinh:** tất cả các cỡ pháo của Phương diện quân Ukraina 4  
**Kiểm:** tất cả các cỡ pháo của Phương diện quân Ukraina 4 (F1 1.0)  
**Cửa sổ (rút gọn):** Qua hơn 3 tháng đầu năm 1944, Tập đoàn quân 17 (Đức) lần lượt để mất các vị trí quan trọng ở hạ lưu tả ngạn sông Dniepr và cuối cùng, bị Phương diện quân Ukraina 4 (Liên Xô) dồn trở lại Krym. Cái "cầu tàu" Perekop đã bị khóa chặt. Tập đoàn quân 17 (Đức) bị cắt đứt liên lạc hoàn toàn với Cụm tập đoàn quân Nam. 10 giờ 30 phút sáng ngày 8 tháng 4, tất…

**Bài:** Thu Phương (9,292 âm tiết), cửa sổ ở 72% bài  
**Trạng thái:** kept  
**Câu hỏi:** Việt Anh tự khắc họa âm nhạc của mình là gì khi chia sẻ trên tờ Elle Việt Nam?  
**Đáp án sinh:** cuốn nhật ký tâm lý qua từng giai đoạn  
**Kiểm:** cuốn nhật ký tâm lý qua từng giai đoạn (F1 1.0)  
**Cửa sổ (rút gọn):** Chia sẻ trên tờ Elle Việt Nam, Việt Anh tự khắc họa âm nhạc của anh là "cuốn nhật ký tâm lý qua từng giai đoạn", "cho dù viết cho ai, về ai, đều có hình ảnh cá nhân mình trong đó". Anh nói:"Nó không có sự rạch ròi rằng, câu này cho anh, câu này cho tôi nhưng nó phản ánh khá rõ cảm xúc và suy tư của người viết. Những điều tôi nghĩ trong cuộc sống đề…

**Bài:** Thu Phương (9,292 âm tiết), cửa sổ ở 54% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quãng giọng của Thu Phương trải dài từ nốt nào đến nốt nào?  
**Đáp án sinh:** từ nốt B2 cho đến D5  
**Kiểm:** B2 cho đến D5 (F1 0.8)  
**Cửa sổ (rút gọn):** Tại concert "Yên" của Hoàng Dũng diễn ra ngày 4/11/2022, Thu Phương đã có dịp tái ngộ lại học trò là nam ca sĩ Hoàng Dũng sau 7 năm từ chương trình The Voice 2015 và thể hiện ca khúc Chưa bao giờ. Tại đây, nam ca sĩ đã gửi lời cảm ơn đến người thầy của mình là Thu Phương và cô cũng liên tục xúc động rơi nước mắt trước tình cảm của học trò khi cả 2 …

**Bài:** Thu Phương (9,292 âm tiết), cửa sổ ở 88% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thu Phương và Huy MC kết hôn vào năm nào?  
**Đáp án sinh:** Năm 1993  
**Kiểm:** Năm 1993 (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, Thu Phương không lên tiếng và giữ thái độ im lặng trên truyền thông về sự việc này. Hai thí sinh trong đội Thu Phương sau đó cũng lên tiếng tố Thu Phương trên các diễn đàn, tuy nhiên sự việc được giới trong nghề đánh giá là một chiêu PR của các thí sinh nhằm gây sự chú ý bằng cách tạo scandal với HLV. Cuối cùng, một thí sinh trong đội cũ…

**Bài:** Thu Phương (9,292 âm tiết), cửa sổ ở 33% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Thu Phương trở thành công dân của quốc gia nào vào tháng 5 năm 2008?  
**Đáp án sinh:** công dân Mỹ  
**Kiểm:** Mỹ (F1 0.5)  
**Cửa sổ (rút gọn):** Thu Phương bị cấm hoạt động nghệ thuật trong nước, không được tiếp tục hưởng quyền công dân và quyền nghệ sĩ tại Việt Nam. Các tiết mục cũng như các sản phẩm băng đĩa nhạc của Thu Phương không được phép lưu hành và phổ biến tại Việt Nam. Tuy nhiên, không có lệnh nào cấm Thu Phương về nước. Tại Việt Nam, Thu Phương bị dư luận và báo chí Việt Nam lên…

**Bài:** Thu Phương (9,292 âm tiết), cửa sổ ở 76% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ca khúc 'Biển hát chiều nay' do ai sáng tác nhạc và lời?  
**Đáp án sinh:** Hồng Đăng  
**Kiểm:** Hồng Đăng (F1 1.0)  
**Cửa sổ (rút gọn):** Dòng sông lơ đãng(nhạc và lời: Việt Anh) Có phải em mùa thu Hà Nội (nhạc: Trần Quang Lộc, thơ: Tô Như Châu) Unbreak my heart (nhạc Mỹ: Diane Warren, lời Việt: Đỗ Quang) Bang Bang (nhạc Mỹ, lời Việt: Phạm Duy) Mắt buồn (nhạc và lời: Trường Huy) Những mùa hoa bỏ lại (nhạc và lời: Việt Anh) Biển hát chiều nay (nhạc và lời: Hồng Đăng) Biển nỗi nhớ và e…

**Bài:** Thu Phương (9,292 âm tiết), cửa sổ ở 21% bài  
**Trạng thái:** kept  
**Câu hỏi:** Album nào được xem là đĩa nhạc cuối cùng của Thu Phương tại Việt Nam?  
**Đáp án sinh:** Như chưa bắt đầu  
**Kiểm:** Như chưa bắt đầu (F1 1.0)  
**Cửa sổ (rút gọn):** Năm 2000, sau khoảng thời gian nghỉ sinh con gái Thanh Thảo và phát hành đĩa Một đời mây gió (1999), Phương ký hợp đồng với Phương Nam Film kết hợp với nhạc sĩ Quốc Bảo làm album Chào em! Chào xinh tươi với các bài hit Chào em! chào xinh tươi (hát với Trung Kiên), Ngủ ngoan nhé ngày xưa, Bài hát đôi cho em (hát với Quang Minh). Sau đó, Thu Phương t…

**Bài:** Thu Phương (9,292 âm tiết), cửa sổ ở 42% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thu Phương đảm nhận vai trò gì trong chương trình VSTAR - Ngôi sao đêm nay từ năm 2012 tới 2014?  
**Đáp án sinh:** giám khảo  
**Kiểm:** giám khảo (F1 1.0)  
**Cửa sổ (rút gọn):** Trong các DVD Paris By Night, Thu Phương xuất hiện với các bài Trăng dưới chân mình, Hà Nội 12 mùa hoa, Dạ khúc cho tình nhân, Bài thơ không đoạn kết, Nghìn trùng xa cách, 10 & 20 tình cũ. Ngoài ra, Thu Phương cũng thể hiện các màn mashup cũng như liên khúc: màn song ca LK: Định mệnh & Tình bơ vơ trong chương trình PBN VIP 106 (hát cùng Phạm Quốc T…

**Bài:** Thu Phương (9,292 âm tiết), cửa sổ ở 21% bài  
**Trạng thái:** kept  
**Câu hỏi:** Album nào được xem là đĩa nhạc cuối cùng của Thu Phương tại Việt Nam?  
**Đáp án sinh:** Như chưa bắt đầu  
**Kiểm:** Như chưa bắt đầu (F1 1.0)  
**Cửa sổ (rút gọn):** Năm 2000, sau khoảng thời gian nghỉ sinh con gái Thanh Thảo và phát hành đĩa Một đời mây gió (1999), Phương ký hợp đồng với Phương Nam Film kết hợp với nhạc sĩ Quốc Bảo làm album Chào em! Chào xinh tươi với các bài hit Chào em! chào xinh tươi (hát với Trung Kiên), Ngủ ngoan nhé ngày xưa, Bài hát đôi cho em (hát với Quang Minh). Sau đó, Thu Phương t…

**Bài:** Diêm Tích Sơn (15,512 âm tiết), cửa sổ ở 89% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trách nhiệm duy trì di tích của Diêm Tích Sơn được trao cho ai vào năm 2011?  
**Đáp án sinh:** chính quyền thành phố Đài Bắc  
**Kiểm:** chính quyền thành phố Đài Bắc (F1 1.0)  
**Cửa sổ (rút gọn):** Năm 2011, khi phụ tá cuối cùng của ông đã 81 tuổi và không thể chăm sóc dinh thự được nữa, trách nhiệm duy trì di tích được trao cho chính quyền thành phố Đài Bắc. Sau Nội chiến, giống như hầu hết tướng lĩnh Quốc dân đảng khác không đổi phe, Diêm Tích Sơn bị bộ máy tuyên truyền của Cộng sản biến thành ác quỷ. Phải cho đến sau năm 1979, với những cả…

**Bài:** Diêm Tích Sơn (15,512 âm tiết), cửa sổ ở 11% bài  
**Trạng thái:** kept  
**Câu hỏi:** Diêm Tích Sơn được Tưởng Giới Thạch ban thưởng những chức vụ nào sau khi chiếm được Bắc Kinh vào tháng 6 năm 1928?  
**Đáp án sinh:** Bộ trưởng Bộ Nội chính và Phó tổng tư lệnh Lục-hải-không quân  
**Kiểm:** Bộ trưởng Bộ Nội chính và Phó tổng tư lệnh Lục-hải-không quân (F1 1.0)  
**Cửa sổ (rút gọn):** Tháng 6 năm 1928, Diêm Tích Sơn chiếm được Bắc Kinh, kết thúc thắng lợi cuộc Bắc phạt. Diêm Tích Sơn được Tưởng Giới Thạch ban thưởng các chức Bộ trưởng Bộ Nội chính và Phó tổng tư lệnh Lục-hải-không quân. Do ủng hộ các chiến dịch quân sự và công cuộc đàn áp Cộng sản của Tưởng Giới Thạch, Tưởng Giới Thạch công nhận Diêm Tích Sơn là chủ tịch của tỉn…

**Bài:** Diêm Tích Sơn (15,512 âm tiết), cửa sổ ở 73% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chính trị viên của Lưu Bá Thừa là ai?  
**Đáp án sinh:** Đặng Tiểu Bình  
**Kiểm:** Đặng Tiểu Bình (F1 1.0)  
**Cửa sổ (rút gọn):** Trong cùng năm đó, cựu tướng của Diêm Tích Sơn là Phó Tác Nghĩa chiếm được một số thành thị quan trọng tại Nội Mông: Bao Đầu và Hohhot. Nếu cả Diêm Tích Sơn và Phó Tác Nghĩa giành được thắng lợi, họ sẽ cắt đứt đường nối giữa tổng hành dinh của Cộng sản tại Diên An và quân đội của họ tại Đông Bắc. Chỉ huy Giải phóng quân tại địa phương là Lưu Bá Thừ…

**Bài:** Diêm Tích Sơn (15,512 âm tiết), cửa sổ ở 94% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Tác phẩm nào được đề cập trong đoạn trích có tiêu đề là 'Modern China's Ethnic Frontiers: A Journey to the West'?  
**Đáp án sinh:** Routelage  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** The USA and Canada: Routelage. Modern China's Ethnic Frontiers: A Journey to the West. Truy cập ngày 21 tháng 5 năm 2012. The Search for Modern China, W.W. "CHINA: President Resigns."  TIME Magazine. Truy cập ngày 24 tháng 2 năm 2011. "Foreign News: Yen to Nanking."  TIME Magazine. Truy cập ngày 24 tháng 2 năm 2011. ngày 19 tháng 5 năm 1930. Truy c…

**Bài:** Diêm Tích Sơn (15,512 âm tiết), cửa sổ ở 30% bài  
**Trạng thái:** kept  
**Câu hỏi:** Diêm Tích Sơn đã tiến hành phần lớn các nỗ lực truyền bá tư tưởng của mình thông qua mạng lưới các tổ chức bán tôn giáo mang tên gì?  
**Đáp án sinh:** Tẩy tâm xã  
**Kiểm:** Tẩy tâm xã (F1 1.0)  
**Cửa sổ (rút gọn):** Dù tình hình kinh tế Sơn Tây được cải thiện đáng kể, song những nỗ lực của Diêm Tích Sơn vẫn bị giới hạn, bởi thực tế là bản thân ông thiếu kiến thức chính quy về kinh tế hay công nghiệp. Diêm Tích Sơn cũng không có những cố vấn giàu kinh nghiệm để có thể chỉ đạo những dự án dù chỉ phức tạp ở mức độ tương đối có liên quan đến kế hoạch phát triển ki…

**Bài:** Diêm Tích Sơn (15,512 âm tiết), cửa sổ ở 63% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vệ Lập Hoàng đã thiết lập hệ thống phòng thủ vững chắc tại đâu?  
**Đáp án sinh:** Linh Thạch quan  
**Kiểm:** Linh Thạch quan (F1 1.0)  
**Cửa sổ (rút gọn):** Lực lượng phòng thủ của Diêm Tích Sơn dưới quyền chỉ huy của Vệ Lập Hoàng thiết lập một hệ thống phòng thủ vững chắc tại Linh Thạch quan, song cuối cùng buộc phải bỏ vị trí khi quân Nhật phá vỡ phòng tuyến thông qua một đèo khác và đe dọa Lâm Phần từ phía đông. Vệ Lập Hoằng thành công trong việc ngăn chặn quân Nhật chiếm dãy núi Trung Điều chiến lư…

**Bài:** Diêm Tích Sơn (15,512 âm tiết), cửa sổ ở 83% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Diêm Tích Sơn giữ chức vụ gì trong chính phủ do Lý Tông Nhân thiết lập?  
**Đáp án sinh:** Viện trưởng Hành chính viện  
**Kiểm:** Viện trưởng Hành chính viện, tức thủ tướng (F1 0.62)  
**Cửa sổ (rút gọn):** Một thời gian ngắn sau khi đến Nam Kinh, Diêm Tích Sơn tham gia tranh chấp giữa tổng thống lâm thời Lý Tông Nhân với cựu tổng thống Tưởng Giới Thạch. Mặc dù Tưởng Giới Thạch đã từ chức, song nhiều quan chức và tướng lĩnh vẫn trung thành với ông ta, và Tưởng Giới Thạch giữ lại hơn 200 triệu USD, không cho Lý Tông Nhân sử dụng chúng để chống lại lực …

**Bài:** Diêm Tích Sơn (15,512 âm tiết), cửa sổ ở 96% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Cuốn sách nào được trích dẫn trong đoạn văn có tiêu đề là 'Modern China: An Encyclopedia of History, Culture, and Nationalism'?  
**Đáp án sinh:** Modern China: An Encyclopedia of History, Culture, and Nationalism  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Truy cập ngày 24 tháng 2 năm 2011. "Foreign News: Yen to Nanking."  TIME Magazine. Truy cập ngày 24 tháng 2 năm 2011. ngày 19 tháng 5 năm 1930. Truy cập ngày 24 tháng 2 năm 2011. Modern China: An Encyclopedia of History, Culture, and Nationalism. United States of America: Wang Ke-wen. Truy cập ngày 4 tháng 6 năm 2012. Larry Wortzel Dictionary of Co…

**Bài:** EXO (nhóm nhạc) (10,083 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tên của chuyến lưu diễn EXO PLANET #4 là gì?  
**Đáp án sinh:** The EℓyXiOn  
**Kiểm:** The EℓyXiOn (F1 1.0)  
**Cửa sổ (rút gọn):** 2016: EXO from EXOPLANET #2 – The EXO'luXion in Seoul 2017: EXO from EXOPLANET #3 – The EXO'rdium in Japan 2017: EXO from EXOPLANET #3 – The EXO'rdium in Seoul 2018: EXO PLANET #4 – The EℓyXiOn – in Japan 2018: EXO PLANET #4 – The EℓyXiOn – in Seoul 2019: EXO PLANET #5 – The EXplOration – in Japan 2021: EXO FILMLIVE JAPAN TOUR - EXO PLANET 2021 201…

**Bài:** EXO (nhóm nhạc) (10,083 âm tiết), cửa sổ ở 22% bài  
**Trạng thái:** kept  
**Câu hỏi:** EXO đã phát hành phiên bản tái phát hành của album Exodus với tựa đề nào vào ngày 3 tháng 6 năm 2015?  
**Đáp án sinh:** Love Me Right  
**Kiểm:** Love Me Right (F1 1.0)  
**Cửa sổ (rút gọn):** Chúng tôi cũng có kế hoạch thực hiện các bước pháp lý để đáp trả lại những hoạt động và quá trình quảng bá bất hợp pháp của Tao." EXO phát hành phiên bản tái phát hành của Exodus với tựa đề Love Me Right vào ngày 3 tháng 6 năm 2015. Phiên bản này có thêm bốn bài hát, trong đó bao gồm cả "Love Me Right". Do sự vắng mặt của Tao, nhóm quảng bá ca khúc…

**Bài:** EXO (nhóm nhạc) (10,083 âm tiết), cửa sổ ở 46% bài  
**Trạng thái:** kept  
**Câu hỏi:** Album solo thứ 3 của Lay ra mắt tại Hoa Kỳ vào tháng 10 năm 2018 có tên là gì?  
**Đáp án sinh:** Namanana  
**Kiểm:** Namanana (F1 1.0)  
**Cửa sổ (rút gọn):** Vào tháng 3 năm 2018, tập đoàn đúc tiền của Hàn Quốc đã công bố kế hoạch tạo ra các huy chương kỷ niệm chính thức cho EXO, vinh danh nhóm vì sự đóng góp của họ cho sự lan rộng văn hóa Hàn Quốc ra toàn cầu. Bộ chín huy chương với mỗi huy chương kỷ niệm gắn với một thành viên trong nhóm đã được công bố vào ngày 18 tháng 4 tại một buổi lễ ở Seoul. Vào…

**Bài:** EXO (nhóm nhạc) (10,083 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Vụ lật phà nào đã khiến EP Overdose của EXO bị trì hoãn phát hành?  
**Đáp án sinh:** vụ lật phà Sewol  
**Kiểm:** Sewol (F1 0.4)  
**Cửa sổ (rút gọn):** Ban đầu EP dự kiến được phát hành vào ngày 21 tháng 4 nhưng sau đó bị trì hoãn do vụ lật phà Sewol xảy ra vào ngày 16 tháng 4. Overdose có cách thức quảng bá giống với Mama: EXO-K quảng bá ở Hàn Quốc và EXO-M quảng bá chủ yếu ở Trung Quốc. EP được đặt mua trước trên 660.000 bản, khiến nó trở thành EP của Hàn Quốc có lượng đặt mua trước cao nhất lịc…

**Bài:** EXO (nhóm nhạc) (10,083 âm tiết), cửa sổ ở 11% bài  
**Trạng thái:** kept  
**Câu hỏi:** Album phòng thu đầu tiên của EXO được phát hành vào ngày nào?  
**Đáp án sinh:** 3 tháng 6 năm 2013  
**Kiểm:** 3 tháng 6 năm 2013 (F1 1.0)  
**Cửa sổ (rút gọn):** EXO đã nhận giải Nhóm nhạc tân binh châu Á xuất sắc nhất tại Mnet Asian Music Awards 2012 và Giải tân binh tại Golden Disc Awards. 2013–2014: Thành công thương mại Album phòng thu đầu tiên của nhóm XOXO được phát hành vào ngày 3 tháng 6 năm 2013 với hai phiên bản: tiếng Hàn và tiếng Quan Thoại. Khác với quá trình quảng bá riêng biệt của EXO-K và EX…

**Bài:** EXO (nhóm nhạc) (10,083 âm tiết), cửa sổ ở 49% bài  
**Trạng thái:** kept  
**Câu hỏi:** Album nào được mô tả là album bán chạy nhất của EXO với doanh số 1.951.879 bản tại Hàn Quốc vào năm 2018?  
**Đáp án sinh:** Don't Mess Up My Tempo  
**Kiểm:** Don't Mess Up My Tempo (F1 1.0)  
**Cửa sổ (rút gọn):** Love Shot được phát hành vào ngày 13 tháng 12 dưới dạng tái phát hành của Don't Mess Up My Tempo. Đĩa đơn dẫn đường Love Shot của album trở thành đĩa đơn quán quân thứ ba của EXO trên bảng xếp hạng Billboard World Digital Songs và trụ hạng trong ba tuần liên tiếp. Don't Mess Up My Tempo đã bán được 1.951.879 bản tại Hàn Quốc vào năm 2018 và là albu…

**Bài:** EXO (nhóm nhạc) (10,083 âm tiết), cửa sổ ở 70% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo tờ Dazed, phần vũ đạo của EXO đã đưa nhóm đến vị trí nào trong lĩnh vực nhạc pop?  
**Đáp án sinh:** dẫn đầu sự thống trị nhạc pop  
**Kiểm:** dẫn đầu sự thống trị nhạc pop (F1 1.0)  
**Cửa sổ (rút gọn):** Chanyeol còn tham gia vào quá trình viết lời cho "Gravity" và "With You", cả hai ca khúc đều trích từ album phòng thu thứ sáu Don't Mess Up My Tempo của nhóm. EXO đã được khen ngợi đặc biệt vì vũ đạo đồng bộ và các thiết kế sân khấu phức tạp của họ. Thời gian đầu của sự nghiệp, các vũ đạo của nhóm lần lượt được biên đạo bởi các biên đạo múa hip hop…

**Bài:** EXO (nhóm nhạc) (10,083 âm tiết), cửa sổ ở 83% bài  
**Trạng thái:** kept  
**Câu hỏi:** EXO được bổ nhiệm làm đại sứ cho công ty các môn thể thao về tuyết nào có trụ sở tại Thụy Sĩ vào năm 2018?  
**Đáp án sinh:** Kessler  
**Kiểm:** Kessler (F1 1.0)  
**Cửa sổ (rút gọn):** Cũng trong năm 2016, nhóm trở thành gương mặt chính thức cho bộ sưu tập xuân của thương hiệu quần áo quốc tế SPAO, trong đó bao gồm các bưu thiếp phiên bản giới hạn và áp phích cho khách hàng. Năm 2018, nhờ màn trình diễn của EXO tại Lễ bế mạc cho Thế vận hội mùa đông 2018, nhóm trở thành gương mặt thương hiệu của công ty các môn thể thao về tuyết …

**Bài:** Robert Lewandowski (10,387 âm tiết), cửa sổ ở 14% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lewandowski đã phá vỡ kỷ lục ghi bàn liên tiếp của câu lạc bộ tại Bundesliga với thành tích bao nhiêu trận?  
**Đáp án sinh:** 12 trận  
**Kiểm:** 12 trận (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 21 tháng 4, Lewandowski kiến tạo cho Kagawa đem về chiến thắng 2–0 trước Borussia Mönchengladbach giúp Dortmund bảo vệ thành công chức vô địch. Trận đấu cuối cùng của Bundesliga mùa giải 2011-12, anh lập cú đúp trong chiến thắng 4-0 trước Freiburg. Lewandowski đem về cho Dortmund cú đúp danh hiệu vô địch mùa giải 2011-12 với hat-trick trong tr…

**Bài:** Robert Lewandowski (10,387 âm tiết), cửa sổ ở 49% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lewandowski đã nhận được giải thưởng nào do tạp chí France Football bình chọn giữa mùa giải 2021-2022?  
**Đáp án sinh:** Tiền đạo của năm  
**Kiểm:** Tiền đạo của năm (F1 1.0)  
**Cửa sổ (rút gọn):** Vào ngày 18 tháng 9, Lewandowski ghi bàn trong trận đấu thứ 13 liên tiếp trên sân nhà tại Bundesliga trước VfL Bochum, vượt qua kỷ lục 12 trận trước đó do Gerd Müller nắm giữ (tháng 10 năm 1969 đến tháng 4 năm 1970) và Jupp Heynckes (tháng 6 năm 1972 đến tháng 2 năm 1973).Vào ngày 23 tháng 11, Lewandowski đã mở tỷ số bằng một cú đá xe đạp chổng ngư…

**Bài:** Robert Lewandowski (10,387 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lewandowski cùng với cầu thủ nào của Bắc Ireland trở thành cầu thủ ghi bàn nhiều nhất vòng loại Euro 2016?  
**Đáp án sinh:** David Healy  
**Kiểm:** David Healy (F1 1.0)  
**Cửa sổ (rút gọn):** 2013–2017: Đảm nhận băng đội trưởng Ngày 26 tháng 3 năm 2013, trong khuôn khổ lượt trận thứ 7 của vòng loại World Cup 2014 khu vực châu Âu, Lewandowski ghi được hai bàn thắng trên chấm phạt đền trong chiến thắng 5-0 trước San Marino và lượt trận thứ 9, anh chỉ có được một bàn thắng trong trận hòa 1-1 trước Montenegro. Ba Lan không thể góp mặt ở Wor…

**Bài:** Robert Lewandowski (10,387 âm tiết), cửa sổ ở 44% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lewandowski đã cân bằng kỷ lục 49 năm của Gerd Müller về số bàn thắng trong một mùa giải Bundesliga bằng cách nào?  
**Đáp án sinh:** pha thực hiện phạt đền thành công ở trận hòa Freiburg 2-2  
**Kiểm:** pha thực hiện phạt đền thành công ở trận hòa Freiburg 2-2 (F1 1.0)  
**Cửa sổ (rút gọn):** Việc hủy bỏ Quả bóng vàng 2020 đã vấp phải sự chỉ trích mạnh mẽ, vì hầu hết các tổ chức tin tức và thể thao đều tin rằng Lewandowski là người thắng cuộc và đáng lẽ ra đã giành được giải thưởng này. Vào ngày 17 tháng 1 năm 2021, Lewandowski trở thành cầu thủ đầu tiên trong lịch sử Bundesliga ghi được 21 bàn chỉ sau 16 trận - một kỷ lục mới của Hinru…

**Bài:** Robert Lewandowski (10,387 âm tiết), cửa sổ ở 85% bài  
**Trạng thái:** kept  
**Câu hỏi:** Robert Lewandowski đã giành danh hiệu Vua phá lưới Bundesliga mùa giải 2020–21 với bao nhiêu bàn thắng?  
**Đáp án sinh:** 41 bàn  
**Kiểm:** 41 bàn (F1 1.0)  
**Cửa sổ (rút gọn):** Cầu thủ xuất sắc nhất của Ekstraklasa: 2009 Vua phá lưới Ekstraklasa: 2009-10 Vua phá lưới Bundesliga: 2013–14 (20 bàn), 2015–16 (30 bàn), 2017–18 (29 bàn), 2018–19 (22 bàn), 2019–20 (34 bàn), 2020–21 (41 bàn). FIFA FIFPro World 11: 2020, 2021 Vua phá lưới La Liga: 2022-2023 (23 bàn) Vua phá lưới DFB Pokal: 2011–12 (7 bàn), 2016–17 (5 bàn), 2017–18…

**Bài:** Robert Lewandowski (10,387 âm tiết), cửa sổ ở 89% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cầu thủ nào đã giành giải Cầu thủ xuất sắc nhất năm của World Soccer vào các năm 2020 và 2021?  
**Đáp án sinh:** Cầu thủ xuất sắc nhất năm của World Soccer: 2020, 2021  
**Kiểm:** Cầu thủ xuất sắc nhất năm của World Soccer: 2020, 2021 (F1 1.0)  
**Cửa sổ (rút gọn):** Cầu thủ hay nhất vòng loại UEFA Euro: 2016 Cầu thủ xuất sắc nhất năm của World Soccer: 2020, 2021 Cầu thủ xuất sắc nhất năm của Globe Soccer: 2020 Đội hình UEFA Champions League: 2015, 2017, 2020 Đội hình tiêu biểu của Bundesliga: 2014, 2015, 2016, 2017, 2018, 2019, 2020 Cầu thủ xuất sắc nhất năm của UEFA: 2020 Đội hình xuất sắc nhất của ESM: 2019-…

**Bài:** Robert Lewandowski (10,387 âm tiết), cửa sổ ở 28% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lewandowski đạt cột mốc 100 bàn thắng cho Bayern sau bao nhiêu trận đấu?  
**Đáp án sinh:** 137 trận  
**Kiểm:** 137 trận (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 25 tháng 2, anh lập hat-trick trong chiến thắng hủy diệt 8-0 trước Hamburger SV. Ngày 11 tháng 3 năm 2017, Lewandowski đạt đến cột mốc 100 bàn thắng sau 137 trận cho Bayern với cú đúp trong chiến thắng 3-0 trước Eintracht Frankfurt tại Bundesliga. 2017–2019: Liên tiếp đoạt Chiếc giày vàng và là cầu thủ ghi bàn nước ngoài mọi thời đại tại Bunde…

**Bài:** Robert Lewandowski (10,387 âm tiết), cửa sổ ở 77% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cha của Lewandowski từng chơi bóng cho đội nào ở giải hạng hai?  
**Đáp án sinh:** Hutnik Warsaw  
**Kiểm:** Hutnik Warsaw (F1 1.0)  
**Cửa sổ (rút gọn):** Cha của Lewandowski, Krzysztof (mất năm 2005), là nhà vô địch judo Ba Lan, và cũng chơi bóng cho Hutnik Warsaw ở giải hạng hai. Mẹ anh, Iwona, là cựu cầu thủ bóng chuyền cho AZS Warsaw và sau đó là phó chủ tịch của Partyzant Leszno. Chị gái của anh, Milena, cũng chơi bóng chuyền và từng đại diện cho đội tuyển quốc gia U21. Vợ anh, Anna Lewandowska,…

**Bài:** Thomas Cranmer (9,242 âm tiết), cửa sổ ở 68% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cuộc đảo chính không đổ máu diễn ra vào ngày 13 tháng 10 năm 1549 đã chấm dứt quyền nhiếp chính của ai?  
**Đáp án sinh:** Seymour  
**Kiểm:** Seymour (F1 1.0)  
**Cửa sổ (rút gọn):** Nhưng sau một loạt những trao đổi giữa hai bên, một cuộc đảo chính không đổ máu diễn ra trong ngày 13 tháng 10 năm 1549 đã chấm dứt quyền nhiếp chính của Seymour. Mặc dù các chính trị gia có quan điểm tôn giáo bảo thủ ủng hộ cuộc đảo chính của Dudley, những người cải cách giành được quyền kiểm soát và tiếp tục củng cố những thành quả của cuộc Cải c…

**Bài:** Thomas Cranmer (9,242 âm tiết), cửa sổ ở 63% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cranmer được công nhận là người biên tập toàn bộ tác phẩm nào?  
**Đáp án sinh:** Sách Cầu nguyện chung  
**Kiểm:** Sách Cầu nguyện chung (F1 1.0)  
**Cửa sổ (rút gọn):** Ông cần những học giả đến đào tạo một thế hệ mới các chức sắc cũng như hỗ trợ công cuộc cải cách trong lĩnh vực thần học và giáo nghi. Nhà cải cách người Ba Lan, Jan Łaski cũng đến Anh theo lời mời của Cranmer, nhưng ông không thể thuyết phục Osiander và Melanchthon đến Anh. Sách Cầu nguyện chung (1548 – 1549) Khi việc sử dụng tiếng Anh trong lễ th…

**Bài:** Thomas Cranmer (9,242 âm tiết), cửa sổ ở 74% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cranmer đã mời những nhà cải cách hàng đầu nào của lục địa đến Anh vào tháng 3 năm 1552?  
**Đáp án sinh:** Bullinger, John Calvin, và Melanchthon  
**Kiểm:** Bullinger, John Calvin, và Melanchthon (F1 1.0)  
**Cửa sổ (rút gọn):** Động thái này chứng tỏ Cranmer không hề nhớ đến ân oán cũ. Cranmer cùng Martyr nhận ra rằng một bộ luật tôn giáo theo khuynh hướng cải cách nếu được thông qua tại Anh sẽ có ảnh hưởng quốc tế. Cranmer lập kế hoạch tập hợp tất cả các giáo hội cải cách tại châu Âu dưới sự lãnh đạo của nước Anh nhằm chống lại Công đồng Trent của Giáo hội Công giáo được…

**Bài:** Thomas Cranmer (9,242 âm tiết), cửa sổ ở 37% bài  
**Trạng thái:** kept  
**Câu hỏi:** Phái đoàn Đức rời nước Anh vào ngày nào?  
**Đáp án sinh:** ngày 1 tháng 10  
**Kiểm:** ngày 1 tháng 10 (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 27 tháng 5 năm 1538, phái đoàn đến Anh. Sau vài lần hội kiến với nhà vua, tại Điện Lambeth, phái đoàn thảo luận với Cromwell và Cranmer về những dị biệt từ hai phía. Không có sự tiến bộ rõ rệt, một phần do Cromwell quá bận tâm đến nỗ lực đẩy mạnh tiến trình, phần khác do phía người Anh với chủ trương quân bình giữa lập trường bảo thủ và cấp ti…

**Bài:** Thomas Cranmer (9,242 âm tiết), cửa sổ ở 9% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Cranmer, Henry VIII là người như thế nào?  
**Đáp án sinh:** người tốt bụng nhất trong những ông hoàng  
**Kiểm:** người tốt bụng nhất trong những ông hoàng (F1 1.0)  
**Cửa sổ (rút gọn):** Theo truyền thuyết, ông là nhà nhân văn đầy nhiệt huyết, chuyên tâm nghiên cứu Kinh Thánh, điều này dẫn dắt ông đến với tư tưởng Luther đã được phổ biến từ thập niên 1520. Tuy nhiên, những ghi chú của Cranmer cho thấy lúc đầu ông phản bác Martin Luther mà khâm phục Erasmus. Khi Hồng y Wolsey, tể tướng của nhà vua, chọn vài học giả từ Cambridge đi s…

**Bài:** Thomas Cranmer (9,242 âm tiết), cửa sổ ở 78% bài  
**Trạng thái:** kept  
**Câu hỏi:** Edward VI đã lập di chúc truyền ngôi cho ai thay vì Mary?  
**Đáp án sinh:** Lady Jane Grey  
**Kiểm:** Lady Jane Grey (F1 1.0)  
**Cửa sổ (rút gọn):** Edward VI mắc bệnh lao, bệnh trở nặng, các thành viên hội đồng cơ mật được báo cho biết nhà vua sẽ không sống lâu. Ngày 17 tháng 6 năm 1553, nhà vua lập di chúc truyền ngôi cho Lady Jane Grey, một người em họ và là tín hữu Kháng Cách, thay vì Mary con gái của Henry với Catharine Aragon, một giáo dân Công giáo. Quyết định này của Edward là mâu thuẫn…

**Bài:** Thomas Cranmer (9,242 âm tiết), cửa sổ ở 2% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thomas Cranmer chào đời vào năm nào?  
**Đáp án sinh:** 1489  
**Kiểm:** 1489 (F1 1.0)  
**Cửa sổ (rút gọn):** Ông viết và soạn hai phiên bản cho Sách Cầu nguyện chung là quyển giáo nghi hoàn chỉnh cho Giáo hội Anh. Với sự trợ giúp của những nhà cải cách châu Âu mà ông dành cho họ quyền tị nạn, Cranmer đã xây dựng những chuẩn mực mới trong các lĩnh vực thần học như Tiệc Thánh, tình trạng độc thân của giáo sĩ, việc sử dụng ảnh tượng tại những nơi thờ phượng,…

**Bài:** Thomas Cranmer (9,242 âm tiết), cửa sổ ở 13% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Cranmer đã kết hôn với ai vào tháng 7 năm 1532?  
**Đáp án sinh:** Margarete  
**Kiểm:** Margarete, cháu gái của vợ Osiander (F1 0.0)  
**Cửa sổ (rút gọn):** Henry tỏ ra chú tâm khi nghe Gardiner cùng Foxe trình bày kế hoạch này. Không ai biết rõ nhà vua hay quan Tể tướng Thomas More công khai ủng hộ kế hoạch, nhưng dần dà Cranmer cũng được yêu cầu gia nhập phái đoàn nhà vua cử đến Rome để thu thập ý kiến của giới đại học. Edward Foxe phối hợp những nỗ lực nghiên cứu để phái đoàn kiến tạo hai văn kiện C…

**Bài:** Lịch sử Azerbaijan (13,262 âm tiết), cửa sổ ở 76% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người được chính phủ ở Moscow bổ nhiệm làm bí thư thứ nhất của Đảng Cộng sản Azerbaijan vào năm 1969?  
**Đáp án sinh:** Heydar Aliyev  
**Kiểm:** Heydar Aliyev (F1 1.0)  
**Cửa sổ (rút gọn):** Người Đức cũng đã có những nỗ lực không kết quả để tranh thủ sự hợp tác của các nhân vật chính trị lưu vong, đáng chú ý nhất là Mammed Amin Rasulzade. Các chính sách phá bỏ Stalin và cải tiến sau những năm 1950 đã dẫn đến các điều kiện giáo dục và phúc lợi tốt hơn cho hầu hết Azerbaijan. Điều này cũng đồng thời với giai đoạn đô thị hóa và công nghi…

**Bài:** Lịch sử Azerbaijan (13,262 âm tiết), cửa sổ ở 88% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Mỏ khí đốt nào được phát hiện vào đầu năm 1999 khiến Azerbaijan có khả năng trở thành một nhà xuất khẩu khí đốt lớn?  
**Đáp án sinh:** mỏ khí đốt Shah Deniz  
**Kiểm:** Shah Deniz (F1 0.57)  
**Cửa sổ (rút gọn):** Vì vậy, vào cuối năm 1996, Heydar Aliyev là một  người thống trị tuyệt đối  ở Azerbaijan. Do kết quả của những cải cách hạn chế và việc ký kết cái gọi là "Hợp đồng Thế kỷ" vào tháng 10 năm 1994 (phức hợp mỏ dầu khổng lồ Azeri-Chirag-Guneshli) dẫn đến việc tăng xuất khẩu dầu sang các thị trường phương Tây, kinh tế bắt đầu cải thiện. Tuy nhiên, mức đ…

**Bài:** Lịch sử Azerbaijan (13,262 âm tiết), cửa sổ ở 42% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà Safavi Iran trở thành một chế độ gì trong thời kỳ trị vì của Ismail I và Tahmasp I?  
**Đáp án sinh:** chế độ thần quyền phong kiến  
**Kiểm:** chế độ thần quyền phong kiến (F1 1.0)  
**Cửa sổ (rút gọn):** Nhà Safavi do Ismail I lãnh đạo đã mở rộng căn cứ của họ ở Ardabil; họ đã chinh phục Kavkaz, các vùng ở Tiểu Á, Lưỡng Hà, Trung Á và các vùng phía tây Nam Á. Ismail đã cướp phá Baku vào năm 1501 và đàn áp các Shirvanshah dòng Sunni. Azerbaijan, Armenia và Dagestan đã bị nhà Safavi chinh phục từ năm 1500 đến 1502. Trong thời trị vì của Ismail I và c…

**Bài:** Lịch sử Azerbaijan (13,262 âm tiết), cửa sổ ở 75% bài  
**Trạng thái:** kept  
**Câu hỏi:** Mục tiêu đặc biệt của ông trong việc thanh trừng là ai?  
**Đáp án sinh:** giới trí thức  
**Kiểm:** giới trí thức (F1 1.0)  
**Cửa sổ (rút gọn):** Mục tiêu đặc biệt của ông là giới trí thức nhưng ông cũng thanh trừng các lãnh đạo Cộng sản có thiện cảm với phe đối lập hoặc những người có thể đã từng nghiêng về Chủ nghĩa liên Thổ hoặc có liên hệ với các phong trào cách mạng ở Iran hoặc Thổ Nhĩ Kỳ. Trong những năm 1940, Cộng hòa Xã hội chủ nghĩa Xô viết Azerbaijan đã cung cấp phần lớn khí đốt và…

**Bài:** Lịch sử Azerbaijan (13,262 âm tiết), cửa sổ ở 87% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào ngày 3 tháng 10 năm 1993, ai đã giành chiến thắng áp đảo trong cuộc bầu cử tổng thống Azerbaijan?  
**Đáp án sinh:** Aliyev  
**Kiểm:** Aliyev (F1 1.0)  
**Cửa sổ (rút gọn):** Tại Baku, Aliyev cầm cương và nhanh chóng củng cố vị trí của mình. Cuộc trưng cầu tín nhiệm vào tháng 8 đã tước bỏ chức vụ của Elchibey. Nhiệm kỳ tổng thống của Heydar Aliyev (1993–2003) Vào ngày 3 tháng 10 năm 1993, một cuộc bầu cử tổng thống được tổ chức và Aliyev đã giành chiến thắng áp đảo. Đến tháng 3 năm 1994, Aliyev đã có thể thoát khỏi một …

**Bài:** Lịch sử Azerbaijan (13,262 âm tiết), cửa sổ ở 82% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai được bầu làm tổng thống Azerbaijan với hơn 60% phiếu bầu sau khi các lực lượng vũ trang do Mặt trận nhân dân Azerbaijan lãnh đạo hạ bệ Mütallibov?  
**Đáp án sinh:** Abulfaz Elchibey  
**Kiểm:** Abulfaz Elchibey (F1 1.0)  
**Cửa sổ (rút gọn):** Trong khi đó, xung đột về Nagorno Karabakh vẫn tiếp tục bất chấp những nỗ lực thương lượng dàn xếp. Đầu năm 1992, lãnh đạo người Armenia của Karabakh tuyên bố trở thành một nước cộng hòa độc lập. Trong thời điểm bây giờ là một cuộc chiến toàn diện giữa Armenia và Azerbaijan, người Armenia đã giành được ưu thế với sự hỗ trợ bí mật của Quân đội Nga. …

**Bài:** Lịch sử Azerbaijan (13,262 âm tiết), cửa sổ ở 70% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người đứng đầu trong ba nội các đầu tiên của nước cộng hòa Azerbaijan?  
**Đáp án sinh:** Fatali Khan Khoyski  
**Kiểm:** Fatali Khan Khoyski (F1 1.0)  
**Cửa sổ (rút gọn):** Nước cộng hòa được điều hành bởi năm nội các, tất cả được thành lập bởi liên minh của Musavat và các đảng khác bao gồm Khối xã hội chủ nghĩa, Đảng độc lập, Đảng tự do, Đảng Xã hội-Dân chủ Hummat (hoặc Endeavour) và Đảng Bảo thủ Ittihad (Liên minh). Người đứng đầu trong ba nội các đầu tiên là Fatali Khan Khoyski; trong hai nội các cuối là Nasib Yusi…

**Bài:** Lịch sử Azerbaijan (13,262 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Đảng Musavat được hình thành vào năm nào?  
**Đáp án sinh:** 1911  
**Kiểm:** năm 1911 (F1 0.67)  
**Cửa sổ (rút gọn):** Tình hình được cải thiện trong giai đoạn 1906–1914 khi một hệ thống nghị viện hạn chế ra đời ở Nga và các nghị sĩ Hồi giáo từ Azerbaijan đang tích cực thúc đẩy lợi ích của Azerbaijan. Vào năm 1911, Đảng Musavat theo chủ nghĩa liên Hồi giáo và liên Thổ, lấy cảm hứng từ hệ tư tưởng chủ nghĩa hiện đại cánh tả của Mammed Amin Rasulzade, đã được hình th…

**Bài:** Qumran (9,642 âm tiết), cửa sổ ở 0% bài  
**Trạng thái:** kept  
**Câu hỏi:** Các cuộn bản thảo Biển Chết được tìm thấy tại Qumran phần lớn được viết trên chất liệu gì?  
**Đáp án sinh:** giấy da  
**Kiểm:** giấy da (F1 1.0)  
**Cửa sổ (rút gọn):** Qumran (,  - Khirbet Qumran) là một địa điểm khảo cổ ở Bờ Tây. Nó nằm ở một cao nguyên khô ráo cách bờ tây bắc của Biển Chết khoảng một dặm, gần nơi định cư của người Do Thái và kibbutz Kalya. Nơi định cư thời văn minh Hy Lạp hóa này được xây dựng trong triều đại Yohanan Hyrcanus (Vương quốc Hasmoneus), 134-104 trước Công nguyên hoặc hơi muộn hơn, …

**Bài:** Qumran (9,642 âm tiết), cửa sổ ở 87% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cuốn sách 'Wealth in the Dead Sea Scrolls and the Qumran Community' của Catherine M. Murphy được xuất bản tại đâu?  
**Đáp án sinh:** Leiden  
**Kiểm:** Leiden (F1 1.0)  
**Cửa sổ (rút gọn):** Murphy, Catherine M., Wealth in the Dead Sea Scrolls and the Qumran Community, (Leiden: Brill 2002). "Did any perfume industry exist at ʻEin Feshkha?," Israel Exploration Journal 55 no 1 2005, p 97-100. Patrich, Joseph, "Khirbet Qumran in the Light of New Archaeological Explorations in the Qumran Caves", in Methods of Investigation of the Dead Sea …

**Bài:** Qumran (9,642 âm tiết), cửa sổ ở 70% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cuốn sách 'Qumran: A Field Guide' của Hanan Eshel được xuất bản tại thành phố nào?  
**Đáp án sinh:** Leiden  
**Kiểm:** Leiden (F1 1.0)  
**Cửa sổ (rút gọn):** Bernus-Taylor et al.; ResO 4; Leuven: Peeters, 1992) 61-84. Eshel, Hanan, Qumran: A Field Guide. The Dead Sea Scrolls: A Full History. volume 1 (Leiden: Brill, 2009). Galor, Katharina, "Plastered Pools: A New Perspective", in Khirbet Qumran et Ain Feshkha, Vol. Humbert, Jean-Baptiste & Gunneweg, Jan, (Vandenhoeck & Ruprecht Goettingen, 2003) 291-32…

**Bài:** Qumran (9,642 âm tiết), cửa sổ ở 47% bài  
**Trạng thái:** kept  
**Câu hỏi:** Karl Heinrich Rengstorf đề xuất rằng Cuộn Kinh Thánh tìm được ở gần Biển Chết là sản phẩm của thư viện nào?  
**Đáp án sinh:** thư viện của đền thờ Jerusalem  
**Kiểm:** thư viện của đền thờ Jerusalem (F1 1.0)  
**Cửa sổ (rút gọn):** Năm 1955 người đồng giám đốc khai quật ban đầu của De Vaux - G. Lankester Harding – đã viết một bài báo trong đó ông trình bày Qumran là "một tòa nhà trong đó Gioan Tẩy giả, và dường như cả chúa Giêsu, đã học tập: Khirbet Qumran". Những người khác bên ngoài nhóm De Vaux đề xuất những giải thích khác, những người như Henri del Medico, Solomon Zeitli…

**Bài:** Qumran (9,642 âm tiết), cửa sổ ở 34% bài  
**Trạng thái:** kept  
**Câu hỏi:** Các tiền đúc chót thuộc về Hoàng đế Caracalla được sản xuất bởi xưởng đúc tiền nào?  
**Đáp án sinh:** xưởng đúc tiền của Rome  
**Kiểm:** xưởng đúc tiền của Rome (F1 1.0)  
**Cửa sổ (rút gọn):** Các tiền đúc chót thuộc về Hoàng đế Caracalla và do xưởng đúc tiền của Rome (206-210 sau CN). Các gợi ý mới cho rằng các kho cất giấu tiền đúc bằng bạc ở Qumran có thể liên quan tới các chiến dịch quân sự La Mã trong khu vực, như được chứng thực trong đầu thế kỷ thứ 3 sau CN. Rất có thể tiền đúc bằng bạc là khoản tiền quân đội La Mã trả cho các đội…

**Bài:** Qumran (9,642 âm tiết), cửa sổ ở 46% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo G. Lankester Harding, Qumran là nơi mà Gioan Tẩy giả và dường như cả chúa Giêsu đã làm gì?  
**Đáp án sinh:** học tập  
**Kiểm:** học tập (F1 1.0)  
**Cửa sổ (rút gọn):** Nơi cư ngụ của giáo phái Essenes Có vài nghi ngờ nghiêm trọng về việc giải thích địa điểm Qumran của De Vaux. Trong khi nhà khảo cổ học E.-M. Laperrousaz, có một số quan điểm hoàn toàn khác biệt, thì các thành viên trong nhóm De Vaux hầu như theo cùng một tường thuật với vài khác biệt nhỏ, trong đó có J. Năm 1955 người đồng giám đốc khai quật ban đ…

**Bài:** Qumran (9,642 âm tiết), cửa sổ ở 9% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Gustaf Dalman đã nhận ra Qumran là một thành trì hay pháo đài vào năm nào?  
**Đáp án sinh:** 1914  
**Kiểm:** năm 1914 (F1 0.67)  
**Cửa sổ (rút gọn):** Masterman cũng đặt câu hỏi tại sao một pháo đài nhỏ thế này mà lại có một nghĩa trang trên 1.000 ngôi mộ. Gustaf Dalman tới thăm Qumran năm 1914, và nhận ra rõ ràng Qumran là một "burg" (thành trì), hoặc pháo đài. Nhà khảo cổ Michael Avi-Yonah đồng ý với nhận định của Dalman cho rằng Qumran là một pháo đài và xuất bản một bản đồ xác định các phế tí…

**Bài:** Qumran (9,642 âm tiết), cửa sổ ở 27% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhiều bể chứa nước lớn được đặt cao dần lên theo bậc thang ở Qumran đã được nhiều học giả coi là những gì?  
**Đáp án sinh:** những bồn tắm theo nghi thức tôn giáo  
**Kiểm:** những bồn tắm theo nghi thức tôn giáo (F1 1.0)  
**Cửa sổ (rút gọn):** Nhiều bể chứa nước lớn được đặt cao dần lên theo bậc thang ở Qumran đã được nhiều học giả coi là những bồn tắm theo nghi thức tôn giáo. Điều này phù hợp với mô hình nơi định cư tôn giáo. Tuy nhiên có những khó khăn khi suy đoán rằng mọi bể chứa nước đều là bồn tắm. Có lẽ nước ở Qumran là do nước mưa chảy tới mỗi năm 2 đợt. Nước là một trong những t…

**Bài:** Ben-Hur (phim 1959) (10,912 âm tiết), cửa sổ ở 95% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Phim nào được đề cập trong đoạn trích đã giành giải Oscar cho phim hay nhất?  
**Đáp án sinh:** Phim giành giải Oscar cho phim hay nhất  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Classical Myth & Culture in the Cinema. New York: Oxford University Press, 2001. Wreszin, Michael and Macdonald, Dwight. Jackson, Miss.: University Press of Mississippi, 2003. "William Wyler." In Conversations with the Great Moviemakers of Hollywood's Golden Age at the American Film Institute. New York: Random House, 2007. Miklós Rózsa's Ben-Hur: A…

**Bài:** Ben-Hur (phim 1959) (10,912 âm tiết), cửa sổ ở 58% bài  
**Trạng thái:** kept  
**Câu hỏi:** Phim Ben-Hur được chiếu ra mắt tại rạp chiếu bóng nào ở thành phố New York?  
**Đáp án sinh:** rạp chiếu bóng Loew  
**Kiểm:** rạp chiếu bóng Loew (F1 1.0)  
**Cửa sổ (rút gọn):** Trong phim, việc lành bệnh này xảy ra sau khi chúa Giêsu đã chết, để nhấn mạnh cách mà "máu chúa Kitô" rửa sạch mọi tội lỗi thế gian. Trong tiểu thuyết, quan hệ giữa Quintus Arrius với Ben-Hur rất khác. Arrius quen biết cha của Ben-Hur. Ông cũng chết ít lâu sau khi nhận Ben-Hur làm con nuôi, chuyển gia tài và tước hiệu của mình cho Ben-Hur trước kh…

**Bài:** Ben-Hur (phim 1959) (10,912 âm tiết), cửa sổ ở 23% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà văn nào được xác định là người viết kịch bản cuối cùng cho bộ phim Ben-Hur?  
**Đáp án sinh:** Christopher Fry  
**Kiểm:** Christopher Fry (F1 1.0)  
**Cửa sổ (rút gọn):** Vidal cũng thêm vào vài chi tiết nhỏ như Ben-Hur mua một cái trâm cài tóc cho Tirzah và một con ngựa cho Messala. Vidal cho biết rằng ông đã sửa chữa nửa đầu tiên của kịch bản (tất cả mọi thứ cho tới cảnh cuộc đua xe chariot), và viết 10 phiên bản của cảnh Judah Ben-Hur đối mặt với Messala để xin trả tự do của gia đình mình. Nhà văn viết kịch bản c…

**Bài:** Ben-Hur (phim 1959) (10,912 âm tiết), cửa sổ ở 25% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo báo New York Times, ai đã nghi ngờ quyết định ban đầu của Nghiệp đoàn nhà văn viết kịch bản về vấn đề ai được ghi là nhà viết kịch bản phim Ben-Hur?  
**Đáp án sinh:** Vidal  
**Kiểm:** Vidal (F1 1.0)  
**Cửa sổ (rút gọn):** Wyler nói rằng ông ta đã tìm cách ghi Tunberg và Fry là đồng tác giả kịch bản. Lúc đầu Tunberg đồng ý, nhưng sau đó đã đổi ý, khi Nghiệp đoàn nhà văn viết kịch bản Hoa Kỳ muốn điều tra vụ việc theo thông lệ. Tuy nhiên theo Gore Vidal và nhà viết sử điện ảnh Gary Giddins, thì Wyler đã tìm cách chỉ ghi tên Fry là nhà viết kịch bản. Vụ tranh cãi về vi…

**Bài:** Ben-Hur (phim 1959) (10,912 âm tiết), cửa sổ ở 83% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà xuất bản của cuốn sách 'Epics, Spectacles, and Blockbusters: A Hollywood History' là gì?  
**Đáp án sinh:** Wayne State University Press  
**Kiểm:** Wayne State University Press (F1 1.0)  
**Cửa sổ (rút gọn):** New York: Jove Books, 1987. Warning Shadows: Home Alone With Classic Cinema. Technicolor Movies: The History of Dye Transfer Printing. Hall, Sheldon and Neale, Stephen. Epics, Spectacles, and Blockbusters: A Hollywood History. Detroit, Mich.: Wayne State University Press, 2010. Fatal Flaws of the Most Correct Book on Earth. Maitland, Fla.: Xulon Pr…

**Bài:** Ben-Hur (phim 1959) (10,912 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo bài tường thuật trên báo New York Times, điều kiện nào khiến William Wyler từ chối đạo diễn cho đến khi chắc chắn?  
**Đáp án sinh:** mình đã có một nhân vật chính xuất sắc  
**Kiểm:** một nhân vật chính xuất sắc (F1 0.8)  
**Cửa sổ (rút gọn):** Zimbalist đã chỉ cho Wyler vài storyboard sơ đẳng về cuộc đua xe chariot. Wyler, người từng là một trong 30 phụ tá đạo diễn ở phim Ben-Hur năm 1925, bắt đầu tỏ ra quan tâm tới phim này. Zimbalist bảo Wyler: "Hãy quên cảnh đua xe chariot. Đó chỉ là một trò thứ yếu". Zimbalist nói rằng thách thức thực sự là làm sao đem lại cho cuốn phim một sự "toàn …

**Bài:** Ben-Hur (phim 1959) (10,912 âm tiết), cửa sổ ở 83% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà xuất bản của cuốn sách 'Epics, Spectacles, and Blockbusters: A Hollywood History' là gì?  
**Đáp án sinh:** Wayne State University Press  
**Kiểm:** Wayne State University Press (F1 1.0)  
**Cửa sổ (rút gọn):** New York: Jove Books, 1987. Warning Shadows: Home Alone With Classic Cinema. Technicolor Movies: The History of Dye Transfer Printing. Hall, Sheldon and Neale, Stephen. Epics, Spectacles, and Blockbusters: A Hollywood History. Detroit, Mich.: Wayne State University Press, 2010. Fatal Flaws of the Most Correct Book on Earth. Maitland, Fla.: Xulon Pr…

**Bài:** Ben-Hur (phim 1959) (10,912 âm tiết), cửa sổ ở 56% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo tiểu thuyết, nhân vật nào đã giết Messala khoảng 5 năm sau cuộc đua xe chariot?  
**Đáp án sinh:** Iras  
**Kiểm:** Iras (F1 1.0)  
**Cửa sổ (rút gọn):** Trong tiểu thuyết, Messala bị thương nặng nhưng không đến nỗi táng mạng trong cuộc đua xe chariot. Sau đó anh ta lập mưu giết Judah Ben-Hur,nhưng kế hoạch của anh ta bị thất bại. Phần kết tiểu thuyết cho biết là Iras đã giết Messala khoảng 5 năm sau cuộc đua xe chariot. Trong phim, Messala bị tai nạn khi đua xe chariot do chính mưu toan của anh ta …

**Bài:** Mass Effect 3 (8,862 âm tiết), cửa sổ ở 75% bài  
**Trạng thái:** kept  
**Câu hỏi:** DLC Firepack của Mass Effect 3 được phát hành vào ngày nào?  
**Đáp án sinh:** 8 tháng 8 năm 2012  
**Kiểm:** Ngày 8 tháng 8 năm 2012 (F1 0.91)  
**Cửa sổ (rút gọn):** Shepard sẽ do đó du hành đến một phần mới của thiên hà . DLC cũng sẽ có những vũ khí khác nhau vốn chỉ có sẵn thông qua chơi mạng, nhưng giờ được đưa vào chơi đơn . Ngày 8 tháng 8 năm 2012, DLC Firepack được phát hành với giá 160 Microsoft point hoặc $2, làm cho nó là DLC thu phí đầu tiên của trò chơi. DLC bao gồm 7 vũ khí là súng bắn tỉa Indra và …

**Bài:** Mass Effect 3 (8,862 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chế độ co-op chơi mạng trong Mass Effect 3 được gọi là gì?  
**Đáp án sinh:** Galaxy at War  
**Kiểm:** Galaxy at War (F1 1.0)  
**Cửa sổ (rút gọn):** Kẻ thù sẽ không hành động cá nhân như đã làm trong các trò chơi trước đó, mà thay vào đó chiến đấu và hỗ trợ lẫn nhau trong nhóm. Kẻ thù trong trò chơi bao gồm người máy Cerberus cao 15-foot (4,6 m), lính xung kích và lính đột kích theo phong cách ninja, cũng như husk của hầu hết các chủng tộc và các tàu Reaper khác nhau với chiều dài từ 500 đến 2.…

**Bài:** Mass Effect 3 (8,862 âm tiết), cửa sổ ở 13% bài  
**Trạng thái:** kept  
**Câu hỏi:** Mass Effect 3 cung cấp một chế độ co-op chơi mạng có tên là gì?  
**Đáp án sinh:** Galaxy at War  
**Kiểm:** Galaxy at War (F1 1.0)  
**Cửa sổ (rút gọn):** Các mệnh lệnh bằng lời có thể được ban hành để di chuyển đồng đội và sử dụng khả năng của họ bằng việc sử dụng Kinect . Di chuyển và bắn, một "chuyển động tự sát" trong Mass Effect 2 giờ sẽ là một lựa chọn khả thi bởi một hệ thống cận chiến đã sửa đổi, bổ sung . Người chơi có thể thực hiện các cú đấm và tấn công uy lực, với giết bằng cận chiến ngay…

**Bài:** Mass Effect 3 (8,862 âm tiết), cửa sổ ở 53% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trang web nào của Bỉ đã báo cáo rằng BioWare cộng tác với DICE để phát triển vũ khí cho Mass Effect 3 vào ngày 20 tháng 4?  
**Đáp án sinh:** 4gamers.be  
**Kiểm:** 4gamers.be (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 20 tháng 4, trang web 4gamers.be của Bỉ báo cáo rằng BioWare đã cộng tác với nhà phát triển DICE của Battlefield để phát triển vũ khí cho trò chơi . Cùng ngày, Game Informer' công bố các ảnh chụp màn hình đầu tiên của Mass Effect 3 để giúp thúc đẩy ảnh bìa câu chuyện này 10 tháng 5 . Ngày 3 tháng 5 năm 2011, IGN đã công bố rằng Mass Effect 3 s…

**Bài:** Mass Effect 3 (8,862 âm tiết), cửa sổ ở 85% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chiến dịch internet nào được tổ chức để yêu cầu một kết thúc tốt hơn cho Mass Effect 3?  
**Đáp án sinh:** Retake Mass Effect  
**Kiểm:** Retake Mass Effect (F1 1.0)  
**Cửa sổ (rút gọn):** But it's also a spectacular, powerfully imagined and dramatically involving final act to one of gaming’s richest sci-fi sagas." Tom Francis của PC Gamer Mỹ đã đưa cho trò chơi số điểm 93/100 và kết thúc với câu nói "...kết thúc của loạt game là một túi hỗn hợp. Thỏa mãn ở một số điểm, vô nghĩa với một số điểm khác, và cuối cùng là quá đơn giản. Tuy…

**Bài:** Mass Effect 3 (8,862 âm tiết), cửa sổ ở 82% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Andrew Reiner của Game Informer, Mass Effect 3 được đánh giá bao nhiêu điểm?  
**Đáp án sinh:** 10 trên 10  
**Kiểm:** 10 trên 10 (F1 1.0)  
**Cửa sổ (rút gọn):** Thường được gọi một cách thông tục là "FemShep", cô được đặc trưng trong đoạn trailer chuyên dụng của riêng mình cho trò chơi và graced các trang bìa của Mass Effect 3 N7 Collector's Edition . Ngoài ra, các phiên bản tiêu chuẩn của trò chơi đặc trưng bao gồm slipcase đảo ngược, cho phép người mua hiển thị phiên bản nam hay nữ của Shepard ở mặt trướ…

**Bài:** Mass Effect 3 (8,862 âm tiết), cửa sổ ở 18% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trong chế độ chơi mạng, người chơi được phép mang theo tối đa bao nhiêu khẩu súng tại một thời điểm trong túi đồ?  
**Đáp án sinh:** hai khẩu súng  
**Kiểm:** hai khẩu súng (F1 1.0)  
**Cửa sổ (rút gọn):** Trận chiến diễn ra trên sự lựa chọn của hơn 15 bản đồ, với 4 độ khó là Bronze (Dễ), Silver (Bình thường), Gold (Khó) và Platinum (Rất khó); bản đồ Platinum ngẫu nhiên sẽ đtạo ra đơn vị tăng từ các chủng tộc ngẫu nhiên ngoài chủng tộc người chơi chống lại, ví dụ như là một ravager của Reaper chiến đấu bên cạnh lính Cerberus hoặc một Geth Prime hỗ tr…

**Bài:** Mass Effect 3 (8,862 âm tiết), cửa sổ ở 50% bài  
**Trạng thái:** kept  
**Câu hỏi:** BioWare cảm thấy họ đã không làm tốt điều gì trong Mass Effect 2?  
**Đáp án sinh:** định hướng người chơi mới  
**Kiểm:** định hướng người chơi mới (F1 1.0)  
**Cửa sổ (rút gọn):** Cốt truyện cũng được nhấn mạnh về sự thân thiện cho người chơi thiếu kinh nghiệm với thương hiệu vì BioWare cảm thấy họ "không làm một công việc thực sự tốt để định hướng người chơi mới" trong Mass Effect 2 . Để bắt đầu quá trình soạn thảo, Hudson và Walters thảo luận và tạo ra một tài liệu câu chuyện không dài hơn ba hoặc bốn trang có chứa tất cả …

**Bài:** Nhân vật của vũ trụ Mass Effect (8,553 âm tiết), cửa sổ ở 51% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Theo Aria T'loak, ba hội Blue Suns, Eclipse và Blood Pack chỉ kết hợp lại với nhau trong trường hợp nào?  
**Đáp án sinh:** trừ khi có chiến tranh xảy ra  
**Kiểm:** chiến tranh xảy ra (F1 0.73)  
**Cửa sổ (rút gọn):** Tác động của anh đến 3 hội mạnh tới mức họ phải thành lập một liên minh tạm thời để chống lại Archangel. Việc Blue Suns, Eclipse và Blood Pack kết hợp lại với nhau là chưa từng có; trừ khi có chiến tranh xảy ra, cả ba hội đều không bao giờ kết hợp lại với nhau (như Aria T'loak giải thích). Đến khi Shepard đến được nơi ở của Archangel thì anh ta bỏ …

**Bài:** Nhân vật của vũ trụ Mass Effect (8,553 âm tiết), cửa sổ ở 21% bài  
**Trạng thái:** kept  
**Câu hỏi:** Liara được lồng tiếng bởi ai?  
**Đáp án sinh:** Ali Hillis  
**Kiểm:** Ali Hillis (F1 1.0)  
**Cửa sổ (rút gọn):** Cuối cùng, mối quan hệ này đạt đến một điểm phá vỡ sau sự sụp đổ của Thessia, khi mà Liara trong khu của Javik, thất vọng với anh ta vì "không có câu trả lời". Shepard có thể khuếch tán tình hình hoặc cho phép Liara bỏ đi. Nếu tình hình được giải quyết, cả hai sẽ bắt đầu tôn trọng và đánh giá cao lẫn nhau. Liara được lồng tiếng bởi Ali Hillis, với …

**Bài:** Nhân vật của vũ trụ Mass Effect (8,553 âm tiết), cửa sổ ở 95% bài  
**Trạng thái:** kept  
**Câu hỏi:** Kai Leng chủ yếu sử dụng vũ khí gì để tấn công?  
**Đáp án sinh:** kiếm  
**Kiểm:** kiếm (F1 1.0)  
**Cửa sổ (rút gọn):** Các nhân vật ngoài nhóm= Các nhân vật phản diện Nhân vật đứng đầu của Ceberus, người xuất hiện và chi tài sản ra để tái tạo lại Shepard sau vụ tấn công ở đầu phần 2, cũng như giúp Shepard đánh bại chủng loài Collectors ở cuối phần 2. Mục đích của The Illusive Man ban đầu không rõ ràng nhưng dần dần được sáng tỏ ở phần 3. The Illusive Man muốn bảo v…

**Bài:** Nhân vật của vũ trụ Mass Effect (8,553 âm tiết), cửa sổ ở 58% bài  
**Trạng thái:** kept  
**Câu hỏi:** Garrus được lồng tiếng bởi ai?  
**Đáp án sinh:** Bramdon Keener  
**Kiểm:** Bramdon Keener (F1 1.0)  
**Cửa sổ (rút gọn):** Anh tìm đến Citadel cùng Shepard, Harkin (Dưới bí danh là Fade) là một trong những người làm cho Sidonis biến vào bóng tối. Sau khi bắt và thẩm vấn Harkin, anh ta đặt lịch hẹn cho Sidonis tới một quán nước và sau đó thì Garrus có quyền giết hắn ta. Shepard nói với Garrus là anh/cô sẽ ra nói chuyện với hắn một lúc để dụ cho hắn ta vào tầm ngắm của G…

**Bài:** Nhân vật của vũ trụ Mass Effect (8,553 âm tiết), cửa sổ ở 94% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhân vật đứng đầu của Cerberus trong Mass Effect là ai?  
**Đáp án sinh:** The Illusive Man  
**Kiểm:** The Illusive Man (F1 1.0)  
**Cửa sổ (rút gọn):** Do điều này trái với luật justicar của mình, Samara đã tìm giết Nihlus để trị tội. Bà truy đuổi anh suốt 2 tuần cho tới khi Nihlus dùng kế để đem luật của Samara chống lại chính bà, tạo ra một tình huống mà bà phải chọn hoặc là cứu một người vô tội, hoặc là bắt anh. Là người bảo vệ cho những người vô tội, Samara chọn cách thứ 1 và để Nihlus trốn th…

**Bài:** Nhân vật của vũ trụ Mass Effect (8,553 âm tiết), cửa sổ ở 35% bài  
**Trạng thái:** kept  
**Câu hỏi:** Kaidan Alenko được thăng cấp bậc gì trong những tháng sau các sự kiện của Mass Effect 2?  
**Đáp án sinh:** thiếu tá  
**Kiểm:** thiếu tá (F1 1.0)  
**Cửa sổ (rút gọn):** Collector tấn công thuộc địa và Kaidan bị cắn bởi một Collector Swarm, khiến anh bị tê liệt tạm thời. Shepard sớm biết rằng Kaidan được phái đến thuộc địa để cài đặt một mạng lưới các khẩu pháo phòng thủ để bảo vệ chống lại các cuộc tấn công của Collector trong tương lai. Sau khi đánh lui Collector và Harbinger, Alenko cuối cùng được giải cứu bởi S…

**Bài:** Nhân vật của vũ trụ Mass Effect (8,553 âm tiết), cửa sổ ở 95% bài  
**Trạng thái:** kept  
**Câu hỏi:** Kai Leng chủ yếu sử dụng vũ khí gì để tấn công?  
**Đáp án sinh:** kiếm  
**Kiểm:** kiếm (F1 1.0)  
**Cửa sổ (rút gọn):** Các nhân vật ngoài nhóm= Các nhân vật phản diện Nhân vật đứng đầu của Ceberus, người xuất hiện và chi tài sản ra để tái tạo lại Shepard sau vụ tấn công ở đầu phần 2, cũng như giúp Shepard đánh bại chủng loài Collectors ở cuối phần 2. Mục đích của The Illusive Man ban đầu không rõ ràng nhưng dần dần được sáng tỏ ở phần 3. The Illusive Man muốn bảo v…

**Bài:** Nhân vật của vũ trụ Mass Effect (8,553 âm tiết), cửa sổ ở 50% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người đứng sau việc gây ra rắc rối cho ba hội lính đánh thuê Blood Pack, Eclipse và Blue Suns tại Cụm Sao Terminus?  
**Đáp án sinh:** Archangel  
**Kiểm:** Archangel (F1 1.0)  
**Cửa sổ (rút gọn):** Anh đến đó với đội của mình gồm 12 thành viên khác. Archangel đã gây ra rất nhiều rắc rối cho ba hội lính đánh thuê thành công nhất và quyền lực nhất Cụm Sao Terminus là Blood Pack, Eclipse và Blue Suns. Tác động của anh đến 3 hội mạnh tới mức họ phải thành lập một liên minh tạm thời để chống lại Archangel. Việc Blue Suns, Eclipse và Blood Pack kết…

**Bài:** SpaceX (10,152 âm tiết), cửa sổ ở 67% bài  
**Trạng thái:** kept  
**Câu hỏi:** SpaceX đã mua cơ sở vật chất tại McGregor từ công ty nào?  
**Đáp án sinh:** Beal Aerospace  
**Kiểm:** Beal Aerospace (F1 1.0)  
**Cửa sổ (rút gọn):** SpaceX vận hành Cơ sở Thử nghiệm và Phát triển Tên lửa đầu tiên của mình ở McGregor, Texas. Tất cả các động cơ tên lửa SpaceX đều được thử nghiệm trên bệ thử tên lửa, và thử nghiệm bay VTVL ở độ cao thấp đối với phương tiện thử nghiệm. Falcon 9 Grasshopper v1.0 và F9R Dev1 trong giai đoạn 2013–2014 được thực hiện tại McGregor. Việc thử nghiệm các n…

**Bài:** SpaceX (10,152 âm tiết), cửa sổ ở 14% bài  
**Trạng thái:** kept  
**Câu hỏi:** Gwynne Shotwell được thăng chức chủ tịch công ty vào thời điểm nào?  
**Đáp án sinh:** vào thời điểm này  
**Kiểm:** vào thời điểm này (F1 1.0)  
**Cửa sổ (rút gọn):** Dự án Falcon 1 đã sớm ngừng hoạt động để SpaceX tập trung nguồn lực của công ty vào việc phát triển tên lửa có quỹ đạo lớn hơn, Falcon 9. Gwynne Shotwell cũng được thăng chức chủ tịch công ty vào thời điểm này, vì vai trò của cô trong việc đàm phán thành công hợp đồng CRS với NASA. 2010–2012: Falcon 9, Dragon, và những hợp đồng từ NASA SpaceX ban đ…

**Bài:** SpaceX (10,152 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Sứ mệnh Inspiration4 đã phóng Mô-đun phục hồi của Phi hành đoàn Dragon từ khu phức hợp phóng nào?  
**Đáp án sinh:** Khu phức hợp phóng 39A  
**Kiểm:** Khu phức hợp phóng 39A, Trung tâm Vũ trụ Florida Kennedy (F1 0.5)  
**Cửa sổ (rút gọn):** Vào tháng 2 năm 2019, SpaceX đã bảo đảm một hợp đồng trị giá 297 triệu đô la Mỹ từ Không quân Hoa Kỳ để khởi động ba nhiệm vụ an ninh quốc gia khác, tất cả dự kiến ​​ra mắt không sớm hơn năm 2021. Vào ngày 7 tháng 8 năm 2020, Lực lượng Không gian Hoa Kỳ đã trao các hợp đồng phóng An ninh Quốc gia (NSSL) cho 5 – 7 năm tiếp theo. SpaceX đã giành được…

**Bài:** SpaceX (10,152 âm tiết), cửa sổ ở 58% bài  
**Trạng thái:** answer_not_verbatim  
**Câu hỏi:** SpaceX đã xây dựng đường chạy thử Hyperloop dài bao nhiêu gần trụ sở chính của công ty?  
**Đáp án sinh:** 1,6 km (0,99 mi)  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Ngoài ra, các vệ tinh được thiết kế để tự động tránh va chạm dựa trên dữ liệu theo dõi được liên kết lên. Vào tháng 6 năm 2015, SpaceX thông báo rằng họ sẽ tài trợ cho một cuộc thi Hyperloop và sẽ xây dựng một đường chạy thử dài 1,6 km (0,99 mi) gần trụ sở chính của SpaceX cho các cuộc thi. Công ty đã tổ chức các cuộc thi thường niên kể từ năm 2017…

**Bài:** SpaceX (10,152 âm tiết), cửa sổ ở 48% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** SpaceX đã mua hai giàn khoan dầu nước sâu để thiết kế lại nhằm hỗ trợ cho phi vụ phóng của hệ thống nào?  
**Đáp án sinh:** Starship  
**Kiểm:** tàu Starship (F1 0.67)  
**Cửa sổ (rút gọn):** Vào ngày 27 tháng 3 năm 2020, SpaceX đã tiết lộ tàu vũ trụ tiếp tế Dragon XL chở hàng hóa có áp suất và không áp suất, các thí nghiệm và các nguồn cung cấp khác tới trạm vũ trụ Lunar Gateway theo kế hoạch của NASA theo hợp đồng Gateway Logistics Services (GLS). NASA có kế hoạch sử dụng Dragon XL để vận chuyển vật liệu thu thập mẫu, bộ đồ vũ trụ và …

**Bài:** SpaceX (10,152 âm tiết), cửa sổ ở 86% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Không quân Hoa Kỳ đã trao cho SpaceX hai nhiệm vụ cấp EELV nào vào tháng 12 năm 2012?  
**Đáp án sinh:** Đài quan sát Khí hậu Không gian Sâu (DSCOVR) và Chương trình Thử nghiệm Không gian 2 (STP-2)  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Hợp đồng bao gồm các dịch vụ phóng được đặt hàng vào tháng 6 năm 2010, cho các lần phóng đến tháng 12 năm 2012. Musk tuyên bố trong cùng một thông báo năm 2008 rằng SpaceX đã bán 14 hợp đồng cho các chuyến bay trên các phương tiện Falcon khác nhau. Vào tháng 12 năm 2012, SpaceX đã công bố hai hợp đồng phóng đầu tiên với Bộ Quốc phòng Hoa Kỳ (DoD). …

**Bài:** SpaceX (10,152 âm tiết), cửa sổ ở 36% bài  
**Trạng thái:** kept  
**Câu hỏi:** Falcon 1 là tên lửa sử dụng nhiên liệu lỏng do tư nhân tài trợ đầu tiên đạt được thành tựu gì?  
**Đáp án sinh:** bay lên quỹ đạo  
**Kiểm:** bay lên quỹ đạo (F1 1.0)  
**Cửa sổ (rút gọn):** Nó đã được phóng lên năm lần từ năm 2006 đến năm 2009, trong đó có 2 lần thành công. Được cho là hoạt động thử nghiệm ban đầu để phát triển Falcon 9, Falcon 1 là tên lửa sử dụng nhiên liệu lỏng, do tư nhân tài trợ đầu tiên bay lên quỹ đạo. Falcon 9 là phương tiện phóng có sức nâng hạng trung có khả năng phóng đến 22.800 kg (50.265 lb) lên quỹ đạo, …

**Bài:** SpaceX (10,152 âm tiết), cửa sổ ở 44% bài  
**Trạng thái:** answer_not_verbatim  
**Câu hỏi:** Mỗi động cơ SuperDraco tạo ra lực đẩy bao nhiêu?  
**Đáp án sinh:** 73 kN (16.000 lbf)  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** SuperDraco là động cơ tên lửa đẩy chất lỏng cường độ cao, giống như Draco, sử dụng chất đẩy monomethyl hydrazine và nitơ tetroxide. Tám động cơ SuperDraco cung cấp khả năng thoát hiểm khi phóng cho phi thuyền Dragon 2 do phi hành đoàn trong kịch bản hủy bỏ phóng. Mỗi động cơ SuperDraco tạo ra lực đẩy 73 kN (16.000 lbf). Các khái niệm ban đầu cho tà…

**Bài:** Chiến dịch tấn công Uman–Botoşani (10,564 âm tiết), cửa sổ ở 28% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Các đơn vị trực thuộc Tư lệnh Tập đoàn quân gồm những đơn vị nào?  
**Đáp án sinh:** Lữ đoàn pháo tự hành cận vệ 6, Trung đoàn bộ binh mô tô 156, Tiểu đoàn công binh 181 và Phi đội trinh sát liên lạc 387  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Các đơn vị trực thuộc Tư lệnh Tập đoàn quân gồm Lữ đoàn pháo tự hành cận vệ 6, Trung đoàn bộ binh mô tô 156, Tiểu đoàn công binh 181 và Phi đội trinh sát liên lạc 387. Tập đoàn quân không quân 5 của trung tướng không quân S. Biên chế gồm 1 sư đoàn tiêm kích, 2 sư đoàn cường kích, 1 sư đoàn ném bom ban ngày, 1 sư đoàn ném bom hỗn hợp, 1 trung đoàn n…

**Bài:** Chiến dịch tấn công Uman–Botoşani (10,564 âm tiết), cửa sổ ở 29% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Biên chế của đơn vị được mô tả trong đoạn trích gồm những thành phần nào?  
**Đáp án sinh:** 1 sư đoàn tiêm kích, 2 sư đoàn cường kích, 1 sư đoàn ném bom ban ngày, 1 sư đoàn ném bom hỗn hợp, 1 trung đoàn ném bom ban đêm, 1 sư đoàn vận tải, 1 trung đoàn đổ bộ đường không, 1 trung đoàn trinh sát, cứu hộ, 1 trung đoàn công binh đường băng, 2 trung đoàn phòng không  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Biên chế gồm 1 sư đoàn tiêm kích, 2 sư đoàn cường kích, 1 sư đoàn ném bom ban ngày, 1 sư đoàn ném bom hỗn hợp, 1 trung đoàn ném bom ban đêm, 1 sư đoàn vận tải, 1 trung đoàn đổ bộ đường không, 1 trung đoàn trinh sát, cứu hộ, 1 trung đoàn công binh đường băng, 2 trung đoàn phòng không. Các đơn vị trực thuộc Phương diện quân: Quân đoàn kỵ binh cận vệ …

**Bài:** Chiến dịch tấn công Uman–Botoşani (10,564 âm tiết), cửa sổ ở 28% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân không quân 5 thuộc quyền chỉ huy của ai?  
**Đáp án sinh:** trung tướng không quân S.  
**Kiểm:** trung tướng không quân S (F1 0.8)  
**Cửa sổ (rút gọn):** Tập đoàn quân không quân 5 của trung tướng không quân S. Biên chế gồm 1 sư đoàn tiêm kích, 2 sư đoàn cường kích, 1 sư đoàn ném bom ban ngày, 1 sư đoàn ném bom hỗn hợp, 1 trung đoàn ném bom ban đêm, 1 sư đoàn vận tải, 1 trung đoàn đổ bộ đường không, 1 trung đoàn trinh sát, cứu hộ, 1 trung đoàn công binh đường băng, 2 trung đoàn phòng không. Các đơn …

**Bài:** Chiến dịch tấn công Uman–Botoşani (10,564 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Tập đoàn quân 8 (Đức) và Tập đoàn quân 4 (Romania) đã huy động những đơn vị xe tăng và cơ giới nào để tổ chức phản công từ ngày 20 tháng 5 đến ngày 6 tháng 6 năm 1944?  
**Đáp án sinh:** các sư đoàn xe tăng 14, 23, 24, Sư đoàn cơ giới SS "Đại Đức", Sư đoàn SS "Đầu lâu" và Sư đoàn xe tăng "Đại Romania"  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** 9 tập đoàn quân của Phương diện quân Ukraina 2 phải dừng lại và tổ chức phòng ngự dọc theo tuyến sông Seret ở phía Tây và Dniestr ở phía Đông, trấn giữ phía Bắc "cửa ngõ Foksal" trên thung lũng sông Prut hướng tới Iaşi. Bộ Tổng tư lệnh Quân đội Liên Xô dự kiến tiếp tục tấn công vào cuối tháng 5 nhưng đã phải hoãn lại. Lợi dụng tình trạng hưu chiến …

**Bài:** Chiến dịch tấn công Uman–Botoşani (10,564 âm tiết), cửa sổ ở 94% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn bộ binh 4 được cải tổ và tái trang bị thành đơn vị nào vào ngày 10 tháng 10 năm 1944?  
**Đáp án sinh:** Quân đoàn xe tăng 4  
**Kiểm:** Quân đoàn xe tăng 4 (F1 1.0)  
**Cửa sổ (rút gọn):** Tháng 4 năm 1944, Quân đoàn bộ binh 4 bị thiệt hại nặng phải giải thể. Đến ngày 10 tháng 10 bộ khung của nó được cải tổ và tái trang bị thành Quân đoàn xe tăng 4 bố trí ở Budapest. Tình huống chia cắt đã buộc Bộ Tổng tư lệnh Lục quân Đức phải rút bớt quân ở Balkan để ném ra tuyến biên giới Romania đã tạo điều kiện cho Quân đội giải phóng Nam Tư của…

**Bài:** Chiến dịch tấn công Uman–Botoşani (10,564 âm tiết), cửa sổ ở 40% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân 53 đã huy động bao nhiêu sư đoàn bộ binh vào thê đội 1 để tấn công bên cánh trái của Tập đoàn quân cận vệ 4?  
**Đáp án sinh:** 5 sư đoàn bộ binh  
**Kiểm:** 5 sư đoàn bộ binh (F1 1.0)  
**Cửa sổ (rút gọn):** Tập đoàn quân 53 huy động 5 sư đoàn bộ binh vào thê đội 1, tấn công bên cánh trái của Tập đoàn quân cận vệ 4, trong ngày N+1 phải phá vỡ tuyến phòng thủ của quân Đức dọc theo sông Bolsaya Vys tại Malyi Viska (Mala Viska) theo hướng chung đến Kolodistoye-KalninoBoloto (Kalnybolota), yểm hộ cánh trái của cụm xung kích. Chiều sâu nhiệm vụ của các Tập …

**Bài:** Chiến dịch tấn công Uman–Botoşani (10,564 âm tiết), cửa sổ ở 73% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn cơ giới cận vệ 5 được triển khai nhằm vào địa điểm nào?  
**Đáp án sinh:** Khristinovka  
**Kiểm:** Khristinovka (F1 1.0)  
**Cửa sổ (rút gọn):** Quân đoàn cơ giới cận vệ 5 được triển khai nhằm vào Khristinovka. Ngày 7 tháng 3, các tập đoàn quân cận vệ 5 và 7 cũng phát động cuộc tấn công hợp điểm về NovoUkrainka. Tập đoàn quân cận vệ 7 chỉ để lại Lữ đoàn bộ binh 3 và Trung đoàn cơ giới 8 phối hợp với cánh phải của Tập đoàn quân 57 giải quyết cứ điểm tiền tiêu Novgorodka của quân Đức. Chủ lực…

**Bài:** Chiến dịch tấn công Uman–Botoşani (10,564 âm tiết), cửa sổ ở 10% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tư lệnh của Phương diện quân Ukraina 2?  
**Đáp án sinh:** Nguyên soái I. Koniev  
**Kiểm:** Nguyên soái I. Koniev (F1 1.0)  
**Cửa sổ (rút gọn):** Tình hình thời tiết không khả quan và việc mở nhiều trận đánh vượt sông có thể ảnh hưởng tiêu cực đến khả năng cơ động chiến dịch của xe tăng, cơ giới và pháo binh. Binh lực và kế hoạch Phương diện quân Ukraina 2 do Nguyên soái I. Koniev làm tư lệnh, đang chiếm giữ tuyến Tynovka - Rizino - Erky - Tovmach - Lipyanka - Kanizh - Shestakovka - Kalinovk…

**Bài:** Chính quyền Uông Tinh Vệ (10,520 âm tiết), cửa sổ ở 13% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thủ phủ của tỉnh Chiết Giang là thành phố nào?  
**Đáp án sinh:** Hàng Châu  
**Kiểm:** Hàng Châu (F1 1.0)  
**Cửa sổ (rút gọn):** An Huy: 51.888 sq mi (134.390 km 2 ); thủ phủ: Hợp phì Chiết Giang: 39.780 sq mi (103.000 km 2 ); thủ phủ: Hàng Châu Theo các nguồn khác, tổng phần mở rộng lãnh thổ trong thời kỳ 1940 là 1.264.000 km 2 . Năm 1940, một thỏa thuận được ký kết giữa nhà nước bù nhìn Nội Mông Cổ Mạnh Giang và chế độ Nam Kinh, hợp nhất cái trước vào cái sau như một bộ ph…

**Bài:** Chính quyền Uông Tinh Vệ (10,520 âm tiết), cửa sổ ở 19% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Vương Tinh Vệ đã chính thức đến Tokyo vào tháng 6 năm 1941 để gặp ai?  
**Đáp án sinh:** thủ tướng Fumimaro Konoe  
**Kiểm:** thủ tướng Fumimaro Konoe và nội các của ông (F1 0.62)  
**Cửa sổ (rút gọn):** Nỗ lực mở rộng sự công nhận của người Nhật Trong khi Uông đã thành công trong việc bảo đảm từ Nhật Bản một "hiệp ước cơ bản" công nhận sự thành lập đảng mới của ông vào tháng 11 năm 1940, thì tài liệu được đưa ra đã cấp cho Chính phủ Quốc dân Đảng được tổ chức lại hầu như không có bất kỳ quyền hạn nào. Hiệp ước ban đầu này đã loại trừ mọi khả năng …

**Bài:** Chính quyền Uông Tinh Vệ (10,520 âm tiết), cửa sổ ở 22% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào năm 1943, nhà lãnh đạo Nhật Bản nào đã nhận ra rằng làn sóng chiến tranh đang chống lại họ và tìm kiếm cách thức mới để củng cố lực lượng?  
**Đáp án sinh:** Hideki Tojo  
**Kiểm:** Hideki Tojo (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, đến năm 1943, các nhà lãnh đạo Nhật Bản bao gồm Hideki Tojo, nhận ra rằng làn sóng chiến tranh đang chống lại họ, đã tìm kiếm những cách thức mới để củng cố các lực lượng mỏng manh của Nhật Bản. Cuối cùng, Tokyo cũng thấy cần phải công nhận đầy đủ chính phủ của Vương Tinh Vệ là một đồng minh đầy đủ và Hiệp ước Liên minh thay thế đã được …

**Bài:** Chính quyền Uông Tinh Vệ (10,520 âm tiết), cửa sổ ở 6% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào tháng 4 năm 1938, đại hội toàn quốc của Quốc dân Đảng đã chỉ định Uông Tinh Vệ giữ chức vụ gì?  
**Đáp án sinh:** phó chủ tịch đảng  
**Kiểm:** phó chủ tịch đảng (F1 1.0)  
**Cửa sổ (rút gọn):** Điều này giúp ông kiểm soát được mối quan hệ Trung - Nhật đang xấu đi. Trong khi Tưởng Giới Thạch tập trung sự chú ý chính của mình chống lại Đảng Cộng sản Trung Quốc Uông Tinh Vệ cần mẫn nỗ lực để gìn giữ hòa bình giữa Trung Quốc và Nhật Bản, liên tục nhấn mạnh sự cần thiết của một thời kỳ hòa bình kéo dài để Trung Quốc nâng mình về kinh tế và quâ…

**Bài:** Chính quyền Uông Tinh Vệ (10,520 âm tiết), cửa sổ ở 12% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thủ phủ của khu vực Chiết Giang trong chính quyền bù nhìn do Nhật Bản kiểm soát là thành phố nào?  
**Đáp án sinh:** Hàng Châu  
**Kiểm:** Hàng Châu (F1 1.0)  
**Cửa sổ (rút gọn):** Các vùng lãnh thổ do Nhật Bản kiểm soát khác có các cơ quan hành chính quân sự trực tiếp báo cáo với bộ chỉ huy quân sự Nhật Bản ở Nam Kinh, ngoại trừ Quảng Đông và Quảng Tây có trụ sở chính tại Quảng Đông. Các khu vực chiếm đóng quân sự ở miền trung và miền nam cuối cùng được liên kết với nhau sau Chiến dịch Ichi-Go vào năm 1944, mặc dù các đơn vị…

**Bài:** Chính quyền Uông Tinh Vệ (10,520 âm tiết), cửa sổ ở 81% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Chen Jicheng giữ chức vụ gì tại Mãn châu trong giai đoạn 1943–1945?  
**Đáp án sinh:** đại sứ tại Mãn châu  
**Kiểm:** đại sứ (F1 0.57)  
**Cửa sổ (rút gọn):** Chen Jicheng : đại sứ tại Mãn châu (1943–1945) Wang Xiang (chính trị gia Trung Hoa Dân Quốc) : Giám đốc Cơ quan Giáo dục Sơn Tây , Tỉnh trưởng kiêm Chỉ huy An ninh Sơn Tây He Peirong : Thống đốc tỉnh Hồ Bắc (1938–1942), Chỉ huy An ninh ở Hồ Bắc Ni Daolang : Tỉnh trưởng tỉnh An Huy Wang Ruikai : Thống đốc tỉnh Chiết Giang (1938–1941) Zhu Qinglai : B…

**Bài:** Chính quyền Uông Tinh Vệ (10,520 âm tiết), cửa sổ ở 59% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cơ quan bí mật nào được thành lập với sự hỗ trợ của các 'cố vấn' Quân đội Nhật Bản?  
**Đáp án sinh:** Tewu  
**Kiểm:** Tewu (F1 1.0)  
**Cửa sổ (rút gọn):** Ở Thượng Hải năm 1941, con số này đã tăng lên gấp mười một lần. Cuộc sống hàng ngày thường khó khăn ở Cộng hòa Trung Hoa Dân Quốc do Chính phủ Quốc dân Đảng kiểm soát, và ngày càng phát triển do chiến tranh chống lại Nhật Bản (khoảng năm 1943). Cư dân địa phương tìm đến chợ đen để có được những vật phẩm cần thiết hoặc gây ảnh hưởng đến cơ sở cầm qu…

**Bài:** Chính quyền Uông Tinh Vệ (10,520 âm tiết), cửa sổ ở 79% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai giữ chức Thị trưởng thành phố đặc biệt Thiên Tân trong giai đoạn 1939–1943?  
**Đáp án sinh:** Wen Shizhen  
**Kiểm:** Wen Shizhen (F1 1.0)  
**Cửa sổ (rút gọn):** Zhang Renli : Thị trưởng thành phố đặc biệt Thiên Tân (1943) Yan Jiachi : Thứ trưởng Bộ Tài chính, Giám đốc Kiểm soát của Nhân dân tệ Xu Xiuzhi : Thị trưởng thành phố đặc biệt Bắc Kinh (1945) Lian Yu : đại sứ tại Mãn châu (1940–1943), đại sứ tại Nhật Bản (1945) Zhu Lühe : Phó tổng tư pháp, Chủ tịch Ủy ban hành động kỷ luật đối với công chức trung ư…

**Bài:** Chiến dịch hợp vây Korsun–Shevchenkovsky (12,916 âm tiết), cửa sổ ở 30% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Lý do mà I. Konev đưa ra để đề nghị với G. Zhukov cho Phương diện quân Ukraina 2 tấn công sớm hơn một ngày là gì?  
**Đáp án sinh:** không cho quân Đức có thêm dù chỉ một ngày để nghỉ ngơi  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Sư đoàn xe tăng 17; Sư đoàn xe tăng SS "Adolf Hitler"; Các sư đoàn bộ binh 5, 355, 367, 381. Quân đội Liên Xô tấn công Chỉ thị của Đại bản doanh Liên Xô ngày 12 tháng 1 quy định thời điểm tấn công vào ngày 25 tháng 1. Konev đã đề nghị với G. Zhukov cho Phương diện quân Ukraina 2 được tấn công sớm hơn một ngày, lấy lý do là "không cho quân Đức có th…

**Bài:** Chiến dịch hợp vây Korsun–Shevchenkovsky (12,916 âm tiết), cửa sổ ở 57% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tướng Stemmermann đã bác bỏ tối hậu thư vì tin tưởng vào lời hứa của ai?  
**Đáp án sinh:** Hitler và Bộ chỉ huy cụm Tập đoàn quân Nam (Đức)  
**Kiểm:** Hitler và Bộ chỉ huy cụm Tập đoàn quân Nam (Đức) (F1 1.0)  
**Cửa sổ (rút gọn):** Các điều kiện đầu hàng này tương tự như những gì mà Quân đội Liên Xô đặt ra cho thống chế Paulus tại Stalingrad một năm trước đó. Tuy nhiên, tin tưởng vào lời hứa của Hitler và Bộ chỉ huy cụm Tập đoàn quân Nam (Đức), tướng Stemmermann đã bác bỏ tối hậu thư này. Ngày 6 tháng 2, Tập đoàn quân xe tăng 1 (Đức) mới tập kết đủ các sư đoàn xe tăng tại khu…

**Bài:** Chiến dịch hợp vây Korsun–Shevchenkovsky (12,916 âm tiết), cửa sổ ở 88% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Tướng Wilhelm Stemmermann đã thiệt mạng trong chiến dịch Korsun-Shevchenkovsky do nguyên nhân nào?  
**Đáp án sinh:** pháo chống tăng Liên Xô bắn trúng xe của ông ta trên đường tháo chạy khỏi vòng vây  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Cả hai tập đoàn quân xe tăng 1 và 4, những lực lượng đột kích và phòng thủ tích cực của Cụm tập đoàn quân này đều bị dồn về cánh Bắc sau những thiệt hại nặng. Tại cánh quân này, khoảng cách giữa Tập đoàn quân xe tăng 4 và Tập đoàn quân xe tăng 1 cũng bị giãn rộng hơn sau cuộc vận động chiến dồn quân sang phía Đông trong 10 ngày đầu tháng 2 năm 1944…

**Bài:** Chiến dịch hợp vây Korsun–Shevchenkovsky (12,916 âm tiết), cửa sổ ở 25% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cụm tác chiến Quân đoàn xe tăng 47 của tướng Nikolaus von Vormann có tổng quân số bao nhiêu người?  
**Đáp án sinh:** 50.000 người  
**Kiểm:** 50.000 người (F1 1.0)  
**Cửa sổ (rút gọn):** Cụm tác chiến Quân đoàn xe tăng 47 của tướng Nikolaus von Vormann, gồm các sư đoàn xe tăng 3, 11, 14; các sư đoàn bộ binh 168, 255, 320, 332; Trung đoàn pháo tự hành 265. Tổng quân số 50.000 người, được trang bị 300 pháo và súng cối, 158 xe tăng, 25 pháo tự hành, 10 pháo chống tăng. Đến ngày 28 tháng 1, Cụm quân Đức bị bao vây tại khu vực Korsun - …

**Bài:** Chiến dịch hợp vây Korsun–Shevchenkovsky (12,916 âm tiết), cửa sổ ở 92% bài  
**Trạng thái:** kept  
**Câu hỏi:** Romistrov được phong danh hiệu Anh hùng Liên Xô vào năm nào?  
**Đáp án sinh:** 1965  
**Kiểm:** 1965 (F1 1.0)  
**Cửa sổ (rút gọn):** Romistrov, tư lệnh Tập đoàn quân xe tăng cận vệ 5, đơn vị đóng vai trò chủ công của chiến dịch được thăng quân hàm Đại tướng xe tăng và được tặng thưởng Huân chương Suvorov hạng nhất. Sau chiến tranh, ông trở thành Tiến sĩ khoa học quân sự, được phong danh hiệu Anh hùng Liên Xô năm 1965 và từ trần tại Moskva năm 1982. Корсунь-Шевченковская наступат…

**Bài:** Chiến dịch hợp vây Korsun–Shevchenkovsky (12,916 âm tiết), cửa sổ ở 23% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân xe tăng 1 của tướng Hans-Valentin Hube đóng tại khu vực nào?  
**Đáp án sinh:** Vòng cung Dniepr  
**Kiểm:** Vòng cung Dniepr (F1 1.0)  
**Cửa sổ (rút gọn):** Quân đội Đức Quốc xã đóng trên khu vực bị tấn công gồm có: Tại khu vực "Vòng cung Dniepr" Tập đoàn quân xe tăng 1 (cánh phải) của tướng Hans-Valentin Hube, gồm có: Cụm tác chiến Quân đoàn 42 (1/3) của trung tướng Theo-Helmut Lieb, Phó tư lệnh quân đoàn gồm Cụm tác chiến độc lập B; các sư đoàn bộ binh 57, 82, 88; Trung đoàn pháo tự hành 202. Tổng qu…

**Bài:** Chiến dịch hợp vây Korsun–Shevchenkovsky (12,916 âm tiết), cửa sổ ở 97% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cuốn sách về việc bao vây và phá vây của một nhóm cựu sĩ quan Đức Quốc xã được biên soạn vào năm nào?  
**Đáp án sinh:** 1952  
**Kiểm:** 1952 (F1 1.0)  
**Cửa sổ (rút gọn):** The Encirclement and Breakout of a German Army in the East, 1944. Drexel Hill (Philadelphia), Pennsylvania: Casemate Publishers. Diễn đàn của một số thân nhân cựu binh Đức Quốc xã thăm lại nơi từng là chiến trường Korsun–Shevchenkovsky Ảnh vệ tinh (ngày nay) của khu vực đã từng diễn ra Chiến dịch hợp vây Korsun–Shevchenkovsky Ảnh vệ tinh (ngày nay)…

**Bài:** Chiến dịch hợp vây Korsun–Shevchenkovsky (12,916 âm tiết), cửa sổ ở 74% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cây cầu tại bến vượt do lính Sư đoàn xe tăng 5 SS của tướng Herbert Otto Gille xây dựng đã bị lực lượng nào bắn gãy?  
**Đáp án sinh:** pháo binh Liên Xô  
**Kiểm:** pháo binh Liên Xô (F1 1.0)  
**Cửa sổ (rút gọn):** Tại bến vượt, sau khi vài chiếc xe tăng Đức sang được bờ bên kia, cây cầu do lính Sư đoàn xe tăng 5 SS của tướng Herbert Otto Gille vừa xây dựng xong đã bị pháo binh Liên Xô bắn gãy. Tướng Theo-Helmut Lieb và trung tá Franz Bäke phải ngồi lên ngựa và lội qua sông. Nhiều lính Đức chết cóng và chết đuối khi cố bơi qua qua con sông mùa đông lạnh giá. …

**Bài:** Cat Stevens (12,759 âm tiết), cửa sổ ở 74% bài  
**Trạng thái:** kept  
**Câu hỏi:** Buổi biểu diễn trực tiếp đầu tiên của Yusuf tại London sau 28 năm được phát sóng vào tháng 4 năm 2007 diễn ra tại đâu?  
**Đáp án sinh:** Hội trường Porchester  
**Kiểm:** Hội trường Porchester (F1 1.0)  
**Cửa sổ (rút gọn):** Tháng 4 năm 2007, BBC1 phát sóng một buổi biểu diễn tại Hội trường Porchester do Yusuf thực hiện trong một phần của BBC Sessions, đây là buổi diễn trực tiếp đầu tiên của ông tại London sau 28 năm (trước đó là trong buổi hòa nhạc UNICEF "Năm của trẻ em" năm 1979). Ông chơi một số bài hát mới cùng với một số bài cũ như "Father and Son", "The Wind", "…

**Bài:** Cat Stevens (12,759 âm tiết), cửa sổ ở 53% bài  
**Trạng thái:** kept  
**Câu hỏi:** Bài hát nào mà Yusuf đã viết về vụ bị từ chối nhập cảnh vào Mỹ năm 2004?  
**Đáp án sinh:** Boots and Sand  
**Kiểm:** Boots and Sand (F1 1.0)  
**Cửa sổ (rút gọn):** Ông Powell đã trả lời rằng danh sách theo dõi đã được xem lại, và nói thêm, "Tôi nghĩ rằng chúng tôi có nghĩa vụ xem xét các vấn đề này để xem liệu chúng tôi có đúng hay không". Yusuf tin rằng việc ông bị đưa vào "danh sách theo dõi" có thể chỉ đơn giản là một lỗi nhỏ: do nhầm ông với một người đàn ông cùng tên, nhưng cách viết khác nhau. Ngày 01 t…

**Bài:** Cat Stevens (12,759 âm tiết), cửa sổ ở 73% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người chơi guitar và hát nền cùng Yusuf trong buổi biểu diễn tại thành phố New York vào tháng 12 năm 2006?  
**Đáp án sinh:** Alun Davies  
**Kiểm:** Alun Davies (F1 1.0)  
**Cửa sổ (rút gọn):** Bài này cũng thường được John Frusciante của nhóm Red Hot Chili Peppers chơi lại trong các buổi biểu diễn. Tháng 12 năm 2006, Yusuf là một trong những nghệ sĩ biểu diễn tại buổi hòa nhạc giải Nobel Hòa bình ở Oslo, Na Uy, để vinh danh những người đọat giải, Muhammad Yunus và Grameen Bank. Ông đã biểu diễn các bài "Midday (Avoid City After Dark)", "…

**Bài:** Cat Stevens (12,759 âm tiết), cửa sổ ở 34% bài  
**Trạng thái:** kept  
**Câu hỏi:** Album tổng hợp thành công nhất của Cat Stevens là album nào?  
**Đáp án sinh:** Greatest Hits năm 1975  
**Kiểm:** Greatest Hits năm 1975 (F1 1.0)  
**Cửa sổ (rút gọn):** Đặc biệt "Was Dog a Doughnut" là một bài kết hợp techno-pop thời kỳ đầu với tiền thân của thể loại âm nhạc điện năm 1980, cũng sử dụng khá sớm music sequencer. Izitso có bài hit lọt bảng xếp hạng cuối cùng của ông, "(Remember the Days of) Old Schoolyard", một bài hát synthpop thời kỳ đầu  mà sử dụng bộ tổng hợp đa âm; đây là bản song ca với đồng ng…

**Bài:** Cat Stevens (12,759 âm tiết), cửa sổ ở 57% bài  
**Trạng thái:** kept  
**Câu hỏi:** Yusuf đã viết về trải nghiệm liên quan đến thiệt hại khó sửa chữa trong một bài báo có tiêu đề gì?  
**Đáp án sinh:** A Cat in a Wild World  
**Kiểm:** A Cat in a Wild World (F1 1.0)  
**Cửa sổ (rút gọn):** Và những thiệt hại thường là khó sửa chữa ", và nói thêm rằng ông dự định tặng số tiền ông nhận từ tòa án cho trẻ mồ côi là nạn nhân của thảm họa sóng thần ở Ấn Độ Dương. Yusuf đã viết về trải nghiệm này trong một bài báo có tiêu đề "A Cat in a Wild World". Tin đồn thất thiệt liên quan đến việc phụ nữ không che mặt Ngày 18 tháng 7 năm 2008, Yusuf đ…

**Bài:** Cat Stevens (12,759 âm tiết), cửa sổ ở 62% bài  
**Trạng thái:** kept  
**Câu hỏi:** Yusuf giải thích rằng ông đã dừng biểu diễn bằng tiếng Anh là do sự hiểu lầm của ông về điều gì?  
**Đáp án sinh:** đức tin Hồi giáo  
**Kiểm:** đức tin Hồi giáo (F1 1.0)  
**Cửa sổ (rút gọn):** Nhân dịp phát hành lại album Cat Stevens thứ 2000 của mình, ông đã giải thích rằng ông đã dừng biểu diễn bằng tiếng Anh là do sự hiểu lầm của ông về đức tin Hồi giáo. "Vấn đề của âm nhạc Hồi giáo không phải cộc lốc và khô khan như tôi đã bị dẫn dắt để tin như vậy... Tôi đã tin vào dị giáo, có lẽ đó là sai lầm của tôi." Yusuf đã cho rằng quyết định …

**Bài:** Cat Stevens (12,759 âm tiết), cửa sổ ở 83% bài  
**Trạng thái:** kept  
**Câu hỏi:** Yusuf đã mô tả album An Other Cup là như thế nào?  
**Đáp án sinh:** sản xuất vượt mức  
**Kiểm:** sản xuất vượt mức (F1 1.0)  
**Cửa sổ (rút gọn):** bằng bất cứ điều gì bạn muốn đổ vào nó. Đối với những người đang muốn tìm Cat Stevens, họ có thể sẽ tìm thấy anh ta trong đĩa này. Nếu bạn muốn tìm [Yusuf] Islam, hãy vào sâu hơn, bạn sẽ tìm thấy anh ta ". Yusuf đã mô tả album này là "sản xuất vượt mức" và An Other Cup là một trở ngại cần thiết mà ông phải vượt qua nếu trước để ông có thể phát hành…

**Bài:** Cat Stevens (12,759 âm tiết), cửa sổ ở 81% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo lời giải thích của Yusuf Islam, album An Other Cup đóng vai trò là cầu nối giữa hai khu vực nào?  
**Đáp án sinh:** Đông và Tây  
**Kiểm:** Đông và Tây (F1 1.0)  
**Cửa sổ (rút gọn):** Đối với nhiều người, nó nhắc họ về một cái gì đó họ muốn lưu giữ. Cái tên đó là một phần lịch sử của tôi và rất nhiều điều tôi mơ ước khi còn là Cat Stevens nay đã trở thành sự thật với Yusuf Islam ". Tờ báo định kỳ Das Magazin Thụy Sĩ đã hỏi Yusuf lý do tại sao tựa của album là An Other Cup, chứ không phải là "Another Cup". Câu trả lời của ông là …

**Bài:** Bắc phạt (1926–1928) (10,114 âm tiết), cửa sổ ở 57% bài  
**Trạng thái:** kept  
**Câu hỏi:** Biến cố xảy ra vào ngày 12 và 14/4 tại Thượng Hải, nơi hàng trăm người cộng sản bị bắt và giết theo lệnh của Tưởng Giới Thạch, được gọi là gì?  
**Đáp án sinh:** vụ thảm sát Thượng Hải  
**Kiểm:** vụ thảm sát Thượng Hải (F1 1.0)  
**Cửa sổ (rút gọn):** Trong ngày 12 và 14/4, hàng trăm người cộng sản ở Thượng Hải đã bị bắt và giết theo lệnh của Tưởng trong một biến cố được gọi là "vụ thảm sát Thượng Hải", chấm dứt việc liên minh giữa những người theo dân tộc chủ nghĩa và cộng sản. Cuộc thanh trừng bị lên án bởi Uông Tinh Vệ, hiện là lãnh đạo của chính quyền Vũ Hán, chính thức chia rẽ giữa phe cánh…

**Bài:** Bắc phạt (1926–1928) (10,114 âm tiết), cửa sổ ở 13% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tôn Trung Sơn được chẩn đoán mắc bệnh gì vào ngày 20/1/1925?  
**Đáp án sinh:** ung thư gan giai đoạn cuối  
**Kiểm:** ung thư gan giai đoạn cuối (F1 1.0)  
**Cửa sổ (rút gọn):** Tôn khẳng định để giải quyết vấn đề đất nước cần có một Hội nghị Quốc dân do dân bầu, Đoàn khước từ chủ trương triển khai một hội nghị bao gồm các lực lượng quân sự, chính trị và thương nhân, còn được gọi Hội nghị Thiện hậu (善後會議). Ngày 1/1/1925, Tôn Trung Sơn được đưa vào bệnh viện. Ngày 20/1, bệnh tình trở nên xấu hơn, ông được chẩn đoán ung thư …

**Bài:** Bắc phạt (1926–1928) (10,114 âm tiết), cửa sổ ở 52% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Mikhail Borodin là người liên lạc chính thức giữa Quốc dân đảng và chính phủ của quốc gia nào?  
**Đáp án sinh:** Liên Xô  
**Kiểm:** Liên Xô tại Moskva (F1 0.67)  
**Cửa sổ (rút gọn):** Căng thẳng giữa phe cánh tả ở Vũ Hán và phe cánh hữu ở Nam Kinh gây tranh cãi, dẫn tới chiến dịch Bắc phạt phải tạm ngừng. Trong khi đó, sau kết quả của cuộc tấn công Thượng Hải, Nam Kinh, sự trợ giúp của quân đội Phụng hệ đã ngăn chặn quân đội của Tôn Truyền Phương sụp đổ, và cuối cùng họ đã xoay xở để tập hợp lại và tăng cường lực lượng cho giai …

**Bài:** Bắc phạt (1926–1928) (10,114 âm tiết), cửa sổ ở 19% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người lãnh đạo chính phủ Bắc Dương và quân phiệt Phụng hệ, kiểm soát Mãn Châu, Sơn Đông và Trực Lệ?  
**Đáp án sinh:** Trương Tác Lâm  
**Kiểm:** Trương Tác Lâm (F1 1.0)  
**Cửa sổ (rút gọn):** Đồng thời, Tưởng thực hiện các động thái hòa giải đối với Liên Xô và cố gắng cân bằng hỗ trợ cần thiết của Liên Xô và Đảng Cộng sản Trung Quốc trong cuộc chiến chống lại các quân phiệt với những lo ngại về ảnh hưởng cộng sản ngày càng tăng với Quốc Dân Đảng. Sau cuộc đảo chính, Tưởng đã thương lượng một thỏa hiệp, theo đó các thành viên cứng rắn củ…

**Bài:** Bắc phạt (1926–1928) (10,114 âm tiết), cửa sổ ở 78% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sự kiện nào đã bắt đầu khi xung đột nổ ra giữa quân đội Trung Quốc và Nhật Bản vào sáng sớm hôm sau khi quân đội của Hikosuke Fukuda chuẩn bị rời khỏi Tế Nam?  
**Đáp án sinh:** sự cố Tế Nam  
**Kiểm:** sự cố Tế Nam (F1 1.0)  
**Cửa sổ (rút gọn):** Trong khi đó, lực lượng của Phùng tiến vào Sơn Đông từ phía tây, chiếm được Gia Tường vào ngày 15. Tôn Truyền Phương quyết định thực hiện một cuộc phản công hai mũi nhọn chống lại quân đội số một và số hai của Quốc quân, cẩn thận để đưa quân đội số một trở lại tuyến đường sắt Long Đàm. Cuộc tấn công của ông chống lại Quân đội số hai đã thất bại, và…

**Bài:** Bắc phạt (1926–1928) (10,114 âm tiết), cửa sổ ở 94% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Ai là người đã khuyến khích Đảng Cộng sản hợp tác với Quốc dân đảng vì tin rằng tổ chức này có khả năng hoàn thành cuộc cách mạng Trung Quốc?  
**Đáp án sinh:** Joseph Stalin  
**Kiểm:** Stalin (F1 0.67)  
**Cửa sổ (rút gọn):** Trương Học Lương tiếp tục kiểm soát Mãn Châu như một quốc gia độc lập gần như và các quân phiệt địa phương ở Tứ Xuyên, Vân Nam và Quý Châu vẫn như trước khi Bắc phạt. Quân phiệt bị đánh bại Trương Tông Xương trở lại Sơn Đông vào năm 1929, nơi ông đã phát động một cuộc nổi dậy chống lại cấp dưới trước đây Lưu Trân Niên. Cuộc nổi loạn bị dập tắt nhan…

**Bài:** Bắc phạt (1926–1928) (10,114 âm tiết), cửa sổ ở 54% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Mikhail Borodin là người liên lạc chính thức giữa Quốc dân đảng và chính phủ nào?  
**Đáp án sinh:** Liên Xô  
**Kiểm:** chính phủ Liên Xô tại Moskva (F1 0.5)  
**Cửa sổ (rút gọn):** Là một phần của Mặt trận Thống nhất đầu tiên, nhiều thành viên của Đảng Cộng sản Trung Quốc đã gia nhập Quốc dân đảng, và họ đã gây ảnh hưởng đáng kể đối với phe cánh tả. Mikhail Borodin, người liên lạc chính thức giữa Quốc dân đảng và chính phủ Liên Xô tại Moskva, đã dành nhiều năm để xây dựng liên minh này, đồng thời khuyến khích mở rộng Đảng Cộn…

**Bài:** Bắc phạt (1926–1928) (10,114 âm tiết), cửa sổ ở 31% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cuộc đình công ở Quảng Đông-Hồng Kong đã kết thúc vào ngày nào?  
**Đáp án sinh:** ngày 10 tháng 10  
**Kiểm:** ngày 10 tháng 10 (F1 1.0)  
**Cửa sổ (rút gọn):** Tôn chiếm lại hầu hết lãnh thổ đã mất, khẳng định lại quyền lực của mình một cách tàn nhẫn bằng cách giết chết hàng trăm học sinh, giáo viên và các thành viên nghi ngờ là của Quốc dân đảng, những người bị chặt đầu treo vào cột tại những nơi công cộng. Với việc tiến lên phía trước bị tạm ngừng, Tưởng điện cho chính phủ Quảng Châu, yêu cầu chấm dứt c…

**Bài:** Chiến dịch tấn công Proskurov–Chernovtsy (17,745 âm tiết), cửa sổ ở 24% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân xe tăng 1 của Đức Quốc xã do vị tướng nào chỉ huy?  
**Đáp án sinh:** thượng tướng Hans-Valentin Hube  
**Kiểm:** thượng tướng Hans-Valentin Hube (F1 1.0)  
**Cửa sổ (rút gọn):** Mãi đến ngày 1 tháng 3, Tập đoàn quân 60 mới vượt được 60 km từ Mlinov đến Yampol trên một vùng hầu như không có đường sá. Tập đoàn quân xe tăng 1 đến ngày 2 tháng 3 mới đổ quân xuống ga Shepetovka trong khi nhiên liệu của họ vẫn còn đang nằm ở đâu đó trên tuyến đường sắt Berdichev - Shepetovka. Tập đoàn quân xe tăng cận vệ 3 phải san sẻ cho Tập đo…

**Bài:** Chiến dịch tấn công Proskurov–Chernovtsy (17,745 âm tiết), cửa sổ ở 2% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cụm tập đoàn quân Nam Ukraina do ai chỉ huy sau khi Cụm tập đoàn quân Nam (Đức) bị chia đôi?  
**Đáp án sinh:** Thượng tướng Johannes Hans Frießner  
**Kiểm:** Thượng tướng Johannes Hans Frießner (F1 1.0)  
**Cửa sổ (rút gọn):** Các trung đoàn xe tăng hạng nặng 503, 506, 509 (Đức) khi vào trận đều được biên chế 56 xe tăng Tiger I nhưng khi thoát vây chỉ còn lại 5 đến 7 chiếc. Kết quả của chiến dịch này và cũng là của Chiến dịch tấn công Uman–Botoşani đã cắt đôi mặt trận của Cụm tập đoàn quân Nam (Đức) tại Tây Ukraina. Tổng hành dinh quân đội Đức Quốc xã đã phải chia Cụm tậ…

**Bài:** Chiến dịch tấn công Proskurov–Chernovtsy (17,745 âm tiết), cửa sổ ở 72% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Lữ đoàn xe tăng 45 cùng với đơn vị nào đã kịp thời giải vây cho Sư đoàn bộ binh 359?  
**Đáp án sinh:** Lữ đoàn xe tăng cận vệ 13 (Quân đoàn xe tăng cận vệ 4)  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Chỉ huy lữ đoàn, đại tá G. Gasparyan phải chuyển sang đánh phá các bến vượt sông của bộ binh Đức tại Biala Kernitsy (???) và Lenchuvky (???). Ngày 5 tháng 4, Lữ đoàn xe tăng 45 (Quân đoàn xe tăng cận vệ 11) cũng tới nơi nhưng đã muộn. Phần lớn số quân Đức thoát vây đã sang bên kia sông Koropets và đánh vào sau lưng Tập đoàn quân cận vệ 1 (Liên Xô).…

**Bài:** Chiến dịch tấn công Proskurov–Chernovtsy (17,745 âm tiết), cửa sổ ở 26% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người chỉ huy Tập đoàn quân xe tăng 4?  
**Đáp án sinh:** thượng tướng Erhard Raus  
**Kiểm:** thượng tướng Erhard Raus (F1 1.0)  
**Cửa sổ (rút gọn):** Trung đoàn xe tăng hạng nặng của đại tá Franz Bäke gồm các tiểu đoàn xe tăng hạng nặng 506, 509.Quân đoàn xe tăng 24 của tướng Walther Nehring, trong biên chế có:Sư đoàn xe tăng 20 của tướng Georg Jauer.Sư đoàn xe tăng 25 của tướng Hans Tröger.Sư đoàn bộ binh 208 của tướng Hans Pieckenbrock.Sư đoàn bộ binh 371 của tướng Hermann Niehoff.Lữ đoàn cơ g…

**Bài:** Chiến dịch tấn công Proskurov–Chernovtsy (17,745 âm tiết), cửa sổ ở 11% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Quân đoàn cơ giới cận vệ 6 bao gồm những lữ đoàn cơ giới nào?  
**Đáp án sinh:** lữ đoàn cơ giới cận vệ 16, 17; Lữ đoàn cơ giới 49  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Các đơn vị trực thuộc Tập đoàn quân: Lữ đoàn xe tăng 91; Trung đoàn pháo tự hành 50; Tiểu đoàn trinh sát cơ giới 39, Trung đoàn cơ giới cận vệ 90; các trung đoàn phòng không 1381, 1393; Trung đoàn công binh 182. Tập đoàn quân xe tăng 4 do trung tướng D. Quân đoàn cơ giới cận vệ 6 gồm các lữ đoàn cơ giới cận vệ 16, 17; Lữ đoàn cơ giới 49; các trung …

**Bài:** Chiến dịch tấn công Proskurov–Chernovtsy (17,745 âm tiết), cửa sổ ở 69% bài  
**Trạng thái:** kept  
**Câu hỏi:** Bộ tư lệnh Phương diện quân Ukraina 1 nhận được báo cáo về cuộc phá vây của quân Đức vào thời điểm nào?  
**Đáp án sinh:** chiều ngày 1 tháng 4  
**Kiểm:** chiều ngày 1 tháng 4 (F1 1.0)  
**Cửa sổ (rút gọn):** Thay vì thực hiện các đòn chia cắt vào cụm quân của Tập đoàn quân xe tăng 1 (Đức), Tập đoàn quân xe tăng 4 và Tập đoàn quân 38 (Liên Xô) phải mở cuộc truy kích lên phía Bắc. Từ ngày 2 đến ngày 7 tháng 4, 89 xe tăng và 15 pháo tự hành còn lại của Quân đoàn xe tăng cận vệ 10 đã giao chiến với 3 sư đoàn xe tăng Đức trong các trận đánh đẫm máu tại khu …

**Bài:** Chiến dịch tấn công Proskurov–Chernovtsy (17,745 âm tiết), cửa sổ ở 21% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người yêu cầu Đại bản doanh lấy Tập đoàn quân xe tăng 4 của tướng D. Lelyushenko từ lực lượng dự bị để tăng viện cho Phương diện quân?  
**Đáp án sinh:** G. Zhukov  
**Kiểm:** G. Zhukov (F1 1.0)  
**Cửa sổ (rút gọn):** Đòn đột kích mạnh nhất sẽ được các tập đoàn quân xe tăng Liên Xô giáng vào đoạn tiếp giáp giữa Tập đoàn quân xe tăng 4 và Tập đoàn quân xe tăng 1 (Đức) đang mỏng đi sau nỗ lực phá vây cứu Cụm quân Đức ở Korsun–Shevchenkovsky. Xét thấy một mình Tập đoàn quân xe tăng cận vệ 3 của tướng P. Rybalko không đủ mạnh để đột phá sâu, G. Zhukov yêu cầu Đại bả…

**Bài:** Chiến dịch tấn công Proskurov–Chernovtsy (17,745 âm tiết), cửa sổ ở 36% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn bộ binh 67 đã đánh bật đòn phản kích của sư đoàn xe tăng 1 SS và các lữ đoàn cơ giới 249, 300 (Đức) tại địa điểm nào?  
**Đáp án sinh:** Lipovets  
**Kiểm:** Lipovets (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 11 tháng 3, Quân đoàn bộ binh 67 đã đánh bật đòn phản kích của sư đoàn xe tăng 1 SS và các lữ đoàn cơ giới 249, 300 (Đức) tại Lipovets và bắt đầu tấn công dọc theo đường cao tốc Fastov - Vinnitsa. Quân đoàn xe tăng 25 đã vượt lên phía trước, đánh chiếm Troshchiev (???), Voronovitsa, Demidovka, vây bọc Vinnitsa từ phía Nam. Quân đoàn bộ binh 67…

**Bài:** Dacia thuộc La Mã (11,735 âm tiết), cửa sổ ở 29% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hành tỉnh Dacia ban đầu của Trajan được đổi tên thành tên gì?  
**Đáp án sinh:** Thượng Dacia  
**Kiểm:** Thượng Dacia (F1 1.0)  
**Cửa sổ (rút gọn):** Những vùng đất của Hạ Moesia ở phía bắc của sông Danube lại được chia ra và tái lập thành một tỉnh mới được gọi là Hạ Dacia. Hành tỉnh Dacia ban đầu của Trajan lại được đổi tên thành Thượng Dacia . Cũng vào thời điểm này, Hadrianus đã chuyển Legio IV Flavia Felix ra khỏi căn cứ của nó tại Ulpia Traiana Sarmizegetusa, và ra lệnh cho nó đóng quân tại…

**Bài:** Dacia thuộc La Mã (11,735 âm tiết), cửa sổ ở 57% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vũ khí đặc biệt của người Dacia được mô tả trên di vật có nguồn gốc từ cohort I Aelia Dacorum là gì?  
**Đáp án sinh:** Sica  
**Kiểm:** Sica (F1 1.0)  
**Cửa sổ (rút gọn):** Những kiểu dáng kiến trúc bản địa từ trước thời Dacia thuộc La Mã, chẳng hạn như ngôi nhà trũng truyền thống và các hầm chứa lương thực, vẫn còn trong thời kì La Mã. Những căn nhà ở như vậy tiếp tục được xây dựng vào thời kỳ La Mã, ngay cả trong các khu định cư mà rõ ràng được thành lập sau khi La Mã thôn tính, chẳng hạn như Obreja. Tại những nơi m…

**Bài:** Dacia thuộc La Mã (11,735 âm tiết), cửa sổ ở 73% bài  
**Trạng thái:** kept  
**Câu hỏi:** Các khu định cư kết nối đến các doanh trại quân đội được với hệ thống hào xung quanh trong Dacia thuộc La Mã được gọi là gì?  
**Đáp án sinh:** vici quân sự  
**Kiểm:** vici quân sự (F1 1.0)  
**Cửa sổ (rút gọn):** Chúng bao gồm Brucla, Blandiana, Germisara, Petris, và Aquae.Vị trí của Brucla, Blandiana, và Petris thì không được biết chắc chắn. Tuy nhiên, trong trường hợp của Petris, có lý do để cho rằng nó đã được xác định là tại Uroi ở România. Nếu điều này là đúng thì nó có một ví trí rất quan trọng trong giao thương và cũng giữ vai trò quan trọng trong vi…

**Bài:** Dacia thuộc La Mã (11,735 âm tiết), cửa sổ ở 10% bài  
**Trạng thái:** kept  
**Câu hỏi:** Viên thống đốc Moesia nào đã bị người Daci dưới sự lãnh đạo của vua Decebalus giết chết trong khoảng năm 84 hoặc 85 CN?  
**Đáp án sinh:** Oppius Sabinus  
**Kiểm:** Oppius Sabinus (F1 1.0)  
**Cửa sổ (rút gọn):** Sau khi ông ta bị ám sát, vương quốc Dacia bị tan vỡ thành bốn thực thể chính trị khác biệt, sau này trở thành năm. Từ lúc Burebista qua đời cho tới khi Decebalus nổi lên, quân đội La Mã vẫn tiếp tục những cuộc xung đột chống lại người Daci và Getae. Các bộ lạc này liên tục đánh phá các tỉnh lân cận như Moesia và Pannonia khiến cho các thống đốc đị…

**Bài:** Dacia thuộc La Mã (11,735 âm tiết), cửa sổ ở 17% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào ngày 11 tháng 8 năm 106, các nguồn La Mã đã coi vùng Dacia là một tỉnh thuộc đối tượng nào?  
**Đáp án sinh:** hoàng đế  
**Kiểm:** hoàng đế (F1 1.0)  
**Cửa sổ (rút gọn):** Một trong những người đầu hàng đã tiết lộ vị trí của kho báu hoàng gia Dacia, mà giá trị của nó là rất lớn: 500.000 bảng vàng (226.800 kg) 1.000.000 bảng bạc(453.600 kg). Dacia dưới triều đại của các hoàng đế nhà Antoninus và Severus (từ năm 106-235) Với việc sáp nhập vương quốc của Decebalus, Dacia đã trở thành hành tỉnh mới nhất của La Mã, nó cũn…

**Bài:** Dacia thuộc La Mã (11,735 âm tiết), cửa sổ ở 25% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hadrianus đã cho tháo dỡ công trình nào trên sông Danube như một biện pháp khẩn cấp?  
**Đáp án sinh:** cây cầu của Apollodorus  
**Kiểm:** cây cầu của Apollodorus (F1 1.0)  
**Cửa sổ (rút gọn):** Con đường thứ hai là tuyến đường chính lớn hơn và nó đã đi ngang qua Apulum, và kéo dài từ biển Đen xa xôi ở phía đông tới tận Hạ Pannonia ở phía tây và có lẽ vượt xa hơn nữa. Những sự tái tổ chức đầu tiên (117-138) Hadrianus đang có mặt tại Antioch ở Syria, khi nghe tin Traianus đã qua đời. Nhưng ông đã không có thời gian để trở về Roma ngay, vì ô…

**Bài:** Dacia thuộc La Mã (11,735 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** Viên thống đốc của tỉnh Dacia vào năm 169 là ai?  
**Đáp án sinh:** Agricola  
**Kiểm:** Agricola (F1 1.0)  
**Cửa sổ (rút gọn):** Các căn biệt thự ngoại ô tại Ulpia Traiana Sarmizegetusa bị thiêu trụi, và trại binh tại Slăveni đã bị phá hủy bởi người Marcomanni. Vào lúc Marcus Aurelius đến được Aquileia trong năm 168 sau công nguyên, người Iazyges đã bắt đi hơn 100.000 người La Mã làm tù binh. Chiến tranh vẫn sẽ tiếp tục ở Dacia trong vòng hai năm tới, và vào năm 169 viên thố…

**Bài:** Dacia thuộc La Mã (11,735 âm tiết), cửa sổ ở 8% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vương quốc của Burebista kéo dài từ Pannonia ở phía tây đến đâu ở phía đông?  
**Đáp án sinh:** Biển Đen  
**Kiểm:** Biển Đen (F1 1.0)  
**Cửa sổ (rút gọn):** Người Daci và người Getae thường xuyên có tác động qua lại với những người La Mã trước khi Dacia được sáp nhập vào đế quốc La Mã. Tuy nhiên, sự chú ý của La Mã vào khu vực xung quanh hạ lưu sông Danube đã được tăng thêm khi Burebista (năm 82-44 trước Công nguyên) thống nhất các bộ lạc bản địa và bắt đầu một chiến dịch bành trướng tích cực. Vương qu…

**Bài:** Trận Königgrätz (20,435 âm tiết), cửa sổ ở 97% bài  
**Trạng thái:** kept  
**Câu hỏi:** Từ lóng nào trong tiếng Anh tương tự như "Königgrätz" trong tiếng Áo để chỉ sự thất bại?  
**Đáp án sinh:** Waterloo  
**Kiểm:** Waterloo (F1 1.0)  
**Cửa sổ (rút gọn):** Do trận thảm bại này mà cho đến nay từ "Königgrätz" vẫn được sử dụng như một từ lóng ở Áo, có nghĩa là "thất bại", tương tự như "Waterloo" trong tiếng Anh. Anh pháo binh Jabůrek, một nhân vật hư cấu, có lẽ là người Tiệp Khắc thông thường nổi tiếng nhất tham gia trận đánh • a) Các nhà văn Pháp trong và sau năm 1866 thường ưu tiên dùng cái tên "Sadow…

**Bài:** Trận Königgrätz (20,435 âm tiết), cửa sổ ở 91% bài  
**Trạng thái:** kept  
**Câu hỏi:** Dư luận Pháp đã đề nghị điều gì sau khi nhìn nhận trận Königgrätz như là một thất bại của Pháp?  
**Đáp án sinh:** Revanche pour Sadova  
**Kiểm:** Revanche pour Sadova (F1 1.0)  
**Cửa sổ (rút gọn):** Nói đến Rhein, Rouher ám chỉ các thành phố ở miền Tây Phổ (Köln, Düsseldorf và vùng Ruhr với các thành phố Essen, Bochum và Dortmund ở Westfalen), những trung tâm công nghiệp quan trọng mà Berlin không thể tồn tại nếu không có. Ngay cả những người theo chủ nghĩa tự do đối lập với Napoléon cũng chủ trương ủng hộ các cuộc phiêu lưu quân sự. Thay vì đ…

**Bài:** Trận Königgrätz (20,435 âm tiết), cửa sổ ở 12% bài  
**Trạng thái:** kept  
**Câu hỏi:** Moltke đã mô tả vị trí phòng ngự của quân Áo đằng sau sông Bistritz như thế nào?  
**Đáp án sinh:** cực kỳ vững mạnh  
**Kiểm:** cực kỳ vững mạnh (F1 1.0)  
**Cửa sổ (rút gọn):** Niềm tin của ông bắt đầu được hồi sinh khi mà ông chỉnh đốn quân ngũ để chuẩn bị trận đánh quyết định sắp sửa xảy ra. Benedeck tập trung binh lực hướng về phía Tây dọc theo một mặt trận trải dài 10 dặm Anh từ Josephstadtz về hướng Nam tới Königgrätz và ở trên ngôi làng Sadowa.. Moltke đã mô tả vị trí phòng ngự của quân Áo đằng sau sông Bistritz là …

**Bài:** Trận Königgrätz (20,435 âm tiết), cửa sổ ở 4% bài  
**Trạng thái:** kept  
**Câu hỏi:** Bismarck đã hứa hẹn nhượng bộ vùng nào cho Pháp để đổi lại thái độ trung lập của nước này?  
**Đáp án sinh:** vùng ven sông Rhine  
**Kiểm:** vùng ven sông Rhine (F1 1.0)  
**Cửa sổ (rút gọn):** Đồng thời, giới lãnh đạo Nga cũng biết ơn Bismarck vì đã niêm phong biên giới của Phổ với Ba Lan trong cuộc khởi nghĩa của nhân dân Ba Lan vào năm 1863 chống lại ách thống trị của người Nga – điều này khiến cho Nga dễ dàng dập tắt cuộc khởi nghĩa. Vào tháng 10 năm 1865, Bismarck tiếp kiến Hoàng đế Pháp là Napoléon III tại Biarritz và hứa hẹn sẽ như…

**Bài:** Trận Königgrätz (20,435 âm tiết), cửa sổ ở 21% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Ai là người đã hạ trại tại lâu đài Cerekwitz vào đêm ngày 1 tháng 7 năm 1866?  
**Đáp án sinh:** Đại tá Franz von Zychlinski  
**Kiểm:** tiền quân của Sư đoàn số 7 (tướng Fransecky) do Đại tá Franz von Zychlinski chỉ huy (F1 0.45)  
**Cửa sổ (rút gọn):** Họ kêu gọi thống nhất ba tập đoàn quân, và thậm chí Blumenthal còn đưa ra một đề xuất mang nặng phong cách Napoléon nhằm "tiến thẳng về Viên mà không cần biết quân địch ở đâu". Dù đang bị cảm nặng, Moltke vẫn giữ cái đầu lạnh và đề xuất của Blumenthal bị từ chối. Hội nghị quyết định giữ khoảng cách giữa hai Tập đoàn quân số 1 và 2 chí ít là cho đến…

**Bài:** Trận Königgrätz (20,435 âm tiết), cửa sổ ở 32% bài  
**Trạng thái:** kept  
**Câu hỏi:** Loại vũ khí nào đã giúp lợi thế của quân Phổ bị vô hiệu hóa do bị che khuất bởi nhà cửa, cây cối và khói súng?  
**Đáp án sinh:** súng trường nạp hậu Dreyse  
**Kiểm:** súng trường nạp hậu Dreyse (F1 1.0)  
**Cửa sổ (rút gọn):** Bộ binh Áo trấn giữ các ngọn cầu và làng bản, và bắn xối xả vào các đội hình tiến công của Phổ. Quân Phổ chỉ có thể tiến chậm dọc theo những nẻo đường chật hẹp và đánh trả sự kháng cự của quân Áo trong các căn nhà. Hỏa lực của người Áo đã đốn quỵ từng lớp quân địch. Trong khi đó, lợi thế mà súng trường nạp hậu Dreyse đem lại cho quân Phổ bị vô hiệu…

**Bài:** Trận Königgrätz (20,435 âm tiết), cửa sổ ở 98% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tên gọi nào được vua Wilhelm I chọn cho trận đánh sau chiến thắng lớn nhất của mình?  
**Đáp án sinh:** Königgrätz  
**Kiểm:** Königgrätz (F1 1.0)  
**Cửa sổ (rút gọn):** • a) Các nhà văn Pháp trong và sau năm 1866 thường ưu tiên dùng cái tên "Sadowa" hơn là "Königgrätz", gọi trận đánh theo tên một ngôi làng trên sông Bistritz nơi mà giao chiến đã diễn ra giữa trung quân Phổ với đối phương vào buổi sáng ngày 3 tháng 7. Các tác giả khác chỉ ra rằng tên gọi hợp lý nhất của trận đánh phải là "Chlum", do trận đánh chiếm…

**Bài:** Trận Königgrätz (20,435 âm tiết), cửa sổ ở 20% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vị trí nào mà vua Wilhelm I của Phổ đã thiết lập Tổng hành dinh vào buổi chiều ngày 2 tháng 7?  
**Đáp án sinh:** Gitschin  
**Kiểm:** Gitschin (F1 1.0)  
**Cửa sổ (rút gọn):** Trong khi Moltke muốn giữ vững tính linh hoạt do sự phân rẽ các đạo quân đem lại, các chỉ huy tập đoàn quân mang hãy còn lo sợ quân của Benedek đột ngột xuất hiện và đánh bại từng tập đoàn quân riêng lẻ. Do vậy, Blumenthal yêu cầu cho Tập đoàn quân số 2 vượt sông Elbe để hội quân với Friedrich Karl và truy đuổi địch quân, nhưng bị Moltke bác bỏ. Sá…

**Bài:** Chiến dịch Leningrad–Novgorod (10,567 âm tiết), cửa sổ ở 58% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chỉ thị số 220023 của Đại bản doanh ngày 13 tháng 1 năm 1944 yêu cầu giải tán đơn vị quân sự nào?  
**Đáp án sinh:** Phương diện quân Volkhov  
**Kiểm:** Phương diện quân Volkhov (F1 1.0)  
**Cửa sổ (rút gọn):** Sau khi nhiệm vụ Luga hoàn thành, ngày 13 tháng 1 năm 1944 Đại bản doanh ra Chỉ thị số 220023 có nội dung yêu cầu giải tán Phương diện quân Volkhov. Các Tập đoàn quân số 54, 59 và 8 của nó được chuyển giao cho Phương diện quân Leningrad. Tập đoàn quân xung kích số 1 được trả về cho Phương diện quân Baltic 2. Bộ chỉ huy Phương diện quân được chuyển …

**Bài:** Chiến dịch Leningrad–Novgorod (10,567 âm tiết), cửa sổ ở 13% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hạm đội nào được đề cập là hỗ trợ cho Phương diện quân Leningrad với quân số 89.600 người?  
**Đáp án sinh:** Hạm đội Baltic  
**Kiểm:** Hạm đội Baltic (F1 1.0)  
**Cửa sổ (rút gọn):** Phương diện quân Leningrad đóng dọc trên các tuyến ở sông Neva, vịnh Phần Lan, bờ nam của hồ Ladoga từ Moskovskoy Dubrovki (???) tới Gontovoy Lipki (???) và cả vùng bàn đạp Oranienbaum (Lomnosov) (khi TDQ xung kích số 2 được chuyển giao cho PDQ Leningrad vào mùa thu năm 1943). Binh lực gồm 30 sư đoàn bộ binh, 3 lữ đoàn bộ binh, 4 lữ đoàn xe tăng, 3…

**Bài:** Chiến dịch Leningrad–Novgorod (10,567 âm tiết), cửa sổ ở 55% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tướng Walter Model đã hạ lệnh cho Tập đoàn quân số 18 (Đức) phải lấy lại tuyến liên lạc giữa hai địa điểm nào?  
**Đáp án sinh:** Luga và Pskov  
**Kiểm:** Luga và Pskov (F1 1.0)  
**Cửa sổ (rút gọn):** Các thành phố Lyady, Sara-Goru, Gdov lần lượt được giải phóng và đến ngày 2 tháng 4 quân đội Liên Xô đã tiếp cận bờ hồ Chudskoe. Từ vị trí này, Tập đoàn quân só 42 dự tính sẽ mở một đòn đánh bọc vòng, giải phóng Plyussa, Strugi Krasnye, cắt đứt tuyến đường bộ Luga - Pskov và hội quân với Tập đoàn quân số 67 để hợp vây Luga. Sự thành công của Tập đo…

**Bài:** Chiến dịch Leningrad–Novgorod (10,567 âm tiết), cửa sổ ở 17% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hai kế hoạch tấn công nào được đề xuất cho chiến dịch dự kiến bắt đầu vào mùa đông?  
**Đáp án sinh:** Neva I và Neva II  
**Kiểm:** Neva I và Neva II (F1 1.0)  
**Cửa sổ (rút gọn):** Chiến dịch dự kiến sẽ bắt đầu vào mùa đông khi binh lực đã chuẩn bị đầy đủ và mặt băng đủ dày để pháo binh băng qua. Hai kế hoạch tấn công, Neva I và Neva II, được đề xuất. Kế hoạch Neva I được đưa ra dựa trên giả thuyết rằng, trước sức ép từ các khu vực khác, quân đội Đức tại miền bắc Liên Xô sẽ tự động rút lui khỏi Leningrad và trên đường đi cũng…

**Bài:** Chiến dịch Leningrad–Novgorod (10,567 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tư lệnh của Phương diện quân Volkhov?  
**Đáp án sinh:** Đại tướng K. A, Meretskov  
**Kiểm:** Đại tướng K. A, Meretskov (F1 1.0)  
**Cửa sổ (rút gọn):** Maslennikov, từ ngáy 14 đến 24 tháng 3 là V. Romanovsky, đến cuối tháng 3 là V. Tập đoàn quân số 67 (trung tướng V. Sviridov, đến cuối tháng 3 là trung tướng V. Tập đoàn quân không quân số 13 (thượng tướng không quân S. Phương diện quân Volkhov (giải thể vào ngày 15 tháng 2 năm 1944) (tư lệnh: Đại tướng K. A, Meretskov, tham mưu trưởng: trung tướng…

**Bài:** Chiến dịch Leningrad–Novgorod (10,567 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thành phố nào được nêu là nổi bật nhất trong số các thành phố và thị xã được giải phóng trong chiến dịch tháng 1?  
**Đáp án sinh:** Novgorod  
**Kiểm:** Novgorod (F1 1.0)  
**Cửa sổ (rút gọn):** Trong tháng 1, các phương diện quân Volkhov và Leningrad đã đánh bật quân Đức khỏi các vị trí mà họ đã chiếm giữ suốt 2 năm, phá giải hoàn toàn sự uy hiếp đối với thành phố Leningrad, giải phóng hoàn toản tỉnh Leningrad và một phần Kalinin (tỉnh), đẩy quân thù lui về tuyến Panther-Wotan. Trong số các thành phố và thị xã được giải phóng, nổi bật nhấ…

**Bài:** Chiến dịch Leningrad–Novgorod (10,567 âm tiết), cửa sổ ở 3% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tư lệnh của Phương diện quân Leningrad?  
**Đáp án sinh:** Đại tướng L. Govorov  
**Kiểm:** Đại tướng L. Govorov (F1 1.0)  
**Cửa sổ (rút gọn):** Các lực lượng tham gia một chiến dịch như vậy được dự kiến là các phương diện quân Leningrad, Volkhov, Tây Bắc và Tây. Trong đó, các Phương diện quân Volkhov và Leningrad sẽ lãnh nhiệm vụ giải trừ hoàn toàn sự uy hiếp của quân Đức tại Leningrad. Binh lực và kế hoạch Phương diện quân Leningrad (tư lệnh: Đại tướng L. Govorov, tham mưu trưởng: trung t…

**Bài:** Chiến dịch Leningrad–Novgorod (10,567 âm tiết), cửa sổ ở 29% bài  
**Trạng thái:** kept  
**Câu hỏi:** Kế hoạch lui binh của quân Đức trong tháng 1 năm 1944 được đặt tên là gì?  
**Đáp án sinh:** Xanh lam  
**Kiểm:** Xanh lam (F1 1.0)  
**Cửa sổ (rút gọn):** Kế hoạch lui binh này được đặt tên là "Xanh lam" và theo đó, trong tháng 1 năm 1944 thì quân Đức sẽ rút lui 150 dặm về một phòng tuyến tự nhiên được tạo thành bởi sông Narva, sông Velikaya, hồ Chudskoe (còn gọi là hồ Peipus) và Pskov. Vị trí đóng quân này, mang tên "tuyến Panther-Wotan", được chống đỡ bằng những công sự được xây dựng từ hồi tháng 9…

**Bài:** Trận Gravelotte (10,028 âm tiết), cửa sổ ở 29% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tầm bắn hiệu quả của khẩu Chassepot lên đến bao nhiêu mét?  
**Đáp án sinh:** gần 1.500 m  
**Kiểm:** gần 1.500 m (F1 1.0)  
**Cửa sổ (rút gọn):** Ngay lập tức, các khẩu đại bác và súng máy mitrailleuse của Pháp đáp trả ác liệt. Sau được điều gấp vào vị trí ở hướng bắc và nam Amanvillers, các sư đoàn bộ binh của Quân đoàn III Pháp cũng tuôn đạn xối xả vào trận tuyến pháo binh Phổ. Các sĩ quan pháo binh của Manstein đã mắc sai lầm nghiêm trọng khi họ khai triển pháo binh trong tầm đạn súng trư…

**Bài:** Trận Gravelotte (10,028 âm tiết), cửa sổ ở 19% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo sử gia Michael A. Howard, điểm yếu của trận tuyến phòng thủ vững chắc của Bazaine nằm ở đâu?  
**Đáp án sinh:** cánh phải  
**Kiểm:** cánh phải (F1 1.0)  
**Cửa sổ (rút gọn):** Gần đó, viên Thống chế bố trí lực lượng trừ bị chủ chốt của mình, đội Cận vệ Đế chế, yểm trợ cánh trái và trung tâm, do ông tiên liệu rằng quân Phổ sẽ phát động mũi tấn công chủ lực theo hướng này. Theo nhìn nhận của sử gia Anh Michael A. Howard, điểm yếu của trận tuyến phòng thủ vững chắc của Bazaine nằm ở cánh phải, do không gì có thể ngăn cản cá…

**Bài:** Trận Gravelotte (10,028 âm tiết), cửa sổ ở 75% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vua Wilhelm I đã ban lệnh tiếp tục tiến công vào ngày hôm sau trước sự khăng khăng của ai?  
**Đáp án sinh:** Moltke  
**Kiểm:** Moltke (F1 1.0)  
**Cửa sổ (rút gọn):** Khi trèo qua ngọn dốc ở bên kia con kênh, một số đơn vị đi đầu của Quân đoàn II đã nổ súng vào những toán quân mà họ nhìn thấy mập mờ qua hàng cây. Trái với nhầm tưởng của binh lính Quân đoàn II, đây là những người lính Đông Phổ của Goeben còn sót lại quanh Saint-Hubert sau cuộc chạy loạn và đang trấn giữ một trận tuyến mỏng manh. Những người lính …

**Bài:** Trận Gravelotte (10,028 âm tiết), cửa sổ ở 33% bài  
**Trạng thái:** kept  
**Câu hỏi:** Moltke đã gửi bức điện cho Steinmetz nhằm ngăn chặn điều gì?  
**Đáp án sinh:** vị tướng bốc động này làm cho tình hình xấu thêm  
**Kiểm:** vị tướng bốc động này làm cho tình hình xấu thêm (F1 1.0)  
**Cửa sổ (rút gọn):** Từ trên các cao điểm phía nam Flavigny, tướng Moltke đã nghe thấy những tiếng đạn pháo đầu tiên của Quân đoàn IX và nhanh chóng rút ra kết luận rằng các thuộc tướng đã tấn công sớm hơn dự kiến của ông. Ông liền gửi gấp một bức điện cho Steinmetz để ngăn chặn vị tướng bốc động này làm cho tình hình xấu thêm. Theo bức điện, những gì đang diễn ra ở Ve…

**Bài:** Trận Gravelotte (10,028 âm tiết), cửa sổ ở 10% bài  
**Trạng thái:** kept  
**Câu hỏi:** Loại vũ khí nào của Pháp có độ chính xác và tầm bắn vượt xa súng trường Dreyse của Phổ trong trận đánh ngày 16 tháng 8?  
**Đáp án sinh:** súng trường nạp hậu Chassepot  
**Kiểm:** súng trường nạp hậu Chassepot (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 16 tháng 8, Bazaine ra lệnh hoãn hành quân đến chiều do quân kỵ binh tuần tiễu của Pháp không tìm thấy một lực lượng địch nào ở phía nam và các đơn vị cuối cùng của hai Quân đoàn III và IV Pháp vẫn chưa vượt sông Moselle. Trái ngược với những gì mà viên Thống chế Pháp suy nghĩ, các thành phần quân Phổ thuộc Quân đoàn III dưới quyền Trung tướng…

**Bài:** Trận Gravelotte (10,028 âm tiết), cửa sổ ở 3% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, trận Gravelotte được quyết định bởi yếu tố nào?  
**Đáp án sinh:** pháo binh Phổ  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Số quân Phổ chết và bị thương lên tới khoảng 2 vạn người trong ngày hôm đó. Tuy nhiên, bị ảnh hưởng nặng nề bởi chiến thuật phòng ngự của Pháp vốn đã ăn sâu vào tâm trí họ từ năm 1866, các tướng lĩnh Pháp từ chối phản công, ngay cả khi xác lính Phổ chất đầy dưới chân họ. Điều đó đem lại thời gian cho phía Phổ điều động pháo binh bịt kín các lỗ hổng…

**Bài:** Trận Gravelotte (10,028 âm tiết), cửa sổ ở 85% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo đánh giá của tờ báo quốc gia National Zeitung của Phổ, trận Gravelotte là sự kiện như thế nào trong cuộc chiến?  
**Đáp án sinh:** sự kiện có tầm quan trọng lớn nhất trong cuộc chiến  
**Kiểm:** sự kiện có tầm quan trọng lớn nhất trong cuộc chiến (F1 1.0)  
**Cửa sổ (rút gọn):** Vào ngày 19 tháng 8, Bazaine báo cáo với Hoàng đế về tình hình Tập đoàn quân Rhine: "Quân lực đã mỏi mệt với những trận đánh không ngừng nghỉ ấy, những trận đánh đã không để cho họ hồi sức; họ cần phải được nghỉ hai hoặc ba ngày.... Tôi vẫn dự tính tiến lên phía bắc và chiến đấu mở đường qua Montmédy trên đoạn đường Ste Ménéhould-Châlons, nếu như n…

**Bài:** Trận Gravelotte (10,028 âm tiết), cửa sổ ở 67% bài  
**Trạng thái:** kept  
**Câu hỏi:** Viên chỉ huy Cận vệ Đế chế đã bắt đầu quay quân trở lại vị trí trong trạng thái cảm xúc nào?  
**Đáp án sinh:** Trong cơn giận dữ  
**Kiểm:** Trong cơn giận dữ (F1 1.0)  
**Cửa sổ (rút gọn):** Không cần phải kêu tôi ra khỏi các vị trí tuyệt vời của mình để làm vậy. Trong cơn giận dữ, viên chỉ huy Cận vệ Đế chế bắt đầu quay quân trở lại vị trí. Hình ảnh đội Cận vệ "thần thánh" rút lui với sự nhốn nháo rõ rệt không chỉ khẳng định nỗi sợ hãi của những mớ loan quân chạy khỏi mặt trận Quân đoàn VI mà còn gây cho một bộ phận Quân đoàn IV hoảng…

**Bài:** Trận bán đảo Kerch (1942) (11,765 âm tiết), cửa sổ ở 74% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Theo Robert Forcyzk, Quân đội Liên Xô mất bao nhiêu người chết, bị bắt, mất tích và bị thương trong chiến dịch?  
**Đáp án sinh:** 162.282  
**Kiểm:** 162.282 người (F1 0.67)  
**Cửa sổ (rút gọn):** Người Đức tuyên bố trong chiến dịch này, họ tiêu diệt, bắt sống và làm bị thương 170.000 quân Liên Xô nhưng con số này còn bao gồm cả các thường dân mà quân Đức gọi là các phần tử du kích. Theo Robert Forcyzk, Quân đội Liên Xô mất 162.282 người chết, bị bắt, mất tích và bị thương; 116.045 người đã rút sang Taman và các căn cứ hải quân khác bằng đườ…

**Bài:** Trận bán đảo Kerch (1942) (11,765 âm tiết), cửa sổ ở 12% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hạm đội Biển Đen do Phó đô đốc F. chỉ huy có bao nhiêu tàu ngầm lớp U?  
**Đáp án sinh:** 12 tàu ngầm lớp U  
**Kiểm:** 12 tàu ngầm lớp U (F1 1.0)  
**Cửa sổ (rút gọn):** Bộ binh sơn chiến: các sư đoàn 6, 96 Thiết giáp: Sư đoàn xe tăng 54. Pháo binh: Các trung đoàn 116, 456. Lực lượng dự bị của Phương diện quân: Các sư đoàn bộ binh 156, 398, 400 và Sư đoàn kỵ binh 72. Hạm đội Biển Đen do Phó đô đốc F. Lực lượng tàu nổi: 2 tàu tuần dương, 6 tàu khu trục, 62 pháo hạm, 38 tàu phóng ngư lôi, 130 tàu vận tải, 200 tàu đán…

**Bài:** Trận bán đảo Kerch (1942) (11,765 âm tiết), cửa sổ ở 31% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đội Liên Xô đã đánh chiếm những thị trấn nào vào ngày 1 tháng 2?  
**Đáp án sinh:** Koktebel, Karagoz, Vladislavovka và Kyet  
**Kiểm:** Koktebel, Karagoz, Vladislavovka và Kyet (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 29 tháng 12, thêm 2.000 quân của Tập đoàn quân 51 đổ bộ lên các đầu cầu phía Bắc Kerch. Quân đội Liên Xô bắt đầu tổ chức tấn công. Lính Romania buộc phải lùi về Kerch, Bagerovo và Mayak Salyn. Ngày 28 tháng 12, đòn quyết định diễn ra tại Feodosya. Sau ba ngày lênh đênh trên biển, 3 giờ sáng ngày 28 tháng 12, đội đổ bộ đầu tiên đã tiếp cận bờ b…

**Bài:** Trận bán đảo Kerch (1942) (11,765 âm tiết), cửa sổ ở 8% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Tập đoàn quân 51 do tướng V. Lvov chỉ huy có biến chế gồm những đơn vị nào?  
**Đáp án sinh:** Quân đoàn bộ binh 9 gồm các sư đoàn bộ binh 109, 156, 279 và Lữ đoàn bộ binh nhẹ 12 Các sư đoàn bộ binh độc lập: 172, 184, 271, 320, 321. Hải quân đánh bộ: Lữ đoàn 83 Kỵ binh: Các sư đoàn 40, 42, 48  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Chernyak lần lượt chỉ huy. Bộ binh: Các sư đoàn bộ binh nhẹ 157, 236, 396, 404. Bộ binh sơn chiến: Các sư đoàn 9 Thiết giáp: Lữ đoàn xe tăng 63 Hải quân đánh bộ (tăng cường từ Hạm đội Biển Đen): Lữ đoàn 74, các tiểu đoàn 1, 2 của Lữ đoàn 9 Pháo binh: 2 trung đoàn Tập đoàn quân 51 do tướng V. Lvov chỉ huy, biến chế gồm có: Quân đoàn bộ binh 9 gồm cá…

**Bài:** Trận bán đảo Kerch (1942) (11,765 âm tiết), cửa sổ ở 26% bài  
**Trạng thái:** kept  
**Câu hỏi:** Các tàu của căn cứ hải quân Taman đã đổ lên bờ bao nhiêu quân vào trước bình minh ngày 27 tháng 12?  
**Đáp án sinh:** 13.225 quân  
**Kiểm:** 13.225 quân (F1 1.0)  
**Cửa sổ (rút gọn):** Các cuộc đổ bộ tại bán đảo Kerch Đêm 24 rạng ngày 25 tháng 12 năm 1941, các tàu vận tải của các căn cứ Novorossiysk và Tuapse đã sắp xếp đầy đủ người, vũ khí và hàng hóa lên tàu. Bốn hải đoàn vận tải chở theo Sư đoàn bộ binh 157 và Lữ đoàn xe tăng 63. Hai hải đoàn vận tải còn lại chở theo sư đoàn bộ binh 404. Do phải di chuyển xa hơn đến Feodosya, …

**Bài:** Trận bán đảo Kerch (1942) (11,765 âm tiết), cửa sổ ở 8% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Tập đoàn quân 51 do tướng V. Lvov chỉ huy có biên chế gồm những đơn vị bộ binh nhẹ nào?  
**Đáp án sinh:** Các sư đoàn bộ binh nhẹ 157, 236, 396, 404  
**Kiểm:** Lữ đoàn bộ binh nhẹ 12 (F1 0.5)  
**Cửa sổ (rút gọn):** Bộ binh: Các sư đoàn bộ binh nhẹ 157, 236, 396, 404. Bộ binh sơn chiến: Các sư đoàn 9 Thiết giáp: Lữ đoàn xe tăng 63 Hải quân đánh bộ (tăng cường từ Hạm đội Biển Đen): Lữ đoàn 74, các tiểu đoàn 1, 2 của Lữ đoàn 9 Pháo binh: 2 trung đoàn Tập đoàn quân 51 do tướng V. Lvov chỉ huy, biến chế gồm có: Quân đoàn bộ binh 9 gồm các sư đoàn bộ binh 109, 156,…

**Bài:** Trận bán đảo Kerch (1942) (11,765 âm tiết), cửa sổ ở 77% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo đánh giá của D. Mekhlis tại Hội nghị quân sự cấp cao tháng 5 năm 1942, tư lệnh Phương diện quân Krym được mô tả là một kẻ như thế nào?  
**Đáp án sinh:** một kẻ nói dối nguy hiểm  
**Kiểm:** một kẻ nói dối nguy hiểm (F1 1.0)  
**Cửa sổ (rút gọn):** Phương pháp chỉ huy của ông này đã được đánh giá tại Hội nghị quân sự cấp cao tháng 5 năm 1942 của Đại bản doanh Liên Xô là quan liêu, giấy tờ, hình thức chủ nghĩa, kiêu ngạo và bất tuân thượng lệnh. Khi đánh giá Tư lệnh phương diện quân D. Mekhlis không tiếc lời chê bai ông này là con người "tẻ nhạt", "lười thâm nhập thực tế", "không quan tâm đến …

**Bài:** Trận bán đảo Kerch (1942) (11,765 âm tiết), cửa sổ ở 36% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Erich von Manstein lý giải việc điều chủ lực Tập đoàn quân 11 sang hướng Kerch là do sự kiện gì xảy ra vào ngày 1 tháng 1 năm 1942?  
**Đáp án sinh:** Không quân Liên Xô tổ chức nhiều trận oanh tạc xuống các sân bay Sem Kolodezey và Vladislavovka, cắt đứt tuyến đường hàng không cuối cùng của Quân đoàn bộ binh 42 (Đức)  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Sư đoàn sơn chiến Romania tại Kol Taky (Zavitne) và Mareevka, phía Nam Eltigen cũng bỏ chạy về Marfovka để tránh bị bao vây. Quân đoàn bộ binh 42 (Đức) được tách thành ba cụm quân rút lui theo ba hướng. Sư đoàn bộ binh 46 (Đức) và Sư đoàn sơn chiến 1 Romania từ Marfovka rút theo đường bộ về Vladislavovka. Sư đoàn bộ binh 73 rút theo đường sắt từ Ke…

**Bài:** Chiến dịch tấn công Novgorod-Luga (9,769 âm tiết), cửa sổ ở 64% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân Đức trong vòng vây đã bỏ lại những loại khí tài nào khi tổ chức tấn công nhằm phá vòng vây chạy về Strugi Krasniye?  
**Đáp án sinh:** xe tăng và đại bác  
**Kiểm:** xe tăng và đại bác (F1 1.0)  
**Cửa sổ (rút gọn):** Một phần của sư đoàn bộ binh số 58 (Đức) bị bao vây. Quân Đức vội vã tung vào trận địa sư đoàn bộ binh thuộc không quân số 13 và một phần sư đoàn thiết giáp số 12 để cứu vãn tình hình nhưng các lực lượng này đã bị đánh bại với tổn thất hết sức nặng nề. Trung đoàn bộ binh ném lựu thuộc sư đoàn thiết giáp số 12 cũng bị lọt vào vòng vây. Ngày 13 tháng…

**Bài:** Chiến dịch tấn công Novgorod-Luga (9,769 âm tiết), cửa sổ ở 80% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tân tư lệnh Cụm Tập đoàn quân Bắc vẫn tin tưởng có thể giữ vững phòng tuyến giữa hồ Ilmen và hồ Chudsko?  
**Đáp án sinh:** Walter Model  
**Kiểm:** Walter Model (F1 1.0)  
**Cửa sổ (rút gọn):** Quân đội Liên Xô đã không thành công trong việc bao vây quân Đức ở Luga và cả ở phía Tây Nam hồ Ilmen, tuy nhiên tình hình của Tập đoàn quân số 18 (Đức) vẫn hết sức nguy hiểm và bắt buộc phải rút lui để bảo toàn lực lượng. Cho đến cuối cùng, tân tư lệnh Cụm Tập đoàn quân Bắc Walter Model vẫn tin tưởng rằng có thể giữ vững phòng tuyến giữa hồ Ilmen …

**Bài:** Chiến dịch tấn công Novgorod-Luga (9,769 âm tiết), cửa sổ ở 33% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sư đoàn bộ binh số 212 của Đức có nhiệm vụ bảo vệ cho quân đoàn nào đang rút lui tại Mga?  
**Đáp án sinh:** quân đoàn số 26  
**Kiểm:** quân đoàn số 26 (F1 1.0)  
**Cửa sổ (rút gọn):** Cho đến chiều ngày 21 tháng 1, Mga được giải phóng và sau đó quân đội Liên Xô đã giành lại quyền kiểm soát tuyến đường sắt Kirov. Tuy nhiên, trong những ngày sau đó các đợt tiến công của quân đội Liên Xô không được thuận lợi như thế. Sư đoàn bộ binh số 212 (Đức) - lực lượng cản hậu tại Mga có nhiệm vụ bảo vệ cho quân đoàn số 26 đang rút lui - đã ch…

**Bài:** Chiến dịch tấn công Novgorod-Luga (9,769 âm tiết), cửa sổ ở 11% bài  
**Trạng thái:** kept  
**Câu hỏi:** Đòn tấn công chính của Phương diện quân Volkhov trong kế hoạch tháng 9 năm 1943 do đơn vị nào thực hiện?  
**Đáp án sinh:** Tập đoàn quân số 59  
**Kiểm:** Tập đoàn quân số 59 (F1 1.0)  
**Cửa sổ (rút gọn):** Vào tháng 9 năm 1943, hội đồng quân sự của các Phương diện quân Leningrad và Volkhov đã trình lên Đại bản doanh Bộ Tổng tư lệnh Tối cao Liên Xô (STAVKA) kế hoạch và một cuộc tấn công quy mô lớn do hai phương diện quân này cùng phối hợp thực hiện, với mục tiêu là đánh bại chủ lực của Tập đoàn quân số 18 (Đức) và phá giải hoàn toàn sự uy hiếp của quâ…

**Bài:** Chiến dịch tấn công Novgorod-Luga (9,769 âm tiết), cửa sổ ở 92% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo nghiên cứu thống kê "Nga và Liên Xô trong các cuộc chiến tranh của thế kỷ 20", thương vong của Phương diện quân Volkhov trong chiến dịch này bao gồm bao nhiêu người chết và mất tích?  
**Đáp án sinh:** 12.011 chết và mất tích  
**Kiểm:** 12.011 chết và mất tích (F1 1.0)  
**Cửa sổ (rút gọn):** Quan trọng hơn, quân đội Liên Xô đã giành lại quyền kiểm soát nhiều tuyến giao thông đường sắt có tầm quan trọng chiến lược như tuyến đường sắt Kirov và đường sắt Tháng Mười. Không lâu sau đó, 7 tuyến đường sắt từ Leningrad sẽ được tái khởi động: ở Vologda, Rybinsk, Moskva, Novgorod, Batyetskiy, Luga và Ust-Luga. Theo nghiên cứu thống kê "Nga và Li…

**Bài:** Chiến dịch tấn công Novgorod-Luga (9,769 âm tiết), cửa sổ ở 86% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo hồi ký của Đại tướng S. Shtemenko, quyết định giải tán Phương diện quân Volkhov được ông đánh giá như thế nào?  
**Đáp án sinh:** một sai lầm  
**Kiểm:** là một sai lầm (F1 0.86)  
**Cửa sổ (rút gọn):** Trong hồi ký của mình, Đại tướng S. Shtemenko - đại diện Ban tham mưu của Phương diện quân Baltic 2 - đã cho rằng quyết định giải tán Phương diện quân Volkhov là một sai lầm: Hơn hai tháng sau, vào ngày 18 tháng 4 năm 1944, quân đội Liên Xô đã cho thành lập Phương diện quân Baltic 3, với lực lượng bao gồm các Tập đoàn quân số 42, 54, 67 của Phương …

**Bài:** Chiến dịch tấn công Novgorod-Luga (9,769 âm tiết), cửa sổ ở 7% bài  
**Trạng thái:** kept  
**Câu hỏi:** Phương diện quân Volkhov có bao nhiêu binh sĩ và sĩ quan tính đến đầu chiến dịch?  
**Đáp án sinh:** 260.000 binh sĩ và sĩ quan  
**Kiểm:** 260.000 binh sĩ và sĩ quan (F1 1.0)  
**Cửa sổ (rút gọn):** Tập đoàn quân số 42 (thượng tướng I. Tập đoàn quân số 67 (trung tướng V. Tập đoàn quân không quân số 13 (thượng tướng không quân S. Đầu năm 1944, phương diện quân Volkhov đóng quân theo một tuyến kéo dài từ Gontovoy Lipki đến Lezno, xa hơn nữa là từ sông Volkhov đến hồ Ilmen. Đồng thời, họ cũng chống giữ một đầu cầu vượt sông Volkhov trong khu vực …

**Bài:** Chiến dịch tấn công Novgorod-Luga (9,769 âm tiết), cửa sổ ở 18% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trung tướng pháo binh nào chỉ huy Tập đoàn quân số 16?  
**Đáp án sinh:** Christian Hansen  
**Kiểm:** Christian Hansen (F1 1.0)  
**Cửa sổ (rút gọn):** Tập đoàn quân số 16 (trung tướng pháo binh Christian Hansen) Tập đoàn quân không quân số 1 (tướng Kurt Pflyugbeyl) Chong mặt đối diện với phương diện quân Volkhov tại đây là một phần Tập đoàn quân số 18 của Đức, bao gồm 3 sư đoàn bộ binh thuộc không quân, 6 sư đoàn bộ binh và 3 lữ đoàn bộ binh thuộc các quân đoàn số 38, 26, 28. Tại đây, quân Đức đã…

**Bài:** Con đường ảo mộng (18,032 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, Adam tìm đến đâu sau khi bị vợ tống ra khỏi căn biệt thự cao cấp trên đỉnh Hollywood?  
**Đáp án sinh:** một nhà nghỉ rẻ tiền  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Tôi nghĩ anh ta là kiểu người mà khán giả hay nói 'Tôi khá giống anh bây giờ. Tôi không hiểu tại sao anh phải chịu nỗi đau như vậy'". Sau khi bị tước mất vai trò sáng tạo trong phim, Adam còn chịu thêm một vố khác nữa khi cô vợ cắm sừng anh với một kẻ dọn bể bơi (Billy Ray Cyrus đóng) và tống anh ra khỏi căn biệt thự cao cấp trên đỉnh Hollywood. Kh…

**Bài:** Con đường ảo mộng (18,032 âm tiết), cửa sổ ở 34% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo nhận định của cây bút Michael Wilmington trên tờ The Chicago Tribune, Mulholland Drive được ví von là một cơn gì?  
**Đáp án sinh:** ác mộng  
**Kiểm:** cơn ác mộng (F1 0.8)  
**Cửa sổ (rút gọn):** Cô ấy cần Betty che chở. Betty lấy cớ đó để điều khiển Rita như một con búp bê. Rita là tưởng tượng của Betty về người mà cô ấy muốn Camilla trở thành". Watts còn chia sẻ thêm rằng những trải nghiệm ban đầu của cô ở Hollywood cũng giống hệt như những gì Diane từng trải qua. Cụ thể, cô đã chịu đựng một vài thất bại trong nghề, thử những vai diễn chẳ…

**Bài:** Con đường ảo mộng (18,032 âm tiết), cửa sổ ở 44% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Gregory Weight cho rằng David Lynch đã phô bày nhiều hơn mức cần thiết điều gì?  
**Đáp án sinh:** cái bộ mặt mà ông ấy tin chỉ có thể ngự trị điều dối trá và xấu xa  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Nhà phê bình Gregory Weight cảnh báo người xem về cách giải thích có phần cay độc về nhiều sự kiện xảy ra trong phim, cho rằng Lynch đã phô bày nhiều hơn mức cần thiết "cái bộ mặt mà ông ấy tin chỉ có thể ngự trị điều dối trá và xấu xa". Mặc dù vậy, dưới quan điểm của Weight, bất chấp những tuyên bố về sự thao túng, lừa gạt, dối trá mà Lynch gán ch…

**Bài:** Con đường ảo mộng (18,032 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** kept  
**Câu hỏi:** Todd McGowan cho rằng phần đầu phim có thể cắt nghĩa thành tưởng tượng của nhân vật nào cho đến khi Diane Selwyn lộ diện?  
**Đáp án sinh:** Rita  
**Kiểm:** Rita (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, Todd McGowan (tác giả của một quyển sách chuyên bàn về những chủ đề trong phim của Lynch) lại cho rằng phần đầu phim có thể cắt nghĩa thành tưởng tượng của Rita, cho đến khi nhân vật chủ chốt Diane Selwyn lộ diện. Về cơ bản, Betty là đối tượng để Rita xua đi mối băn khoăn về việc mất trí nhớ của mình. Còn theo nhà sử học điện ảnh Steven …

**Bài:** Con đường ảo mộng (18,032 âm tiết), cửa sổ ở 80% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhạc nền của bộ phim Mulholland Drive do ai giám sát chỉ đạo?  
**Đáp án sinh:** Angelo Badalamenti  
**Kiểm:** Angelo Badalamenti (F1 1.0)  
**Cửa sổ (rút gọn):** Sau cùng, thứ duy nhất còn sót lại chỉ là sự lặng im và khó hiểu". Nhạc nền của Mulholland Drive do Angelo Badalamenti giám sát chỉ đạo. Bộ phim đã giúp ông giành lấy hai đề cử danh giá của Viện phim Mỹ (AFI) và Viện Hàn lâm Nghệ thuật Điện ảnh và Truyền hình Anh (BAFTA) cho hạng mục âm nhạc. Ngoài ra, ông cũng là người từng cộng tác với Lynch tron…

**Bài:** Con đường ảo mộng (18,032 âm tiết), cửa sổ ở 97% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quyển Lynch on Lynch được Chris Rodley chấp bút là phiên bản năm nào?  
**Đáp án sinh:** 2005  
**Kiểm:** 2005 (F1 1.0)  
**Cửa sổ (rút gọn):** Đây cũng là bộ phim thứ hai của Lynch mà công ty này phát hành (sau Eraserhead ra mắt vào tháng 9 năm 2014). Cả hai định dạng đều bao gồm các cuộc phỏng vấn gần đây với đoàn làm phim cũng như giới thiệu về phiên bản năm 2005 của quyển Lynch on Lynch do Chris Rodley chấp bút. Bản ra mắt này cũng đi kèm với trailer gốc và các phần bổ sung khác. Giải …

**Bài:** Con đường ảo mộng (18,032 âm tiết), cửa sổ ở 29% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Theo lời kể của Harring, vị đạo diễn đã quả quyết điều gì về bộ phim Mulholland Drive khi hai người đến gặp ông tại nhà riêng?  
**Đáp án sinh:** Mulholland Drive sẽ trở thành phim điện ảnh tầm cỡ quốc tế... nhưng sẽ có cảnh khỏa thân đấy  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Nữ diễn viên hăm dọa: "Nếu lần này không phải là sự thật, tôi không bảo đảm mình có thể giải quyết mọi chuyện theo cách tình cảm nhất đâu". Rồi hai người đến gặp Lynch tại nhà riêng của ông. Vị đạo diễn quả quyết: "Mulholland Drive sẽ trở thành phim điện ảnh tầm cỡ quốc tế... nhưng sẽ có cảnh khỏa thân đấy" – Harring vừa cười, vừa kể lại kỉ niệm "c…

**Bài:** Con đường ảo mộng (18,032 âm tiết), cửa sổ ở 34% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Theo nhận định của Michael Wilmington trên tờ The Chicago Tribune, Mulholland Drive được ví von là một cơn ác mộng và là bức chân dung của điều gì?  
**Đáp án sinh:** nơi giấc mơ vàng Hollywood biến thành ôi thiu  
**Kiểm:** giấc mơ vàng Hollywood biến thành ôi thiu, hóa thành món hầm độc hại của sự thù hận, đố kị, dàn xếp lôi thôi cùng sự thất bại trong việc hủy hoại tâm hồn (F1 0.33)  
**Cửa sổ (rút gọn):** Cụ thể, cô đã chịu đựng một vài thất bại trong nghề, thử những vai diễn chẳng mấy tiềm năng, gặp những kẻ bị số phận quay lưng. Hồi tưởng về khoảng thời gian đó, cô bùi ngùi nhắc lại: "Có rất nhiều hứa hẹn, nhưng rồi thực tế chẳng hề có gì xảy ra cả. Tôi rỗng túi và trở nên khá cô đơn". Viết trên tờ The Chicago Tribune, cây bút Michael Wilmington v…

**Bài:** Leopard 2 (10,182 âm tiết), cửa sổ ở 9% bài  
**Trạng thái:** answer_not_verbatim  
**Câu hỏi:** Quân đội Hà Lan đã từ chối mua xe tăng M1 do những nguyên nhân nào?  
**Đáp án sinh:** chi phí vận hành cao và việc người Mỹ từ chối bán pháo 120 mm cho Hà Lan  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Nguyên mẫu số 20 được trang bị với trọng lượng mô phỏng, sau đó nó được phát hiện ra rằng nguyên mẫu bằng trọng lượng của tháp pháo mà không có giáp được trang bị mô-đun, hủy bỏ hiệu lực tất cả các dữ liệu hiệu suất. Sau khi thử nghiệm so sánh các Leopard 2 nguyên mẫu này đã được trả lại Đức để đánh giá thêm, nhưng tháp pháo nguyên mẫu số 19 vẫn đư…

**Bài:** Leopard 2 (10,182 âm tiết), cửa sổ ở 24% bài  
**Trạng thái:** kept  
**Câu hỏi:** Kính ngắm chính của chiến xa được làm từ chất liệu nào và tích hợp loại laser trạng thái rắn nào?  
**Đáp án sinh:** Neodymium tích hợp Yttrium Aluminium Garnet (Nd: YAG) laser trạng thái rắn  
**Kiểm:** Neodymium tích hợp Yttrium Aluminium Garnet (Nd: YAG) laser trạng thái rắn (F1 1.0)  
**Cửa sổ (rút gọn):** Kính ngắm chính làm từ Neodymium tích hợp Yttrium Aluminium Garnet (Nd: YAG) laser trạng thái rắn rangefinder và 120 phần tử cadmium thủy ngân telluride, CdHgTe (còn được gọi là CMT) kính ngắm nhiệt Zeiss thuộc bộ phận kiểm soát hỏa lực của chiến xa. Một kính viễn vọng phụ trợ 8x FERO-Z18 cũng được gắn đồng trục cho các xạ thủ. EMES-15 gồm 2 kênh q…

**Bài:** Leopard 2 (10,182 âm tiết), cửa sổ ở 25% bài  
**Trạng thái:** kept  
**Câu hỏi:** Kính tiềm vọng độc lập của chỉ huy trên hệ thống EMES-15 là loại nào?  
**Đáp án sinh:** Rheinmetall Zeiss PERI-R 17 A2  
**Kiểm:** Rheinmetall Zeiss PERI-R 17 A2 (F1 1.0)  
**Cửa sổ (rút gọn):** Một kính viễn vọng phụ trợ 8x FERO-Z18 cũng được gắn đồng trục cho các xạ thủ. EMES-15 gồm 2 kênh quang học: ban ngày và ban đêm. Kính ngắm ban đêm bao gồm camera ảnh nhiệt với độ phóng đại 4x hoặc 12x. Kính ngắm ban ngày thì chỉ có độ phóng đại cố định là 12x, do vậy nhược điểm của kênh ngắm ban ngày là trường nhìn rất hẹp, nếu mục tiêu di động ở …

**Bài:** Leopard 2 (10,182 âm tiết), cửa sổ ở 52% bài  
**Trạng thái:** kept  
**Câu hỏi:** Pz 87 WE được lên kế hoạch sửa đổi và nâng cấp từ loại chiến xa nào?  
**Đáp án sinh:** Pz 87 của Thụy Sĩ  
**Kiểm:** Pz 87 của Thụy Sĩ (F1 1.0)  
**Cửa sổ (rút gọn):** Áo (114 chiếc), Canada (107 chiếc), Chile (140 chiếc), Đan Mạch (51 chiếc), Phần Lan (139 chiếc), Hy Lạp (183 chiếc), Na Uy (52 chiếc), Ba Lan (128 chiếc), Bồ Đào Nha (37 chiếc), Singapore (96 chiếc) Tây Ban Nha (108 chiếc), Thụy Điển (160 chiếc), và Thổ Nhĩ Kỳ (339 chiếc) là những nước mua chiến xa tồn kho. Pz 87 WE ('WertErhaltung), được lên kế h…

**Bài:** Leopard 2 (10,182 âm tiết), cửa sổ ở 81% bài  
**Trạng thái:** kept  
**Câu hỏi:** Panzerschnellbrücke 2 hiện đang được sử dụng bởi những quốc gia nào?  
**Đáp án sinh:** chỉ bởi Đức, Singapore và Hà Lan  
**Kiểm:** Đức, Singapore và Hà Lan (F1 0.83)  
**Cửa sổ (rút gọn):** Nó phục vụ trong các quân đội Đức (nơi mà nó được gọi Büffel hoặc Bergepanzer 3), Hà Lan (người đồng phát triển nó và gọi nó là Buffel), Áo, Canada, Hy Lạp, Singapore, Tây Ban Nha (nơi nó được gọi là Leopard 2ER Buffalo), Thụy Điển (dưới hình thức sửa đổi như Bgbv 120), và Thụy Sĩ. Panzerschnellbrücke 2 Xe này, được tạo ra bởi MAN SE, là một xe thi…

**Bài:** Leopard 2 (10,182 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chiến xa Leopard 2A5 của Đan Mạch được trang bị tấm ngụy trang Barracuda của Thụy Điển nhằm hạn chế sự hấp thụ nhiệt năng mặt trời để giảm điều gì?  
**Đáp án sinh:** hồng ngoại và nhiệt độ bên trong  
**Kiểm:** hồng ngoại và nhiệt độ bên trong (F1 1.0)  
**Cửa sổ (rút gọn):** Trong một cuộc tấn công ngày 02 tháng 11 năm 2007, một Leopard 2A6M đã gặp phải một thiết bị nổ tự tạo (IED) và sống sót mà không có thương vong: "Kíp lái của tôi tình cờ gặp IED và làm nên lịch sử", Bộ trưởng Bộ Quốc phòng Canada, Tướng Rick Hillier từ chối báo cáo rằng chiến xa Leopard 2 đã bị tấn công bởi IED, và nhấn mạnh rằng chiến xa đã được …

**Bài:** Leopard 2 (10,182 âm tiết), cửa sổ ở 18% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Leopard 2 được trang bị bao nhiêu ống bắn đạn khói Wegmann 76 mm ở mỗi bên xe?  
**Đáp án sinh:** 4  
**Kiểm:** 4 ống bắn đạn khói Wegmann 76 mm (F1 0.22)  
**Cửa sổ (rút gọn):** Trong chiến tranh Nga-Ucraina 2022, có nhiều hình ảnh và video mô tả những chiếc Leopard 2 bị phá hủy hoàn toàn do khoang đạn phía sau tháp pháo bị bắn trúng và nổ tung, có khi chỉ bởi những chiếc Flycam dân dụng gắn đầu đạn chống tăng đời cũ như RPG-7 lao từ trên cao xuống. Mỗi bên xe có 4 ống bắn đạn khói Wegmann 76 mm được gắn ở hai bên tháp phá…

**Bài:** Leopard 2 (10,182 âm tiết), cửa sổ ở 91% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đội Phần Lan ban đầu mua bao nhiêu chiếc Leopard 2A4 từ kho hàng tồn của Đức vào năm 2003?  
**Đáp án sinh:** 124 chiếc 2A4  
**Kiểm:** 124 chiếc (F1 0.8)  
**Cửa sổ (rút gọn):** : Quân đội Phần Lan ban đầu mua 124 chiếc 2A4 từ kho hàng tồn của Đức vào năm 2003. 20 đã chuyển đổi thành xe lắp đặt cầu, chiến xa kỹ thuật. 12 chiến xa đã được tháo rời để sử dụng như xe dự bị, để lại 92 chiến xa hoạt động. Trong năm 2009 quân đội Phần Lan đã mua 15 chiếc Leopard 2A4 của Đức cho dự bị thay thế lực lượng chiến xa hiện có Finland c…

**Bài:** Cây trồng biến đổi gen (10,521 âm tiết), cửa sổ ở 80% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo ví dụ được nêu, tất cả cá hồi biến đổi gen được nuôi làm thực phẩm đều là cá cái, tam bội và có đặc điểm gì về mặt sinh sản?  
**Đáp án sinh:** 99% là vô sinh về mặt sinh sản  
**Kiểm:** 99% là vô sinh về mặt sinh sản (F1 1.0)  
**Cửa sổ (rút gọn):** Để giải quyết một số mối lo ngại này, một số GMO đã được phát triển với các đặc điểm để giúp kiểm soát sự lan rộng của chúng. Ví dụ: để ngăn cá hồi biến đổi gen vô tình sinh sản với cá hồi hoang dã, tất cả cá được nuôi làm thực phẩm đều là cá cái, tam bội, 99% là vô sinh về mặt sinh sản và được nuôi ở những khu vực mà cá hồi sổng chuồng sẽ không th…

**Bài:** Cây trồng biến đổi gen (10,521 âm tiết), cửa sổ ở 32% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Cơ quan nào đã thực hiện đánh giá lợi ích khoa học cho các GMO được phê duyệt tại châu Âu?  
**Đáp án sinh:** Cơ quan an toàn thực phẩm châu Âu (EFSA- the European Food Safety Authority)  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Hơn 90% bông BĐG được trồng tại Mỹ, Argentina, Ấn Độ, Paraguay, Pakistan, Trung Quốc, Mexico, Nam Phi và Australia. Hoa Kỳ và Canada trồng hạt cải dầu BĐG với tỷ lệ ứng dụng là 90%. Quan trọng hơn, các quốc gia này cũng là cũng là nơi xuất khẩu thực phẩm chính tới các khu vực của thế giới, bao gồm các nước đang phát triển lớn. Liên minh châu Âu vốn…

**Bài:** Cây trồng biến đổi gen (10,521 âm tiết), cửa sổ ở 2% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cây trồng biến đổi gen đầu tiên được phê chuẩn bán ở Mỹ vào năm 1994 là loại cây nào?  
**Đáp án sinh:** cà chua FlavrSavr  
**Kiểm:** cà chua FlavrSavr (F1 1.0)  
**Cửa sổ (rút gọn):** Dưới tác động của các nhân tố gây đột biến, vật chất di truyền được biến đổi theo hai hướng: thêm đoạn hay bớt đoạn. Như vậy, quá trình thêm đoạn nhờ chuyển gen cũng tương tự như quá trình thêm đoạn DNA trong đột biến tự nhiên. Tuy nhiên, hai quá trình này có nhiều điểm khác nhau: Nếu quá trình chọn lọc tự nhiên chỉ giữ lại những biến dị có lợi cho…

**Bài:** Cây trồng biến đổi gen (10,521 âm tiết), cửa sổ ở 86% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thuật ngữ nào thường được sử dụng hoán đổi với 'biến đổi khí hậu' để chỉ những thay đổi lớn và dài hạn của khí hậu trên trái đất?  
**Đáp án sinh:** nóng lên trên toàn cầu  
**Kiểm:** nóng lên trên toàn cầu (F1 1.0)  
**Cửa sổ (rút gọn):** Có sự khác biệt lớn trong sự chấp nhận của người tiêu dùng đối với GMO, người châu Âu có nhiều khả năng nhìn nhận thực phẩm biến đổi gen một cách tiêu cực hơn so với người Bắc Mỹ. GMOs xuất hiện khi niềm tin của công chúng vào an toàn thực phẩm đang suy giảm, do các mối đe dọa thực phẩm gần đây như Bệnh bò điên và các vụ bê bối khác liên quan đến q…

**Bài:** Cây trồng biến đổi gen (10,521 âm tiết), cửa sổ ở 74% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Các chuyên gia CNSH hiện nay đang cố gắng làm gì để giảm thiểu rủi ro và theo dõi các thử nghiệm cây trồng biến đổi gen?  
**Đáp án sinh:** giảm thiểu các rủi ro nêu trên và theo dõi cẩn thận các thử nghiệm cây trồng biến đổi gen trong phòng thí nghiệm, cũng như ngoài đồng ruộng trước khi đưa ra thị trường thương mại  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Tuy nhiên, khả năng xảy ra điều này là vô cùng nhỏ. Hiện nay, các chuyên gia CNSH đang cố gắng giảm thiểu các rủi ro nêu trên và theo dõi cẩn thận các thử nghiệm cây trồng biến đổi gen trong phòng thí nghiệm, cũng như ngoài đồng ruộng trước khi đưa ra thị trường thương mại. Nếu được thiết kế và sử dụng đúng phương pháp thì có thể quản lý được các n…

**Bài:** Cây trồng biến đổi gen (10,521 âm tiết), cửa sổ ở 93% bài  
**Trạng thái:** kept  
**Câu hỏi:** Khuẩn Bacillus thuringiensis (Bt) là vi sinh vật phổ biến trong đất được sử dụng trong loại thuốc trừ sâu nào?  
**Đáp án sinh:** thuốc trừ sâu sinh học  
**Kiểm:** thuốc trừ sâu sinh học (F1 1.0)  
**Cửa sổ (rút gọn):** Kiểu gen: Đặc tính gen của một cá nhân. Kiểu gen thường là một bằng chứng của các tính cách bên ngoài, nhưng cũng có thể được phản ánh theo các cách hóa sinh tinh vi hơn, không phải là bằng chứng có thể nhìn thấy được. Khuẩn bacillusthuringiensis(Bt): Một vi sinh vật phổ biến trong đất có trong thuốc trừ sâu sinh học do nông dân sử dụng, gồm sản xu…

**Bài:** Cây trồng biến đổi gen (10,521 âm tiết), cửa sổ ở 57% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo báo cáo của PG Economics, từ năm 1996 đến 2016 cây trồng BĐG đã mang về bao nhiêu giá trị kinh tế?  
**Đáp án sinh:** 186,1 tỷ đô la  
**Kiểm:** 186,1 tỷ đô la (F1 1.0)  
**Cửa sổ (rút gọn):** Báo cáo năm 2017 của ISAAA cũng cho thấy có nhiều hơn những sản phẩm CNSH được thương mại hóa với những lợi ích trực tiếp đối với người tiêu dùng. Hai thế hệ khoai tây Innate®  đã được cấp phép tại Mỹ và Canada: một với tính trạng giảm thâm và chống đốm nâu cùng hàm lượng acrylamide thấp, và một với các tính trạng nói trên kết hợp cùng mức độ đường…

**Bài:** Cây trồng biến đổi gen (10,521 âm tiết), cửa sổ ở 65% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo kết quả của dự án, tính đến thời điểm hiện tại, có bằng chứng khoa học nào cho thấy mối liên hệ giữa sinh vật BĐG với những rủi ro lớn hơn đối với môi trường và sự an toàn của thực phẩm, thức ăn chăn nuôi so với các sinh vật và cây trồng truyền thống không?  
**Đáp án sinh:** KHÔNG có bất cứ bằng chứng khoa học  
**Kiểm:** KHÔNG có bất cứ bằng chứng khoa học (F1 1.0)  
**Cửa sổ (rút gọn):** Theo kết quả của dự án, tính đến thời điểm hiện tại, KHÔNG có bất cứ bằng chứng khoa học cho thấy mối liên hệ giữa sinh vật BĐG với những rủi ro lớn hơn đối với môi trường, và sự an toàn của thực phẩm, thức ăn chăn nuôi so với các sinh vật và cây trồng truyền thống. Vào năm 2016, hơn 100 học giả đoạt giải Nobel đã cùng ký bức thư ngỏ kêu gọi Tổ chứ…

**Bài:** Rượu vang trắng (8,975 âm tiết), cửa sổ ở 57% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quá trình lên men malolactic chuyển đổi axit malic thành chất gì?  
**Đáp án sinh:** axit lactic  
**Kiểm:** axit lactic (F1 1.0)  
**Cửa sổ (rút gọn):** Việc sử dụng thêm men được lựa chọn cho những điều kiện làm việc khó khăn này trở nên rất quan trọng. Ngược lại, một số nhà sản xuất trồng nho của họ theo phương pháp hữu cơ hoặc sinh học: cặn có chất lượng tốt mà không có hóa chất tổng hợp gây hại cho men nên chúng được giữ lại trong rượu. Độ đục của dịch nho đảm bảo cung cấp đủ men và quá trình l…

**Bài:** Rượu vang trắng (8,975 âm tiết), cửa sổ ở 37% bài  
**Trạng thái:** kept  
**Câu hỏi:** Những quả nho có màu được gọi là gì trong quá trình sản xuất rượu vang trắng?  
**Đáp án sinh:** Teinturier  
**Kiểm:** Teinturier (F1 1.0)  
**Cửa sổ (rút gọn):** Ngoài ra, rượu vang trắng cũng được sản xuất trên đất có lớp đất nền đá vôi như đá phấn của vùng sản xuất rượu Champagne hoặc đá vôi dưới lớp đá mác silic của Chassagne-Montrachet tạo thành phông nền cho một số loại rượu vang uy tín nhất thế giới. Việc sản xuất rượu vang trắng về cơ bản tương tự như sản xuất rượu vang đỏ, mặc dù có một số chi tiết …

**Bài:** Rượu vang trắng (8,975 âm tiết), cửa sổ ở 23% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Loại rượu vang nào được Dom Perignon tạo ra và trở nên huyền thoại?  
**Đáp án sinh:** rượu sâm banh  
**Kiểm:** rượu sâm banh huyền thoại (F1 0.75)  
**Cửa sổ (rút gọn):** Những nỗ lực bắt chước đều không thành công và việc sử dụng nấm mốc quý vẫn là một bí mật. Mãi đến 120 năm sau, một phương pháp thu hoạch rất muộn mới được thử nghiệm trên các bờ sông Rhine dốc. Việc sử dụng nó ở Sauternes đã được chứng thực vào năm 1836 tại Château La Tour Blanche nhưng vào thời điểm đó, việc thu hoạch rất muộn đã cho ra một loại …

**Bài:** Rượu vang trắng (8,975 âm tiết), cửa sổ ở 83% bài  
**Trạng thái:** kept  
**Câu hỏi:** Loại rượu vang nào được khuyến nghị khi kết hợp với pho mát mốc xanh?  
**Đáp án sinh:** Rượu vang cường hóa  
**Kiểm:** Rượu vang cường hóa (F1 1.0)  
**Cửa sổ (rút gọn):** Rượu vang thơm, chẳng hạn như Gewurztraminer và một số loại rượu vang sủi bọt hỗ trợ hương vị mạnh mẽ của pho mát vỏ rửa (Maroilles, Epoisses, Munster, v.v.). Rượu vang trắng trung tính (Castilla-La Mancha, Italian Trebbiano) rất phù hợp với pho mát cừu và cũng có Manchego và pecorino romano cho một chút cay. Pho mát ép chín yêu cầu một loại rượu v…

**Bài:** Rượu vang trắng (8,975 âm tiết), cửa sổ ở 2% bài  
**Trạng thái:** kept  
**Câu hỏi:** Rượu vang trắng khô được làm bằng cách nào?  
**Đáp án sinh:** lên men toàn bộ lượng đường trong nước ép nho  
**Kiểm:** lên men toàn bộ lượng đường trong nước ép nho (F1 1.0)  
**Cửa sổ (rút gọn):** Rượu vang trắng khô là loại phổ biến nhất, được làm bằng cách lên men toàn bộ lượng đường trong nước ép nho. Rượu vang trắng ngọt được làm bằng cách dừng quá trình lên men trước khi tất cả đường được chuyển hóa thành rượu. Có một số cách để làm điều này, chẳng hạn như để nho chín lâu hơn trên cây, phơi khô nho hoặc sử dụng một loại nấm mốc đặc biệt…

**Bài:** Rượu vang trắng (8,975 âm tiết), cửa sổ ở 68% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quá trình lão hóa trong thùng gỗ sồi tạo ra những hương thơm nào cho rượu vang?  
**Đáp án sinh:** vani, bơ, bánh mì brioche, bánh nướng, caramel  
**Kiểm:** vani, bơ, bánh mì brioche, bánh nướng, caramel (F1 1.0)  
**Cửa sổ (rút gọn):** Trái cây nhiệt đới cũng có mặt: dứa, xoài và vải thiều. Rõ ràng là bảng hương thơm bao gồm các hương vị nấu chín này: táo, mứt, trái cây kẹo, v.v. Rượu vang trắng cũng có thể truyền tải hương thơm hoa của cây keo, kim ngân, cỏ roi ngựa, hoa violet, v.v. (Hương của mật ong cũng có thể được đồng hóa). Quá trình lão hóa cũng mang lại những hương vị kh…

**Bài:** Rượu vang trắng (8,975 âm tiết), cửa sổ ở 12% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cảng nào đã đặt tên cho giống nho Malvasia?  
**Đáp án sinh:** Monemvasia  
**Kiểm:** Monemvasia (F1 1.0)  
**Cửa sổ (rút gọn):** Diện tích trồng nho ở Trung Âu đã lên tới 100.000 ha, gấp 3,5 lần diện tích vào những năm 1990. Từ thế kỷ 13, thương nhân đã phân biệt vinum hunicum (rượu của người Hun), loại rượu được dân thường uống, với vinum francium (rượu của người Frank), loại rượu dành cho tầng lớp quý tộc giàu có. Nho Riesling và Sylvaner đã được biết đến từ cuối thời Trun…

**Bài:** Rượu vang trắng (8,975 âm tiết), cửa sổ ở 49% bài  
**Trạng thái:** kept  
**Câu hỏi:** Bentonite đóng vai trò gì trong quá trình lắng các colloid?  
**Đáp án sinh:** chất dằn cơ học  
**Kiểm:** chất dằn cơ học (F1 1.0)  
**Cửa sổ (rút gọn):** Các hạt lơ lửng lắng xuống đáy bể. Điều này được tạo điều kiện thuận lợi bằng việc bổ sung các enzym pectolytic, là những carbon chuỗi dài được tạo thành từ các hợp chất pectic. Các pectic này làm tăng độ nhớt của nước ép, cắt các hạt lơ lửng thành các chuỗi ngắn hơn và đẩy nhanh quá trình kết tủa. Cần làm lạnh dịch nho: nếu quá trình lên men bắt đ…

**Bài:** Jimmy Page (11,578 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Biểu tượng Zoso trên áo của Jimmy Page được lấy từ cuốn sách nào?  
**Đáp án sinh:** Ars Magica Arteficii  
**Kiểm:** Ars Magica Arteficii (1557) của Gerolamo Cardano (F1 0.6)  
**Cửa sổ (rút gọn):** Cám ơn anh nhiều."Năm 2003, trả lời phỏng vấn với tạp chí Q, Page trả lời câu hỏi rằng liệu ông có ý tiếc nuối khi từng nghiệp ngập heroin và cocaine: "Tôi không hề thấy tiếc về điều đó, vì khi tôi cần tập trung, tôi vẫn luôn tập trung. Cả Presence lẫn In Through the Out Door đều được thu trong vỏn vẹn 3 tuần, vậy nên nó chỉ được có vậy. Đáng lẽ tô…

**Bài:** Jimmy Page (11,578 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** kept  
**Câu hỏi:** Jimmy Page đã trả lời như thế nào khi Huw Wheldon hỏi về tương lai mà cậu muốn sau khi kết thúc việc đi học?  
**Đáp án sinh:** Cháu muốn làm nghiên cứu sinh  
**Kiểm:** Cháu muốn làm nghiên cứu sinh (F1 1.0)  
**Cửa sổ (rút gọn):** Ca khúc "Baby Let's Play House" của Presley thường được Page nhắc tới như là niềm cảm hứng chơi guitar của cá nhân mình. Cho dù từng được lên truyền hình trên kênh BBC1 vào năm 1957 với cây Hofner President, Page sau này vẫn nói chiếc guitar đầu tiên của ông là chiếc 1959 Futurama Grazioso, rồi sau đó là cây Fender Telecaster. Phong cách âm nhạc củ…

**Bài:** Jimmy Page (11,578 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chiếc guitar Jimmy Page 'Number Two' Les Paul được Gibson ra mắt vào tháng 12 năm 2009 là thiết kế lại từ chiếc nào mà Page sử dụng từ khoảng năm 1974?  
**Đáp án sinh:** chiếc No. 2  
**Kiểm:** chiếc No. 2 (F1 1.0)  
**Cửa sổ (rút gọn):** Gần đây, Gibson cũng cho tái sản xuất chiếc 1960 Les Paul Black Beauty – chiếc mà Page từng bị ăn cắp vào năm 1970 – với một vài cải tiến. Dòng guitar này được bày bán vào năm 2008 với 25 chiếc được Page ký tên trong tổng số 500 chiếc được sản xuất. Tháng 12 năm 2009, Gibson ra mắt dòng Jimmy Page "Number Two" Les Paul. Đây là chiếc guitar thiết kế…

**Bài:** Jimmy Page (11,578 âm tiết), cửa sổ ở 34% bài  
**Trạng thái:** kept  
**Câu hỏi:** Page đã mua lại phòng thu The Sol ở Cookham từ ai vào đầu thập niên 80?  
**Đáp án sinh:** Gus Dudgeon  
**Kiểm:** Gus Dudgeon (F1 1.0)  
**Cửa sổ (rút gọn):** Sau đó, anh chuyển sang cộng tác một vài dự án nhỏ lẻ với các ban nhạc The Firm, The Honeydrippers, một vài lần thực hiện các dự án cá nhân, trong đó có cả nhạc phim. Anh cũng bắt đầu tham gia vào nhiều hoạt động nhân đạo. Page quay trở lại sân khấu với Jeff Beck vào tháng 3 năm 1981 trong buổi diễn tại nhà hát Hammersmith Odeon. Cũng trong năm 198…

**Bài:** Jimmy Page (11,578 âm tiết), cửa sổ ở 16% bài  
**Trạng thái:** kept  
**Câu hỏi:** Album nào của John Williams mà Jimmy Page bắt đầu sáng tác?  
**Đáp án sinh:** The Maureeny Wishful Album  
**Kiểm:** The Maureeny Wishful Album (F1 1.0)  
**Cửa sổ (rút gọn):** Anh bắt đầu sáng tác trong album The Maureeny Wishful Album của John Williams cùng Big Jim Sullivan. Sau đó anh tham gia làm nghệ sĩ hợp đồng trong Sunshine Superman (1966) của Donovan, Jeune Homme (1968) và Je Suis Né Dans La Rue (1969) của Johnny Hallyday, Love Chronicles (1969) của Al Stewart và 5 ca khúc trong album đầu tay With a Little Help f…

**Bài:** Jimmy Page (11,578 âm tiết), cửa sổ ở 29% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quản lý Peter Grant đã quyết định đặt tên ban nhạc mới là gì?  
**Đáp án sinh:** Led Zeppelin  
**Kiểm:** Led Zeppelin (F1 1.0)  
**Cửa sổ (rút gọn):** Có rất nhiều nghệ sĩ tài năng quanh đây mà họ chưa được kết dính để trở thành một ban nhạc. Chìa khóa ở đây là nếu muốn tìm được ban nhạc ưng ý, nhất thiết ta cần phải đốt cháy hết tâm huyết của mình." Cuối cùng, anh chọn được ca sĩ Robert Plant và tay trống John Bonham từ nhóm Band of Joy trong khi anh đề nghị cộng tác với John Paul Jones – người …

**Bài:** Jimmy Page (11,578 âm tiết), cửa sổ ở 92% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Page, Crowley là một thiên tài bị lãng quên của thế kỷ nào?  
**Đáp án sinh:** thế kỷ 20  
**Kiểm:** thế kỷ 20 (F1 1.0)  
**Cửa sổ (rút gọn):** Cửa hàng sách đã từng cho bán một bản sao cuốn Goetia (1904) của nhà huyền bí học người Anh, Aleister Crowley. Page luôn thể hiện rõ mối quan tâm đặc biệt của mình với những ghi chép của Crowley. "Tôi nghĩ Crowley là một thiên tài bị lãng quên của thế kỷ 20, bởi vì toàn bộ sự nghiệp của ông ấy dành cho việc giải phóng con người, thực thể và cả nhữn…

**Bài:** Jimmy Page (11,578 âm tiết), cửa sổ ở 58% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chiếc guitar 1959 Fender Telecaster của Jimmy Page là quà tặng của ai?  
**Đáp án sinh:** Jeff Beck  
**Kiểm:** Jeff Beck (F1 1.0)  
**Cửa sổ (rút gọn):** Page bổ sung thêm 4 phần coil split cho humbucker để tạo thêm nhiều hiệu ứng khác, bổ sung phía dưới phần pickguard của chiếc guitar kể từ sau khi Led Zeppelin tan rã. 1971 Gibson EDS-1275 2-cần nổi tiếng của Page được chơi trong các ca khúc "Stairway to Heaven", "The Song Remains the Same", "The Rain Song", "Celebration Day" tại các buổi trình diễ…

**Bài:** Chiến dịch phản công Mozhaisk-Vyazma (11,333 âm tiết), cửa sổ ở 46% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Quân đoàn kỵ binh cận vệ 1 phải dừng lại trước tuyến phòng thủ của những đơn vị quân Đức nào khi chỉ còn cách Vyazma 30 km về phía Tây Nam?  
**Đáp án sinh:** Sư đoàn xe tăng 5 và các sư đoàn bộ binh 31 và 131  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Từ ngày 8 đến ngày 16 tháng 2, Tập đoàn quân 33 và Quân đoàn kỵ binh cận vệ 1 bắt đầu tấn công trên hướng Lyadovo (???) - Voroshyaka (???), phía Nam Vyazma. Quân Đức huy động các sư đoàn xe tăng 6, 7, Sư đoàn cơ giới 10, các sư đoàn bộ binh 137 và 403 tổ chức phản kích, đánh bật các cuộc tấn công của kỵ binh và bộ binh Liên Xô. Không có xe tăng yểm…

**Bài:** Chiến dịch phản công Mozhaisk-Vyazma (11,333 âm tiết), cửa sổ ở 79% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sư đoàn xe tăng 11 (Đức) đã kéo quân đến nơi khi trên chiến trường chỉ còn lại những gì?  
**Đáp án sinh:** hai khẩu pháo và xác chết của hơn 300 lính Đức  
**Kiểm:** hai khẩu pháo và xác chết của hơn 300 lính Đức (F1 1.0)  
**Cửa sổ (rút gọn):** Khi Sư đoàn xe tăng 11 (Đức) kéo quân đến nơi thì trên chiến trường chỉ còn lại hai khẩu pháo và xác chết của hơn 300 lính Đức. Ngày 10 tháng 6, trinh sát của Quân đoàn bộ binh 20 (Đức) phát hiện một toán quân hỗn hợp bộ binh và du kích Liên Xô dùng 10 xe bọc thép chiếm được của quân Đức đột phá qua đường sắt Smolensk - Vyazma ở phía Tây Yartsevo 5…

**Bài:** Chiến dịch phản công Mozhaisk-Vyazma (11,333 âm tiết), cửa sổ ở 37% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tiểu đoàn dù nào thuộc Lữ đoàn 201 là đơn vị duy nhất đổ bộ đúng mục tiêu và đánh chiếm cây cầu Znamenka?  
**Đáp án sinh:** Tiểu đoàn dù 2  
**Kiểm:** Tiểu đoàn dù 2 (F1 1.0)  
**Cửa sổ (rút gọn):** Chỉ có Tiểu đoàn dù 2 (Lữ đoàn 201) đổ bộ đúng mục tiêu, đánh chiếm cây cầu Znamenka và làm gián đoạn giao thông của quân Đức trên đường cao tốc Warsawa. Sư xuất hiện của quân dù phía sau lưng Tập đoàn quân 4 (Đức) đã gây ra mối lo ngại cho tướng Gotthard Heinrici. Ngày 21 tháng 1, Các sư đoàn bộ binh 56 và 216 (Đức) được điều từ Milyatino lên phía…

**Bài:** Chiến dịch phản công Mozhaisk-Vyazma (11,333 âm tiết), cửa sổ ở 87% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn kỵ binh cận vệ 1 đã thoát vây về khu vực của đơn vị nào?  
**Đáp án sinh:** Tập đoàn quân 10  
**Kiểm:** Tập đoàn quân 10 (F1 1.0)  
**Cửa sổ (rút gọn):** Việc Quân đoàn kỵ binh cận vệ 1 thoát vây về khu vực của Tập đoàn quân 10 hoàn toàn không nằm trong dự kiến ban đầu của Bộ Tư lệnh Phương diện quân Tây (Liên Xô). Quân đội Đức Quốc xã sau khi thua một trận lớn đấu tiên trước cửa ngõ Moskva đã kịp thời được củng cố lại. Đến đầu tháng 3, mặt trận cánh Nam của Cụm tập đoàn quân Trung tâm đã ổn định tr…

**Bài:** Chiến dịch phản công Mozhaisk-Vyazma (11,333 âm tiết), cửa sổ ở 46% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Quân đoàn kỵ binh cận vệ 1 phải dừng lại trước tuyến phòng thủ của những đơn vị quân Đức nào khi chỉ còn cách Vyazma 30 km về phía Tây Nam?  
**Đáp án sinh:** Sư đoàn xe tăng 5 và các sư đoàn bộ binh 31 và 131  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Ngày 17 tháng 2, Quân đoàn kỵ binh cận vệ 1 cố gắng tổ chức tấn công từ Semlevo vào Tây Nam Vyazma. Ngày 18 tháng 2, Sư đoàn kỵ binh cận vệ 1 và sư đoàn kỵ binh 41 đánh chiếm làng Stogovka (???). Ngày 19 tháng 2, bốn sư đoàn kỵ binh đã đột phá đến phía Bắc Semlevo. Ngày 20 tháng 2, kỵ binh Liên Xô phá hoại 6 đến 7 km đường sắt Smolensk - Vyazma đoạ…

**Bài:** Chiến dịch phản công Mozhaisk-Vyazma (11,333 âm tiết), cửa sổ ở 76% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lực lượng của đội quân hỗn hợp do tướng P. Belov chỉ huy đã tăng lên đến bao nhiêu người?  
**Đáp án sinh:** gần 20.000 người  
**Kiểm:** gần 20.000 người (F1 1.0)  
**Cửa sổ (rút gọn):** Belov phải rút quân về khu du kích phía nam con đường sắt Smolensk - Spas Demensk. Trên đường rút quân xuống phía nam, tướng P. Belov thu thập thêm gần 800 quân (trong đó gần một nửa đã bị thương) của các sư đoàn thuộc Tập đoàn quân 33 và liên lạc với Trung đoàn du kích Zhabo đang hoạt động tại khu vực phía Bắc Yelnya. Lực lượng của đội quân hỗn hợ…

**Bài:** Chiến dịch phản công Mozhaisk-Vyazma (11,333 âm tiết), cửa sổ ở 82% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo các thống kê chính thức, tổn thất của Phương diện quân Tây (Liên Xô) trong chiến dịch gồm bao nhiêu người chết và mất tích?  
**Đáp án sinh:** 148.940 người chết và mất tích  
**Kiểm:** 148.940 người chết và mất tích (F1 1.0)  
**Cửa sổ (rút gọn):** Trong đó có 6.000 binh sĩ và sĩ quan tử trận trong cuộc phá vây. Một số tài liệu cho rằng, Tập đoàn quân 33 (Liên Xô) chỉ còn 889 người thoát vây. Tổn thất của Phương diện quân Tây (Liên Xô) trong chiến dịch, theo các thống kê chính thức gồm 148.940 người chết và mất tích, 286.722 người bị thương.. Tổn thất của các tập đoàn đoàn quân xe tăng 3, 4 v…

**Bài:** Chiến dịch phản công Mozhaisk-Vyazma (11,333 âm tiết), cửa sổ ở 80% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Theo các thống kê chính thức, tổn thất của Phương diện quân Tây (Liên Xô) trong chiến dịch gồm bao nhiêu người chết và mất tích?  
**Đáp án sinh:** 148.940 người chết và mất tích  
**Kiểm:** 148.940 người (F1 0.5)  
**Cửa sổ (rút gọn):** P Orlov đã ngăn cản được cuộc truy đuổi của Sư đoàn xe tăng 6 (Đức) và chạy thoát về khu vực đóng quân của Tập đoàn quân xung kích 4 (Liên Xô). Trong khi đó thì đoàn quân chủ yếu của tướng P. Belov đã luồn rừng, men theo sông Desna xuống phía Nam và đột phá sang khu vực đóng quân của Tập đoàn quân 10 (Liên Xô) tại thị trấn Schelakovsk. Với sự giúp …

**Bài:** Học thuyết về nhà nước của chủ nghĩa Marx Lenin (11,351 âm tiết), cửa sổ ở 21% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà nước thực hiện quyền lực của mình trên cơ sở sức mạnh cưỡng bức của điều gì?  
**Đáp án sinh:** pháp luật  
**Kiểm:** pháp luật (F1 1.0)  
**Cửa sổ (rút gọn):** Bộ máy quyền lực đó bao gồm các đội vũ trang đặc biệt (quân đội, cảnh sát, nhà tù, v.v.) và bộ máy quản lý hành chính mà xã hội (cán bộ, công chức, viên chức, lãnh đạo, quan lại nha sai....) mà xã hội thị tộc, bộ lạc không hề biết đến trước đó. Nhà nước thực hiện quyền lực của mình trên cơ sở sức mạnh cưỡng bức của pháp luật và dùng các thiết chế (…

**Bài:** Học thuyết về nhà nước của chủ nghĩa Marx Lenin (11,351 âm tiết), cửa sổ ở 49% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Theo Chủ nghĩa Marx – Lenin, nhà nước vô sản là kiểu nhà nước thứ mấy trong lịch sử của xã hội loài người?  
**Đáp án sinh:** kiểu nhà nước cuối cùng trong lịch sử của xã hội loài người  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Theo Chủ nghĩa Marx – Lenin thì Nhà nước vô sản là một kiểu nhà nước đặc biệt trong lịch sử. Tính chất đặc biệt của nó trước hết là ở chỗ nó chỉ tồn tại trong thời kỳ quá độ lên chủ nghĩa cộng sản, nó là kiểu nhà nước cuối cùng trong lịch sử của xã hội loài người. Sự tồn tại của nhà nước vô sản trong thời kỳ quá độ này được cho là tất yếu vì trong …

**Bài:** Học thuyết về nhà nước của chủ nghĩa Marx Lenin (11,351 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Theo V. Lenin, nhiệm vụ nào được xem là bức bách và quan trọng hơn việc đập tan sự phản kháng của tư sản?  
**Đáp án sinh:** tích cực xây dựng chủ nghĩa cộng sản, sáng tạo ra những quan hệ kinh tế mới, sáng tạo ra một xã hội mới  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Đặt mối tương quan với chức năng tổ chức – xây dựng, thì chức năng trấn áp chỉ là việc quét sạch các đống rác rưởi trước khi xây dựng mà chưa phải là bản thân việc xây dựng. Ngay từ năm 1847, F. Engels đã nêu ra 12 nhiệm vụ mà giai cấp công nhân phải thực hiện sau khi giành được chính quyền, thì tất cả các nhiệm vụ đó đều trực tiếp liên quan tới tổ…

**Bài:** Học thuyết về nhà nước của chủ nghĩa Marx Lenin (11,351 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo V. Lenin, vũ khí duy nhất mà nhờ đó giai cấp vô sản có thể chiến thắng giai cấp tư sản là gì?  
**Đáp án sinh:** quản lý  
**Kiểm:** quản lý (F1 1.0)  
**Cửa sổ (rút gọn):** Đề cập chức năng tổ chức xây dựng của Nhà nước chuyên chính vô sản, V. Lenin dành sự chú ý đặc biệt cho nhiệm vụ quản lý. Sau khi giành được chính quyền, theo V. Lenin, vũ khí duy nhất mà nhờ đó giai cấp vô sản có thể chiến thắng giai cấp tư sản là quản lý. Trong nhiệm vụ quản lý toàn diện đời sống xã hội, V. Lenin xem quản lý nhà nước trong thời k…

**Bài:** Học thuyết về nhà nước của chủ nghĩa Marx Lenin (11,351 âm tiết), cửa sổ ở 13% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo bản chất, nhà nước là bộ máy quan trọng nhất của thành phần nào trong xã hội có giai cấp?  
**Đáp án sinh:** kiến trúc thượng tầng  
**Kiểm:** kiến trúc thượng tầng (F1 1.0)  
**Cửa sổ (rút gọn):** Nhà nước ra đời tựa hồ đứng ngoài xã hội, làm cho xã hội tồn tại trong vòng trật tự nhất định nhưng trên thực tế, chỉ giai cấp có thế lực nhất - giai cấp thống trị về kinh tế mới có đủ điều kiện lập ra và sử dụng bộ máy nhà nước. Nhờ có nhà nước, giai cấp này cũng trở thành giai cấp thống trị về mặt chính trị, và do đó có thêm những phương tiện mới…

**Bài:** Học thuyết về nhà nước của chủ nghĩa Marx Lenin (11,351 âm tiết), cửa sổ ở 0% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Tác phẩm nào của F. Engels phản ánh những nội dung cơ bản ban đầu về học thuyết Nhà nước của Chủ nghĩa Marx – Lenin?  
**Đáp án sinh:** Nguồn gốc của gia đình, chế độ sở hữu và của nhà nước  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Học thuyết về Nhà nước của Chủ nghĩa Marx – Lenin hay còn gọi là Lý luận về Nhà nước và Pháp luật của Chủ nghĩa Marx – Lenin là hệ thống những kiến thức của chủ nghĩa Marx – Lenin về những quy luật phát sinh, phát triển đặc thù, những đặc tính chung và biểu hiện quan trọng nhất của nhà nước nói chung và nhà nước Xã hội chủ nghĩa nói riêng. Tập trun…

**Bài:** Học thuyết về nhà nước của chủ nghĩa Marx Lenin (11,351 âm tiết), cửa sổ ở 94% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người dịch cuốn sách Nhập môn Marx của Eduardo del Rio?  
**Đáp án sinh:** Nguyễn Hà  
**Kiểm:** Nguyễn Hà (F1 1.0)  
**Cửa sổ (rút gọn):** Giáo trình lý luận Nhà nước và Pháp luật, Trường Đại học Luật Hà Nội, Nhà xuất bản Công an nhân dân, Hà Nội, năm 2008 Giáo trình Lý luận Nhà nước và Pháp luật, Trường Đại học Luật Hà Nội, Nhà xuất bản Công an nhân dân, Hà Nội, năm 2003 (bản sao) Giáo trình lịch sử Nhà nước và pháp luật Việt Nam, Trường Đại học Luật Hà Nội, nhà xuất bản Công an nhân…

**Bài:** Học thuyết về nhà nước của chủ nghĩa Marx Lenin (11,351 âm tiết), cửa sổ ở 30% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Kiểu nhà nước là khái niệm dùng để chỉ bộ máy thống trị đó thuộc về giai cấp nào, tồn tại trên cơ sở chế độ kinh tế nào, tương ứng với hình thái kinh tế-xã hội nào?  
**Đáp án sinh:** Kiểu nhà nước  
**Kiểm:** bộ máy thống trị đó thuộc về giai cấp nào, tồn tại trên cơ sở chế độ kinh tế nào, tương ứng với hình thái kinh tế-xã hội nào (F1 0.0)  
**Cửa sổ (rút gọn):** Chúng là hai mặt của một thể thống nhất. Tính chất của chức năng đối nội quyết định tính chất chức năng đối ngoại của nhà nước ngược lại tính chất và những nhu cầu của chức năng đối ngoại có tác động mạnh mẽ trở lại chức năng đối nội. Kiểu nhà nước là khái niệm dùng để chỉ bộ máy thống trị đó thuộc về giai cấp nào, tồn tại trên cơ sở chế độ kinh tế…

**Bài:** Chủ nghĩa cộng sản vô trị (12,362 âm tiết), cửa sổ ở 50% bài  
**Trạng thái:** kept  
**Câu hỏi:** FCL xuất bản tác phẩm nào vào năm 1953?  
**Đáp án sinh:** Manifeste du communisme libertaire  
**Kiểm:** Manifeste du communisme libertaire (F1 1.0)  
**Cửa sổ (rút gọn):** OPB đã thúc đẩy một động thái chứng kiến ​​FA đổi tên thành Fédération Communiste Libertaire (FCL) sau Đại hội năm 1953 tại Paris, trong khi một bài báo trên Le Libertaire ám chỉ việc chấm dứt hợp tác với Nhóm Siêu thực Pháp do André Breton lãnh đạo. Quy trình quyết định mới được thành lập dựa trên sự nhất trí: mỗi người đều có quyền phủ quyết đối …

**Bài:** Chủ nghĩa cộng sản vô trị (12,362 âm tiết), cửa sổ ở 24% bài  
**Trạng thái:** kept  
**Câu hỏi:** Giuseppe Ciancabilla đã viết tác phẩm nào?  
**Đáp án sinh:** Chống lại tổ chức  
**Kiểm:** Chống lại tổ chức (F1 1.0)  
**Cửa sổ (rút gọn):** Chủ nghĩa bất hợp pháp (Illegalism) nổi lên thành một thực tiễn và trong chủ nghĩa này "những hành động các kẻ đánh bom và sát thủ vô trị (đây là "tuyên truyền bằng hành động") và các kẻ trộm vô trị (đây là sự "giành lại của cá nhân") bày tỏ sự tuyệt vọng và sự từ chối bạo lực của họ đối với một xã hội không thể chịu nổi. Hơn nữa, họ rõ ràng là để …

**Bài:** Chủ nghĩa cộng sản vô trị (12,362 âm tiết), cửa sổ ở 36% bài  
**Trạng thái:** kept  
**Câu hỏi:** Miguel Jimenez cho rằng Platform của Dielo Truda có quá nhiều ảnh hưởng của chủ nghĩa nào?  
**Đáp án sinh:** chủ nghĩa marx  
**Kiểm:** chủ nghĩa marx (F1 1.0)  
**Cửa sổ (rút gọn):** Nhưng Malatesta, ban đầu phản đối Platform, sau này lại đồng ý với Platform. Điều này xác nhận rằng sự khác biệt ban đầu về quan điểm là do sự nhầm lẫn ngôn ngữ: "Tôi thấy mình ít nhiều đồng ý với cách họ quan niệm về tổ chức vô trị (nghĩa là quan niệm của Platform khác xa với tinh thần độc đoán mà Platform dường như đã bày tổ), và tôi xác nhận niề…

**Bài:** Chủ nghĩa cộng sản vô trị (12,362 âm tiết), cửa sổ ở 34% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Bốn nguyên tắc chính mà một tổ chức vô trị nên hoạt động dựa trên theo Cương lĩnh tổ chức của Tổng liên minh những người theo chủ nghĩa vô trị là gì?  
**Đáp án sinh:** thống nhất về tư tưởng, thống nhất về chiến thuật, hành động tập thể (collective action) và chủ nghĩa liên bang (federalism)  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Một nhóm những người vô trị Nga lưu vong đã cố gắng giải quyết và giải thích những thất bại của phong trào vô trị trong Cách mạng Nga. Họ đã viết "Cương lĩnh tổ chức của Tổng liên minh những người theo chủ nghĩa vô trị" (Organizational Platform of the General Union of Anarchists). Nói chính xác thì là do Dielo Truda viết vào năm 1926. Cuốn pamfơlê …

**Bài:** Chủ nghĩa cộng sản vô trị (12,362 âm tiết), cửa sổ ở 96% bài  
**Trạng thái:** kept  
**Câu hỏi:** Phim tài liệu ngắn giới thiệu ý tưởng cộng sản vô trị theo lời của chính Peter Kropotkin có tên là gì?  
**Đáp án sinh:** Kropotkin: The Coming Revolution  
**Kiểm:** Kropotkin: The Coming Revolution (F1 1.0)  
**Cửa sổ (rút gọn):** GLIMPSES INTO THE YEAR 2100 (50 years after the revolution) Daily life in the libertarian communist society Michael Schmidt and Lucien van der Walt. Black Flame: The Revolutionary Class Politics of Anarchism and Syndicalism. The Rise and Fall of The Green Mountain Anarchist Collective, 2015. Các văn bản về chủ nghĩa vô trị tiếng Việt tại Thư viện ả…

**Bài:** Chủ nghĩa cộng sản vô trị (12,362 âm tiết), cửa sổ ở 67% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Theo Peter Kropotkin, xu hướng tiến hóa của con người là gì?  
**Đáp án sinh:** để con người hợp tác với nhau vì lợi ích chung và sự sống còn của mọi người thay vì tồn tại như những đối thủ cạnh tranh đơn độc  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Ngoài việc tin rằng tiền thuê nhà và các khoản phí khác là bóc lột, những người cộng sản vô trị cảm thấy đây là những áp lực tùy tiện khiến mọi người thực hiện các chức năng không liên quan. Ví dụ, họ đặt câu hỏi tại sao một người phải làm việc 'X giờ' một ngày để chỉ sống ở một nơi nào đó. Vì vậy, thay vì làm việc có điều kiện vì đồng lương kiếm đ…

**Bài:** Chủ nghĩa cộng sản vô trị (12,362 âm tiết), cửa sổ ở 57% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Liên đoàn những người cộng sản vô trị (FdCA) được thành lập vào năm nào tại Ý?  
**Đáp án sinh:** 1985  
**Kiểm:** năm 1985 (F1 0.67)  
**Cửa sổ (rút gọn):** Alfredo Maria Bonanno, một nhà vô trị nổi dậy có ảnh hưởng, sẽ nổi lên từ trong các nhóm này, chịu ảnh hưởng từ hoạt động của nhà vô trị lưu vong người Tây Ban Nha José Lluis Facerías. Vào đầu những năm 70, một khuynh hướng theo chủ nghĩa cương lĩnh xuất hiện trong Liên đoàn vô trị Ý. Khuynh hướng này đã biện luận cho sự gắn kết chiến lược sâu hơn …

**Bài:** Chủ nghĩa cộng sản vô trị (12,362 âm tiết), cửa sổ ở 85% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Kropotkin, sản phẩm người lao động làm ra thuộc về ai?  
**Đáp án sinh:** tổng thể cộng đồng  
**Kiểm:** tổng thể cộng đồng (F1 1.0)  
**Cửa sổ (rút gọn):** Ngược lại, Kropotkin cho rằng sản phẩm người lao động làm ra là thuộc về tổng thể cộng đồng, không chỉ công nhân. Ông lập luận rằng vì người lao động dựa vào thành tựu và nỗ lực của hàng triệu người trước đó nên mới có thể làm ra sản phẩm, công việc của người ấy nên thuộc về cộng đồng, thay vì chỉ chính người ấy. Nói cách khác, thành quả của người …

**Bài:** Trận Wœrth (8,873 âm tiết), cửa sổ ở 78% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Theo nhà sử học quân sự Anh David J. Stone, trận chiến Wœrth-Froeschwiller là cơ hội cho hai quân đoàn nào bộc lộ năng lực trong liên minh chiến đấu với Liên bang Bắc Đức?  
**Đáp án sinh:** hai quân đoàn Bayern và Quân đoàn Baden-Württemberg  
**Kiểm:** Bayern và Quân đoàn Baden-Württemberg (F1 0.77)  
**Cửa sổ (rút gọn):** Thắng lợi này đã khai lối cho Binh đoàn 3 vượt dãy Vosges tiến về nội địa Pháp và Paris, đồng thời dọn đường cho họ đánh xuống Strasbourg – thủ phủ vùng Alsace – ở mạn nam.. Ông viết vào nhật ký của mình sau trận chiến: "Hôm nay ta đã đánh bại hoàn toàn Thống chế MacMahon, đẩy quân của ông ta vào một cuộc tháo chạy toàn diện và nhốn nháo". Không ch…

**Bài:** Trận Wœrth (8,873 âm tiết), cửa sổ ở 6% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người chỉ huy Binh đoàn số 1 trong cánh trái của quân đội Đức?  
**Đáp án sinh:** Thượng tướng Bộ binh Karl von Steinmetz  
**Kiểm:** Thượng tướng Bộ binh Karl von Steinmetz (F1 1.0)  
**Cửa sổ (rút gọn):** Cánh trái của ông gồm Binh đoàn số 1 (50.000 quân) dưới quyền Thượng tướng Bộ binh Karl von Steinmetz và Binh đoàn số 2 (134.000 quân) dưới quyền Vương tử Friedrich Karl trên mạn bắc, cánh phải gồm 125.000 quân của Binh đoàn số 3 do Thái tử Friedrich Wilhelm chỉ huy ở phía nam. Cuối ngày 3 tháng 8, Moltke đánh điện cho Friedrich Wilhelm: "Chúng tôi…

**Bài:** Trận Wœrth (8,873 âm tiết), cửa sổ ở 75% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo nhật ký của Thái tử Phổ, ông đã đánh bại ai trong trận Wœrth?  
**Đáp án sinh:** Thống chế MacMahon  
**Kiểm:** Thống chế MacMahon (F1 1.0)  
**Cửa sổ (rút gọn):** Số quân Pháp bị giết và bị thương lên đến 11.000 người và phần lớn con số này là do pháo binh Đức gây nên. Hãi hùng trước sự xuất hiện của quân Đức từ các bên sườn và đằng sau, 9.212 sĩ quan và binh lính Pháp còn lành lặn đã nộp mình cho quân Đức (trước sự phấn khởi của các binh sĩ Đức, nhiều tù binh Pháp sau trận đánh đã gọi Napoléon III là "mụ gi…

**Bài:** Trận Wœrth (8,873 âm tiết), cửa sổ ở 79% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Theo nhà sử học quân sự Anh David J. Stone, trận chiến Wœrth-Froeschwiller là cơ hội cho hai quân đoàn nào bộc lộ năng lực trong liên minh chiến đấu với Liên bang Bắc Đức?  
**Đáp án sinh:** hai quân đoàn Bayern và Quân đoàn Baden-Württemberg  
**Kiểm:** Bayern và Quân đoàn Baden-Württemberg (F1 0.77)  
**Cửa sổ (rút gọn):** Không chỉ bị quân chủ lực của Friedrich Wilhelm đuổi khỏi những đỉnh núi dễ cố thủ của dãy Vosges và cô lập khỏi quân chủ lực Binh đoàn sông Rhin, Quân đoàn I phải bỏ lại mọi lều trại, gà mèn, bếp dã chiến, nồi niêu, thực phẩm, đạn súng trường, đạn đại bác trong cuộc bỏ chạy tán loạn của mình và hoàn toàn không còn khả năng chiến đấu trong suốt tuầ…

**Bài:** Trận Wœrth (8,873 âm tiết), cửa sổ ở 8% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tướng nào đã chỉ huy Sư đoàn 2 Pháp trong trận đánh tại thị trấn biên ải Wissembourg?  
**Đáp án sinh:** tướng Abel Douay  
**Kiểm:** Abel Douay (F1 0.8)  
**Cửa sổ (rút gọn):** Trong trận đánh lớn đầu tiên của cuộc chiến, 50.000 quân Đức thuộc các Quân đoàn V, XI (Phổ) và II (Bayern) đã đè bẹp hàng phòng thủ của Sư đoàn 2 – đơn vị đi đầu của Quân đoàn I – gồm 8.600 quân Pháp do tướng Abel Douay chỉ huy ở thị trấn biên ải Wissembourg. Bản thân Douay bị thiệt mạng khi một xe đạn phát nổ và người kế nhiệm ông là tướng Jean P…

**Bài:** Trận Wœrth (8,873 âm tiết), cửa sổ ở 31% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Kirchbach đã bị thương trong trận nào?  
**Đáp án sinh:** Wissembourg  
**Kiểm:** trận Wissembourg (F1 0.67)  
**Cửa sổ (rút gọn):** Được nhìn nhận là một trong những vị tướng táo bạo nhất của quân đội Phổ từ cuộc chiến tranh với Áo năm 1866, Kirchbach đã bị thương trong trận Wissembourg và đến giờ vẫn chưa thể cưỡi ngựa. Nhưng điều đó vẫn không thể ngăn cản ông phát lệnh cho bộ binh của mình tấn công chiếm Wœrth và "những cao điểm phía bên kia". Cùng lúc, được cổ vũ bởi thắng l…

**Bài:** Trận Wœrth (8,873 âm tiết), cửa sổ ở 84% bài  
**Trạng thái:** answer_not_verbatim  
**Câu hỏi:** Hai yếu tố then chốt nào đã quyết định đại thắng của phía Phổ-Đức trong chiến tranh hiện đại?  
**Đáp án sinh:** ưu thế tuyệt đối về quân số và sức mạnh pháo binh  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Mặc dù chiến thuật nói trên chưa đủ để hạn chế đáng kể con số tổn thất của phía Phổ-Đức, đại thắng của họ đã được quyết định bởi hai yếu tố then chốt của chiến tranh hiện đại: Thứ nhất là ưu thế tuyệt đối về quân số: với lực lượng đông gấp đôi quân Pháp, các đạo binh của Thái tử Friedrich Wilhelm chỉ đơn thuần nới rộng chiến tuyến và bọc sườn các v…

**Bài:** Trận Wœrth (8,873 âm tiết), cửa sổ ở 12% bài  
**Trạng thái:** kept  
**Câu hỏi:** MacMahon đã bố trí sư đoàn nào dưới quyền tướng Noel Raoult ở trung tâm trận địa phòng thủ quanh ngôi làng Frœschwiller?  
**Đáp án sinh:** Sư đoàn số 3  
**Kiểm:** Sư đoàn số 3 (F1 1.0)  
**Cửa sổ (rút gọn):** Không có Quân đoàn V, MacMahon chỉ nắm được trong tay 42.800 bộ binh, 5.570 kỵ binh và 167 đại bác để đối mặt với 3 đội hình hàng dọc của Thái tử nước Phổ, với 89.000 bộ binh, 7.500 kỵ binh và 342 đại bác. Vào ngày 5 tháng 8, MacMahon khai triển 5 sư đoàn của mình trong một cứ điểm phòng ngự vững chắc nằm trên một dãy đồi cao, dốc và phủ rừng chạy …

**Bài:** Mại dâm tại Việt Nam (11,547 âm tiết), cửa sổ ở 37% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo một bài báo, tỷ lệ tối thiểu gái bán dâm ở Hà Nội phải tìm đến bọn cho vay nặng lãi là bao nhiêu?  
**Đáp án sinh:** 70%  
**Kiểm:** 70% (F1 1.0)  
**Cửa sổ (rút gọn):** Thu nhập nhiều nhưng phần lớn thu nhập kiếm được lại được gái bán dâm ném vào nghiện ngập, hút chích, vũ trường, cờ bạc nên "tiền vào thì nhanh mà ra cũng nhanh". Càng kiếm nhiều thì càng ăn chơi nhiều, một bài báo cho biết ít nhất 70% gái bán dâm ở Hà Nội phải tìm đến bọn cho vay nặng lãi. Vay ít thì là 5 triệu, không ít vay nợ tới cả trăm triệu. …

**Bài:** Mại dâm tại Việt Nam (11,547 âm tiết), cửa sổ ở 23% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo khảo sát của Bộ Lao động thương binh xã hội, thu nhập trung bình của gái mại dâm vào đầu năm 2012 là bao nhiêu?  
**Đáp án sinh:** 10,6 triệu đồng/tháng  
**Kiểm:** 10,6 triệu đồng/tháng (F1 1.0)  
**Cửa sổ (rút gọn):** Năm 2012, tần suất bán dâm trung bình của mỗi gái mại dâm là 60 lần/tháng, riêng Hải Phòng là 187 lần/tháng (162 lần cho khách lạ và 25 lần cho khách quen) Khảo sát của Bộ Lao động thương binh xã hội cho biết, vào đầu năm 2012, thu nhập trung bình của gái mại dâm đạt 10,6 triệu đồng/tháng, chưa kể các khoản phụ khác, cao gấp 2,5 lần thu nhập trung …

**Bài:** Mại dâm tại Việt Nam (11,547 âm tiết), cửa sổ ở 64% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo đại diện huyện Củ Chi, mại dâm tại Thành phố Hồ Chí Minh hiện nay đã bung ra đến đâu?  
**Đáp án sinh:** toàn thành, chỗ nào cũng có  
**Kiểm:** toàn thành, chỗ nào cũng có (F1 1.0)  
**Cửa sổ (rút gọn):** Phạt xong họ lại tiếp tục đến một địa bàn khác hoạt động, nếu có bị bắt cũng chỉ lập biên bản xử phạt hành chính tiếp mà không có chế tài xử lý cụ thể. Không chỉ riêng gì TP Hồ Chí Minh, mà các tỉnh thành khác cả nước cũng gặp rất nhiều khó khăn trong công tác quản lý đối tượng mại dâm, nói thật sự là không quản lý được. Tại Hà Nội, từ khi biện phá…

**Bài:** Mại dâm tại Việt Nam (11,547 âm tiết), cửa sổ ở 76% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tiến sĩ Đỗ Đức Hồng Hà đề xuất cần bổ sung thêm tội danh nào vào luật Hình sự để tăng tính răn đe?  
**Đáp án sinh:** Bán dâm  
**Kiểm:** Bán dâm (F1 1.0)  
**Cửa sổ (rút gọn):** Điều này đang tồn tại những bất cập và một số địa phương đã đưa ra cách làm riêng... Nếu anh phát hiện họ bán dâm, anh phạt tiền rồi để họ ra ngoài tiếp tục hoạt động thì xem như là thả nổi. Thậm chí có người chịu phạt một ít nhưng vẫn còn một khoản đủ sống. Như vậy, xử lý pháp luật vẫn chưa rốt ráo. Quyết định của Đà Nẵng đưa ra là để giúp những n…

**Bài:** Mại dâm tại Việt Nam (11,547 âm tiết), cửa sổ ở 70% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, nguyên nhân khiến tỷ lệ nhiễm HIV qua đường tình dục tăng nhanh là do các quy định bất hợp lý tại văn bản pháp luật nào?  
**Đáp án sinh:** Luật xử lý vi phạm hành chính năm 2012  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Tỷ lệ rất cao gái mại dâm trong các trung tâm này đã mang mầm bệnh như AIDS, lậu mủ, giang mai... Ví dụ, ở Trung tâm Giáo dục Lao động Xã hội số 2 (Ba Vì - Hà Nội) có 208 học viên, số nghiện ma túy lên tới 50%, số nhiễm HIV lên tới 10%, nếu tính cả lậu mủ, giang mai thì có tới 142 người (70%) bị nhiễm. Khi thả họ ra thì không ai biết họ sẽ đi đâu v…

**Bài:** Mại dâm tại Việt Nam (11,547 âm tiết), cửa sổ ở 81% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Theo Nghị định 178/2004/NĐ-CP, ngoài việc xử lý hành chính, cán bộ, công chức, người thuộc lực lượng vũ trang bị bắt khi mua dâm còn bị xử lý như thế nào?  
**Đáp án sinh:** thông báo cho người đứng đầu cơ quan, tổ chức quản lý người đó để xử lý  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** hành vi mua dâm bị phạt nặng để răn đe tối đa những người có ý định mua dâm (khi đó tự khắc số gái bán dâm cũng giảm đi). Ở những nước này, mua dâm là tội hình sự, có thể bị phạt hàng ngàn USD và đi tù nhiều tháng. Cảnh sát cũng công khai danh tính kẻ mua dâm nơi công cộng để họ phải cảm thấy hổ thẹn. So với những nước này, mức phạt tại Việt Nam nh…

**Bài:** Mại dâm tại Việt Nam (11,547 âm tiết), cửa sổ ở 87% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Ông Lê Văn Quý đề xuất cần gom các cơ sở kinh doanh dịch vụ dễ phát sinh mại dâm vào một khu riêng nhằm mục đích gì?  
**Đáp án sinh:** tăng cường sự quản lý của Nhà nước đối với những cơ sở dịch vụ dễ phát sinh mại dâm  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** "Một hiện tượng mới trong xã hội phát triển là hình thành một tầng lớp mới gọi là "đại gia". Họ giàu có nhờ những nguồn này nguồn khác, kể cả lao động hay bất chính; từ đó, nảy sinh nhu cầu mua dâm "chân dài". Đáp ứng lại điều đó, một số người mẫu, diễn viên, sinh viên (gọi nôm na là "chân dài") hình thành các nhóm bán dâm cao cấp, do tham tiền bạc…

**Bài:** Mại dâm tại Việt Nam (11,547 âm tiết), cửa sổ ở 0% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Thủ tướng Chính phủ Nguyễn Xuân Phúc, Việt Nam sẽ không phát triển theo hướng nào?  
**Đáp án sinh:** phố đèn đỏ, không làm casino tràn lan  
**Kiểm:** phố đèn đỏ, không làm casino tràn lan (F1 1.0)  
**Cửa sổ (rút gọn):** Mại dâm ở Việt Nam là một chủ đề về hoạt động mại dâm tại Việt Nam, cũng như những quy định của pháp luật về hành vi mua bán dâm, chủ chứa, môi giới mại dâm... Gần đây, có những ý kiến cho rằng Việt Nam nên hợp pháp hóa mại dâm, coi đây là một ngành nghề kinh doanh. Tuy nhiên, những ý kiến này đã vi phạm Hiến pháp năm 2013 (Khoản 2 Điều 36 quy định…

**Bài:** Fate/Zero (10,060 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** kept  
**Câu hỏi:** Địa điểm triệu hồi Chén Thánh trong Cuộc Chiến Chén Thánh lần II được đặt tại đâu?  
**Đáp án sinh:** dinh thự Tohsaka  
**Kiểm:** dinh thự Tohsaka (F1 1.0)  
**Cửa sổ (rút gọn):** Vì lợi ích của nhân loại, Kiritsugu nhẫn tâm phá hủy mọi thứ và bất cứ ai đe dọa sự bình an của những người khác. Tuy nhiên, Kiritsugu thấy chính mình bị xé rách rất sâu giữa tình yêu Kiritsugu đã tìm thấy cho gia đình mới của mình - Irisviel (vợ Kiritsugu) và Illya (con gái họ) - cùng những cái mà Kiritsugu phải làm để có được Chén Thánh (Holy Gra…

**Bài:** Fate/Zero (10,060 âm tiết), cửa sổ ở 68% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trong Holy Grail War IV, Lancelot được triệu hồi bởi ai?  
**Đáp án sinh:** Kariya  
**Kiểm:** Kariya (F1 1.0)  
**Cửa sổ (rút gọn):** Lancelot là một hiệp sĩ rất giỏi thế nhưng kể từ lúc bắt đầu cuộc tình với Guinevere thì mọi chuyện cũng trở nên xấu đi sau khi bị Arthur phát hiện. Chỗ đứng của ông trong hội bàn tròn dần bị suy giảm, sự việc ngày càng trở nên nghiêm trọng hơn. Một cuộc nội chiến đã nổ ra, nước Anh bị chia rẽ và bị chìm trong ngọn lửa chiến tranh. Lancelot liên tụ…

**Bài:** Fate/Zero (10,060 âm tiết), cửa sổ ở 44% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trong Fate/Zero, cặp đôi nào được mô tả là thú vị nhất?  
**Đáp án sinh:** Waver Velvet và Alexander Đại Đế của Macedonia  
**Kiểm:** Waver Velvet và Alexander Đại Đế của Macedonia (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên Mystic face, một khả năng của Lancer gây cuốn hút đối với người khác giới làm cho Kayneth không tin tưởng, sợ anh ta quyến rũ vợ mình, đặc biệt là sau khi biết được về quá khứ của Lancer lúc còn sống. Cặp đôi thú vị nhất trong Fate/Zero này có lẽ là Waver Velvet và Alexander Đại Đế của Macedonia. Waver là một nhà giả kim thuật, một học si…

**Bài:** Fate/Zero (10,060 âm tiết), cửa sổ ở 43% bài  
**Trạng thái:** kept  
**Câu hỏi:** Matou Kariya đã sử dụng thứ gì để trợ giúp cho việc trở lại tham gia Holy Grail War sau nhiều năm không sử dụng pháp thuật?  
**Đáp án sinh:** trùng độc  
**Kiểm:** trùng độc (F1 1.0)  
**Cửa sổ (rút gọn):** Do đó, Matou Kariya đã trở lại và tình nguyện tham gia Holy Grail War với hy vọng chiến thắng để mang Sakura trở lại với mẹ và chị của cô bé. Nhiều năm không sử dụng pháp thuật, để trở lại Matou Kariya phải sử dụng "trùng độc" (tử trùng) để trợ giúp, và cũng biết rõ không thể sống sót sau Holy Grail War lần này, dù thắng hay thua. Berserker của Kar…

**Bài:** Fate/Zero (10,060 âm tiết), cửa sổ ở 64% bài  
**Trạng thái:** kept  
**Câu hỏi:** Berserker được gọi dưới tên nào cho đến khi tiết lộ danh tính?  
**Đáp án sinh:** Black Knight  
**Kiểm:** Black Knight (F1 1.0)  
**Cửa sổ (rút gọn):** Cho đến khi tiết lộ danh tính, Berserker được gọi dưới tên Black Knight. Gender: Male, Height: 191 cm, Weight: 81 kg. Còn được gọi là Knight of the Lake (Hiệp sĩ của Lake). Ông là một trong số các hiệp sĩ bàn tròn và đã từng rất trung thành với vua Arthur. Mọi chuyện bắt đầu xấu đi khi Lancelot có tình yêu với nữ hoàng Artoria, Guinevere. Berserker…

**Bài:** Fate/Zero (10,060 âm tiết), cửa sổ ở 7% bài  
**Trạng thái:** kept  
**Câu hỏi:** Địa điểm triệu hồi Chén Thánh trong Cuộc Chiến Chén Thánh lần II được đặt tại đâu?  
**Đáp án sinh:** dinh thự Tohsaka  
**Kiểm:** dinh thự Tohsaka (F1 1.0)  
**Cửa sổ (rút gọn):** Một cuộc chiến thực sự gay go, quyết liệt và đẫm máu giữa các bậc đàn anh, cha chú của đám thiếu niên trong Fate/Stay Night và Fate/Stay Night - Unlimited Blade Works cùng Fate/Stay night - Heaven's Feel. Cuộc Chiến Chén Thánh lần I (The Holy Grail War I): cuộc chiến đã kết thúc trước khi Chén Thánh kịp hoàn thành và cuộc triệu hồi Chén Thánh vẫn c…

**Bài:** Fate/Zero (10,060 âm tiết), cửa sổ ở 57% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trong anime Fate Series, Gilgamesh xuất hiện dưới class nào?  
**Đáp án sinh:** Archer  
**Kiểm:** Archer (F1 1.0)  
**Cửa sổ (rút gọn):** Nhiều anh hùng và câu chuyện thần thoại, truyền thuyết trên thế giới cũng sao chép từ ông mà ra. Mặc dù có rất nhiều vua (Vua của kỵ sĩ, Vua chinh phục,…) nhưng ông là người duy nhất được trời đất vinh danh với danh hiệu vua của tất cả các anh hùng. Trong anime Fate Series, Gilgamesh được Tohsaka Tokiomi (cha của Tohsaka Rin) triệu hồi và xuất hiện…

**Bài:** Fate/Zero (10,060 âm tiết), cửa sổ ở 26% bài  
**Trạng thái:** kept  
**Câu hỏi:** Khả năng đặc biệt của Rider trong Fate/Stay Night là gì?  
**Đáp án sinh:** Riding Skill  
**Kiểm:** Riding Skill (F1 1.0)  
**Cửa sổ (rút gọn):** Khả năng đặc biệt của Rider là Riding Skill, giúp cho Rider có thể phát huy tối đa khả năng của vật cưỡi. Từ một thứ tầm thường như ngựa hay xe mô tô tới những con vật trong truyền thuyết như Unicorn hay Pegasus. Str: D, End: D, Ag: B, Man: C, Luk: E + Caster: Servant vượt trội về phép thuật cũng như lượng mana dự trữ của bản thân. Str: E, End: E, …

**Bài:** Người Mã Lai (11,257 âm tiết), cửa sổ ở 88% bài  
**Trạng thái:** kept  
**Câu hỏi:** Đô đốc Hang Tuah của Malacca được một số người xem là cha đẻ của môn võ nào?  
**Đáp án sinh:** silat Mã Lai  
**Kiểm:** silat Mã Lai (F1 1.0)  
**Cửa sổ (rút gọn):** Tầm ảnh hưởng của các vương quốc Hồi giáo Mã Lai như Malacca, Johor, Pattani và Brunei đã góp phần vào việc truyền bá loại võ thuật này tại quần đảo Mã Lai. Thông qua một mê cung phức tạp các eo biển và sông đã tạo điều kiện trao đổi thương mại trên khắp khu vực, Pencak Silat đã theo đó đi tận vào các khu vực rừng rậm và lên các vùng đồi núi. Đô đố…

**Bài:** Người Mã Lai (11,257 âm tiết), cửa sổ ở 13% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo The Encyclopedia of Malaysia: Early History, thuyết nào về nguồn gốc người Mã Lai được công bố vào năm 1889?  
**Đáp án sinh:** Thuyết Vân Nam  
**Kiểm:** Thuyết Vân Nam (F1 1.0)  
**Cửa sổ (rút gọn):** The Encyclopedia of Malaysia: Early History, đã chỉ ra tổng cộng ba giả thuyết về nguồn gốc của người Mã Lai: Thuyết Vân Nam, di cư theo sông Mê Kông (công bố năm 1889) - "thuyết người Mã Lai nguyên thủy" có nguồn gốc từ Vân Nam được R.H. Logen, Slamet Muljana và Asmah Haji Omar ủng hộ. Các bằng chứng khác hỗ trợ cho thuyết này bao gồm: các công cụ…

**Bài:** Người Mã Lai (11,257 âm tiết), cửa sổ ở 21% bài  
**Trạng thái:** kept  
**Câu hỏi:** Các dân tộc là hậu duệ của người Mã Lai nguyên thủy đáng chú ý ngày nay gồm những ai?  
**Đáp án sinh:** người Moken, người Jakun, người Orang Kuala, người Temuan và Orang Kanaq  
**Kiểm:** người Moken, người Jakun, người Orang Kuala, người Temuan và Orang Kanaq (F1 1.0)  
**Cửa sổ (rút gọn):** Vào cuối thế kỷ cuối cùng TCN, các kampung này bắt đầu tham gia vào một số hoạt động thương mại với thế giới bên ngoài. Người Mã Lai thứ hai được xem là tổ tiên trực tiếp của người Mã Lai ngày nay  Các đợt di cư của họ đã gián tiếp buộc một số nhóm người Mã Lai nguyên thủy và thổ dân phải rút lui vào khu vực đồi núi ở sâu trong thượng nguồn các con…

**Bài:** Người Mã Lai (11,257 âm tiết), cửa sổ ở 2% bài  
**Trạng thái:** kept  
**Câu hỏi:** Người Mã Lai là dân tộc thuộc nhóm ngôn ngữ nào?  
**Đáp án sinh:** Nam Đảo  
**Kiểm:** Nam Đảo (F1 1.0)  
**Cửa sổ (rút gọn):** |region9 = |pop9 = 8.789.585 (ước tính 2010) |region10 = |pop10 = 27.000 |pop11 = 653.449 (ước tính 2010) |languages = tiếng Mã Lai, tiếng Indonesia, tiếng Yawi, tiếng Thái, tiếng Anh |religions = Hồi giáo Sunni (xấp xỉ 99,9%) |region5=|pop5=14.749.378 (ước tính 2010)|ref5=|region12=|pop12=29.431|region13=|pop13=16.920|ref13=|region14= Vương Quốc A…

**Bài:** Người Mã Lai (11,257 âm tiết), cửa sổ ở 64% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Ngài Richard O. Winstedt đã gọi Biên niên sử Mã Lai là gì?  
**Đáp án sinh:** nổi tiếng nhất, đặc biệt nhất và tốt nhất trong tất cả các tác phẩm văn học Mã Lai  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Trong thời kỳ này, các tác phẩm văn học Trung Đông nổi tiếng đã được dịch và các sách tôn giáo được viết bằng tiếng Mã Lai. Trong số các tác phẩm nổi tiếng nhất, có Hikayat Muhammad Hanafiah và Hikayat Amir Hamzah. Bộ phận quan trọng nhất của văn học Mã Lai có lẽ là Biên niên sử Mã Lai hay Sulalatus Salatin lừng danh. Nó được một trong số những học…

**Bài:** Người Mã Lai (11,257 âm tiết), cửa sổ ở 67% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tác phẩm nào của Abdullah thường thuật về chuyến hành hương của ông đến Mecca vào năm 1854?  
**Đáp án sinh:** Kisah Pelayaran Abdullah ke Mekah  
**Kiểm:** Kisah Pelayaran Abdullah ke Mekah (F1 1.0)  
**Cửa sổ (rút gọn):** Các tác phẩm quan trọng nhất của ông là Hikayat Abdullah (tự truyện), Kisah Pelayaran Abdullah ke Kelantan (miêu tả về chuyến đi của ông tới Kelantan) và Kisah Pelayaran Abdullah ke Mekah (thường thuật về chuyến hành hương của ông đến Mecca vào năm 1854). Tác phẩm của ông là một nguồn cảm hứng cho các thế hệ nhà văn tương lai và đánh dấu một giai đ…

**Bài:** Người Mã Lai (11,257 âm tiết), cửa sổ ở 50% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sự sụp đổ của các vương quốc Mã Lai tại Đông Sumatra trong năm 1946 đã đẩy các chiến hữu Mã Lai quay sang chống lại ý tưởng nào?  
**Đáp án sinh:** Đại Indonesia và ảo tưởng về Cộng hòa Hồi giáo  
**Kiểm:** Đại Indonesia và ảo tưởng về Cộng hòa Hồi giáo (F1 1.0)  
**Cửa sổ (rút gọn):** Sự sụp đổ của các vương quốc Mã Lai gồm Deli, Langkat, Serdang và Asahan tại Đông Sumatra trong "cách mạng Xã hội" vào năm 1946 đã có tác động mạnh mẽ đến những người cùng chí hướng Mã Lai của họ và đẩy các chiến hữu Mã Lai quay sang chống lại ý tưởng về Đại Indonesia và ảo tưởng về Cộng hòa Hồi giáo. Tháng 3 năm 1946, Tổ chức Dân tộc Mã Lai Thống …

**Bài:** Người Mã Lai (11,257 âm tiết), cửa sổ ở 0% bài  
**Trạng thái:** kept  
**Câu hỏi:** Các ngôn ngữ nào được liệt kê trong thông tin nhân khẩu học của Malaysia?  
**Đáp án sinh:** tiếng Mã Lai, tiếng Indonesia, tiếng Yawi, tiếng Thái, tiếng Anh  
**Kiểm:** tiếng Mã Lai, tiếng Indonesia, tiếng Yawi, tiếng Thái, tiếng Anh (F1 1.0)  
**Cửa sổ (rút gọn):** Hàng thứ hai: Hassanal Bolkiah của Brunei • Lat • Mahathir Mohamad Hàng thứ ba: Saloma • Siti Nurhaliza • Surin Pitsuwan Hàng thứ tư: Sheikh Muszaphar Shukor • Tunku Abdul Rahman • Thái tử phi Sarah |poptime = khoảng 27,8 triệu |pop6 = 3.354.475 (ước tính 2010) |region7 = |pop7 = 261.902 (ước tính 2010) |region9 = |pop9 = 8.789.585 (ước tính 2010) …

**Bài:** George V của Anh (8,895 âm tiết), cửa sổ ở 33% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vua George V đã bắn hạ được bao nhiêu con hổ trong chuyến săn bắn tại Nepal?  
**Đáp án sinh:** 21 con hổ  
**Kiểm:** 21 con hổ (F1 1.0)  
**Cửa sổ (rút gọn):** Ông cho biết rằng ông sẽ từ chối khai mạc Quốc hội trừ phi tuyên bố được sửa đổi. Vì vậy, Tuyên bố lên ngôi 1910 rút ngắn nội dung hơn và loại bỏ phần nhiều những từ ngữ gây khó chịu. Lễ đăng quang của George và Mary diễn ra tại Tu viện Westminster ngày 22 tháng 6 năm 1911, và tổ chức Liên hoan đế quốc ở London. Tháng 7, Vua và Vương hậu đến thăm I…

**Bài:** George V của Anh (8,895 âm tiết), cửa sổ ở 2% bài  
**Trạng thái:** kept  
**Câu hỏi:** George V chào đời tại địa điểm nào ở London?  
**Đáp án sinh:** Marlborough House  
**Kiểm:** Marlborough House (F1 1.0)  
**Cửa sổ (rút gọn):** Thời đại của ông chứng kiến sự trỗi dậy của chủ nghĩa xã hội, chủ nghĩa cộng sản, chủ nghĩa phát xít, chủ nghĩa cộng hòa Ireland, và phong trào giành độc lập Ấn Độ, tất cả đã làm thay đổi đáng kể tình hình chính trị. Đạo luật Nghị viện 1911 thiết lập quyền lực tối cao của Hạ viện Anh được lập nên qua bầu cử đối với Thượng viện không qua bầu cử. Bởi…

**Bài:** George V của Anh (8,895 âm tiết), cửa sổ ở 0% bài  
**Trạng thái:** kept  
**Câu hỏi:** George Frederick Ernest Albert là con trai thứ hai của ai?  
**Đáp án sinh:** Thân vương xứ Wales Albert Edward  
**Kiểm:** Thân vương xứ Wales Albert Edward (F1 1.0)  
**Cửa sổ (rút gọn):** Ông tên đầy đủ là George Frederick Ernest Albert, là con trai thứ hai của Thân vương xứ Wales Albert Edward (về sau là Quốc vương Edward VII), và là cháu nội của Nữ vương Anh đương thời, Victoria của Anh. Tại thời điểm chào đời, ông đứng thứ ba trong danh sách kế vị của Anh sau cha và anh trai, Vương tôn Albert Victor, Công tước xứ Clarence và Avon…

**Bài:** George V của Anh (8,895 âm tiết), cửa sổ ở 81% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vị chỉ huy trưởng của Order of the Dannebrog (Đan Mạch) được trao tặng huân chương nào của Tây Ban Nha?  
**Đáp án sinh:** Collar of the Huân chương Charles III (Spain)  
**Kiểm:** Collar of the Huân chương Charles III (F1 0.93)  
**Cửa sổ (rút gọn):** Chỉ huy trưởng của Order of the Dannebrog (Đan Mạch) Knight of the Order of the Seraphim (Thụy Điển), 14 tháng 6 năm 1905 Collar of the Huân chương Charles III (Spain) Knight of the Order of the Golden Fleece (Tây Ban Nha) Knight of the Order of Saint Hubert (Bavaria) Knight of the Order of the Most Holy Annunciation (Italia) Grand Commander of the…

**Bài:** George V của Anh (8,895 âm tiết), cửa sổ ở 94% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Danh hiệu nào được liệt kê trong đoạn trích liên quan đến Hội đồng Cơ mật của Vương quốc Anh?  
**Đáp án sinh:** Thành viên Hội đồng Cơ mật của Vương quốc Anh  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Knights Grand Commander of the Order of the Indian Empire Knights Grand Cross of the Royal Victorian Order Grand Commanders of the Order of the Dannebrog Grand Crosses of the House Order of the Wendish Crown Grand Crosses of the Order of the Colonial Empire Grand Crosses of the Saxe-Ernestine House Order Knights Grand Cross of the Order of Saints M…

**Bài:** George V của Anh (8,895 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** kept  
**Câu hỏi:** George và May kết hôn vào ngày nào?  
**Đáp án sinh:** 6 tháng 7 năm 1893  
**Kiểm:** ngày 6 tháng 7 năm 1893 (F1 0.91)  
**Cửa sổ (rút gọn):** Ngày 14 tháng 1 năm 1892, sáu tuần sau lễ đính hôn chính thức, Albert Victor chết vì bệnh viêm phổi, để lại George bấy giờ đứng thứ hai trong danh sách kế vị, và khả năng rất cao sẽ nối ngôi sau phụ thân. George cũng chỉ mới hồi phục sau căn bệnh trầm trọng của chính ông, sau khi nằm liệt giường suốt sáu tuần vì sốt thương hàn, căn bệnh được cho là…

**Bài:** George V của Anh (8,895 âm tiết), cửa sổ ở 29% bài  
**Trạng thái:** answer_not_verbatim  
**Câu hỏi:** George đã viết gì trong nhật ký của mình sau khi Quốc vương Edward qua đời?  
**Đáp án sinh:** Tôi đã mất đi người bạn tuyệt vời nhất và người cha tuyệt vời nhất ... Tôi không bao giờ to tiếng với ông ấy trong suốt cuộc đời tôi. Tôi đau lòng và choáng ngợp với sự đau buồn nhưng nhờ Chúa tôi sẽ gánh vác trách nhiệm và May thân yêu là niềm an ủi của tôi vì cô ấy luôn là như vậy. Xin Chúa cho tôi sức mạnh và hướng dẫn tôi thực hiện các nhiệm vụ nặng nề đang đặt trên vai tôi  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Quốc vương và Hoàng đế Ngày 6 tháng 5 năm 1910, Quốc vương Edward mất, và George lên ngôi. Ông viết trong quyển nhật ký, "Tôi đã mất đi người bạn tuyệt vời nhất và người cha tuyệt vời nhất ... Tôi không bao giờ to tiếng với ông ấy trong suốt cuộc đời tôi. Tôi đau lòng và choáng ngợp với sự đau buồn nhưng nhờ Chúa tôi sẽ gánh vác trách nhiệm và May …

**Bài:** George V của Anh (8,895 âm tiết), cửa sổ ở 18% bài  
**Trạng thái:** kept  
**Câu hỏi:** Harold Nicolson nhận xét George chỉ làm gì khi ở vị trí Công tước xứ York?  
**Đáp án sinh:** giết [tức là. săn bắn] động vật và dán tem  
**Kiểm:** giết [tức là. săn bắn] động vật và dán tem (F1 1.0)  
**Cửa sổ (rút gọn):** Công tước và Bà Công tước xứ York sống chủ yếu tại York Cottage, một ngôi nhà tương đối nhỏ tại Sandringham, Norfolk, cuộc sống của họ giống như một gia đình trung lưu ấm cúng hơn là gia đình vương thất. George thích sự đơn giản, gần như tĩnh lặng, cuộc sống của ông tương đối phẳng lặng so với cách sống năng động của cha ông. Người viết tiểu sử chí…

**Bài:** 2018 (10,370 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cầu vượt biển nào được khánh thành vào ngày 17 tháng 10 và được mô tả là lớn nhất thế giới?  
**Đáp án sinh:** Cầu Hồng Kông - Chu Hải - Ma Cao  
**Kiểm:** Cầu Hồng Kông - Chu Hải - Ma Cao (F1 1.0)  
**Cửa sổ (rút gọn):** 13 tháng 10: Ít nhất 3 người chết và 8 người bị thương nặng sau khi một máy bay cỡ nhỏ đã lao vào nhóm người đang đứng tại sân bay Wasserkuppe ở bang Hesse của Đức. 29 người thiệt mạng sau khi mưa lớn và lũ lụt gây lở xuống một ngôi trường tiểu học tại khu vực Bắc Sumatra, Indonesia. 4 người thiệt mạng và 1 người bị thương khi xảy ra một vụ xả súng…

**Bài:** 2018 (10,370 âm tiết), cửa sổ ở 57% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là nhà văn truyện tranh người Mỹ được liệt kê trong danh sách các nhân vật sinh ngày 28 tháng 1?  
**Đáp án sinh:** Mort Walker  
**Kiểm:** Mort Walker (F1 1.0)  
**Cửa sổ (rút gọn):** Hiromu Nonaka, chính khách Nhật Bản (s. Ingvar Kamprad, doanh nhân Thụy Điển (s. Mort Walker, nhà văn truyện tranh người Mỹ (s. 28 tháng 1: Gene Sharp, giáo sư khoa học chính trị Mỹ (s. 29 tháng 1: Ion Ciubuc, chính trị gia và thủ tướng thứ ba của Moldova (s. Mark Salling, diễn viên người Mỹ (s. Clyde Scott, cầu thủ bóng bầu dục,diễn viên người Mỹ …

**Bài:** 2018 (10,370 âm tiết), cửa sổ ở 53% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là nữ diễn viên người Mỹ được liệt kê trong danh sách các nhân vật sinh ngày 19 tháng 1?  
**Đáp án sinh:** Dorothy Malone  
**Kiểm:** Dorothy Malone (F1 1.0)  
**Cửa sổ (rút gọn):** Lucas Mangope, chính trị gia Nam Phi (s. Peter Mayle, tác giả người Anh (s. Stansfield Turner, đô đốc và học thuật người Mỹ (s. 19 tháng 1: Dorothy Malone, nữ diễn viên người Mỹ (s. Paul Bocuse, đầu bếp người Pháp (s. Graeme Langlands, cầu thủ bóng bầu dục Úc (s. Naomi Parker Fraley, nữ thợ máy hải quân Mỹ (s. Jim Rodford, nghệ sĩ guitar bass người…

**Bài:** 2018 (10,370 âm tiết), cửa sổ ở 34% bài  
**Trạng thái:** kept  
**Câu hỏi:** Phim nào do Alfonso Cuarón đạo diễn đã đoạt giải Sư tử vàng tại Liên hoan phim Venezia 2018?  
**Đáp án sinh:** Roma  
**Kiểm:** Roma (F1 1.0)  
**Cửa sổ (rút gọn):** Bế mạc Đại hội Thể thao châu Á 2018 diễn ra tại Indonesia. Một vụ hỏa hoạn phá hủy Bảo tàng quốc gia Brasil ở Rio de Janeiro. 3 tháng 9: Một vụ nổ đã xảy ra ở nhà máy sản xuất đạn dược Rheinmetall-Denel, gần thủ phủ Cape Town, tỉnh Somerset West của Nam Phi làm 8 người thiệt mạng. 4 tháng 9: Bão Jebi tiến vào Nhật Bản gây thiệt hại lớn ở vùng Kinki…

**Bài:** 2018 (10,370 âm tiết), cửa sổ ở 19% bài  
**Trạng thái:** kept  
**Câu hỏi:** Núi lửa nào đã phun trào tại Guatemala vào ngày 3 tháng 6, giết chết ít nhất 109 người?  
**Đáp án sinh:** Volcán de Fuego  
**Kiểm:** Volcán de Fuego (F1 1.0)  
**Cửa sổ (rút gọn):** Một cuộc trưng cầu dân ý về hiến pháp về việc có nên bãi bỏ lệnh cấm phá thai ở Ireland hay không, với chiến thắng thuộc về phía bãi bỏ với ​​66,4% và 33,6% cho phần còn lại. giành chiến thắng trước Liverpool F.C. để lần thứ ba liên tiếp vô địch UEFA Champions League. Pedro Sánchez trở thành Thủ tướng Tây Ban Nha sau khi Mariano Rajoy không vượt qu…

**Bài:** 2018 (10,370 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là nguyên Tổng bí thư Ban Chấp hành Trung ương Đảng Cộng sản Việt Nam được nhắc đến trong danh sách các nhân vật sinh vào tháng 9?  
**Đáp án sinh:** Đỗ Mười  
**Kiểm:** Đỗ Mười (F1 1.0)  
**Cửa sổ (rút gọn):** Bob Jane, lái xe và doanh nhân ô tô Úc (s. 29 tháng 9: Otis Rush, nghệ sĩ guitar và ca sĩ nhạc blues người Mỹ (s. 30 tháng 9: Geoffrey Hayes, người dẫn chương trình truyền hình và diễn viên người Anh (s. Charles Aznavour, ca sĩ người Armenia gốc Pháp (s. Đỗ Mười, nguyên Tổng bí thư Ban Chấp hành Trung ương Đảng Cộng sản Việt Nam, nguyên Chủ tịch Hộ…

**Bài:** 2018 (10,370 âm tiết), cửa sổ ở 75% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ola Ullsten giữ chức vụ gì tại Thụy Điển?  
**Đáp án sinh:** Thủ tướng thứ 28 của Thụy Điển  
**Kiểm:** Thủ tướng thứ 28 của Thụy Điển (F1 1.0)  
**Cửa sổ (rút gọn):** Ola Ullsten, chính trị gia, nhà ngoại gioa, Thủ tướng thứ 28 của Thụy Điển (s. 2 tháng 6: Paul D. Boyer, Nhà hóa sinh người Mỹ (s. 8 tháng 6: Anthony Bourdain, đầu bếp, tác giả, nhà làm phim tài liệu du lịch, nhân vật truyền hình người Mỹ (s. 14 tháng 6: Stanislav Govorukhin, Đạo diễn, nhà biên kịch và diễn viên điện ảnh Liên Xô và Nga (s. 15 tháng…

**Bài:** 2018 (10,370 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cuộc thi Eurovision 2018 được tổ chức tại thành phố nào của Bồ Đào Nha?  
**Đáp án sinh:** Lisbon  
**Kiểm:** Lisbon (F1 1.0)  
**Cửa sổ (rút gọn):** 8-12 tháng 5: Cuộc thi Eurovision 2018 được tổ chức tại Lisbon, Bồ Đào Nha và Netta Barzilai, người Israel giành chiến thắng với bài hát "Toy". Liên minh Pakatan Harapan thuộc phe đối lập lãnh đạo do cựu thủ tướng Mahathir Mohamad lãnh đạo, đảm bảo đa số nghị sĩ trong Quốc hội Malaysia, chấm dứt sự cai trị 61 năm của liên minh Barisan Nasional kể t…

**Bài:** Chiến dịch Bobruysk (8,994 âm tiết), cửa sổ ở 3% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tư lệnh Cánh phải của Phương diện quân Byelorussia 1?  
**Đáp án sinh:** đại tướng Konstantin Konstantinovich Rokossovsky  
**Kiểm:** đại tướng Konstantin Konstantinovich Rokossovsky (F1 1.0)  
**Cửa sổ (rút gọn):** Đây là một căn cứ bàn đạp rất có giá trị về quân sự và trở thành một trong hai khu vực xuất phát tấn công rất thuận lợi của Phương diện quân Byelorussia 1 trong Chiến dịch Bobruysk. Binh lực và kế hoạch Cánh phải của Phương diện quân Byelorussia 1 do đại tướng Konstantin Konstantinovich Rokossovsky làm tư lệnh, thượng tướng M. Malinin làm tham mưu …

**Bài:** Chiến dịch Bobruysk (8,994 âm tiết), cửa sổ ở 40% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thành phố Bobruysk được tổ chức thành một Fester Platz do ai chỉ huy?  
**Đáp án sinh:** chuẩn tướng Adolf Hamann  
**Kiểm:** chuẩn tướng Adolf Hamann (F1 1.0)  
**Cửa sổ (rút gọn):** Các tiểu đoàn bộ binh người Thổ Nhĩ Kỳ 790 và 791. Bộ binh: Các tiểu đoàn xung kích 10, 268; tiểu đoàn quân báo xung kích 4. Pháo binh: Trung đoàn pháo hạng nặng 307 của thiếu tướng Max Lindig Công binh: Các tiểu đoàn cầu 159, 255; các tiểu đoàn công trình 79, 576. Thông tin: Trung đoàn 511 Hậu cần: Trung đoàn 531. Riêng thành phố Bobruysk được tổ …

**Bài:** Chiến dịch Bobruysk (8,994 âm tiết), cửa sổ ở 65% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào ngày 26 tháng 6, Hitler đã huyền chức vị tướng nào vì sai lầm trong việc điều động Quân đoàn xe tăng 41?  
**Đáp án sinh:** tướng Hans Jordan  
**Kiểm:** Hans Jordan (F1 0.8)  
**Cửa sổ (rút gọn):** Một đợt oanh kích quy mô lớn bởi 526 máy bay của Tập đoàn quân không quân số 16 (Liên Xô) đã gây ra nhiều thương vong cùng sự khủng khiếp và hoảng loạn trong hàng ngũ quân Đức. Một số nỗ lực phá vây tự phát được thực hiện ở khu vực bờ Đông sông Berezina trên một địa đoạn dài vài cây số, và quân đội Xô Viết trả lời những cuộc phá vây này cũng bằng n…

**Bài:** Chiến dịch Bobruysk (8,994 âm tiết), cửa sổ ở 17% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người chỉ đạo hoạt động của Phương diện quân Byelorussia 2 với tư cách là Đại diện Đại bản doanh?  
**Đáp án sinh:** Nguyên soái G.  
**Kiểm:** Nguyên soái G. (F1 1.0)  
**Cửa sổ (rút gọn):** Súng cối: 1 trung đoàn. Trinh sát cơ giới: 2 tiểu đoàn.Tập đoàn quân không quân 16 do thượng tướng S. Máy bay tiêm kích: 8 sư đoàn và 1 trung đoàn. Máy bay cường kích: 5 sư đoàn. Máy bay ném bom: 5 sư đoàn Máy bay vận tải, trinh sát, trợ chiến...: 3 trung đoàn Pháo phòng không: 7 trung đoàn. Chỉ đạo hoạt động của Phương diện quân Byelorussia 2 là Đ…

**Bài:** Chiến dịch Bobruysk (8,994 âm tiết), cửa sổ ở 37% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sư đoàn bộ binh 134 của tướng Ernst Karl Julius Philipp đóng ở khu vực nào?  
**Đáp án sinh:** Klichev  
**Kiểm:** Klichev (F1 1.0)  
**Cửa sổ (rút gọn):** Sư đoàn bộ binh 134 của tướng Ernst Karl Julius Philipp đóng ở khu vực Klichev. Sư đoàn cơ giới 36 của tướng Alexander Conrady đóng ở khu vực Glussk.Quân đoàn bộ binh 55 của thiếu tướng Friedrich Herrlein, thành phần gồm 7 trung đoàn bộ binh, 1 cụm tác chiến sư đoàn, 3 trung đoàn pháo, 2 tiểu đoán pháo chống tăng, 2 tiểu đoàn cơ giới, 2 tiểu đoàn s…

**Bài:** Chiến dịch Bobruysk (8,994 âm tiết), cửa sổ ở 19% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cụm kỵ binh cơ giới của tướng I. Pliev thuộc cánh nào trong kế hoạch tấn công Bobruysk của tướng K. Rokossovsky?  
**Đáp án sinh:** cánh trái  
**Kiểm:** cánh trái (F1 1.0)  
**Cửa sổ (rút gọn):** Vì vậy, không ngạc nhiên khi thành phố này là điểm trọng tâm trong kế hoạch tác chiến cũng như trong quá trình diễn biến chiến dịch Bobruysk. Căn cứ vào kinh nghiệm của Chiến dịch Gomel-Rechitsa và lợi thế tạo được do kết quả của Chiến dịch Rogachev-Zhlobin, tướng K. Rokossovsky dự kiến mở hai mũi tấn công vào Bobruysk. Cánh phải gồm Tập đoàn quân …

**Bài:** Chiến dịch Bobruysk (8,994 âm tiết), cửa sổ ở 94% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà xuất bản nào đã phát hành cuốn sách 'Bagration 1944: The Destruction of Army Group Centre'?  
**Đáp án sinh:** Osprey Publishing  
**Kiểm:** Osprey Publishing (F1 1.0)  
**Cửa sổ (rút gọn):** German Defeat in the East, 1944-5, Stackpole, 2007 Niepold, G., translated by Simpkin, R., Battle for White Russia: The destruction of Army Group Centre June 1944, Brassey's, London, 1987, ISBN 0-08-033606-X Stalin: The Court of the Red Tsar, Phoenix, London, 2004, ISBN 0-7538-1766-7 Bagration 1944: The Destruction of Army Group Centre'', Osprey Pu…

**Bài:** Chiến dịch Bobruysk (8,994 âm tiết), cửa sổ ở 75% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà báo Liên Xô nào đã miêu tả về thương vong của quân Đức trong chiến dịch Bobruysk?  
**Đáp án sinh:** Vasily Semyonovich Grossman  
**Kiểm:** Vasily Semyonovich Grossman (F1 1.0)  
**Cửa sổ (rút gọn):** Đây là một thắng lợi lớn của quân đội Liên Xô, đạt được trong thời gian ngắn và trên quy mô lớn. Việc triển khai hiệu quả một lực lượng không quân lớn là một trong những yếu tố góp phần làm nên chiến thắng của quân đội Liên Xô trong trận đánh này. Nhà báo Liên Xô, Vasily Semyonovich Grossman đã miêu tả về thương vong của quân Đức trong chiến dịch B…

**Bài:** Chiến dịch Minsk (9,070 âm tiết), cửa sổ ở 55% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Ai là người được giao quyền chỉ huy Tập đoàn quân 4 (Đức) sau khi Kurt von Tippelskirch di tản?  
**Đáp án sinh:** quân đoàn trưởng Quân đoàn bộ binh 12, trung tướng Vincenz Müller  
**Kiểm:** trung tướng Vincenz Müller (F1 0.5)  
**Cửa sổ (rút gọn):** Nhưng ở Stalingrad, quân đội Liên Xô phải mất đến gần 3 tháng để hoàn thành chiến dịch thì ở Minsk, họ chỉ mất 19 ngày. Việc thanh toán cụm quân Đức bị vây được giao cho Phương diện quân Byelorussia 2 và Tập đoàn quân 31. Khác với các cuộc bao vây ở Stalingrad, ở Korsun-Shevchenkovsky và ở Kamenets-Podolsky; ở Byelorussia trong mùa hè năm 1944, Cụm…

**Bài:** Chiến dịch Minsk (9,070 âm tiết), cửa sổ ở 18% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cụm kỵ binh cơ giới do trung tướng I. chỉ huy có bao nhiêu sư đoàn kỵ binh trong biên chế?  
**Đáp án sinh:** 9 sư đoàn kỵ binh  
**Kiểm:** 9 sư đoàn kỵ binh (F1 1.0)  
**Cửa sổ (rút gọn):** Trong biên chế có 9 sư đoàn bộ binh, 4 trung đoàn xe tăng, 4 trung đoàn pháo tự hành, 1 lữ đoàn và 2 trung đoàn pháo, 1 lữ đoàn Katyusha, 1 lữ đoàn và 2 trung đoàn súng cối, 1 sư đoàn và 1 trung đoàn phòng không. Tập đoàn quân 48 do trung tướng P. Trong biên chế có 8 sư đoàn bộ binh, 2 trung đoàn xe tăng, 4 trung đoàn pháo tự hành, 1 sư đoàn, 1 lữ …

**Bài:** Chiến dịch Minsk (9,070 âm tiết), cửa sổ ở 25% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là quyền tư lệnh của Tập đoàn quân số 4 (Đức) từ ngày 1 tháng 7?  
**Đáp án sinh:** Trung tướng Vincenz Müller  
**Kiểm:** Trung tướng Vincenz Müller (F1 1.0)  
**Cửa sổ (rút gọn):** Tập đoàn quân 39 được tách ra hướng Tây Bắc, phối hợp với Phương diện quân Pribaltic 1 giải quyết dứt điểm cụm cứ điểm Polotsk của Tập đoàn quân 16 (Đức). Phương diện quân Byelorussia 1 dưới quyền chỉ huy của Nguyên soái K. Rokossovsky (được phong hàm ngày 27 tháng 6) có nhiệm vụ phức tạp hơn các phương diện quân khác. Rokossovsky phải sử dụng Tập …

**Bài:** Chiến dịch Minsk (9,070 âm tiết), cửa sổ ở 44% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào lúc 13 giờ chiều ngày 3 tháng 7 năm 1944, sự kiện nào đã xảy ra đối với thủ đô của Byelorussia?  
**Đáp án sinh:** được giải phóng  
**Kiểm:** được giải phóng (F1 1.0)  
**Cửa sổ (rút gọn):** 3 giờ sáng ngày 3 tháng 7 năm 1944, Quân đoàn xe tăng cận vệ 2 "Tatsinskaya" đã đột nhập vào Minsk. Buổi trưa cùng ngày, các trung đoàn xe tăng 36 và 193 của Tập đoàn quân 3 (Phương diện quân Byelorussia 1) cũng tiến vào Minsk từ phía nam. 13 giờ chiều ngày 3 tháng 7, thủ đô của Byelorussia được giải phóng. Ở phía đông Minsk, Tập đoàn quân cận vệ 1…

**Bài:** Chiến dịch Minsk (9,070 âm tiết), cửa sổ ở 3% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tuyến đường rút lui khả dĩ duy nhất của quân Đức về sông Berezina là con đường nào?  
**Đáp án sinh:** con đường tỉnh lộ từ Mogilev về thị trấn Berezino  
**Kiểm:** con đường tỉnh lộ từ Mogilev về thị trấn Berezino (F1 1.0)  
**Cửa sổ (rút gọn):** Các tập đoàn quân 4, 9 và xe tăng 3 hùng mạnh một thời nay chỉ còn là các cụm tác chiến có quân số và trang bị không lớn hơn cấp quân đoàn, phải bố trí phòng thủ trên địa đoạn mặt trận dài hơn 500 km từ Daugavpins đến Pinsk để đối phó với bốn phương diện quân Liên Xô trong giai đoạn tiếp theo. Sau chiến dịch Vitebsk-Orsha và chiến dịch Bobruysk, cá…

**Bài:** Chiến dịch Minsk (9,070 âm tiết), cửa sổ ở 7% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tham mưu trưởng dưới quyền tư lệnh Chernyakhovsky?  
**Đáp án sinh:** thượng tướng A. Pokrovskiy  
**Kiểm:** thượng tướng A. Pokrovskiy (F1 1.0)  
**Cửa sổ (rút gọn):** Chernyakhovsky làm tư lệnh, thượng tướng A. Pokrovskiy làm tham mưu trưởng: Tập đoàn quân cận vệ 11 do trung tướng K. Trong biên chế có 9 sư đoàn bộ binh; 2 lữ đoàn và 6 trung đoàn pháo; 1 sư đoàn và 5 trung đoàn súng cối; 1 lữ đoàn và 3 trung đoàn Katyusha; 2 sư đoàn và 2 trung đoàn phòng không; 4 lữ đoàn và 4 trung đoàn xe tăng; 1 lữ đoàn cơ giới…

**Bài:** Chiến dịch Minsk (9,070 âm tiết), cửa sổ ở 6% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tư lệnh của Phương diện quân Byelorussia 3?  
**Đáp án sinh:** đại tướng I. Chernyakhovsky  
**Kiểm:** đại tướng I. Chernyakhovsky (F1 1.0)  
**Cửa sổ (rút gọn):** Phương diện quân Byelorussia 3 do đại tướng I. Chernyakhovsky làm tư lệnh, thượng tướng A. Pokrovskiy làm tham mưu trưởng: Tập đoàn quân cận vệ 11 do trung tướng K. Trong biên chế có 9 sư đoàn bộ binh; 2 lữ đoàn và 6 trung đoàn pháo; 1 sư đoàn và 5 trung đoàn súng cối; 1 lữ đoàn và 3 trung đoàn Katyusha; 2 sư đoàn và 2 trung đoàn phòng không; 4 lữ …

**Bài:** Chiến dịch Minsk (9,070 âm tiết), cửa sổ ở 33% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Sư đoàn xe tăng 5 của Trung tướng Karl Decker được rút từ đơn vị nào để điều tới bảo vệ thành phố Minsk?  
**Đáp án sinh:** Tập đoàn quân xe tăng 4 (Đức)  
**Kiểm:** Tập đoàn quân xe tăng 4 (Đức) thuộc Cụm Tập đoàn quân Nam Ukraina (F1 0.67)  
**Cửa sổ (rút gọn):** Tuy nhiên, một số viên tướng bị tử trận hoặc bị bắt làm tù binh được thay thế bằng cách đôn chức vụ từ chỉ huy sư đoàn, trung đoàn lên chỉ huy các Cụm tác chiến. Kho cán bộ chỉ huy của quân đội Đức Quốc xã đang gặp khủng hoảng, đặc biệt là các sĩ quan chỉ huy lâu năm, có nhiều kinh nghiệm tác chiến. Kế hoạch tác chiến của phía Đức bao hàm việc hạn …

**Bài:** Chiến dịch Šiauliai (14,350 âm tiết), cửa sổ ở 71% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Khu vực nào được mệnh danh là "cái lò mổ Šiauliai" trong trận đấu tăng - pháo đẫm máu kéo dài hơn 10 ngày?  
**Đáp án sinh:** cái lò mổ Šiauliai  
**Kiểm:** một khu vực (F1 0.0)  
**Cửa sổ (rút gọn):** Hướng phản công quan trọng này do Quân đoàn bộ binh 12 SS trong đó có Sư đoàn xe tăng 7 và 2 sư đoàn còn lại của Quân đoàn bộ binh 26 thực hiện. Ngày 17 tháng 8, Sư đoàn xe tăng 7 (Đức) và các sư đoàn bộ binh 1, 52 bắt đầu tấn công từ Kelma (Kelme) vào Radvilishkis, phía Nam Šiauliai với mục tiêu chiếm giữa đoạn đường sắt từ Šiauliai đi Vilnius, ng…

**Bài:** Chiến dịch Šiauliai (14,350 âm tiết), cửa sổ ở 27% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thống chế Walter Model hy vọng mặt trận của Cụm tập đoàn quân Trung tâm (Đức) sẽ ổn định trở lại khi nào?  
**Đáp án sinh:** trong một vài tuần tới  
**Kiểm:** trong một vài tuần tới (F1 1.0)  
**Cửa sổ (rút gọn):** Điều đó có nghĩa là quân Đức sẽ trụ lại ở bất kỳ đâu có thể trụ được, phòng ngự ở bất cứ địa điểm nào có thể phòng ngự được mà không thể có một trận tuyến liên tục. Thống chế Walter Model hy vọng trong một vài tuần tới, khi các lực lượng viện binh mạnh mẽ kịp đến thì mặt trận của Cụm tập đoàn quân Trung tâm (Đức) sẽ ổn định trở lại. Quân đội Liên X…

**Bài:** Chiến dịch Šiauliai (14,350 âm tiết), cửa sổ ở 58% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tư lệnh Tập đoàn quân 43 (Liên Xô) đánh giá tình hình chiến sự tại Pereveya như thế nào?  
**Đáp án sinh:** vô cùng phức tạp  
**Kiểm:** vô cùng phức tạp (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 1 tháng 8, Lữ đoàn pháo tự hành 393 và Lữ đoàn cơ giới 226 (Đức) tấn công và bao vây 4.000 quân thuộc Sư đoàn bộ binh số 357 thuộc Tập đoàn quân 43 (Liên Xô) tại làng Pereveya (???).. Beloborodov, tư lệnh Tập đoàn quân 43 (Liên Xô) đánh giá tình hình là vô cùng phức tạp và điều Lữ đoàn pháo chống tăng 94 và Trung đoàn pháo chống tăng 759 vào t…

**Bài:** Chiến dịch Šiauliai (14,350 âm tiết), cửa sổ ở 33% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn chủ lực của Tập đoàn quân 39 đã phải dừng lại trước phòng tuyến của quân Đức ở đâu?  
**Đáp án sinh:** Ukmerge trên sông Šventoyi  
**Kiểm:** Ukmerge trên sông Šventoyi (F1 1.0)  
**Cửa sổ (rút gọn):** Hai quân đoàn chủ lực của Tập đoàn quân 39 phải dừng lại trước phòng tuyến của quân Đức ở Ukmerge trên sông Šventoyi. Ngày 23 tháng 7, các quân đoàn bộ binh 84 và 113 được tăng cường Lữ đoàn cận vệ 28 tấn công Ukmerge. Chiều 24 tháng 7, quân đội Liên Xô làm chủ thành phố. Chỉ có một số ít tàn quân của Sư đoàn bộ binh 56 (Đức) thoát được về Kedainai…

**Bài:** Chiến dịch Šiauliai (14,350 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** STAVKA coi Šiauliai là một cụm từ nào có nhiều tác dụng nhất trong vùng Pribaltic?  
**Đáp án sinh:** bàn đạp tác chiến  
**Kiểm:** bàn đạp tác chiến (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên câu trả lời của Đại bản doanh lại là Šiauliai, một nút giao thông quan trọng nằm cách Riga khoảng 100 km về phía Nam. STAVKA cho rằng nếu tấn công Riga ngay sẽ quá mạo hiểm vì Tập đoàn quân xe tăng 3 (Đức) vừa mới được tăng cường thêm 3 sư đoàn, trong đó có 1 sư đoàn xe tăng. Các tin tức của tình báo Liên Xô cho biết, trong một đến hai tu…

**Bài:** Chiến dịch Šiauliai (14,350 âm tiết), cửa sổ ở 59% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tướng I. Bagramian đã điều động Quân đoàn xe tăng 19 từ Tập đoàn quân cận vệ 6 sang dải của Tập đoàn quân 43 vào ngày nào?  
**Đáp án sinh:** ngày 3 tháng 8  
**Kiểm:** ngày 3 tháng 8 (F1 1.0)  
**Cửa sổ (rút gọn):** Tình thế khẩn cấp buộc tướng I. Bagramian phải có những giải pháp quyết liệt. Nhận thấy không còn khả năng tấn công vào bên sườn cụm quân Đức đang công kích Birzhai, ngày 3 tháng 8, ông điều động Quân đoàn xe tăng 19 từ Tập đoàn quân cận vệ 6 và Quân đoàn bộ binh 22 từ lực lượng dự bị sang dải của Tập đoàn quân 43 để trợ chiến. Các Lữ đoàn pháo chố…

**Bài:** Chiến dịch Šiauliai (14,350 âm tiết), cửa sổ ở 95% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà xuất bản nào đã ấn hành cuốn sách 'The Road to Berlin: Stalin's War with Germany, Volume Two' vào năm 1999?  
**Đáp án sinh:** Yale University Press  
**Kiểm:** Yale University Press (F1 1.0)  
**Cửa sổ (rút gọn):** University of Kansas Press 1995. German Defeat in the East 1944 - 45, Stackpole, 2007, ISBN 0-8117-3371-8 The Road to Berlin: Stalin's War with Germany, Volume Two. New Haven, Connecticut: Yale University Press, 1999. Ostfrontdrama 1944, Motorbuchverlag Stuttgart, 1998 Fight for the Soviet Baltic in the Great Patriotic War 1941-1945, Riga, 1967 Pho…

**Bài:** Chiến dịch Šiauliai (14,350 âm tiết), cửa sổ ở 89% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Vụ ám sát Hitler ngày 20 tháng 7 năm 1944 đã diễn ra tại đâu?  
**Đáp án sinh:** Rastelburg  
**Kiểm:** tại Rastelburg, trụ sở Tổng hành dinh của Hitler tại Đông Phổ (F1 0.0)  
**Cửa sổ (rút gọn):** Mặc dù Phương diện quân Pribaltic 1 đã giành được những thắng lợi có tính chiến lược nhưng Đại bản doanh và Bộ Tỏng tham mưu Liên Xô vẫn không hài lòng về sự tồn tại của hành lang Tukums - Riga và hành lang Kurlandia do quân Đức chiếm giữ. Các hành lang đó tuy hẹp nhưng vẫn đủ để quân Đức cơ động lực lượng và khi cần thiết, có thể rút Cụm tập đoàn …

**Bài:** Chiến dịch Vilnius (10,100 âm tiết), cửa sổ ở 6% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo báo cáo của Ya. Erdmana, quân đội Krayova ở địa phương đã tiến hành bao nhiêu hoạt động chống lại du kích Liên Xô từ tháng 1 năm 1942 đến tháng 7 năm 1944?  
**Đáp án sinh:** 81 hoạt động  
**Kiểm:** 81 hoạt động (F1 1.0)  
**Cửa sổ (rút gọn):** Mùa hè năm 1944, quân đội Krayova phát triển lên đến 380.000 người, trong đó có hơn 10.000 sĩ quan, hoạt động trên một phạm vi rất rộng từ Latvia, Litva, Tây Byelorussia, Tây Bắc Ukraina và trong nội địa Ba Lan. Theo báo cáo của Ya. Erdmana, bí thư huyện ủy bí mật của quận Novogrudok, từ tháng 1 năm 1942 đến tháng 7 năm 1944, quân đội Krayova ở địa…

**Bài:** Chiến dịch Vilnius (10,100 âm tiết), cửa sổ ở 86% bài  
**Trạng thái:** kept  
**Câu hỏi:** Aleksander Krzyżanowski bị trục xuất về Ba Lan vào thời điểm nào?  
**Đáp án sinh:** tháng 10 năm 1947  
**Kiểm:** tháng 10 năm 1947 (F1 1.0)  
**Cửa sổ (rút gọn):** Aleksander Krzyżanowski từ chối và tướng I. Chernyakhovsky cho ông ta về để suy nghĩ lại sau khi hứa rằng sẽ cung cấp cho quân Ba Lan vũ khí với điều kiện họ phải đứng về phía quân đội Liên Xô. Ngày 16 tháng 7, Aleksander Krzyżanowski đến gặp tướng I. Chernyakhovsky và vẫn giữ lập trường bất hợp tác với quân đội Liên Xô. Ngày 17 tháng 7, tướng V. A…

**Bài:** Chiến dịch Vilnius (10,100 âm tiết), cửa sổ ở 93% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà xuất bản nào đã phát hành cuốn sách 'Nhớ lại và suy nghĩ'?  
**Đáp án sinh:** Nhà xuất bản Quân đội nhân dân  
**Kiểm:** Nhà xuất bản Quân đội nhân dân (F1 1.0)  
**Cửa sổ (rút gọn):** The Secret War against Soviet Russia. — Boston: Brown & Co, 1946 Tippelskirch K., Geschichte des Zweiten Weltkrieges. — Hamburg: Holsten Verlag, 1956. Schriftenreihe der Vierteljahrshefte für Zeitgeschichte, vol. — М.: Воениздат МВС СССР, 1952. — М.: Высшая школа., 1992. Волков, Федор Дмитриевич, За кулисами второй мировой войны. От первого дня до …

**Bài:** Chiến dịch Vilnius (10,100 âm tiết), cửa sổ ở 70% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân nào được giao nhiệm vụ chủ công trên hướng phụ Lida trong chiến dịch Vilnius?  
**Đáp án sinh:** Tập đoàn quân 31  
**Kiểm:** Tập đoàn quân 31 (F1 1.0)  
**Cửa sổ (rút gọn):** Trong chiến dịch Vilnius, hướng Lida được coi là hướng phụ cùng với hướng tấn công đến Alitus của Tập đoàn quân cận vệ 11. Binh lực của quân Đức trên hướng này chỉ còn lại vài trung đoàn SS bảo vệ hậu cứ, các đơn vị cảnh sát, các đơn vị hậu cần, vận tải cùng tàn quân Đức từ Minsk và Bobruysk kéo về. Trên hướng phụ công này, Tập đoàn quân 31 được gi…

**Bài:** Chiến dịch Vilnius (10,100 âm tiết), cửa sổ ở 91% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Cuốn sách 'Soviet Blitzkrieg: The Battle for White Russia' được xuất bản vào năm nào?  
**Đáp án sinh:** 1944  
**Kiểm:** 2000 (F1 0.0)  
**Cửa sổ (rút gọn):** Hơn 300 người khác được đưa vào diện cần điều tra. Quân đội Quốc gia Ba Lan Soviet Blitzkrieg: The Battle for White Russia, 1944, Lynne Riener, 2000, ISBN 978-1-55587-880-1 Belorussia 1944 - the Soviet General Staff Study Borodziej: The Warsaw Uprising of 1944. Sayers, Michael, Kahn Albert E. The Secret War against Soviet Russia. — Boston: Brown & …

**Bài:** Chiến dịch Vilnius (10,100 âm tiết), cửa sổ ở 65% bài  
**Trạng thái:** answer_not_verbatim  
**Câu hỏi:** Sư đoàn xe tăng 12 (Đức) bị chặn lại ở vị trí nào vào chiều ngày 13 tháng 7?  
**Đáp án sinh:** cách phía Đông Rykolty 6 km  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Đến trưa, Sư đoàn xe tăng 5 (Đức) buộc phải dừng lại và gọi không quân hỗ trợ. Tuy nhiên, cũng giống như ở Vilnius trước đó mấy ngày, các máy bay tấn công mặt đất Ju-87 của không quân Đức vẫn bị các máy bay tiêm kích Yak-3 và La-5 của không quân Liên Xô bắn hạ trước khi kịp ném bom. Không có xe tăng yểm hộ, Sư đoàn bộ binh 1 (Đức) không dám tiến cô…

**Bài:** Chiến dịch Vilnius (10,100 âm tiết), cửa sổ ở 91% bài  
**Trạng thái:** kept  
**Câu hỏi:** Từ năm 1979 đến năm 1996, tổng cộng có bao nhiêu phần tử thân phát xít Đức bị tước quốc tịch Hoa Kỳ?  
**Đáp án sinh:** 107  
**Kiểm:** 107 (F1 1.0)  
**Cửa sổ (rút gọn):** Một cựu thành viên khác người Litva của lực lượng dân cảnh SS Vilnius là Aleksandras Lileikis cũng bị cơ quan OSI phát hiện và bị Tòa án liên bang tại Boston ra lệnh tước quốc tịch Hoa Kỳ. Tổng cộng từ năm 1979 đến năm 1996, đã có 107 phần tử thân phát xít Đức bị tước quốc tịch Hoa Kỳ, trong dó có 48 người bị trục xuất khỏi Hoa Kỳ. Hơn 300 người kh…

**Bài:** Chiến dịch Vilnius (10,100 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** answer_not_verbatim  
**Câu hỏi:** Quân đoàn xe tăng 29 được bố trí ở vị trí nào so với Vilnius?  
**Đáp án sinh:** phía Tây Vilnius 10 km, trên bờ Nam sông Vilya  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Quân Đức có 150 xe tăng và pháo tự hành, khoảng hơn 400 pháo mặt đất, dự định tiến cong thành hai mũi dọc theo bờ Bắc và bờ Nam sông Vilya vào Vilnius. Phương diện quân Byelorussia 3 không bất ngờ trước chiến dịch phản công của quân Đức. Chiều 11 tháng 7, các cuộc chuyển quân của các sư đoàn xe tăng Đức lập tức bị các máy bay trinh sát của Tập đoàn…

**Bài:** Dàn trống (12,607 âm tiết), cửa sổ ở 45% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thiết bị nào được mô tả là bộ điều khiển hiệu suất MIDI được sử dụng rộng rãi thứ hai chỉ sau bàn phím điện tử?  
**Đáp án sinh:** Đệm trống điện tử  
**Kiểm:** Đệm trống điện tử (F1 1.0)  
**Cửa sổ (rút gọn):** Một dàn trống điện tử hoàn toàn cũng dễ kiểm tra âm thanh hơn trống âm hưởng vì mô-đun trống điện tử có các cấp độ mà tay trống đã đặt sẵn trong phòng tập của mình; Ngược lại, khi một dàn trống âm hưởng được kiểm tra âm thanh, hầu hết các trống và chũm chọe cần phải được thu vào mic và từng mic phải được kiểm tra bởi tay trống, giai điệu và cân bằn…

**Bài:** Dàn trống (12,607 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trong nhạc rock, tay trống thường đứng khi chơi thay vì ngồi trên loại ghế nào?  
**Đáp án sinh:** ghế đẩu  
**Kiểm:** ghế đẩu (F1 1.0)  
**Cửa sổ (rút gọn):** Vì vậy, nhiều dàn trống đắt tiền cho các tay trống chuyên nghiệp được bán với rất ít hoặc thậm chí không có phần cứng để cho phép tay trống chọn chân đỡ và cả bàn đạp trống trầmmà anh ta thích. Ở một thái cực khác, nhiều dàn trống rẻ tiền cho người mới được bán dưới dạng một dàn năm phần hoàn chỉnh cùng với hai chân đỡ chữm chọe, một chiếc ghế đẩu …

**Bài:** Dàn trống (12,607 âm tiết), cửa sổ ở 22% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Trong bối cảnh dàn trống, thuật ngữ breakables đề cập đến những thành phần nào?  
**Đáp án sinh:** bất kỳ thành phần cơ bản nào mà tay trống "khách" dự kiến sẽ mang lại  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Dùi trống, trống bẫy và chũm chọe, và đôi khi các thành phần khác, thường được tráo đổi, mỗi tay trống mang theo mình. Thuật ngữ breakables trong bối cảnh này đề cập đến bất kỳ thành phần cơ bản nào mà tay trống "khách" dự kiến sẽ mang lại. Những cân nhắc tương tự được áp dụng nếu sử dụng "dàn trống gia đình" (một dàn trống thuộc sở hữu bởi một địa…

**Bài:** Dàn trống (12,607 âm tiết), cửa sổ ở 25% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Trống bẫy được ví như bộ phận nào của dàn trống, đặc biệt là trong nhạc rock?  
**Đáp án sinh:** "trái tim" của dàn trống  
**Kiểm:** trái tim (F1 0.0)  
**Cửa sổ (rút gọn):** Trống trầm là loại trống có cao độ trầm nhất, cung cấp nhịp cơ bản hoặc yếu tố thời gian với các mẫu xung cơ bản. Một số tay trống có thể sử dụng hai hay nhiều trống trầm, cũng có thể sử dụng một bàn đạp đôi với một trống trầm. Trống trầm đôi là kỹ thuật quan trọng trong thể loại nhạc heavy metal. Sử dụng bàn đạp trống trầm đôi cho phép tay trống c…

**Bài:** Dàn trống (12,607 âm tiết), cửa sổ ở 46% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thiết bị nào được mô tả là bộ điều khiển hiệu suất MIDI được sử dụng rộng rãi thứ hai chỉ sau bàn phím điện tử?  
**Đáp án sinh:** Đệm trống điện tử  
**Kiểm:** Đệm trống điện tử (F1 1.0)  
**Cửa sổ (rút gọn):** Cuối cùng, kỹ sư cần thiết lập một hỗn hợp màn hình cho tay trống để nghe nhạc cụ của anh ta, các nhạc cụ khác và giọng hát của phần còn lại của ban nhạc. Với một dàn trống điện tử, nhiều bước trong số này có thể được giản lược đi. Việc sử dụng thiết bị trống điện tử của tay trống có thể từ việc bổ sung một miếng đệm điện tử vào một dàn trống âm hư…

**Bài:** Dàn trống (12,607 âm tiết), cửa sổ ở 72% bài  
**Trạng thái:** kept  
**Câu hỏi:** Dùi trống truyền thống thường được làm từ chất liệu gì?  
**Đáp án sinh:** gỗ  
**Kiểm:** gỗ (F1 1.0)  
**Cửa sổ (rút gọn):** Một trống bẫy phụ thường được đặt ở bên trái của tay trống (đối diện với trống đúp da sàn và bên trái hi-hat). Trống bẫy phụ được sử dụng tương tự như chũm chọe hiệu ứng, tức là khi cần thêm âm thanh khác. Nói chung, chỉ có một trống bẫy được sử dụng trong dàn, nếu có. Nhiều trống trầm, ngoài thiết lập trống trầm kép Trống cồng (trống trầm một đầu,…

**Bài:** Dàn trống (12,607 âm tiết), cửa sổ ở 36% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hiệu ứng được tạo ra bằng cách đánh một chiếc hi-hat mở và sau đó đóng các chũm chọe lại bằng bàn đạp được sử dụng rộng rãi trong những thể loại nhạc nào?  
**Đáp án sinh:** vũ trường và nhạc funk  
**Kiểm:** vũ trường và nhạc funk (F1 1.0)  
**Cửa sổ (rút gọn):** Khả năng tạo ra nhịp điệu trên những chiếc hi-hat chỉ với chân cho phép người chơi trống sử dụng cả hai dùi trên những chiếc trống hoặc chũm chọe khác. Các âm thanh khác nhau có thể được tạo ra bằng cách nhấn "hi-hat mở" (bàn đạp không bị đè xuống, tạo ra âm thanh ồn ào có biệt danh là "hi-hat cẩu thả") hoặc âm thanh "hi-hat đóng" sắc nét (với bàn …

**Bài:** Dàn trống (12,607 âm tiết), cửa sổ ở 1% bài  
**Trạng thái:** kept  
**Câu hỏi:** Dàn trống được chơi khi tay trống ngồi trên vật dụng nào?  
**Đáp án sinh:** chiếc ghế trống (throne)  
**Kiểm:** một chiếc ghế trống (throne) (F1 0.89)  
**Cửa sổ (rút gọn):** Chúng được phân loại là bộ gõ không có âm vực, cho phép âm nhạc được ghi lại bằng cách sử dụng ký hiệu bộ gõ, trong đó tồn tại một hình thức bán chuẩn cho cả dàn trống và trống điện tử. Dàn trống được chơi khi tay trống ngồi trên một chiếc ghế trống (throne). Trong khi nhiều nhạc cụ như guitar hoặc dương cầm có khả năng thực hiện các giai điệu và h…

**Bài:** Chiến dịch Lublin–Brest (11,222 âm tiết), cửa sổ ở 17% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân 65 do ai chỉ huy?  
**Đáp án sinh:** trung tướng P. Batov  
**Kiểm:** trung tướng P. Batov (F1 1.0)  
**Cửa sổ (rút gọn):** Thiết giáp: 1 trung đoàn xe bọc thép. Tập đoàn quân 65 do trung tướng P. Batov chỉ huy, thành phần gồm có: Bộ binh: 2 quân đoàn và 2 sư đoàn. Tổng cộng 8 sư đoàn và 1 lữ đoàn. Pháo binh: 1 lữ đoàn pháo nòng dài, 4 lữ đoàn lựu pháo, 1 lữ đoàn và 1 trung đoàn và 1 trung đoàn pháo chống tăng, 2 trung đoàn súng cối, 1 sư đoàn và 1 trung đoàn phòng khôn…

**Bài:** Chiến dịch Lublin–Brest (11,222 âm tiết), cửa sổ ở 19% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân Ba Lan 1 do ai chỉ huy?  
**Đáp án sinh:** thượng tướng Zygmunt Henryk Berling  
**Kiểm:** thượng tướng Zygmunt Henryk Berling (F1 1.0)  
**Cửa sổ (rút gọn):** Kolpakchi chỉ huy, thành phần gồm có: Bộ binh: 3 quân đoàn gồm 9 sư đoàn. Pháo binh: 1 lữ đoàn lựu pháp, 3 lữ đoàn và 1 trung đoàn pháo chống tăng, 1 lữ đoàn và 1 trung đoàn súng cối, 1 sư đoàn và 1 trung đoàn phòng không. Thiết giáp, 1 lữ đoàn và 3 trung đoàn pháo tự hành.Tập đoàn quân 70 do trung tướng P. Lyapin chỉ huy, thành phần gồm có: Bộ bin…

**Bài:** Chiến dịch Lublin–Brest (11,222 âm tiết), cửa sổ ở 34% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người chỉ huy Tập đoàn quân 2?  
**Đáp án sinh:** tướng Walter Weiss  
**Kiểm:** tướng Walter Weiss (F1 1.0)  
**Cửa sổ (rút gọn):** Một phần Tập đoàn quân 4 (tái lập) do tướng Friedrich Hoßbach chỉ huy. Biên chế từ tháng 8 năm 1944 có: Quân đoàn bộ binh 6 (tái lập) do trung tướng Horst Großmann chỉ huy, thành phần gồm có: Sư đoàn bộ binh 50 của thiếu tướng Georg Haus, gồm các trung đoàn bộ binh 121, 122, 123, Trung đoàn pháo binh 150, Trung đoàn pháo chống tăng 50, các tiểu đoà…

**Bài:** Chiến dịch Lublin–Brest (11,222 âm tiết), cửa sổ ở 42% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Thống chế Walter Model đặt hy vọng vào các cụm phòng ngự mạnh ở những địa điểm nào để hãm đà tấn công của quân đội Liên Xô?  
**Đáp án sinh:** Brest, Kobrin, Cheremkha (Czeremcha) ở phía bắc và Volodava (Wlodawa), Khelm (Chelm), Lyublin ở phía nam  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** và các tuyến phòng ngự thứ hai, thứ ba trong chiều sâu đến tuyến sông Oder cần có thời gian nhưng thời gian lại đang chống lại cả hai bên. Do đó, thống ché Walter Model đặt hi vọng vào các cụm phòng ngự mạnh ở Brest, Kobrin, Cheremkha (Czeremcha) ở phía bắc và Volodava (Wlodawa), Khelm (Chelm), Lyublin ở phía nam để hãm dà tấn công của quân Đội Liê…

**Bài:** Chiến dịch Lublin–Brest (11,222 âm tiết), cửa sổ ở 42% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào thời điểm nào 5 tập đoàn quân của Phương diện quân Byelorussia 1 đồng loạt nổ súng tấn công tại khu vực cánh phải của Phương diện quân?  
**Đáp án sinh:** 5 giờ 30 phút ngày 18 tháng 7  
**Kiểm:** 5 giờ 30 phút ngày 18 tháng 7 (F1 1.0)  
**Cửa sổ (rút gọn):** Trước và trong thời gian diễn ra chiến dịch, 12 sư đoàn Đức đã được điều động đến hướng Wisla - Narev, 15 sư đoàn Đức bại trận trong giai đoạn 1 và giai đoạn 2 của Chiến dịch Bagration được phục hồi bằng những tân binh sinh từ năm 1926 trở về trước. Lực lượng SS và lực lượng mặt đất của không quân Đức Quốc xã cũng tái trang bị và tổ chức mới nhiều …

**Bài:** Chiến dịch Lublin–Brest (11,222 âm tiết), cửa sổ ở 46% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thống chế Walter Model đã điều sư đoàn nào từ mặt trận Romania đến trấn giữ tại tuyến sông Tây Bug?  
**Đáp án sinh:** Sư đoàn xe tăng 14  
**Kiểm:** Sư đoàn xe tăng 14 (F1 1.0)  
**Cửa sổ (rút gọn):** Các nguyên soái Liên Xô G. Rokossovsky đã lên đài quan sát của tướng V. Kazakov, chỉ huy pháo binh của Phương diện quân Byelorussia 1 để chỉ đạo các trận đánh. Để tăng cường phòng thủ trên hướng này, thống chế Walter Model đã điều Sư đoàn xe tăng 14 vừa từ mặt trận Romania chuyển đến tới trấn giữ tại tuyến sông Tây Bug, đoạn đi qua Domachyevo (Dama…

**Bài:** Chiến dịch Lublin–Brest (11,222 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chính phủ Phần Lan đã tuyên bố chấm dứt liên minh với nước Đức Quốc xã và rút khỏi cuộc chiến với Liên Xô vào ngày nào?  
**Đáp án sinh:** Ngày 15 tháng 9  
**Kiểm:** Ngày 15 tháng 9 (F1 1.0)  
**Cửa sổ (rút gọn):** Ít nhất thì về hình thức chính trị, Moskva giữ đúng nguyên tắc tôn trọng quyền dân tộc tự quyết. Liên Xô không cho phép thành lập một chính phủ cánh tả Ba Lan ở Moskva nhưng họ lại giúp những người cánh tả Ba Lan ở Liên Xô lập ra quân đội của mình, giúp phát triển và trang bị cho quân đội này tương đương với một tập đoàn quân của Liên Xô. Trong chỉ…

**Bài:** Chiến dịch Lublin–Brest (11,222 âm tiết), cửa sổ ở 12% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người chỉ huy Tập đoàn quân 47?  
**Đáp án sinh:** trung tướng N. Gusev  
**Kiểm:** trung tướng N. Gusev (F1 1.0)  
**Cửa sổ (rút gọn):** Radziyevskiy chỉ huy thành phần gồm có: Quân đoàn xe tăng 3 gồm các lữ đoàn xe tăng 50, 51, 103; Lữ đoàn cơ giới 57; các trung đoàn pháo tự hành 1107, 1219; Trung đoàn súng cối 234; Tiểu đoàn cơ giới 74; Tiểu đoàn súng phun lửa 728; Tiểu đoàn mô tô cận vệ 126; Trung đoàn phòng không 121 Quân đoàn xe tăng 16 gồm các lữ đoàn xe tăng 107, 109, 164; Lữ…

**Bài:** Chất thải phóng xạ (9,764 âm tiết), cửa sổ ở 52% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chiến dịch Morris hiện là điểm lưu trữ chất thải phóng xạ cấp cao duy nhất ở quốc gia nào?  
**Đáp án sinh:** Hoa Kỳ  
**Kiểm:** Hoa Kỳ (F1 1.0)  
**Cửa sổ (rút gọn):** Chôn sâu địa chất hiện vẫn là cách duy nhất để xử lý trọn vẹn chất thải hạt nhân cấp cao. Chiến dịch Morris hiện là điểm lưu trữ chất thải phóng xạ cấp cao duy nhất ở Hoa Kỳ. Chất thải siêu urani Chất thải siêu urani (CTSU) là một phân loại chất thải được dùng ở Hoa Kỳ. Luật pháp Mỹ định nghĩa CTSU là chất thải có chứa hạt nhân siêu urani phóng xạ …

**Bài:** Chất thải phóng xạ (9,764 âm tiết), cửa sổ ở 95% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo phát biểu của Fujimura, hầu hết các hợp chất hạt nhân trong chất thải đã được xử lý như thế nào?  
**Đáp án sinh:** đúng cách  
**Kiểm:** đúng cách (F1 1.0)  
**Cửa sổ (rút gọn):** Nhật Bản có thỏa luận với IAEA về lượng urani và plutoni giàu rất lớn, phát hiện trong chất thải hạt nhân bị bỏ đi từ những nhà máy này. Tại buổi họp báo Fujimura nói rằng: "Dựa trên những cuộc điều tra đã có, hầu hết các hợp chất hạt nhân đều đã được xử lý đúng cách, và từ góc nhìn đó, không có vấn đề gì trong công tác bảo đảm an toàn." Nhưng theo…

**Bài:** Chất thải phóng xạ (9,764 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Theo các cơ quan quản lý, nguy cơ gây ung thư do tiếp xúc với bức xạ ion hóa có mối quan hệ như thế nào với liều lượng?  
**Đáp án sinh:** tỉ lệ với liều lượng  
**Kiểm:** tỉ lệ với liều lượng ngay cả với liều lượng thấp (F1 0.62)  
**Cửa sổ (rút gọn):** Năng lượng và dạng của bức xạ ion hóa phát ra bởi chất phóng xạ cũng đóng vai trò quan trọng trong việc xác định sự nguy hiểm của nó với con người. Tính chất hóa học của nguyên tố phóng xạ quyết định tính di động của hợp chất đó cũng như khả năng lan ra môi trường và đầu độc con người. Không chỉ thế, nhiều đồng vị phóng xạ không phân rã ngay thành …

**Bài:** Chất thải phóng xạ (9,764 âm tiết), cửa sổ ở 6% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo các cơ quan quản lý, nguy cơ gây ung thư do tiếp xúc với bức xạ ion hóa có mối quan hệ như thế nào với liều lượng?  
**Đáp án sinh:** tỉ lệ với liều lượng ngay cả với liều lượng thấp  
**Kiểm:** tỉ lệ với liều lượng ngay cả với liều lượng thấp (F1 1.0)  
**Cửa sổ (rút gọn):** Tiếp xúc với chất thải phóng xạ có thể làm hại, thậm chí là chết. Với con người, một lượng 1 [[Sievert (đơn vị) |sievert]] có 5.5% nguy cơ gây ung thư, và các cơ quan quản lý cho rằng nguy cơ này tỉ lệ với liều lượng ngay cả với liều lượng thấp. Bức xạ ion hóa có thể xóa các đoạn mã trong nhiễm sắc thể. Một sinh vật đang phát triển như bào thai bị …

**Bài:** Chất thải phóng xạ (9,764 âm tiết), cửa sổ ở 41% bài  
**Trạng thái:** kept  
**Câu hỏi:** Đuôi quặng urani thường chứa những chất phóng xạ nào?  
**Đáp án sinh:** radi, thori và dấu vết của urani  
**Kiểm:** radi, thori và dấu vết của urani (F1 1.0)  
**Cửa sổ (rút gọn):** Đuôi quặng urani cũng chứa kim loại nặng nguy hiểm hóa học như chì và asen. Những gò đuôi quặng rộng lớn hiện diện ở nhiều địa điểm khai thác cũ, nhất là ở các bang Colorado, New Mexico, và Utah của Hoa Kỳ. Tuy đuôi quặng urani không có tính phóng xạ cao, chúng có chu kỳ bán rã dài. Chúng thường chứa radi, thori và dấu vết của urani. Chất thải cấp …

**Bài:** Chất thải phóng xạ (9,764 âm tiết), cửa sổ ở 25% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trong quá khứ, tác nhân kích hoạt neutron cho bom nguyên tử thường là beryli và chất phóng xạ alpha mạnh nào?  
**Đáp án sinh:** poloni  
**Kiểm:** poloni (F1 1.0)  
**Cửa sổ (rút gọn):** Trong các lò phản ứng nhanh tích hợp, phần plutoni và urani riêng biệt chứa tạp chất là các Actini và không thể dùng làm vũ khí hạt nhân. Tháo dỡ vũ khí hạt nhân Chất thải từ việc tháo dỡ vũ khí hạt nhân hiếm khi chứa phóng xạ beta hay gamma ngoại trừ triti và americi. Nhiều khả năng nó chỉ có các actini phóng xạ alpha như Pu-239, một vật liệu phân…

**Bài:** Chất thải phóng xạ (9,764 âm tiết), cửa sổ ở 23% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tạp chất nào trong plutoni phân rã nhanh hơn Pu-239?  
**Đáp án sinh:** Pu-240  
**Kiểm:** Pu-240 (F1 1.0)  
**Cửa sổ (rút gọn):** Tạp chất Pu-240 phân rã nhanh hơn Pu-239, làm chất lượng của vật liệu tăng dần theo thời gian (trong khi số lượng của nó giảm theo thời gian). Vì thế, một số ý kiến cho rằng, khi thời gian trôi, những khu vực lưu trữ có nguy cơ trở thành "mỏ plutoni", từ đó vật liệu cho vũ khí hạt nhân có thể thu được tương đối dễ dàng. Những ý kiến phản bác chỉ ra…

**Bài:** Chất thải phóng xạ (9,764 âm tiết), cửa sổ ở 89% bài  
**Trạng thái:** kept  
**Câu hỏi:** Băng nhóm mafia nào bị các nhà chức trách Ý điều tra vì vận chuyển và vứt bỏ trái phép chất thải hạt nhân?  
**Đáp án sinh:** 'Ndrangheta  
**Kiểm:** 'Ndrangheta (F1 1.0)  
**Cửa sổ (rút gọn):** Các nhà chức trách Ý đang điều tra băng nhóm mafia 'Ndrangheta bị buộc tội vận chuyển và vứt bỏ trái phép chất thải hạt nhân. Theo một whistleblower, một quản lý của cơ quan nghiên cứu năng lượng quốc gia của Ý, Enea, đã trả tiền cho nhóm để vứt 600 thùng phuy chứa chất thải phóng xạ và độc hại từ Ý, Thụy Sĩ, Pháp, Đức và Mỹ, đến Somalia, nơi chất …

**Bài:** Phi tần (13,534 âm tiết), cửa sổ ở 49% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Theo lệ định đương thời, 8 cung nữ có nhan sắc cùng phẩm hạnh được tuyển chọn trước đại hôn để dạy các bí thuật phòng the được gọi là gì?  
**Đáp án sinh:** Tư trướng (司帳), Tư tẩm (司寝), Tư nghi (司儀), Tư môn (司門)  
**Kiểm:** Tư trướng, Tư tẩm, Tư nghi, Tư môn (F1 0.5)  
**Cửa sổ (rút gọn):** Dưới hàng phi tần còn có Quan nữ tử (官女子), còn gọi Cung nữ tử, là các cung nữ được Hoàng đế lâm hạnh hoặc danh vị để gọi các phi tần bị giáng chức (như Mân Quý phi Từ Giai thị của Hàm Phong Đế). Ngoài ra, các Thị tỳ được lâm hạnh và sinh dục của các Hoàng tử cũng được gọi chung là Quan nữ tử, bên cạnh danh xưng thường thấy là Cách cách. Chiểu theo …

**Bài:** Phi tần (13,534 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Đại Việt thông sử, các bà Cung Từ, Tuyên Từ, Quang Thục và Huy Gia đều được tôn hiệu do nguyên nhân nào?  
**Đáp án sinh:** tự quân lên nối ngôi  
**Kiểm:** tự quân lên nối ngôi (F1 1.0)  
**Cửa sổ (rút gọn):** Người em là Đôn Từ (惇慈), được kén làm Sung viên (充媛), sinh ra Duệ Tông, sau được sách tặng Quang Hiến Thần phi (光憲宸妃). Các vua Nhà Lê sơ thường vì e ngại ngoại thích mà không lập Hoàng hậu, chỉ lấy bậc Quý phi đứng đầu giúp việc nội trị. Trong Đại Việt thông sử có đoạn viết: "Triều Lê ta gia pháp thuận đạo cương thường, kén chọn phi tần tất lấy con…

**Bài:** Phi tần (13,534 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo chỉ dụ năm Minh Mạng thứ 17, ngôi vị nào được đặt ra để giúp Hoàng hậu cai quản mẫu mực sáu viện và giữ nghiêm nội chính?  
**Đáp án sinh:** Hoàng quý phi  
**Kiểm:** Hoàng quý phi (F1 1.0)  
**Cửa sổ (rút gọn):** [Tam sung; 三充]: Sung nghi (充儀), Sung dung (充容), Sung viên (充媛). [Lục chức; 六職]: Tiệp dư (婕妤), Dung hoa (傛華), Nghi nhân (宜人), Tài nhân (才人), Linh nhân (靈人), Lương nhân (良人); Chữ "Quốc sơ" này hay có nhìn nhận là đầu thời Gia Long, song theo nhiều biểu hiện nó ám chỉ khoảng đầu thời Chúa Nguyễn. Một điều chứng minh khác, là dưới triều Gia Long và Min…

**Bài:** Phi tần (13,534 âm tiết), cửa sổ ở 92% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo danh sách các phi tần nổi tiếng, người phụ nữ nào được liệt kê dưới thời Hán Thành Đế?  
**Đáp án sinh:** Ban Tiệp dư, Triệu Hợp Đức  
**Kiểm:** Ban Tiệp dư, Triệu Hợp Đức (F1 1.0)  
**Cửa sổ (rút gọn):** Nhân Tổ: Phế Quý nhân Triệu thị. Cao Tông: Thuần Hiến Hoàng quý phi. Chu U Vương: Bao Tự Tấn Hiến công: Ly Cơ. Tần Huệ Văn vương: Mị Bát tử. Hán Cao Tổ: Thích phu nhân, Bạc phu nhân. Hán Cảnh Đế: Lịch Cơ. Hán Vũ Đế: Lý phu nhân. Hán Nguyên Đế: Phó Chiêu nghi, Phùng Viện, Vương Chiêu Quân. Hán Thành Đế: Ban Tiệp dư, Triệu Hợp Đức. Trần Hậu Chủ: Trươ…

**Bài:** Phi tần (13,534 âm tiết), cửa sổ ở 22% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo điển lệ từ đời Hán, Tấn, Văn Đế đã đặt chức nữ quan nào cùng Lục ti để chuyên giáo hóa điển phạm trong hậu cung?  
**Đáp án sinh:** Lục thượng  
**Kiểm:** Lục thượng (F1 1.0)  
**Cửa sổ (rút gọn):** Bên cạnh đó, Văn Đế lại theo điển lệ từ đời Hán, Tấn mà đặt chức nữ quan gọi là Lục thượng (六尚), cùng Lục ti (六司), chuyên giáo hóa điển phạm trong hậu cung. Nhân Thọ năm thứ 2 (602), Văn Hiến Hoàng hậu qua đời, nhà vua sa vào mỹ sắc, từ cung cấm chọn ra những bậc tài sắc ban phong các chức phi tần: Quý nhân (貴人), 3 người. Thế phụ (世婦), 27 người. Ng…

**Bài:** Phi tần (13,534 âm tiết), cửa sổ ở 49% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo quy định của Thái Tổ, mẹ vua được gọi là gì?  
**Đáp án sinh:** Vương đại phi  
**Kiểm:** Vương đại phi (F1 1.0)  
**Cửa sổ (rút gọn):** Còn từ bậc Quý nhân đến Đáp ứng không hạn định, quy định để tu tâm dưỡng tính, cần tu nội chức, riêng Quan nữ tử chỉ những cung nữ được sủng hạnh. Phi tần được tuyển chọn từ những Tú nữ (秀女) tham gia tuyển tú hoặc con gái các dòng dõi công thần, gọi là Bát Kỳ tuyển tú, hoặc từ cung nữ tấn phong đi lên. Nội mệnh phụ nhà Triều Tiên ban đầu xếp đặt th…

**Bài:** Phi tần (13,534 âm tiết), cửa sổ ở 19% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Tùy thư, nguyên nhân nào khiến Vũ Đế triều Trần ít dịp được gần gũi phi tần?  
**Đáp án sinh:** do bà nguyên phối có tính ghen tuông  
**Kiểm:** bà nguyên phối có tính ghen tuông (F1 0.93)  
**Cửa sổ (rút gọn):** Tài nhân (才人), vị ngang Phò mã Đô úy (駙馬都尉). Năm Vĩnh Minh nguyên niên, Vũ Đế nghe theo Lễ tư tấu thỉnh, thiết lập vị trí Quý phi (貴妃), cũng đem Thục phi từ Cửu tần ra thành độc lập, tăng thêm đãi ngộ của cả hai tước vị này, ngang với Tam tư (三司). Năm thứ 7, triều đình thêm Chiêu dung (昭容) vào Cửu tần, bổ khuyết vị trí cũ của Thục phi. Vũ Đế khai t…

**Bài:** Phi tần (13,534 âm tiết), cửa sổ ở 80% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hậu cung của Đế quốc Ottoman được gọi là gì?  
**Đáp án sinh:** Harem-i Hümâyûn  
**Kiểm:** Harem-i Hümâyûn (F1 1.0)  
**Cửa sổ (rút gọn):** Ba loại này đều do triều đình (hoặc tự người con) sẽ cấp lương nuôi sống. Một loại nữa là có thể thả về nhà, khi ấy có mất đi vì lý do gì, triều đình cũng không quản việc mai táng. Quốc vương của Vương quốc Thái Lan cũng có thiết lập chế độ tước vị riêng cho hậu cung của Ngài. Trong hậu cung, Vương hậu là tước vị tôn quý nhất, nhưng lại có hai cấp …

**Bài:** Vương nữ Margaret, Bá tước phu nhân xứ Snowdon (9,529 âm tiết), cửa sổ ở 36% bài  
**Trạng thái:** kept  
**Câu hỏi:** Margaret sẽ có thể kết hôn trong một năm nếu Quốc hội không ngăn cản bà sau khi thông báo cho cơ quan nào?  
**Đáp án sinh:** Hội đồng Cơ mật của Vương quốc Anh  
**Kiểm:** Hội đồng Cơ mật của Vương quốc Anh (F1 1.0)  
**Cửa sổ (rút gọn):** Margaret không sở hữu khối tài sản lớn của chị gái và sẽ cần khoản trợ cấp 6,000 bảng Anh mỗi năm và 15,000 bảng phụ cấp mà Quốc hội cung cấp cho bà khi có một cuộc hôn nhân phù hợp. Bà không phản đối việc bị loại khỏi hàng ngũ kế vị ngai vàng bởi Nữ vương và tất cả các người con của bà vẫn sẽ sống tốt, nhưng việc nhận được sự chấp thuận của quốc h…

**Bài:** Vương nữ Margaret, Bá tước phu nhân xứ Snowdon (9,529 âm tiết), cửa sổ ở 7% bài  
**Trạng thái:** kept  
**Câu hỏi:** Margaret được làm lễ rửa tội bởi ai?  
**Đáp án sinh:** Cosmo Lang, Tổng Giám mục Canterbury  
**Kiểm:** Cosmo Lang, Tổng Giám mục Canterbury (F1 1.0)  
**Cửa sổ (rút gọn):** Mẹ bà là Công tước phu nhân xứ York (sau này là Vương hậu Elizabeth), con gái út của một quý tộc người Scotland Claude Bowes-Lyon, Bá tước thứ 14 xứ Strathmore và Kinghorne. Công tước phu nhân xứ York ban đầu muốn đặt tên cho cô con gái thứ hai của mình là Ann Margaret, khi bà giải thích với Vương hậu Mary trong một bức thư "Con rất nóng lòng muốn …

**Bài:** Vương nữ Margaret, Bá tước phu nhân xứ Snowdon (9,529 âm tiết), cửa sổ ở 47% bài  
**Trạng thái:** kept  
**Câu hỏi:** Váy cưới của Margaret được thiết kế bởi ai?  
**Đáp án sinh:** Norman Hartnell  
**Kiểm:** Norman Hartnell (F1 1.0)  
**Cửa sổ (rút gọn):** Margaret kết hôn với Armstrong-Jones tại Tu viện Westminster vào ngày 6 tháng 5 năm 1960. Buổi lễ là đám cưới hoàng gia đầu tiên được phát sóng trên truyền hình, thu hút 300 triệu lượt xem trên toàn thế giới. Tổng cộng, 2.000 khách mời đã được mời đến dự lễ cưới. Váy cưới của Margaret được thiết kế bởi Norman Hartnell và bà đã diện bộ váy cùng với …

**Bài:** Vương nữ Margaret, Bá tước phu nhân xứ Snowdon (9,529 âm tiết), cửa sổ ở 27% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Craig Brown, Townsend đã yêu cầu phòng ngủ bên cạnh phòng ngủ của ai trong chuyến đi đến Belfast vào tháng 10 năm 1947?  
**Đáp án sinh:** bà  
**Kiểm:** bà (F1 1.0)  
**Cửa sổ (rút gọn):** Nhà sử học Craig Brown nói rằng, theo một người phụ trách National Trust, Townsend đã yêu cầu phòng ngủ bên cạnh phòng ngủ của bà trong chuyến đi đến Belfast vào tháng 10 năm 1947. Ngoài ra, có giả thuyết cho rằng mối quan hệ của họ bắt đầu vào khoảng năm 1951. Townsend nói rằng tình yêu của ông dành cho bà bắt đầu vào tháng 8 năm 1951, khi Vương n…

**Bài:** Vương nữ Margaret, Bá tước phu nhân xứ Snowdon (9,529 âm tiết), cửa sổ ở 80% bài  
**Trạng thái:** kept  
**Câu hỏi:** Biệt danh nào được gắn cho Vương nữ Margaret do thời trang của bà mang lại?  
**Đáp án sinh:** Phong cách Margaret  
**Kiểm:** Phong cách Margaret (F1 1.0)  
**Cửa sổ (rút gọn):** Randolph Churchill tin rằng những tin đồn "rằng Fisher đã can thiệp để ngăn cản Vương nữ kết hôn với Townsend đã gây hại khôn lường cho Giáo hội Anh"; một cuộc thăm dò của Gallup cho thấy 28% đồng ý và 59% không đồng ý với việc Giáo hội từ chối tái hôn với một người đã ly hôn khi hôn phối còn lại vẫn còn sống. Nhà sử học Warwick cho rằng di sản lâu…

**Bài:** Vương nữ Margaret, Bá tước phu nhân xứ Snowdon (9,529 âm tiết), cửa sổ ở 11% bài  
**Trạng thái:** kept  
**Câu hỏi:** Margaret giữ chức Chủ tịch của tổ chức nào từ năm 1965 cho đến khi qua đời?  
**Đáp án sinh:** Hội Nữ Hướng đạo Anh Quốc  
**Kiểm:** Hội Nữ Hướng đạo Anh Quốc (F1 1.0)  
**Cửa sổ (rút gọn):** Barrie đã đọc truyện cho hai chị em. Ông nội của Margaret là George V qua đời khi bà mới 5 tuổi và bác của bà lên ngôi Quốc vương Edward VIII. Chưa đầy 1 năm sau, trong cuộc khủng hoảng thoái vị vào ngày 11 tháng 12 năm 1936, ông từ bỏ ngai vàng để kết hôn với Wallis Simpson, một người Mỹ đã ly hôn hai lần, người mà cả Giáo hội Anh và các chính phủ…

**Bài:** Vương nữ Margaret, Bá tước phu nhân xứ Snowdon (9,529 âm tiết), cửa sổ ở 46% bài  
**Trạng thái:** kept  
**Câu hỏi:** Margaret kết hôn với Armstrong-Jones tại đâu?  
**Đáp án sinh:** Tu viện Westminster  
**Kiểm:** Tu viện Westminster (F1 1.0)  
**Cửa sổ (rút gọn):** Armstrong-Jones cầu hôn Margaret bằng một chiếc nhẫn đính hôn bằng ruby ​​được bao quanh bởi những viên kim cương có hình hoa hồng. Bà được cho là chấp nhận lời cầu hôn của ông một ngày sau khi biết được từ Townsend rằng ông có ý định kết hôn với một phụ nữ trẻ người Bỉ, Marie-Luce Jamagne, có số tuổi bằng một nửa số tuổi ông và có nét tương đồng v…

**Bài:** Vương nữ Margaret, Bá tước phu nhân xứ Snowdon (9,529 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** kept  
**Câu hỏi:** Bà Margaret đã bay đến quốc gia nào để hồi phục sau khi chuyến thăm Tuvalu bị cắt ngắn do bệnh?  
**Đáp án sinh:** Úc  
**Kiểm:** Úc (F1 1.0)  
**Cửa sổ (rút gọn):** Chuyến thăm của bà đến Tuvalu bị cắt ngắn bởi một căn bệnh, có thể là viêm phổi do virus và bà đã bay đến Úc để hồi phục. Các chuyến thăm nước ngoài khác bao gồm Hoa Kỳ vào năm 1965, Nhật Bản vào năm 1969 và 1979, Hoa Kỳ và Canada vào năm 1974, Úc năm 1975, Philippines năm 1980, Swaziland vào năm 1981 và Trung Quốc năm 1987. Tháng 8 năm 1979, Louis…

**Bài:** Chiến dịch giải phóng Bulgaria (14,328 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai được cử làm Phó tổng tư lệnh quân đội Bulgaria phụ trách các vấn đề chính trị?  
**Đáp án sinh:** Tướng Steryu Antanasov  
**Kiểm:** Tướng Steryu Antanasov (F1 1.0)  
**Cửa sổ (rút gọn):** Tổ của đại tá P. Tartachevsky đến Sư đoàn bộ binh 4, tổ của đại tá V. Kheraskov đến Sư đoàn bộ binh 5, tổ của đại tá I. Titov đến Sư đoàn bộ binh 6, tổ của đại tá S. Galiakberov đến Sư đoàn bộ binh 9, tổ của đại tá F. Grigoryev đến Sư đoàn bộ binh 12, tổ của đại tá kỵ binh G. Shaforyod đến Sư đoàn kỵ binh 1 và tổ của đại tá kỵ binh V. Pogidayev đến…

**Bài:** Chiến dịch giải phóng Bulgaria (14,328 âm tiết), cửa sổ ở 35% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người buộc phải lên đài phát thanh tuyên bố cắt đứt mọi quan hệ với nước Đức Quốc xã và tuyên chiến với nước này vào ngày 8 tháng 9?  
**Đáp án sinh:** Konstantin Muraviev  
**Kiểm:** Konstantin Muraviev (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, không một cảnh sát Bulgrya nào dám bắn vào những người biểu tình. Mật thám Gestapo đã tiến hành một số vụ ám sát những người lãnh đạo cuộc biểu tình đang diễn thuyết trước đám đông người dân Bulgaria. Hàng động đổ dầu vào lửa đó đã làm cho những người biểu tình càng thêm kiên quyết. Cuộc biểu tình và đình công ngày 6 tháng 9 ở Sofia đã c…

**Bài:** Chiến dịch giải phóng Bulgaria (14,328 âm tiết), cửa sổ ở 32% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vua Bulgaria Simeon I đã ủy nhiệm cho ai lập nội các mới và giữ chức thủ tướng vào ngày 2 tháng 9 năm 1944?  
**Đáp án sinh:** Konstantin Muraviev  
**Kiểm:** Konstantin Muraviev (F1 1.0)  
**Cửa sổ (rút gọn):** Bagryanov phải "nói chuyện" với Liên Xô vì theo họ thì "nước xa (chỉ đồng minh Anh-Mỹ) không thể chữa được lửa gần". Bị mắc kẹp giữa "hai làn đạn", ngày 30 tháng 8, I. Bagryanov tuyên bố giải tán nội các và từ chức. Trong hai ngày sau đó, nước Bulgaria không có chính phủ. Ngày 2 tháng 9 năm 1944, Vua Bulgaria Simeon I ủy nhiệm cho Konstantin Muravi…

**Bài:** Chiến dịch giải phóng Bulgaria (14,328 âm tiết), cửa sổ ở 45% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lữ đoàn 4 mang tên gì khi được điều đến yểm hộ cho những người khởi nghĩa vào ngày 8 tháng 9?  
**Đáp án sinh:** Cách mạng Sofia  
**Kiểm:** Cách mạng Sofia (F1 1.0)  
**Cửa sổ (rút gọn):** chính quyền thân Đức tại đây đã điều đội hiến binh đến đàn áp, bắn chết 6 công nhân và làm bị thương 13 người. Ngày 8 tháng 9, Liên đoàn 1 du kích Bulgaria đã điều Lữ đoàn 4 mang tên "Cách mạng Sofia" đến yểm hộ cho những người khởi nghĩa, nhanh chóng tiêu diệt Tiểu đoàn hiến binh 3 Sofia. Tại Plovdiv và Gabrovo, những người biểu tình và quân du kí…

**Bài:** Chiến dịch giải phóng Bulgaria (14,328 âm tiết), cửa sổ ở 12% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Hạm đội biển Đen do ai chỉ huy?  
**Đáp án sinh:** Đô đốc F.  
**Kiểm:** Đô đốc F (F1 0.67)  
**Cửa sổ (rút gọn):** Tập đoàn quân 57 của tướng trung tướng Nikolai Aleksandrovich Gagen gồm 8 sư đoàn bộ binh, 1 lữ đoàn xe tăng, 1 lữ đoàn và 3 trung đoàn pháo, 1 trung đoàn súng cối. Tập đoàn quân 37 của trung tướng Mikhail Nikolayevich Sharokhin gồm 8 sư đoàn bộ binh, 1 sư đoàn đổ bộ đường không, 1 lữ đoàn và 4 trung đoàn pháo, 1 trung đoàn Katyusha, 3 trung đoàn s…

**Bài:** Chiến dịch giải phóng Bulgaria (14,328 âm tiết), cửa sổ ở 11% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tư lệnh của Phương diện quân Ukraina 3?  
**Đáp án sinh:** Đại tướng F. Tolbukhin  
**Kiểm:** Đại tướng F. Tolbukhin (F1 1.0)  
**Cửa sổ (rút gọn):** Tại các bến cảng Varna và Burgas, hải quân Đức có một số tàu chiến rút từ Constanta (Romania) về, một số tàu tuần tiễu, tàu ngầm và các biên đội tàu vận tải. Binh lực và kế hoạch Phương diện quân Ukraina 3 (tư lệnh: Đại tướng F. Tolbukhin, tham mưu trưởng: thượng tướng S. Tập đoàn quân 46 của trung tướng Ivan Timofeyevich Shlemin gồm 7 sư đoàn bộ b…

**Bài:** Chiến dịch giải phóng Bulgaria (14,328 âm tiết), cửa sổ ở 60% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân 37 của tướng M. Sharokhin được Tolbukhin điều động đến đâu để hỗ trợ cho Tập đoàn quân Bulgaria 1?  
**Đáp án sinh:** biên giới phía Tây Bulgaria  
**Kiểm:** biên giới phía Tây Bulgaria (F1 1.0)  
**Cửa sổ (rút gọn):** Tolbukhin sẽ điều động Tập đoàn quân 37 của tướng M. Sharokhin đến biên giới phía Tây Bulgaria để hỗ trợ cho Tập đoàn quân Bulgaria 1. Tập đoàn quân không quân 17 (Liên Xô) sẽ đóng căn cứ chủ yếu tại Sofia. Tolbukhin cũng cho biết quân đội Liên Xô còn có nhiệm vụ tấn công các đơn vị quân Đức Quốc xã tại Nam Tư và yêu cầu phía Bulgaria đáp ứng các đ…

**Bài:** Chiến dịch giải phóng Bulgaria (14,328 âm tiết), cửa sổ ở 52% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tổ bay trên máy bay Po-2 của đại úy N. Kozlov đã phát hiện đầu tàu và hai toa xe bỏ lại tại địa điểm nào?  
**Đáp án sinh:** ga xép Malevo gần thị trấn Khaskovo  
**Kiểm:** ga xép Malevo gần thị trấn Khaskovo (F1 1.0)  
**Cửa sổ (rút gọn):** Biryuzov ra lệnh cho thượng tướng V. Sudet, Tư lệnh tập đoàn quân không quân 17 điều động 5 máy bay cường kích IL-2 và 3 máy bay trinh sát Po-2 do đại tá Boris Smirnov chỉ huy chở các sĩ quan "SMERSH" từ sân bay Sofia tỏa đi các hướng để tìm kiếm đoàn tàu hỏa đặc biệt này. Các đội cận vệ nhân dân (công an) tại các nhà ga đầu mối trên khắp đất nước …

**Bài:** Chiến dịch Debrecen (11,219 âm tiết), cửa sổ ở 54% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Cụm kỵ binh cơ giới của I. Pliev đã cắt đứt đường sắt từ Debrecen qua Solnok đi Budapest tại các thị trấn nào?  
**Đáp án sinh:** Heidi Soboslo (Hajduszoboszlo), Nadudvar, Pyushpek (???), Kartsag (Karcag), Kishuysallash (Kisujszallas) và Kenderesh (Kenderes)  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Ngày 8 tháng 10, cả ba quân đoàn của Cụm kỵ binh cơ giới Pliyev tiếp tục vượt sông Kharmash phối hợp với Tập đoàn quân 53 tấn công lên Solnok. Đến cuối ngày 8 tháng 10, Cụm kỵ binh cơ giới của I. Pliev đã cắt đứt đường sắt từ Debrecen qua Solnok đi Budapest tại các thị trấn Heidi Soboslo (Hajduszoboszlo), Nadudvar, Pyushpek (???), Kartsag (Karcag),…

**Bài:** Chiến dịch Debrecen (11,219 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn bộ binh 29 của Đức do tướng nào chỉ huy?  
**Đáp án sinh:** Kurt Röpke  
**Kiểm:** Kurt Röpke (F1 1.0)  
**Cửa sổ (rút gọn):** Quân đoàn bộ binh 29 (Đức) của tướng Kurt Röpke. Sư đoàn kỵ binh 8 SS "Florian Geyer" Sư đoàn bộ binh sơn chiến 4. Cụm tác chiến sư đoàn Winkler Cụm tác chiến sư đoàn Schopper Sư đoàn bộ binh 9 (Hungary) Quân đoàn bộ binh 17 (Đức) của tướng Hans Kreysing. Trong biên chế gồm có: Sư đoàn bộ binh sơn chiến 27 (Hungary). Sư đoàn bộ binh xung kích 8 (Đứ…

**Bài:** Chiến dịch Debrecen (11,219 âm tiết), cửa sổ ở 96% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, ai là người mà Berlin hoàn toàn có thể tin cậy được cả về chính trị và quân sự để thay thế Horthy Miklós?  
**Đáp án sinh:** Ferenc Szálasi  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Trong trường hợp này, phía Liên Xô đã không tính đến khả năng Hitler dám loại bỏ một đồng minh chính trị của mình là Horthy Miklós để đưa Ferenc Szálasi, một người mà Berlin hoàn toàn có thể tin cậy được cả về chính trị và quân sự lên đốc thúc quân đội Hungary tiếp tục chiến đấu. Đối với quân đội Đức Quốc xã, kết quả của những diễn biến chính trị -…

**Bài:** Chiến dịch Debrecen (11,219 âm tiết), cửa sổ ở 91% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo báo cáo gửi STAVKA, Phương diện quân Ukraina 2 thừa nhận bị tổn thất khoảng bao nhiêu xe tăng?  
**Đáp án sinh:** khoảng 300 xe tăng  
**Kiểm:** 300 xe tăng (F1 0.86)  
**Cửa sổ (rút gọn):** Malinovsky trong báo cáo gửi STAVKA thừa nhận việc Phương diện quân Ukraina 2 bị tổn thất khoảng 300 xe tăng. Phương diện quân Ukraina 2 cũng không thực hiện được ý đồ tiến nhanh lên phía Bắc Budapest để bao vây cụm quân Đức - Hungary tại đây, làm cho Chiến dịch giải phóng Hungary kéo dài thêm gần 5 tháng nữa với những tổn thất không nhỏ. Tuy không…

**Bài:** Chiến dịch Debrecen (11,219 âm tiết), cửa sổ ở 93% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo báo cáo gửi về STAVKA ngày 28 tháng 10, Nguyên soái Liên Xô S. Timoshenko nhận định thế nào về tình trạng binh lực của Phương diện quân Ukraina 2?  
**Đáp án sinh:** binh lực phân tán và rải đều  
**Kiểm:** binh lực phân tán và rải đều (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, thành công này chỉ đủ để trì hoãn ngày tận thế của Đệ tam Đế chế vì không lâu sau đó, ngày 30 tháng 10 Nyíregyháza rơi vào tay quân đội Liên Xô và đến ngày 7 tháng 11 thì họ đã tiến tới vùng ngoại vi của Budapest. Ý định của Phương diện quân Ukraina 2 nhằm bao vây Tập đoàn quân 8 (Đức) và một phần Tập đoàn quân 2 (Hungary) ở Tây Transilv…

**Bài:** Chiến dịch Debrecen (11,219 âm tiết), cửa sổ ở 39% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn bộ binh 17 (Đức) do tướng nào chỉ huy?  
**Đáp án sinh:** Hans Kreysing  
**Kiểm:** Hans Kreysing (F1 1.0)  
**Cửa sổ (rút gọn):** Cụm tác chiến sư đoàn Winkler Cụm tác chiến sư đoàn Schopper Sư đoàn bộ binh 9 (Hungary) Quân đoàn bộ binh 17 (Đức) của tướng Hans Kreysing. Trong biên chế gồm có: Sư đoàn bộ binh sơn chiến 27 (Hungary). Sư đoàn bộ binh xung kích 8 (Đức). Sư đoàn bộ binh nhẹ 9 (Đức) Lữ đoàn bộ binh biên phòng (Hungary) Cụm tác chiến sư đoàn Rath Quân đoàn bộ binh 9…

**Bài:** Chiến dịch Debrecen (11,219 âm tiết), cửa sổ ở 14% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân 46 do trung tướng nào chỉ huy?  
**Đáp án sinh:** Ivan Timofeyevich Shlemin  
**Kiểm:** Ivan Timofeyevich Shlemin (F1 1.0)  
**Cửa sổ (rút gọn):** Công binh: Lữ đoàn kỹ thuật 54. Tập đoàn quân 46 do trung tướng Ivan Timofeyevich Shlemin chỉ huy. Quân đoàn cận vệ 10 gồm các sư đoàn cận vệ 49, 59, 86 và 109. Quân đoàn cận vệ 31 gồm các sư đoàn cận vệ 4, 34 và 40 Quân đoàn 37 gồm các sư đoàn 108 (cận vệ) và 320 Hỗn hợp: Sư đoàn 7 gồm Lữ đoàn pháo hạng nặng 11, Lữ đoàn pháo nòng dài 17, Lữ đoàn l…

**Bài:** Chiến dịch Debrecen (11,219 âm tiết), cửa sổ ở 55% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cụm kỵ binh cơ giới của tướng S. Gorshkov được điều động từ đâu để tăng cường cho Tập đoàn quân 27?  
**Đáp án sinh:** thê đội dự bị  
**Kiểm:** thê đội dự bị (F1 1.0)  
**Cửa sổ (rút gọn):** Ở giữa mặt trận, ngày 10 tháng 10, Nguyên soái R. Malinovsky phải điều chỉnh lại binh lực. Cụm kỵ binh cơ giới của tướng S. Gorshkov từ thê đội dự bị tăng cường cho Tập đoàn quân 27. Quân đoàn bộ binh 33 (Tập đoàn quân 27) được điều động phối thuộc cho Tập đoàn quân xe tăng cận vệ 6. Ngày 11 tháng 10, Tập đoàn quân 27 và Cụm kỵ binh cơ giới Gorshko…

**Bài:** Batman: Arkham City (9,173 âm tiết), cửa sổ ở 21% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Joker mắc phải căn bệnh nào có thể gây tử vong do đột biến từ việc sử dụng công thức Titan?  
**Đáp án sinh:** đột biến bởi việc hắn sử dụng công thức Titan  
**Kiểm:** căn bệnh có thể gây tử vong (F1 0.0)  
**Cửa sổ (rút gọn):** Trong khi đó, Joker mắc phải một căn bệnh có thể gây tử vong, đột biến bởi việc hắn sử dụng công thức Titan, một huyết thanh steroid không ổn định có thể biến người thường thành những con quái vật điên loạn : Nội dung sau đây có thể cho bạn biết trước nội dung của game.Tại một cuộc họp báo được tổ chức bởi Bruce Wayne nhằm tuyên bố phản đối của mìn…

**Bài:** Batman: Arkham City (9,173 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà quản lý cộng đồng châu Âu của Rocksteady có tên là gì?  
**Đáp án sinh:** Sarah Wellock  
**Kiểm:** Sarah Wellock (F1 1.0)  
**Cửa sổ (rút gọn):** Cũng trong tháng 11, Entertainment Weekly gọi nó là một trong 10 trò chơi hay nhất trong thập kỷ qua Trong tuần lễ ra mắt, một vấn đề đã được tìm thấy là tồn tại trong nội dung mã hạn chế. Một số khách hàng phát hiện ra mã mất tích từ bản sao của họ, ngăn ngừa họ sở hữu nhiệm vụ câu chuyện của Catwoman. Vấn đề này được báo cáo bởi khách hàng tại Ca…

**Bài:** Batman: Arkham City (9,173 âm tiết), cửa sổ ở 78% bài  
**Trạng thái:** kept  
**Câu hỏi:** Greg Miller của IGN đã chấm bao nhiêu điểm cho DLC Harley Quinn's Revenge?  
**Đáp án sinh:** 9 trên 10  
**Kiểm:** 9 trên 10 (F1 1.0)  
**Cửa sổ (rút gọn):** Một số khác tuy nhiên lại ca ngợi trò chơi, với Craig Majaski của Gaming-Age ca ngợi đồ họa nó là ngang bằng với phiên bản Xbox/PS3, bao gồm các nội dung DLC trên đĩa và những sử dụng nhất định được cung cấp bởi gamepad. Đối với Harley Quinn's Revenge DLC, Greg Miller của IGN cho số điểm 9 trên 10 và cho nó là Editor's Choice. Miller nói rằng nó "l…

**Bài:** Batman: Arkham City (9,173 âm tiết), cửa sổ ở 7% bài  
**Trạng thái:** kept  
**Câu hỏi:** Đạo diễn nghệ thuật David Hego của Rocksteady mô tả chế độ thám tử mới trong Batman: Arkham City là gì?  
**Đáp án sinh:** chế độ thực tế tăng cường  
**Kiểm:** chế độ thực tế tăng cường (F1 1.0)  
**Cửa sổ (rút gọn):** Trò chơi kết hợp yếu tố giải đố nhiều hơn so với người tiền nhiệm của nó; việc sử dụng "Detective Mode" của Batman, trong đó giúp nổi bật các yếu tố như tình trạng nhân vật và manh mối trên màn hình, được sử dụng để thực hiện các hoạt động pháp y như theo dõi nguồn gốc của một súng trường bắn tỉa. Người chơi có quyền truy cập vào cơ sở dữ liệu hình…

**Bài:** Batman: Arkham City (9,173 âm tiết), cửa sổ ở 55% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trang phục độc quyền cho PS3 mang tên Sinestro Corps ban đầu có thể được mở khóa thông qua mã duy nhất thu được từ việc mua phiên bản extended cut của phim nào trên Blu-ray từ Best Buy?  
**Đáp án sinh:** Green Lantern  
**Kiểm:** Green Lantern (F1 1.0)  
**Cửa sổ (rút gọn):** hợp tác với các nhà bán lẻ và các công ty trên toàn cầu để cung cấp nội dung phần thưởng cho việc đặt hàng trước, bao gồm: Best Buy, Amazon.com, GameStop, Game, Gamestation, EB Games, Tesco và Asda . Nội dung này chỉ có sẵn thông qua đặt hàng trước trò chơi với một nhà bán lẻ cụ thể hoặc mua một sản phẩm như một loại đồ uống NOS để có được một mã m…

**Bài:** Batman: Arkham City (9,173 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Gói giao diện điều khiển Xbox 360 theo chủ đề Batman phát hành ngày 25 tháng 10 năm 2011 bao gồm những thành phần nào?  
**Đáp án sinh:** trò chơi, một DVD của Batman: Gotham Knight, DVD của bộ phim Green Lantern, và video game liên quan Rise of the Manhunters, và một Xbox 360 250GB  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Lẫn lộn liên quan đến việc sử dụng GFWL đã xuất hiện khi một nhà phân phối ược9 thông báo bởi Warner Bros. là Arkham City không sử dụng hệ thống Live, nhưng việc sử dụng các GFWL đã được xác nhận vào cuối tháng 8 . Ngày 25 tháng 10 năm 2011, gói giao diện điều khiển Xbox 360 theo chủ đề Batman được phát hành, bao gồm trò chơi, một DVD của Batman: G…

**Bài:** Batman: Arkham City (9,173 âm tiết), cửa sổ ở 28% bài  
**Trạng thái:** kept  
**Câu hỏi:** Kẻ chủ mưu thật sự đằng sau Thành phố Arkham là ai?  
**Đáp án sinh:** Ra's al Ghul  
**Kiểm:** Ra's al Ghul (F1 1.0)  
**Cửa sổ (rút gọn):** Trước khi Joker có thể lợi dụng thời cơ, Talia xuất hiện và hứa sẽ cho Joker sự bất tử để hắn tha mạng cho Batman. Sau khi trốn thoát với sự giúp đỡ của Catwoman, Batman được Alfred thuyết phục hãy chấm dứt Protocol 10 trước khi đuổi theo Talia và Joker. Batman xâm nhập Wonder Tower và vô hiệu hóa Protocol 10. Ra's al Ghul được tiết lộ là kẻ chủ mư…

**Bài:** Batman: Arkham City (9,173 âm tiết), cửa sổ ở 30% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Joker khỏe mạnh trong đoạn trích thực chất là ai?  
**Đáp án sinh:** quái vật đất sét Clayface  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Joker liên lạc với Batman, đe dọa giết Talia trừ khi Batman gặp hắn tại Nhà hát Monarch. Khi Batman đến nơi, Joker yêu cầu phương thuốc nhưng bị giết bởi Talia trong khi bị xao lãng. Khi Talia thừa nhận ăn cắp phương thuốc từ Quinn, cô bị giết bởi một Joker thứ hai, người vẫn còn mắc căn bệnh. Joker khỏe mạnh hiện nguyên hình là quái vật đất sét Cl…

**Bài:** Chiến tranh nhân dân giải phóng Nam Tư (34,894 âm tiết), cửa sổ ở 69% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thống chế Maximilian von Weichs đã mở cuộc phản công từ Doni-Milanovo vào sau lưng Quân đoàn bộ binh 75 vào ngày nào?  
**Đáp án sinh:** Ngày 30 tháng 9  
**Kiểm:** Ngày 30 tháng 9 (F1 1.0)  
**Cửa sổ (rút gọn):** 2 sư đoàn Đức và 1 sư đoàn quân Chính phủ cứu nguy dân tộc Serbia đã bị bao vây, tiêu diệt và bắt làm tù binh tại khu vực Negotin. Ngày 30 tháng 9, thống chế Maximilian von Weichs mở một cuộc phản công của 2 sư đoàn Đức và 1 sư đoàn Quân Chính phủ cứu nguy dân tộc Serbia từ Doni-Milanovo vào sau lưng Quân đoàn bộ binh 75. Tướng Kosa Popovic đã điều…

**Bài:** Chiến tranh nhân dân giải phóng Nam Tư (34,894 âm tiết), cửa sổ ở 16% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là thủ lĩnh của lực lượng Chetnick được quân Đức thu nạp sau khi hạ vũ khí đầu hàng?  
**Đáp án sinh:** Dragoljub Mihailović  
**Kiểm:** Dragoljub Mihailović (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy đóng quân tại phần đất mà Quân giải phóng nhân dân Nam Tư đẻ lại nhưng các lực lượng Chetnick đã không tổ chức tấn công quân Đức. Tuy nhiên, quân Đức vẫn huy động hai trung đoàn bộ binh và một tiểu đoàn xe tăng tấn công quân Chetnick, đánh chiếm các thị trấn Drinyacha, Nova Kasaba và Shekovichi. Quân Chetnick tan vỡ, một phần nhỏ bỏ chạy và nhậ…

**Bài:** Chiến tranh nhân dân giải phóng Nam Tư (34,894 âm tiết), cửa sổ ở 12% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Ai là Chủ tịch Hội đồng cố vấn được nhắc đến trong đoạn trích?  
**Đáp án sinh:** Josip Broz Tito  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Các thành viên đến từ Bosnia-Herzegovina có Svetozar Vukmanović Tempo và Princip Seljo. Các chỉ huy chủ chốt và chính ủy các đơn vị du kích lớn gồm Kocha Popovic, Nebojsa Jerkovic, Milos Minic, Zdravko Jovanovic và Dragojlo Dudi. Các thành viên của Montenegro do bị chia rẽ nội bộ nên các thành viên đến từ Macedonia gồm Dragan Pavlovic Silja và Laza…

**Bài:** Chiến tranh nhân dân giải phóng Nam Tư (34,894 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Quân đội Đức Quốc xã tại Nam Tư đã huy động các sư đoàn bộ binh nào trong cuộc càn quét lớn vào Montenegro ngày 15 tháng 1 năm 1942?  
**Đáp án sinh:** sư đoàn bộ binh 342, 718  
**Kiểm:** 342, 718 (F1 0.5)  
**Cửa sổ (rút gọn):** Việc này làm chia rẽ thêm cuộc kháng chiến chống quân chiếm đóng Đức-Ý tại Nam Tư và quân đội chiếm đóng Đức Quốc xã đã lợi dụng ngay sự chia rẽ này Quân Đức tấn công lần thứ hai Ngày 15 tháng 1 năm 1942, quân đội Đức Quốc xã tại Nam Tư huy động các sư đoàn bộ binh 342, 718, và trung đoàn pháo binh 398 và 399 cùng 12 tiểu đoàn lính Ustaše từ Croati…

**Bài:** Chiến tranh nhân dân giải phóng Nam Tư (34,894 âm tiết), cửa sổ ở 36% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Ai là người đã yêu cầu hủy bỏ cuộc tấn công trên hướng Konjic và tổ chức phản công theo hướng ngược lại vào ngày 4 tháng 3 năm 1943?  
**Đáp án sinh:** Tổng tư lệnh Josip Broz Tito  
**Kiểm:** Josip Broz Tito (F1 0.67)  
**Cửa sổ (rút gọn):** Ngày 5 tháng 3, quân Ý và quân Chetnick bao vây Imotsky. Vào thời điểm cực kỳ nghiêm trọng của chiến dịch, Tổng tư lệnh Josip Broz Tito đã có một quyết định quan trọng liên quan đến sự tồn vong của chủ lực Quân Giải phóng nhân dân Nam Tư, nòng cốt của phong trào kháng chiến chống phát xít ở Nam Tư. Ngày 4 tháng 3 năm 1943, ông yêu cầu hủy bỏ cuộc t…

**Bài:** Chiến tranh nhân dân giải phóng Nam Tư (34,894 âm tiết), cửa sổ ở 40% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người chỉ huy nhóm nhân viên quân sự Anh đổ bộ xuống Đurđevića Tara vào ngày 20 tháng 6?  
**Đáp án sinh:** đại úy Bill Stewart  
**Kiểm:** đại úy Bill Stewart (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, do địa hình rừng núi nên Sở chỉ huy NOVJ đã điều một tiểu đoàn luồn rừng đi vòng qua Anaker và nối được liên lạc với Trung đoàn 22. Ngày 29 tháng 5, hai tiểu đoàn của Sư đoàn Vô Sản 2 đã có một trận kịch chiến với quân của Sư đoàn 7 SS (Đức) tại Anaker, phối hợp với Sư đoàn Vô Sản 1 chặn được Sư đoàn bộ binh 118 (Đức) trên đèo Piva, củng…

**Bài:** Chiến tranh nhân dân giải phóng Nam Tư (34,894 âm tiết), cửa sổ ở 11% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hội đồng cố vấn của Bộ Tổng tham mưu Quân giải phóng nhân dân Nam Tư được thành lập vào ngày nào?  
**Đáp án sinh:** Ngày 26 tháng 9 năm 1941  
**Kiểm:** Ngày 26 tháng 9 năm 1941 (F1 1.0)  
**Cửa sổ (rút gọn):** Tất cả các thành phố và thị trấn này đều trở thành các căn cứ do các đơn vị du kích Nam Tư đóng giữ với tổng quân số khoảng 15.000 người. Đến giữa tháng 9 năm 1941, vùng giải phóng này trở thành nơi đóng trụ sở của một bộ phận Ban chấp hành trung ương Đảng Cộng sản Nam Tư (KPJ), Bộ Tổng tham mưu Quân giải phóng nhân dân Nam Tư và Tổng tư lệnh Josip…

**Bài:** Chiến tranh nhân dân giải phóng Nam Tư (34,894 âm tiết), cửa sổ ở 70% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là hai vị tướng đã cùng phát biểu và ôm hôn nhau thắm thiết tại cuộc mít tinh mừng Beograd được giải phóng vào ngày 20 tháng 10?  
**Đáp án sinh:** tướng V. Zhdanov (Liên Xô) và tướng Peko Dapchvich (Nam Tư)  
**Kiểm:** tướng V. Zhdanov (Liên Xô) và tướng Peko Dapchvich (Nam Tư) (F1 1.0)  
**Cửa sổ (rút gọn):** và các tiểu đoàn bộ binh Nam Tư đầu tiên của Quân đoàn Vô Sản 14 (NOVJ) đã có mặt tại ngoại ô phía nam Beograd. Tại đây, 20.000 quân Đức và quân Ustaše được trang bị 40 xe tăng và 170 khẩu pháo đã bị bao vây. Các trận đánh trong nội đô Beograd cũng diễn ra khá quyết liệt. Trong những ngày từ 14 đến 17 tháng 10, Quân đoàn bộ binh 75 (Liên Xô), Quân …

**Bài:** Michelle Pfeiffer (13,202 âm tiết), cửa sổ ở 1% bài  
**Trạng thái:** kept  
**Câu hỏi:** Meryl Streep đã có vai chính đầu tiên trong bộ phim nào vào năm 1982?  
**Đáp án sinh:** Grease 2  
**Kiểm:** Grease 2 (F1 1.0)  
**Cửa sổ (rút gọn):** Sau khi bắt đầu sự nghiệp diễn xuất của mình vào năm 1978 với những lần xuất hiện nhỏ trên truyền hình và điện ảnh, cô đã có được vai chính đầu tiên trong Grease 2 (1982), một thất bại về mặt thương mại và phê bình trong đó Pfeiffer được coi là một ngoại lệ tích cực. Vỡ mộng với việc trở thành người được đánh giá cao trong những vai phụ nữ hấp dẫn,…

**Bài:** Michelle Pfeiffer (13,202 âm tiết), cửa sổ ở 13% bài  
**Trạng thái:** kept  
**Câu hỏi:** Meryl Streep được đề cử Giải Quả cầu vàng đầu tiên với tư cách là Nữ diễn viên chính xuất sắc nhất trong phim điện ảnh hoặc phim hài cho vai diễn nào?  
**Đáp án sinh:** Angela de Marco  
**Kiểm:** Angela de Marco (F1 1.0)  
**Cửa sổ (rút gọn):** Sau Scarface, cô đóng vai Diana trong bộ phim hài Into the Night (1985) của John Landis, với Jeff Goldblum; Isabeau d'Anjou trong bộ phim giả tưởng Ladyhawke (1985) của Richard Donner, với Rutger Hauer và Matthew Broderick; Faith Healy trong Sweet Liberty của Alan Alda (1986), với Michael Caine; và Brenda Landers trong một phân đoạn của bộ phim kho…

**Bài:** Michelle Pfeiffer (13,202 âm tiết), cửa sổ ở 53% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trong phim Ant-Man and the Wasp, Michael Douglas vào vai nhân vật nào?  
**Đáp án sinh:** Hank Pym  
**Kiểm:** Hank Pym (F1 1.0)  
**Cửa sổ (rút gọn):** Vào vai vợ của Hank Pym (Michael Douglas), Ant-Man and the Wasp theo chân các nhân vật của bộ phim gốc khi họ cố gắng tìm lại Janet từ Vương quốc lượng tử, nơi cô đã bị mất tích trong vài thập kỷ. Ant-Man and the Wasp được coi là sự trở lại của Pfeiffer với các bộ phim siêu anh hùng, đây là vai diễn đầu tiên trong truyện tranh của cô kể từ Catwoman…

**Bài:** Michelle Pfeiffer (13,202 âm tiết), cửa sổ ở 75% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Amy Longsdorf của The Morning Call, Pfeiffer được mô tả là một trong những ngôi sao điện ảnh như thế nào trên thế giới?  
**Đáp án sinh:** nổi tiếng và được giới phê bình đánh giá cao nhất  
**Kiểm:** nổi tiếng và được giới phê bình đánh giá cao nhất (F1 1.0)  
**Cửa sổ (rút gọn):** Pfeiffer giải thích thêm, "Một số màn trình diễn mà tôi cảm thấy hay nhất là những màn mà tôi đã đánh giá cao", trong khi "Những màn khiến tôi quặn lòng thường là khi tôi nhận được những đánh giá tốt nhất". Pfeiffer được mệnh danh là một trong những ngôi sao điện ảnh lớn nhất thế giới, khẳng định mình là một "ngôi sao lớn" mặc dù vẫn chưa nhận được…

**Bài:** Michelle Pfeiffer (13,202 âm tiết), cửa sổ ở 70% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Theo Mick LaSalle, Pfeiffer được coi là ngoại lệ trong nhóm diễn viên Hollywood được trả lương quá cao vì lý do gì?  
**Đáp án sinh:** không bao giờ có màn trình diễn tồi và luôn thu hút khán giả  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Pfeiffer đặc biệt nổi tiếng vì sự linh hoạt của mình, đã tích lũy được một kho tàng đa dạng trải dài từ các bộ phim lãng mạn, giả tưởng, nhạc kịch, hài kịch và chính kịch. Đến năm 2016, Salon Charles Taylor tuyên bố rằng không có diễn viên nào của thập kỷ trước có thể sánh ngang với nữ diễn viên về độ đa tài. Năm 2021, Adreon Patterson của CinemaBl…

**Bài:** Michelle Pfeiffer (13,202 âm tiết), cửa sổ ở 39% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Nhà phê bình James Berardinelli đã mô tả bộ phim I Could Never Be Your Woman như thế nào?  
**Đáp án sinh:** một bộ phim hài lãng mạn thú vị đủ để khiến bộ phim đáng được đề nghị  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Các bài đánh giá cho I Could Never Be Your Woman có mức độ tích cực vừa phải, với nhà phê bình James Berardinelli nhận thấy Pfeiffer và Rudd "có đủ phản ứng hóa học để kéo dài câu chuyện tình lãng mạn", trong điều mà anh ấy mô tả là "một bộ phim hài lãng mạn thú vị đủ để khiến bộ phim đáng được đề nghị". Tiếp theo, cô đóng vai chính trong Personal …

**Bài:** Michelle Pfeiffer (13,202 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Lynn Hirschberg, những vai diễn hay nhất của Pfeiffer dường như liên quan đến điều gì?  
**Đáp án sinh:** một người phụ nữ đang chiến tranh với chính mình  
**Kiểm:** một người phụ nữ đang chiến tranh với chính mình (F1 1.0)  
**Cửa sổ (rút gọn):** Thường được khen ngợi vì đã che giấu cảm xúc và cảm xúc thật của cô ấy, phim cổ trang, một thể loại đã trở thành thương hiệu của cô. Bản thân Pfeiffer đã thừa nhận là người đặc biệt thành thạo trong lĩnh vực này nhưng cũng tin rằng việc ngụy trang cảm xúc của một người không phải là hiếm về những gì chúng tôi đang thực sự nghĩ. Pfeiffer đã gọi hoạt…

**Bài:** Michelle Pfeiffer (13,202 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** kept  
**Câu hỏi:** Martin Scorsese đã mô tả Pfeiffer là một nữ diễn viên có khả năng khắc họa điều gì với đôi mắt và khuôn mặt?  
**Đáp án sinh:** xung đột nội tâm  
**Kiểm:** xung đột nội tâm (F1 1.0)  
**Cửa sổ (rút gọn):** Cô ấy ít đi những con đường diễn xuất hơn và khiến chúng tôi là những cộng tác viên hạnh phúc trong hành trình của cô ấy. Sự nghiệp của cô ấy cho đến nay là một vòng cung của chiến thắng và lòng dũng cảm". Các nhà làm phim và bạn diễn đồng ý rằng Pfeiffer cực kỳ tận tâm với công việc của mình, phát triển danh tiếng về năng lực và sự chuẩn bị. Khả n…

**Bài:** Không quân Hoàng gia Lào (10,250 âm tiết), cửa sổ ở 82% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ngày 14 tháng 4 năm 1975, Không quân Hoàng gia Lào đã xuất kích thực hiện phi vụ chiến đấu cuối cùng theo lệnh của ai?  
**Đáp án sinh:** Vàng Pao  
**Kiểm:** Vàng Pao (F1 1.0)  
**Cửa sổ (rút gọn):** Chương trình huấn luyện nhân sự ngoài nước chấm dứt. Kể từ đây, các phi công Không lực Hoàng gia Lào chỉ bay được hai giờ mỗi tháng. Ngày 14 tháng 4 năm 1975, Không quân Hoàng gia Lào xuất kích thực hiện phi vụ chiến đấu cuối cùng. Theo lệnh của Vàng Pao, chín chiếc máy bay T-28 đã oanh tạc một đoàn xe tải của Pathet Lào đang trên đường di chuyển v…

**Bài:** Không quân Hoàng gia Lào (10,250 âm tiết), cửa sổ ở 95% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sách 'The Ravens: Pilots of the Secret War in Laos' của Christopher Robbins được xuất bản tại thành phố nào?  
**Đáp án sinh:** Bangkok  
**Kiểm:** Bangkok (F1 1.0)  
**Cửa sổ (rút gọn):** Bill Gunston, An Illustrated Guide to Military Helicopters, Salamander Books Ltd, London 1981. Christopher Robbins, Air America, Avon, New York 1979. Christopher Robbins, The Ravens: Pilots of the Secret War in Laos, Asia Books, Bangkok 2000. David Corn, Blond Ghost: Ted Shackley and the CIA's Crusades, Simon & Schuster, 1994. Kenneth Conboy, Kenne…

**Bài:** Không quân Hoàng gia Lào (10,250 âm tiết), cửa sổ ở 30% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Hiệp ước đình chiến ký kết ngày 10 tháng 5 năm 1962 đã giới hạn hoạt động của Không lực Hoàng gia Lào với những loại máy bay nào?  
**Đáp án sinh:** những chiếc T-6 không còn hoạt động nữa  
**Kiểm:** T-6 (F1 0.22)  
**Cửa sổ (rút gọn):** Ngày 10 tháng 5 năm 1962, hiệp ước đình chiến được ký kết đã giới hạn hoạt động của Không lực Hoàng gia Lào với những chiếc T-6 không còn hoạt động nữa, mặc dù học viên Hàng không Lào được chuyển tiếp đến Lopburi, Thái Lan học khóa huấn luyện T-28 vào tháng 6 năm 1962. Tuy nhiên, trong thời gian ngừng bắn, Vàng Pao đã sử dụng sự hỗ trợ của CIA cho …

**Bài:** Không quân Hoàng gia Lào (10,250 âm tiết), cửa sổ ở 59% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Sự kiện gây chấn động dư luận nào đã xảy ra vào ngày 21 tháng 3 năm 1968 liên quan đến một phi hành đoàn C-47 của Không lực Hoàng gia Lào?  
**Đáp án sinh:** một phi hành đoàn C-47 đã bị bắt tại sân bay Tân Sơn Nhứt, Việt Nam vì buôn lậu vàng và thuốc phiện  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Công tác hỗ trợ hậu cần cho binh lính bằng trực thăng của Không lực Hoàng gia Lào cũng đã chứng minh không đầy đủ. Trước sự thất bại thảm hại tại Nam Bắc vào đầu năm 1968, quân đội Hoàng gia Lào đã trở nên yếu kém, tăng gánh nặng chiến đấu trên vai Không quân Hoàng gia Lào. Không quân được tăng cường thêm từ 45 đến 50 T-28, với thêm 25 đến 30 chiếc…

**Bài:** Không quân Hoàng gia Lào (10,250 âm tiết), cửa sổ ở 12% bài  
**Trạng thái:** kept  
**Câu hỏi:** Cơ quan nào của Pháp đã thiết lập các đơn vị du kích chống Cộng trên khắp miền Bắc nước Lào?  
**Đáp án sinh:** cơ quan tình báo quân đội Pháp (SDECE)  
**Kiểm:** cơ quan tình báo quân đội Pháp (SDECE) (F1 1.0)  
**Cửa sổ (rút gọn):** Bốn trực thăng Sikorsky H-19 của lực lượng không quân mới đã không đáp ứng đầy đủ cho các nhiệm vụ như tải thương, vì vậy thêm hai chiếc H-19 được mua lại từ Không quân Hoàng gia Thái Lan vào tháng 10 năm 1955. Các trực thăng về sau đều được viện trợ không giới hạn và là máy bay chính thức của Hàng không Thái Lan. Ngoài ra, cơ quan tình báo quân độ…

**Bài:** Không quân Hoàng gia Lào (10,250 âm tiết), cửa sổ ở 52% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thao Ma đã chuyển sở chỉ huy của ông từ Savannakhet đến đâu?  
**Đáp án sinh:** Luang Prabang  
**Kiểm:** Luang Prabang (F1 1.0)  
**Cửa sổ (rút gọn):** Sự thất bại hoàn toàn của chương trình này với ý định trinh sát trên không bằng loại máy bay Raven FAC. Viên tham mưu trưởng Không lực Hoàng gia Lào được một số phe cánh đối lập hối lộ để dẫn đầu một cuộc nổi loạn chống lại Thao Ma. Để trả đũa, ngày 4 tháng 6 năm 1966, ông đã phát động một cuộc nổi dậy nhằm trấn áp phe nổi dậy nhưng thất bại. Sau đ…

**Bài:** Không quân Hoàng gia Lào (10,250 âm tiết), cửa sổ ở 31% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thỏa thuận quốc tế về tính trung lập của Lào được ký kết vào ngày nào?  
**Đáp án sinh:** 23 tháng 7 năm 1962  
**Kiểm:** ngày 23 tháng 7 năm 1962 (F1 0.91)  
**Cửa sổ (rút gọn):** Tuy nhiên, trong thời gian ngừng bắn, Vàng Pao đã sử dụng sự hỗ trợ của CIA cho quân đội dân tộc miền núi người H'Mông của ông để bắt đầu đào xới dải đất đường băng ngắn được dùng để yểm trợ hậu cần cho quân của mình bằng máy bay trực thăng và máy bay đường ngắn. Những dải đường băng nguyên thủy nhỏ bé này sẽ lan ra khắp Lào và trở thành một thành …

**Bài:** Không quân Hoàng gia Lào (10,250 âm tiết), cửa sổ ở 37% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chiến dịch Waterpump đã gửi thêm bao nhiêu chiếc T-28 cho Không lực Hoàng gia Lào?  
**Đáp án sinh:** bốn chiếc T-28  
**Kiểm:** bốn chiếc T-28 (F1 1.0)  
**Cửa sổ (rút gọn):** Chiến dịch Waterpump còn gửi thêm bốn chiếc T-28 cho Không lực Hoàng gia Lào. Hai ngày sau, mười chiếc T-28 dư thừa được chuyển từ Việt Nam Cộng hòa; bốn chiếc được Waterpump giữ lại dùng để tiếp tục hoạt động đào tạo huấn luyện trong khi sáu chiếc còn lại được chuyển cho Không lực Hoàng gia Lào. Nhằm khắc phục tình trạng thiếu phi công cho đến khi…

**Bài:** Hải âu cổ rụt Đại Tây Dương (9,354 âm tiết), cửa sổ ở 89% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trung tâm Du lịch Dự án Hải âu cổ rụt ở Rockland cung cấp thông tin về các đàn chim và cuộc sống của chúng, cũng như các dự án bảo tồn khác do tổ chức nào điều hành?  
**Đáp án sinh:** Audubon  
**Kiểm:** Audubon (F1 1.0)  
**Cửa sổ (rút gọn):** Maine nằm ở rìa phía nam của phạm vi sinh sản của chim và với sự thay đổi các kiểu thời tiết, điều này có thể làm quần thể chim thu hẹp về phía bắc. thế=Watching puffins|trái|nhỏ|Chụp ảnh đàn chim. Các đàn hải âu cổ rụt Đại Tây Dương ở các tổ mang đến một cảnh tượng thú vị cho những người quan sát chim và khách du lịch. Ví dụ, 4000 con hải âu cổ rụ…

**Bài:** Hải âu cổ rụt Đại Tây Dương (9,354 âm tiết), cửa sổ ở 25% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hơn 90% số cá thể hải âu cổ rụt Đại Tây Dương trên toàn cầu được tìm thấy ở khu vực nào?  
**Đáp án sinh:** châu Âu  
**Kiểm:** châu Âu (F1 1.0)  
**Cửa sổ (rút gọn):** Phân bố và môi trường sống Hải âu cổ rụt Đại Tây Dương là loài chim sống ở vùng nước lạnh ở Bắc Đại Tây Dương. Loài này sinh sản trên các bờ biển phía tây bắc châu Âu, rìa Bắc Cực và phía đông Bắc Mỹ. Hơn 90% số cá thể trên toàn cầu được tìm thấy ở châu Âu (4.770.000–5.780.000 cặp, tương đương 9.550.000–11.600.000 con trưởng thành), và chỉ riêng cá…

**Bài:** Hải âu cổ rụt Đại Tây Dương (9,354 âm tiết), cửa sổ ở 65% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hải âu cổ rụt Đại Tây Dương thường an toàn hơn khi ở ở đâu?  
**Đáp án sinh:** ngoài biển  
**Kiểm:** ngoài biển (F1 1.0)  
**Cửa sổ (rút gọn):** Động vật săn mồi và ký sinh trùng Hải âu cổ rụt Đại Tây Dương có lẽ an toàn hơn khi ở ngoài biển, nơi mà những mối nguy hiểm thường đến từ bên dưới mặt nước hơn là bên trên; đôi khi người ta có thể nhìn thấy những con hải âu cổ rụt chúi đầu xuống nước để quan sát xung quanh tìm kẻ săn mồi. Hải cẩu đã được biết là giết hải âu và cá lớn cũng có thể l…

**Bài:** Hải âu cổ rụt Đại Tây Dương (9,354 âm tiết), cửa sổ ở 29% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hải âu cổ rụt Đại Tây Dương thường sinh sản theo hình thức nào?  
**Đáp án sinh:** theo đàn lớn  
**Kiểm:** theo đàn lớn (F1 1.0)  
**Cửa sổ (rút gọn):** Cần bắt lại những cá thể đó để truy cập thông tin, đây là nhiệm vụ không hề dễ dàng. Một cá thể được phát hiện đã di chuyển 7.700 km (4.800 dặm) trên đại dương trong 8 tháng, di chuyển về vùng phía bắc đến phía bắc Biển Labrador rồi đi về phía đông nam đến giữa Đại Tây Dương trước khi quay trở lại đất liền. Ở một loài chim sống lâu với kích thước l…

**Bài:** Hải âu cổ rụt Đại Tây Dương (9,354 âm tiết), cửa sổ ở 54% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Tổng thời gian ấp trứng của loài chim được mô tả trong đoạn trích là bao lâu?  
**Đáp án sinh:** khoảng 39–45 ngày  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Vỏ màu trắng hoàn toàn, nhưng sẽ nhanh chóng bị bao phủ bởi bùn. Cả con bố và mẹ đều tham gia ấp trứng. Mỗi con đều có hai mảng ấp không có lông ở phần dưới, nơi máu tăng cường cung cấp nhiệt cho trứng. Con bố mẹ làm nhiệm vụ ấp trứng trong buồng tổ tối dành phần lớn thời gian để ngủ với đầu vùi dưới cánh, thỉnh thoảng chui ra khỏi đường hầm để vỗ …

**Bài:** Hải âu cổ rụt Đại Tây Dương (9,354 âm tiết), cửa sổ ở 17% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, phần nào của loài chim này được mô tả là rất đặc biệt?  
**Đáp án sinh:** Phần mỏ  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Vào cuối mùa sinh sản, bộ lông đen có thể mất đi độ bóng hoặc thậm chí có màu hơi nâu. Các chân ngắn và nằm ngửa trên cơ thể, giúp chim có tư thế đứng thẳng khi ở trên cạn. Cả hai chân và bàn chân có màng lớn đều có màu cam sáng, tương phản với móng vuốt đen, sắc nhọn. Phần mỏ của loài rất đặc biệt. Nhìn từ bên cạnh, mỏ rộng và có hình tam giác, nh…

**Bài:** Hải âu cổ rụt Đại Tây Dương (9,354 âm tiết), cửa sổ ở 9% bài  
**Trạng thái:** kept  
**Câu hỏi:** Pennant đã đặt danh pháp chính thức Fratercula arctica cho hải âu cổ rụt Đại Tây Dương vào năm nào?  
**Đáp án sinh:** 1768  
**Kiểm:** 1768 (F1 1.0)  
**Cửa sổ (rút gọn):** Hải âu cổ rụt Đại Tây Dương được đặt cái tên này muộn hơn nhiều, có lẽ bắt nguồn từ thói quen làm tổ tương tự của chúng. Pennant đặt danh pháp chính thức cho loài này là Fratercula arctica vào năm 1768. Tuy chúng còn được gọi là hải âu cổ rụt thông thường hay "common puffin", Đại hội Điểu học Quốc tế khuyến nghị sử dụng cái tên "Atlantic puffin". B…

**Bài:** Hải âu cổ rụt Đại Tây Dương (9,354 âm tiết), cửa sổ ở 4% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hải âu cổ rụt Đại Tây Dương là loài chim chính thức của tỉnh nào ở Canada?  
**Đáp án sinh:** Newfoundland và Labrador  
**Kiểm:** Newfoundland và Labrador (F1 1.0)  
**Cửa sổ (rút gọn):** Trải qua mùa thu và mùa đông ở vùng biển rộng của vùng biển phía bắc lạnh giá, hải âu cổ rụt Đại Tây Dương quay trở lại các vùng ven biển để bắt đầu mùa sinh sản vào cuối mùa xuân. Chúng làm tổ trên đỉnh vách đá, đào một cái hang để đẻ một quả trứng trắng duy nhất. Chim non chủ yếu ăn cá nguyên con và lớn nhanh. Sau khoảng 6 tuần, chim hoàn toàn tr…

**Bài:** Kamen Rider Agito (10,156 âm tiết), cửa sổ ở 70% bài  
**Trạng thái:** kept  
**Câu hỏi:** Kana đã làm gì khi sợ hãi việc trở thành Agito gần như thức tỉnh?  
**Đáp án sinh:** cố gắng tự sát  
**Kiểm:** cố gắng tự sát (F1 1.0)  
**Cửa sổ (rút gọn):** Những thí nghiệm này khiến cô bị chấn thương nặng, không thể kiểm soát được khả năng Agito của mình, cô đã giết Kazaya một cách vô thức. Điều này khiến cô mất trí và cô đã tự sát ở tuổi 23, mặc dù bạn trai của cô là Shouichi đã cố gắng cứu cô, nhưng cuối cùng anh ấy đã đồng ý với Yukina, để cô chết trong yên bình. Cô bỏ lại người em trai Tetsuya củ…

**Bài:** Kamen Rider Agito (10,156 âm tiết), cửa sổ ở 60% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Sở thích của nhân vật bán ramen trong đoạn trích là gì?  
**Đáp án sinh:** bói Naruto  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Hojo không muốn đi cùng với anh ấy, nhưng khi Hojo là người sử dụng G3 và rời xa Kono, Hikawa đã ăn ramen ở đây với Kono. Sau đó, Ozawa, Omuro và Shouichi cũng dùng bữa với Hikawa. Sở thích của ông là "bói Naruto", ông đọc vận may của khách hàng từ trạng thái của miếng Naruto trong bát ramen mà ông đặt ra. : là giáo sư tại Phòng thí nghiệm Takamura…

**Bài:** Kamen Rider Agito (10,156 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sinh vật bí ẩn nào đóng vai trò là nhân vật phản diện chính trong trò chơi Kamen Rider: Seigi no Keifu?  
**Đáp án sinh:** một sinh vật bí ẩn  
**Kiểm:** sinh vật bí ẩn (F1 0.89)  
**Cửa sổ (rút gọn):** Anh đã có thể biến mọi người thành cát bụi với cát và khả năng đào hang dưới lòng đất của mình. El này có sức mạnh đáng kể rõ ràng từ cuộc chạm trán đầu tiên với Gills, người đã giao chiến với anh ta trong trận chiến vì cái chết của Risa. Anh ta thậm chí còn có thể vượt qua Agito, mặc dù đã chuyển sang Ground Form và Burning Form. Tuy nhiên, anh kh…

**Bài:** Kamen Rider Agito (10,156 âm tiết), cửa sổ ở 27% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ozawa được sinh ra ở đâu và vào năm nào?  
**Đáp án sinh:** New York vào năm 1977  
**Kiểm:** New York vào năm 1977 (F1 1.0)  
**Cửa sổ (rút gọn):** Ông cũng là người đàn ông 45 tuổi mà Shouichi sống cùng, cũng như là giáo sư khoa Tâm lý học tại trường Đại học Jōhoku mà Ozawa từng theo học. Ông là người tính tình thẳng thắn nhưng lại rất hay nhậu nhẹt. Vợ ông không xuất hiện nhưng được biết là đang đi công tác nước ngoài để dạy nghề. : là con trai của giáo sư Yoshihiko Misugi và em họ của Mana,…

**Bài:** Kamen Rider Agito (10,156 âm tiết), cửa sổ ở 16% bài  
**Trạng thái:** kept  
**Câu hỏi:** Kino thừa nhận rằng anh đã trở nên hư hỏng không phải vì sức mạnh Agito mà là do yếu tố nào?  
**Đáp án sinh:** sự yếu đuối của bản thân khi còn là một con người  
**Kiểm:** sự yếu đuối của bản thân khi còn là một con người (F1 1.0)  
**Cửa sổ (rút gọn):** Thật không may, sức mạnh này sẽ khiến trạng thái tinh thần hưng phấn của Kino tiếp tục leo thang thành những ảo tưởng lớn lao, tin rằng một mình anh có thể đánh bại mối đe dọa từ Lord. Những ảo tưởng của anh cuối cùng đã thúc đẩy anh cố gắng loại bỏ Shouichi Tsugami, Kamen Rider Agito. Mặc dù hành động của cánh tay em trai đôi khi sẽ gây trở ngại, …

**Bài:** Kamen Rider Agito (10,156 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** kept  
**Câu hỏi:** Rei Motoki đã quyết định sống cùng ai sau khi tất cả những Unknowns đã bị đánh bại?  
**Đáp án sinh:** Sayaka  
**Kiểm:** Sayaka (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, vì viện nghiên cứu bị tấn công bởi Unknown, cô đã trốn thoát cùng Rei Motoki bằng cách tận dụng hết khả năng tiên đoán của mình. Sau đó, cô bị tách khỏi Rei và chuyển đến gia đình Misugi khi cô đã ngăn chặn vụ tai nạn giao thông xảy ra với Taichi Misugi bằng khả năng tiên đoán của mình, trở thành bạn của Shouichi Tsugami (Tetsuya Sawaki)…

**Bài:** Kamen Rider Agito (10,156 âm tiết), cửa sổ ở 53% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ông cảnh sát duy nhất chiến đấu chống lại Unknown theo cách riêng của mình, ngoài Hikawa và Hojo, là khách quen của quán ramen nào?  
**Đáp án sinh:** Umaiken  
**Kiểm:** Umaiken (F1 1.0)  
**Cửa sổ (rút gọn):** Ông đang theo dõi vụ giết Nobuyuki Kazaya và có một người quen với Mana. Ngoại trừ Hikawa và Hojo, ông là cảnh sát duy nhất chiến đấu chống lại Unknown theo cách riêng của mình. Ông là khách quen của quầy ramen "Umaiken" gần Sở Cảnh sát Thủ đô và có thể ăn ở quầy đó trong thời gian làm việc. Đôi khi khi ăn bento của vợ, ông lại lẩm bẩm: "Ramen ngon…

**Bài:** Kamen Rider Agito (10,156 âm tiết), cửa sổ ở 34% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tomoko đã bị OverLord giết bằng cách nào?  
**Đáp án sinh:** bóp cổ đến chết  
**Kiểm:** bóp cổ đến chết (F1 1.0)  
**Cửa sổ (rút gọn):** El đã chiến đấu với Tetsuya Sawaki khi anh thức tỉnh với tư cách là Agito thứ 2 và cuối cùng ném anh xuống biển. Trong khi anh không thể đánh bại El Lord, Agito đã giữ anh ta đủ lâu để một cảnh sát tên là Makoto Hikawa nhìn thấy một cơn bão vượt qua thuyền Akatsuki và nhảy xuống nước để cứu những người có thể còn sống sót. Anh đã cứu được tất cả mọ…

**Bài:** Carl Nielsen (10,599 âm tiết), cửa sổ ở 31% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nielsen được đưa vào Bệnh viện Quốc gia Copenhagen vào ngày nào?  
**Đáp án sinh:** 1 tháng 10 năm 1931  
**Kiểm:** ngày 1 tháng 10 năm 1931 (F1 0.91)  
**Cửa sổ (rút gọn):** " Sáng tác âm nhạc cuối cùng của Nielsen, tác phẩm đàn organ Commotio, được công chiếu lần đầu tiên sau khi sinh năm 1931. Trong những năm cuối cùng của mình, Nielsen đã cho ra đời một cuốn sách tiểu luận ngắn mang tên Âm nhạc sống (1925), tiếp theo là hồi ký Min Fynske Barndom vào năm 1927. Năm 1926, ông viết trong nhật ký "Đất quê hương kéo tôi n…

**Bài:** Carl Nielsen (10,599 âm tiết), cửa sổ ở 6% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nielsen sinh ra tại địa điểm nào gần Nørre Lyndelse?  
**Đáp án sinh:** Sortelung  
**Kiểm:** Sortelung (F1 1.0)  
**Cửa sổ (rút gọn):** Nielsen sinh vào ngày 09 tháng 6 năm 1865, là con thứ bảy trong số mười hai người con trong một gia đình nông dân nghèo, tại Sortelung gần Nørre Lyndelse, phía nam Odense trên đảo Funen. Cha của ông, Niels Jørgensen, là một họa sĩ nhà và một nhạc sĩ truyền thống, với khả năng chơi đàn và chơi cornet của mình, rất có niềm mong muốn tổ chức các lễ kỷ…

**Bài:** Carl Nielsen (10,599 âm tiết), cửa sổ ở 32% bài  
**Trạng thái:** kept  
**Câu hỏi:** Carl Nielsen được đưa vào Bệnh viện Quốc gia Copenhagen vào ngày nào?  
**Đáp án sinh:** 1 tháng 10 năm 1931  
**Kiểm:** ngày 1 tháng 10 năm 1931 (F1 0.91)  
**Cửa sổ (rút gọn):** Vậy thì nó phải ở nơi tôi đã sinh ra: Sortelung, giáo xứ Frydenlands ". Điều đó đã không xảy ra. Nielsen được đưa vào Bệnh viện Quốc gia Copenhagen (Rigshospitalet) vào ngày 1 tháng 10 năm 1931 sau hàng loạt các cơn đau tim. Ông qua đời ở đó vào lúc 10 phút trước nửa đêm ngày 3 tháng 10, xung quanh là gia đình ông. Những lời cuối cùng của ông với h…

**Bài:** Carl Nielsen (10,599 âm tiết), cửa sổ ở 94% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tiểu hành tinh nào được đặt tên để vinh danh Carl Nielsen?  
**Đáp án sinh:** 6058 Carlnielsen  
**Kiểm:** 6058 Carlnielsen (F1 1.0)  
**Cửa sổ (rút gọn):** Hình ảnh của ông được chọn để ghi nhận những đóng góp của ông trong các sáng tác âm nhạc Đan Mạch như vở opera Maskarade, bản giao hưởng Espansiva và nhiều bài hát của ông bao gồm "Danmark, nu blunder den lyse nat". Một số sự kiện đặc biệt đã được lên kế hoạch vào hoặc khoảng ngày 9 tháng 6 năm 2015 để kỷ niệm 150 năm ngày sinh của Nielsen. Ngoài n…

**Bài:** Carl Nielsen (10,599 âm tiết), cửa sổ ở 22% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nielsen đã chơi nhạc cụ nào trong buổi hòa nhạc ra mắt Bản giao hưởng đầu tiên của ông vào ngày 14 tháng 3 năm 1894?  
**Đáp án sinh:** violin thứ hai  
**Kiểm:** phần violin thứ hai (F1 0.86)  
**Cửa sổ (rút gọn):** Con trai của Nielsen, Hans Børge, bị tàn tật do bệnh viêm màng não và đã dành phần lớn cuộc đời của mình để xa gia đình. Ông mất gần Kolding năm 1956. Một nhà soạn nhạc với bước đi trưởng thành Lúc đầu, những tác phẩm của ông không gây nhiều sự chú ý đủ để chi viện cho cuộc sống của ông ấy. Trong buổi hòa nhạc ra mắt Bản giao hưởng đầu tiên của ông…

**Bài:** Carl Nielsen (10,599 âm tiết), cửa sổ ở 16% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nielsen đã gặp nhà soạn nhạc kiêm nghệ sĩ dương cầm Ferruccio Busoni ở đâu vào năm 1891?  
**Đáp án sinh:** Leipzig  
**Kiểm:** Leipzig (F1 1.0)  
**Cửa sổ (rút gọn):** Sau khi Svendsen nghỉ hưu vào năm 1906, Nielsen ngày càng giữ vai trò nhạc trưởng (được chính thức bổ nhiệm làm trợ lý chỉ huy vào năm 1910). Giữa khi tốt nghiệp và đạt được vị trí này, anh ấy đã kiếm được thu nhập khiêm tốn từ các buổi học violin riêng trong khi nhận được sự hỗ trợ liên tục của những người bảo trợ của mình, không chỉ Jens Georg Ni…

**Bài:** Carl Nielsen (10,599 âm tiết), cửa sổ ở 30% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tác phẩm đàn organ nào được xem là sáng tác âm nhạc cuối cùng của Carl Nielsen?  
**Đáp án sinh:** Commotio  
**Kiểm:** Commotio (F1 1.0)  
**Cửa sổ (rút gọn):** Nếu tôi có thể sống lại cuộc đời của mình, tôi sẽ đuổi mọi ý nghĩ về Nghệ thuật ra khỏi đầu và học nghề cho một thương gia hoặc theo đuổi một số ngành buôn bán hữu ích khác, kết quả cuối cùng có thể nhìn thấy được. Nó hữu ích gì đối với tôi rằng cả thế giới công nhận tôi, nhưng vội vàng bỏ đi và để tôi một mình với đồ đạc của tôi cho đến khi mọi th…

**Bài:** Carl Nielsen (10,599 âm tiết), cửa sổ ở 69% bài  
**Trạng thái:** kept  
**Câu hỏi:** Bản Sonata thứ hai, Op. 35 của Carl Nielsen được viết cho nghệ sĩ vĩ cầm nào?  
**Đáp án sinh:** Peder Møller  
**Kiểm:** Peder Møller (F1 1.0)  
**Cửa sổ (rút gọn):** Bản Sonata thứ hai, Op. 35 của năm 1912 được viết cho nghệ sĩ vĩ cầm Peder Møller, người đầu năm đó đã công chiếu Bản hòa tấu vĩ cầm của nhà soạn nhạc này. Tác phẩm là một ví dụ về âm điệu tiến bộ của nhà soạn nhạc vì, mặc dù nó được cho là ở phím G nhỏ, các chuyển động đầu tiên và cuối cùng kết thúc bằng các phím khác nhau. Nhà phê bình Emilius Ba…

**Bài:** Âm nhạc thời kỳ Trung cổ (11,559 âm tiết), cửa sổ ở 56% bài  
**Trạng thái:** kept  
**Câu hỏi:** Những bản nhạc viết tay từ thời kỳ Thượng kỳ Trung cổ còn tồn tại đến ngày nay bao gồm những tác phẩm nào?  
**Đáp án sinh:** Musica Enchiriadis, Codex Calixtinus của Santiago de Compostela, và Winchester Troper  
**Kiểm:** Musica Enchiriadis, Codex Calixtinus của Santiago de Compostela, và Winchester Troper (F1 1.0)  
**Cửa sổ (rút gọn):** Rất nhiều tác phẩm âm nhạc ra đời trong giai đoạn Thượng kỳ Trung cổ là vô danh. Một số có thể có tên thì hầu như là của các nhà thơ hoặc những người viết lời bài hát trong khi làn điệu dựa trên đó họ phổ lời lại được viết bởi người khác. Vai trò của nhạc đơn âm trong thời kỳ trung cổ không phải lúc nào cũng đáng tin cậy, những bản nhạc viết tay từ…

**Bài:** Âm nhạc thời kỳ Trung cổ (11,559 âm tiết), cửa sổ ở 54% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thể loại nhạc organum đại diện cho hình thức gì sơ khai?  
**Đáp án sinh:** hoà âm và đặc biệt và đối âm sơ khai  
**Kiểm:** hoà âm và đặc biệt và đối âm sơ khai (F1 1.0)  
**Cửa sổ (rút gọn):** Nhạc phức âm thời kỳ đầu: Organum Khoảng cuối thế kỷ 9, ca sĩ ở các tu viện như St. Gall tại Thuỵ Sĩ bắt đầu thử nghiệm với việc thêm yếu tố khác vào trong thánh ca, thường thấy nhất và một giọng khác hát song song hầu hết cao hơn bè ban đầu một quãng bốn hoặc năm đủ. Thể loại nhạc này được gọi là organum và đại diện cho hình thức hoà âm và đặc biệ…

**Bài:** Âm nhạc thời kỳ Trung cổ (11,559 âm tiết), cửa sổ ở 81% bài  
**Trạng thái:** kept  
**Câu hỏi:** Các bản nhạc phổ Italia viết tay còn đến ngày nay bao gồm những tác phẩm nào?  
**Đáp án sinh:** Squarcialupi Codex và Rossi Codex  
**Kiểm:** Squarcialupi Codex và Rossi Codex (F1 1.0)  
**Cửa sổ (rút gọn):** Thể loại chính thứ ba là ballata, nếu nhìn sơ qua sẽ thấy nét tương đồng với thể loại virelai của Pháp. Các bản nhạc phổ Italia viết tay còn đến ngày nay bao gồm Squarcialupi Codex và Rossi Codex. Có thể tìm hiểu các thêm về các nhà soạn nhạc thời trung cổ tại Ý như: Francesco Landini, Gherardello da Firenze, Andrea da Firenze, Lorenzo da Firenze, …

**Bài:** Âm nhạc thời kỳ Trung cổ (11,559 âm tiết), cửa sổ ở 22% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai được cho là người có cống hiến trong sự hoàn thiện của bốn khe nhạc?  
**Đáp án sinh:** Guido d’ Arezzo  
**Kiểm:** Guido d’ Arezzo (F1 1.0)  
**Cửa sổ (rút gọn):** Đâu chính là khởi đầu của hệ thống ký âm trong âm nhạc mà chúng ta biết đến ngày nay. Sự hoàn thiện của bốn khe nhạc được cho là cống hiến của Guido d’ Arezzo (1000-1050 sau công nguyên), một trong những nhà lý luận âm nhạc quan trọng nhất thời kỳ Trung cổ. Trong khi các nguồn tư liệu cổ hơn cho thấy những đóng góp cho sự phát triển hệ thống ký âm …

**Bài:** Âm nhạc thời kỳ Trung cổ (11,559 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hai ký hiệu cơ bản của các nhà ngữ pháp học cổ đại là gì?  
**Đáp án sinh:** acutus, /, lên cao hay gravis, \, xuống thấp  
**Kiểm:** acutus, /, lên cao hay gravis, \, xuống thấp (F1 1.0)  
**Cửa sổ (rút gọn):** Âm nhạc thời kỳ Trung cổ đặt ra nền tảng thực hành về lý thuyết và ký âm cái sẽ hình thành lên cả nền âm nhạc phương Tây của ngày hôm nay mà đóng góp quan trọng và rõ ràng nhất là sự phát triển của một hệ thống ký âm hoàn thiện; tuy nhiên chính những nguyên lý tiền đề, đặc biệt là về nhịp điệu và âm sắc, cũng có vai trò quan trọng không kém trong s…

**Bài:** Âm nhạc thời kỳ Trung cổ (11,559 âm tiết), cửa sổ ở 89% bài  
**Trạng thái:** kept  
**Câu hỏi:** Kỹ thuật faburden của địa phương được biết đến trên khắp lục địa với tên gọi nào?  
**Đáp án sinh:** fauxbordon  
**Kiểm:** fauxbordon (F1 1.0)  
**Cửa sổ (rút gọn):** Nhạc phức điệu, bắt đầu sử dụng từ thế kỷ 12, được chau truốt hơn với những tiếng nói độc lập cao trong suốt thể kỷ 14. Với John Dunstable và các nhà soạn nhạc Anh khác, một phần thông qua kỹ thuật faburden của địa phương (quá trình ứng tác trong đó một bè thánh ca và phần chính của bản nhạc được viết ở các quãng sáu song song phía trên và được phụ…

**Bài:** Âm nhạc thời kỳ Trung cổ (11,559 âm tiết), cửa sổ ở 73% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thuật ngữ 'Ars nova' được ai đặt ra?  
**Đáp án sinh:** Philippe de Vitry  
**Kiểm:** Philippe de Vitry (F1 1.0)  
**Cửa sổ (rút gọn):** Hạ Kỳ trung cổ (1300-1400) Ars nova là một trong số ít thời kỳ âm nhạc có mốc thời gian khởi đầu và phát triển khá rõ ràng trong lịch sử âm nhạc trung cổ, vì nó tương ứng với sự ra đời của Roman de Fauvel ("Câu chuyện của quỷ Nâu Vàng"), một tác phẩm nhạc thơ đồ sộ, vào những năm 1310 và 1314. Roman de Fauvel châm biếm sự lộng hành của nhà thờ trun…

**Bài:** Âm nhạc thời kỳ Trung cổ (11,559 âm tiết), cửa sổ ở 22% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sự hoàn thiện của bốn khe nhạc được cho là cống hiến của ai?  
**Đáp án sinh:** Guido d’ Arezzo  
**Kiểm:** Guido d’ Arezzo (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, những dòng thể hiện một quãng năm dưới giữa nốt Đô và Fa được sử dụng nhiều nhất. Đầu tiên chỉ là những vết gạch trên giấy da, những dòng này sau đó được vẽ bằng hai màu mực khác nhau: thường là đỏ cho Fa và vàng cho Đô. Đâu chính là khởi đầu của hệ thống ký âm trong âm nhạc mà chúng ta biết đến ngày nay. Sự hoàn thiện của bốn khe nhạc đ…

**Bài:** Chiến dịch Viên (13,760 âm tiết), cửa sổ ở 56% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tổng chỉ huy quân đồn trú trong thành phố Viên?  
**Đáp án sinh:** trung tướng bộ binh Rudolf von Bünau  
**Kiểm:** trung tướng bộ binh Rudolf von Bünau (F1 1.0)  
**Cửa sổ (rút gọn):** Nhiều hào chống tăng, hỏa điểm chống tăng và vật cản chống bộ binh được bố trí tại các khu vực trọng yếu và dễ bị tấn công. Trên đường phố bố trí dày dặc các vật cản, hàng rào, tất cả các công trình bằng đá đều được tận dụng làm nơi đồn trú với các hỏa điểm được bố trí khắp các cửa sổ, tầng hầm và gác mái nhà. Tất cả các cây cầu đều được gài mìn. Q…

**Bài:** Chiến dịch Viên (13,760 âm tiết), cửa sổ ở 40% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Vào lúc 15 giờ 35 phút ngày 16 tháng 3, hai tập đoàn quân cận vệ nào thuộc Phương diện quân Ukraina 3 đã đồng loạt triển khai tấn công?  
**Đáp án sinh:** 4 và 9  
**Kiểm:** Tập đoàn quân cận vệ 4 và 9 (F1 0.55)  
**Cửa sổ (rút gọn):** Tuyến thứ hai dọc theo sông Rába từ Dier (Gyor) đến Maribor. Tuyến thứ ba dọc theo biên giới Áo - Hung. Lúc 15 giờ 35 phút ngày 16 tháng 3, sau 35 phút bắn pháo chuẩn bị, hai tập đoàn quân cận vệ 4 và 9 tại cánh phải của Phương diện quân Ukraina 3 đồng loạt triển khai tấn công. Tuy nhiên, với mật độ pháo binh còn thấp (chưa đủ 180 khẩu/km) và xe tă…

**Bài:** Chiến dịch Viên (13,760 âm tiết), cửa sổ ở 63% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Nhiệm vụ chế áp và vô hiệu hóa pháo binh Đức trong hành động tổng công kích được giao cho ai?  
**Đáp án sinh:** Thượng tướng M. Nedelin - chỉ huy pháo binh của Phương diện quân Ukraina 3 - và thượng tướng không quân A. Sudets - tư lệnh Tập đoàn quân không quân số 17  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Việc chế áp và vô hiệu hóa pháo binh Đức được đặc biệt chú ý trong hành động tổng công kích này. Nhiệm vụ chế áp đó đã được giao cho Thượng tướng M. Nedelin - chỉ huy pháo binh của Phương diện quân Ukraina 3 - và thượng tướng không quân A. Sudets - tư lệnh Tập đoàn quân không quân số 17. Cuối cùng, sau một đợt công kích dữ dội bằng nhiều mũi tấn cô…

**Bài:** Chiến dịch Viên (13,760 âm tiết), cửa sổ ở 67% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người lãnh đạo Nhóm kháng chiến O-5 trong cuộc khởi nghĩa ở Viên?  
**Đáp án sinh:** thiếu tá Carl Szokoll  
**Kiểm:** thiếu tá Carl Szokoll (F1 1.0)  
**Cửa sổ (rút gọn):** Cuộc khởi nghĩa bất thành ở Viên Quân đội Liên Xô không đơn độc khi tấn công vào thành phố Viên. Phía trong lòng Viên vẫn tồn tại những nhóm kháng chiến của các lực lượng yêu nước, chống phát xít của Áo. Trong đó nổi bật nhất có Nhóm kháng chiến O-5 (một thành viên của tổ chức "Nước Áo, hãy thức tỉnh") do thiếu tá Carl Szokoll, Trưởng phòng quân lự…

**Bài:** Chiến dịch Viên (13,760 âm tiết), cửa sổ ở 42% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nguyên soái R. Malinovsky ban đầu muốn giữ lại một phần xe tăng cho mình nhưng cơ quan chỉ huy nào đã không chấp nhận?  
**Đáp án sinh:** STAVKA  
**Kiểm:** STAVKA (F1 1.0)  
**Cửa sổ (rút gọn):** Ban đầu, nguyên soái R. Malinovsky muốn giữ lại một phần xe tăng cho mình nhưng STAVKA không chấp nhận. Sáng 17 tháng 3, Quân đoàn xe tăng cận vệ 5 bắt đầu xuất phát. Dù đã có gắng hết sức nhưng phải mất hai ngày sau, Tập đoàn quân xe tăng cận vệ 6 mới tập kết xong cũng như hoàn thành việc trinh sát địa hình. Vì các trận đánh còn kéo dài nên Nguyên…

**Bài:** Chiến dịch Viên (13,760 âm tiết), cửa sổ ở 87% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Vào ngày 15 tháng 5 năm 1955, các nước đồng minh và Chính phủ Áo đã ký kết văn kiện nào tại Cung điện Belvedere?  
**Đáp án sinh:** Tuyên bố chung công nhận nền độc lập và trung lập của Áo  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Không lâu sau khi Viên bị chiếm, các thành phố lớn khác của nước Áo như Salzburg, St. Pölten, Wolfsberg, Klagenfurt, Linz, Innsbruck đều bị quân đội đồng minh chiếm đóng. Quân đội Đức Quốc xã không còn đủ lực lượng để phòng thủ tại miền Nam nước Đức và Tiệp Khắc khi phạm vi chiếm đóng của họ ngày một thu hẹp. Về kinh tế, vùng công nghiệp Viên và kh…

**Bài:** Chiến dịch Viên (13,760 âm tiết), cửa sổ ở 51% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn cơ giới cận vệ số 2 đã bao vây bao nhiêu binh sĩ Đức tại khu vực phía Tây Tovaros?  
**Đáp án sinh:** 17.000 binh sĩ Đức  
**Kiểm:** 17.000 binh sĩ Đức (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày hôm sau, Tập đoàn quân vượt sông Altalena, đánh quỵ các cuộc chống trả dữ dội của quân Đức và hành tiến về phía Tây. Sáng ngày 19, quân đoàn cơ giới cận vệ số 2 được tung vào trận địa để phát huy chiến quả và đến ngày 10 họ đã tiến đến tuyến sông Danube phía Tây Tovaros và bao vây 17.000 binh sĩ Đức tại khu vực này, bao gồm binh lực của các sư…

**Bài:** Chiến dịch Viên (13,760 âm tiết), cửa sổ ở 49% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Ai là người thay thế Otto Wöhler làm tư lệnh Cụm Tập đoàn quân Nam?  
**Đáp án sinh:** thượng tướng Lothar Rendulic  
**Kiểm:** Lothar Rendulic (F1 0.67)  
**Cửa sổ (rút gọn):** Ngày 1 tháng 4, Đại bản doanh ban hành chỉ thị cho Phương diện quân Ukraina 3 về những mục tiêu cụ thể cho hành động tấn công sắp tới. Chủ lực của Phương diện quân phải đánh chiếm được thủ đô Áo là Viên, và phải tiếp cận tuyến Tulln, Sankt Pölten, NeuLengbach không muộn hơn ngày 12 đến 15 tháng 4, còn các Tập đoàn quân số 26, 27, 57 và Tập đoàn quâ…

**Bài:** Chiến dịch Sa mạc Tây (13,736 âm tiết), cửa sổ ở 92% bài  
**Trạng thái:** kept  
**Câu hỏi:** Đơn vị nào của Sư đoàn Thiết giáp số 7 Anh là đơn vị đầu tiên tiến vào Tripoli vào sáng ngày 23 tháng 1?  
**Đáp án sinh:** Trung đoàn Hussar số 11  
**Kiểm:** Trung đoàn Hussar số 11 (F1 1.0)  
**Cửa sổ (rút gọn):** Rommel rút khỏi Buerat ngày 15 tháng 1. Đòn tấn công chính của Anh được tiến hành dọc theo con đường ven biển do Sư đoàn Highland số 51 và 1 lữ đoàn thiết giáp thực hiện, trong khi Sư đoàn Thiết giáp số 7 tiến tới Tarhuna, Castel Benito và Tripoli. Sư đoàn Khinh binh số 90 Đức đánh cầm chân địch dọc theo con đường này, làm trầm trọng thêm tình trạn…

**Bài:** Chiến dịch Sa mạc Tây (13,736 âm tiết), cửa sổ ở 44% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người chỉ huy Quân đoàn châu Phi được phái đến Libya theo Chỉ thị 22 của Hitler?  
**Đáp án sinh:** tướng Erwin Rommel  
**Kiểm:** Erwin Rommel (F1 0.8)  
**Cửa sổ (rút gọn):** Tại Benghazi–Agedabia, quân Anh bắt sống 25.000 tù binh, chiếm 107 xe tăng và 93 khẩu pháo trong tổng số 133.298 người, 420 xe tăng và 845 khẩu pháo bắt được trong toàn Chiến dịch Compass. Trong chiến dịch mau lẹ này, phía Anh bắt được 130.000 quân Ý mà chỉ chịu thương vong có 2.000 người. Suốt giai đoạn đó, người Ý tưởng rằng mình bị áp đảo mạnh v…

**Bài:** Chiến dịch Sa mạc Tây (13,736 âm tiết), cửa sổ ở 67% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Trung tướng Alfred Reade Godwin-Austen đã từ chức do những bất đồng với ai?  
**Đáp án sinh:** Ritchie  
**Kiểm:** Ritchie, tư lệnh Tập đoàn quân số 8 (F1 0.0)  
**Cửa sổ (rút gọn):** Benghazi thất thủ ngày 28 tháng 1 và ngày 3 tháng 2 thì đến lượt Timimi. Tới ngày 6 tháng 2, quân Anh bị đẩy lui về tuyến Gazala cách Tobruk vài dặm về phía tây, nơi mà 7 tuần lễ trước đó Tập đoàn Panzer Đức đã rút đi. Phía Anh chịu 1.309 thương vong từ ngày 21 tháng 1, mất 42 xe tăng bị hạ, 30 chiếc khác bị thương hoặc hỏng hóc và thiệt 40 khẩu ph…

**Bài:** Chiến dịch Sa mạc Tây (13,736 âm tiết), cửa sổ ở 67% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Trung tướng Alfred Reade Godwin-Austen đã từ chức do những bất đồng với ai?  
**Đáp án sinh:** Ritchie  
**Kiểm:** Ritchie, tư lệnh Tập đoàn quân số 8 (F1 0.0)  
**Cửa sổ (rút gọn):** Benghazi thất thủ ngày 28 tháng 1 và ngày 3 tháng 2 thì đến lượt Timimi. Tới ngày 6 tháng 2, quân Anh bị đẩy lui về tuyến Gazala cách Tobruk vài dặm về phía tây, nơi mà 7 tuần lễ trước đó Tập đoàn Panzer Đức đã rút đi. Phía Anh chịu 1.309 thương vong từ ngày 21 tháng 1, mất 42 xe tăng bị hạ, 30 chiếc khác bị thương hoặc hỏng hóc và thiệt 40 khẩu ph…

**Bài:** Chiến dịch Sa mạc Tây (13,736 âm tiết), cửa sổ ở 86% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tham mưu trưởng quân đội Ý đã tán thành việc rút lui 320 km về phía tây tới Buerat vào ngày 24 tháng 11?  
**Đáp án sinh:** Ugo Cavallero  
**Kiểm:** Ugo Cavallero (F1 1.0)  
**Cửa sổ (rút gọn):** Tập đoàn Panzer chỉ còn lại 5.000 quân, 20 xe tăng, 20 súng chống tăng và 50 khẩu pháo dã chiến. Nỗ lực bao vây các lực lượng phe Trục tại Marsa Matruh đã bị mưa phá hỏng và phần còn lại của Quân đoàn châu Phi trốn thoát trong ngày 7 tháng 11. Lực lượng Trục rút dọc theo bờ biển và cắt đứt con đường này, nhưng do thiếu xe tăng và nhiên liệu không t…

**Bài:** Chiến dịch Sa mạc Tây (13,736 âm tiết), cửa sổ ở 91% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Đơn vị nào là đầu tiên tiến vào Tripoli vào sáng ngày 23 tháng 1?  
**Đáp án sinh:** Trung đoàn Hussar số 11 thuộc Sư đoàn Thiết giáp số 7 Anh  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Mặc dù Buerat không được bảo vệ mạnh và đã được tình báo cho hay về tình trạng của lực lượng phe Trục, Montgomery vẫn ngừng lại cho đến ngày 16 tháng 1 năm 1943, khi mà Tập đoàn quân số 8 đã có được ưu thế 4:1 về bộ binh và 7,5:1 về xe tăng. Cuộc oanh tạc bắt đầu ngày 12 tháng 1 và Quân đoàn XXX tấn công ngày 15 tháng 1 theo con đường dọc bờ biển, …

**Bài:** Chiến dịch Sa mạc Tây (13,736 âm tiết), cửa sổ ở 27% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo tuyên bố của người Anh, họ đã gây cho quân Ý thiệt hại bao nhiêu người trong vòng 2 tháng chiến đấu trên sa mạc từ 11 tháng 6 đến 9 tháng 9?  
**Đáp án sinh:** khoảng 3.500 người  
**Kiểm:** khoảng 3.500 người (F1 1.0)  
**Cửa sổ (rút gọn):** Cát làm các thiết bị hao mòn nhanh chóng, rút ngắn tuổi thọ bánh xích xe tăng, làm cạn kiệt phụ tùng thay thế và chỉ có một nửa lực lượng tăng có thể tiếp tục hoạt động. Đứng trước tình hình này và nhận ra rằng một lực lượng hữu hiệu của mình đã kiệt sức mà chẳng có mục đích chiến lược nào, Wavell liền hạn chế mở rộng chiến sự và bàn giao việc phòn…

**Bài:** Chiến dịch Sa mạc Tây (13,736 âm tiết), cửa sổ ở 73% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn Panzer châu Phi tiến vào Ai Cập trong chiến dịch nào nhằm tiêu diệt tàn quân Tập đoàn quân số 8 Anh?  
**Đáp án sinh:** Chiến dịch Aïda  
**Kiểm:** Chiến dịch Aïda (F1 1.0)  
**Cửa sổ (rút gọn):** Mùa xuân năm 1942, các đơn vị Luftwaffe trở lại Địa Trung Hải và vô hiệu hóa khả năng tấn công của quân đồn trú trên đảo. Rommel lúc đó đang rất mong đợi được tấn công, đã chấn chỉnh lại lực lượng tại Libya để đón đầu một cuộc tấn công của Tập đoàn quân số 8 Anh và được Hitler và Mussolini đồng ý với điều kiện là cuộc tiến quân của ông sẽ dừng lại …

**Bài:** Chiến dịch Đông Carpath (17,936 âm tiết), cửa sổ ở 96% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà xuất bản nào đã ấn hành cuốn sách 'Bộ Tổng tham mưu Xô Viết trong chiến tranh'?  
**Đáp án sinh:** Nhà xuất bản Tiến Bộ  
**Kiểm:** Nhà xuất bản Tiến Bộ (F1 1.0)  
**Cửa sổ (rút gọn):** — М.: «Советская Россия», 1972. Шли по чешской земле партизаны... Bộ Tổng tham mưu Xô Viết trong chiến tranh. Nhà xuất bản Tiến Bộ. Những bí mật của Chiến tranh thế giới thứ hai. Nhà xuất bản Sự Thật. Bản đồ các hoạt động quân sự của Liên Xô tại Đông Carpath và cuộc khởi nghĩa Slovakia Bản đồ phòng tuyến Árpád của quân Đức tại khu vực biên giới Slo…

**Bài:** Chiến dịch Đông Carpath (17,936 âm tiết), cửa sổ ở 35% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn Tiệp Khắc 1 đã giành giật điểm cao nào với quân Đức trong ngày 12 tháng 9 năm 1944?  
**Đáp án sinh:** điểm cao 534  
**Kiểm:** điểm cao 534 (F1 1.0)  
**Cửa sổ (rút gọn):** Lợi dụng quân Đức tập trung chặn kích trên hướng Potok, ngày 12 tháng 9 năm 1944, nguyên soái I. Konev điều Quân đoàn cơ giới cận vệ 4 đến khu vực Krosno và đánh chiếm thành phố này hồi 2 giờ 40 phút cùng ngày. Trong cả ngày 12 tháng 9, Quân đoàn Tiệp Khắc 1 đã giành giật điểm cao 534 với quân Đức và kết quả bất phân thắng bại. Quân đoàn Tiệp Khắc …

**Bài:** Chiến dịch Đông Carpath (17,936 âm tiết), cửa sổ ở 1% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn Tiệp Khắc 1 trưởng thành từ đơn vị nào?  
**Đáp án sinh:** Tiểu đoàn tình nguyện Tiệp Khắc  
**Kiểm:** Tiểu đoàn tình nguyện Tiệp Khắc (F1 1.0)  
**Cửa sổ (rút gọn):** Những người khởi nghĩa cố gắng chống chọi với quân Đức tấn công họ từ ba phía trong quân đội Liên Xô vẫn dang bị kẹt lại trên các con đèo ở sườn phía Bắc dãy Carpath. Quân đội Đức Quốc xã đã chống cự dữ dội và tổ chức phòng ngự cứng rắn trong khu vực, khiến cho các mũi tiến công của quân đội Liên Xô gặp rất nhiều khó khăn và thời gian chiến dịch bị…

**Bài:** Chiến dịch Đông Carpath (17,936 âm tiết), cửa sổ ở 54% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo tính toán, việc huy động hết số máy bay ném bom chiến lược của Anh-Mỹ tại châu Âu có thể ngăn cản được lực lượng quân đội nào xâm nhập Slovakia từ đồng bằng Hungary?  
**Đáp án sinh:** 3 sư đoàn Đức và 2 sư đoàn Hungary  
**Kiểm:** 3 sư đoàn Đức và 2 sư đoàn Hungary (F1 1.0)  
**Cửa sổ (rút gọn):** Đối với phương án đổ bộ 2 sư đoàn Liên Xô bằng đường không xuống Slovakia, phía Liên Xô cần tới gần 1.000 chuyến bay của máy bay C-47, mỗi chiếc chỉ chở được không quá 28 người với trang bị, vũ khí hoặc 3 tấn hàng. Trong khi đó, toàn bộ số máy bay vận tải của các Phương diện quân Ukraina 1 và 4 hiện có không quá 170 chiếc. Ngay cả việc đổ 2 sư đoàn…

**Bài:** Chiến dịch Đông Carpath (17,936 âm tiết), cửa sổ ở 50% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là thủ tướng của chế độ Cộng hòa Slovakia (lần thứ nhất) thân Đức được hình thành vào tháng 3 năm 1939?  
**Đáp án sinh:** Josef Tiso  
**Kiểm:** Josef Tiso (F1 1.0)  
**Cửa sổ (rút gọn):** Konev không đồng ý nhưng Tổng tư lệnh tối cao I. Stalin vẫn chuẩn y đề nghị của Bộ Tổng tham mưu. Tình hình Slovakia từ 1939 đến 1944 Sau khi Đức Quốc xã thôn tính phần Đông Tiệp Khắc (cũ), tại lãnh thổ này hình thành các thể chế chính trị khác nhau. Ngày 19 tháng 3 năm 1939, vùng Séc (gồm Bohemia và Morava) ở phía Tây bị nước Đức Quốc xã đặt dưới …

**Bài:** Chiến dịch Đông Carpath (17,936 âm tiết), cửa sổ ở 51% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người đứng đầu cơ quan đại diện ngoại giao Tiệp Khắc tại Moskva, nơi đặt phái đoàn quân sự của Chính phủ Edvard Beneš?  
**Đáp án sinh:** tướng Heliodor Píka  
**Kiểm:** tướng Heliodor Píka (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 19 tháng 3 năm 1939, vùng Séc (gồm Bohemia và Morava) ở phía Tây bị nước Đức Quốc xã đặt dưới chế độ bảo hộ. Tháng 3 năm 1939, tại vùng Slovakia ở phía Đông hình thành chế độ Cộng hòa Slovakia (lần thứ nhất) thân Đức do Josef Tiso làm thủ tướng. Chính phủ Cộng hòa Tiệp Khắc lần thứ nhất do Edvard Beneš lãnh đạo bỏ chạy sang Anh và trở thành ch…

**Bài:** Chiến dịch Đông Carpath (17,936 âm tiết), cửa sổ ở 6% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tư lệnh của Phương diện quân Ukraina 1 tham gia chiến dịch khởi nghĩa ở Slovakia?  
**Đáp án sinh:** Nguyên soái I. Koniev  
**Kiểm:** Nguyên soái I. Koniev (F1 1.0)  
**Cửa sổ (rút gọn):** Từ đầu tháng 8 năm 1944, một cuộc khởi nghĩa ở Slovakia đã được hoạch định với sự tham gia của một số thành viên của Ban lãnh đạo Hội đồng dân tộc Slovakia, Ban lãnh đạo Đảng Cộng sản Slovakia với sự tham gia của các lực lượng du kích trong nước và quốc tế tại Slovakia cùng 2 sư đoàn quân Slovakia sẵn sàng rời bỏ hàng ngũ quân đội Đức Quốc xã để ch…

**Bài:** Chiến dịch Đông Carpath (17,936 âm tiết), cửa sổ ở 83% bài  
**Trạng thái:** kept  
**Câu hỏi:** Chiến dịch Đông Carpath đã có ảnh hưởng tích cực đến các phương diện quân nào đang tấn công bên sườn phải và sườn trái của Phương diện quân Ukraina 4?  
**Đáp án sinh:** Ukraina 1 và Ukraina 2  
**Kiểm:** Ukraina 1 và Ukraina 2 (F1 1.0)  
**Cửa sổ (rút gọn):** Một số khác lại cáo buộc quân đội Liên Xô chỉ đang "lấy thịt đè người", bất chấp thương vong như mọi khi. Chiến dịch Đông Carpath một lần nữa cho thấy rõ bản chất chính trị - quân sự phức tạp của cuộc Chiến tranh thế giới thứ hai, đặc biệt là ở giai đoạn cuối của cuộc chiến. Trong đó, những quyền lợi về chính trị trong quan hệ quốc tế đã đan xen và…

**Bài:** Lực lượng Vũ trang Liên Xô (11,475 âm tiết), cửa sổ ở 16% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sự kiện đáng chú ý nhất về việc quân đội Liên Xô và Đức gặp nhau đã xảy ra ở đâu?  
**Đáp án sinh:** Brest-Litovsk  
**Kiểm:** Brest-Litovsk (F1 1.0)  
**Cửa sổ (rút gọn):** Sau đó, số lượng đã tăng trở lại. Vào ngày 17/9/1939, Hồng quân Liên Xô hành quân vào các vùng lãnh thổ phía đông của Ba Lan (nay là một phần của Belarus và Ukraina), với mục đích bảo vệ Ukraine và Belarus khỏi mối đe dọa bởi Đức, trong đó cuộc tấn công của Đức vào Ba Lan ngày 1/9/1939. Cuộc xâm lược của Liên Xô đã mở ra một mặt trận thứ hai cho ng…

**Bài:** Lực lượng Vũ trang Liên Xô (11,475 âm tiết), cửa sổ ở 93% bài  
**Trạng thái:** kept  
**Câu hỏi:** Đoàn cố vấn quân sự Liên Xô tại Campuchia hoạt động trong khoảng thời gian nào?  
**Đáp án sinh:** tháng 4-12/1970  
**Kiểm:** tháng 4-12/1970 (F1 1.0)  
**Cửa sổ (rút gọn):** Nhóm chuyên gia quân sự Đoàn cố vấn quân sự Liên Xô tại Algeria (1962-1964) Nhóm chuyên gia quân sự Liên Xô tại Angola (1000-1994) Đoàn cố vấn quân sự Liên Xô tại Việt Nam (1961-1991) Đoàn cố vấn quân sự Liên Xô tại Campuchia (tháng 4-12/1970) Nhóm cố vấn quân sự Liên Xô tại Trung Quốc (1923 - cuối những năm 1950) Nhóm chuyên gia quân sự Liên Xô tạ…

**Bài:** Lực lượng Vũ trang Liên Xô (11,475 âm tiết), cửa sổ ở 27% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, xe tăng nào của Hồng quân vượt xa bất kỳ xe tăng nào khác mà quân Đức có vào năm 1941?  
**Đáp án sinh:** Xe tăng T-34  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Do đó, tổng thiệt hại lên tới 8,668,400. Phần lớn các thiệt hại bao gồm người Nga (5,756,000), tiếp theo là người Ukraine (1,377,400). Các thiệt hại của Đức ở Mặt trận phía Đông bao gồm ước tính 3,604,800 thương vong trong chiến đấu và 3,576,300 bị bắt (tổng số 7,181,100); tổn thất của các đồng minh Trục Đức ở Mặt trận phía Đông xấp xỉ 668,163 thươ…

**Bài:** Lực lượng Vũ trang Liên Xô (11,475 âm tiết), cửa sổ ở 64% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Tổng cục Xây dựng Đường bộ Trung ương của Bộ Quốc phòng Liên Xô được thành lập vào năm nào?  
**Đáp án sinh:** Năm 1988  
**Kiểm:** 1988 (F1 0.67)  
**Cửa sổ (rút gọn):** các đơn vị hậu cần Năm 1988, Tổng cục Xây dựng Đường bộ Trung ương của Bộ Quốc phòng Liên Xô được thành lập. Các lực lượng vũ trang Liên Xô được chia theo nguyên tắc lãnh thổ thành các quân khu và các khối quân đội, đồn trú quân sự: Khối quân sự phía Bắc Khối quân sự Trung tâm Khối quân sự phía Nam Khối quân sự tại Đức - Khối quân sự phía Tây Khối …

**Bài:** Lực lượng Vũ trang Liên Xô (11,475 âm tiết), cửa sổ ở 83% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người giữ chức vụ từ năm 1956 đến năm 1985 với cấp bậc Đô đốc Hạm đội Liên Xô?  
**Đáp án sinh:** Sergey Gorshkov  
**Kiểm:** Sergey Gorshkov (F1 1.0)  
**Cửa sổ (rút gọn):** Hạm đội Thái Bình Dương (1935) Căn cứ hải quân Leningrad 1917-1918 - Modil Vasilievich Ivanov, 1924-1926 - Vyacheslav Ivanovich Zof, 1931-1937 - Vladimir Mitrofanovich Orlov, kể từ năm 1935, Đô đốc Hạm đội hạng 1; 1937-1938 - Mikhail Viktorov, Đô đốc Hạm đội hạng 1; 1938-1938 - Pyotr Smirnov, Tư lệnh Tập đoàn quân hạng 1; 1938-1939 - Mikhail Frinov…

**Bài:** Lực lượng Vũ trang Liên Xô (11,475 âm tiết), cửa sổ ở 16% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo tài liệu do Đại tá Krivosheev biên soạn, lực lượng Hồng quân ở Ba Lan có số lượng bao nhiêu lính?  
**Đáp án sinh:** 466,516 lính  
**Kiểm:** 466,516 lính (F1 1.0)  
**Cửa sổ (rút gọn):** Các Hiệp ước Molotov-Ribbentrop, vốn đã bao gồm một giao thức bí mật phân chia ranh giới các "khu vực quyền lợi" của mỗi bên, thiết lập sự phân chia Ba Lan giữa Đức và Liên Xô. Phạm vi lợi ích được xác định của Liên Xô phù hợp với lãnh thổ sau đó chiếm được trong chiến dịch. Lãnh thổ này trở thành một phần của Ukraina Xô và Belarus Xô. Mặc dù các r…

**Bài:** Lực lượng Vũ trang Liên Xô (11,475 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn cơ giới đặc biệt tại Rumania được đồn trú trong khoảng thời gian nào?  
**Đáp án sinh:** 1947-1957  
**Kiểm:** 1947-1957 (F1 1.0)  
**Cửa sổ (rút gọn):** Quân đoàn đặc biệt đồn trú tại Hungary (1955-1957) Quân đoàn cơ giới đặc biệt tại Rumania (1947-1957) Đạo quân có giới hạn Lực lượng Liên Xô tại Afghanistan (Quân đoàn 40, OKSVA) thuộc về quân khu Turkestan và các đơn vị của Lực lượng Biên phòng như là một phần của Đạo quân có giới hạn Lực lượng Liên Xô tại Afghanistan thuộc các khu vực biên giới T…

**Bài:** Lực lượng Vũ trang Liên Xô (11,475 âm tiết), cửa sổ ở 40% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, ít nhất bao nhiêu thường dân Afghanistan đã bị giết ngoài phiến quân trong cuộc chiến?  
**Đáp án sinh:** nửa triệu  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** "Hội chứng Afghanistan" do Quân đội gây ra tương tự như "Hội chứng Việt Nam" của Hoa Kỳ trong cuộc chiến không thành công của chính họ tại Việt Nam. Về mặt chiến thuật, cả hai bên đều tập trung vào các tuyến tiếp tế, nhưng người Hồi giáo Afghanistan đã đào sâu với các đường hầm và vị trí phòng thủ, chống lại các cuộc tấn công bằng pháo và không quâ…

**Bài:** Chiến dịch Tây Carpath (9,006 âm tiết), cửa sổ ở 75% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn bộ binh sơn chiến 49 (Đức) đã chiếm lại thành phố nào vào ngày 9 tháng 3?  
**Đáp án sinh:** Ružomberok  
**Kiểm:** Ružomberok (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 5 tháng 3, Quân đoàn bộ binh sơn chiến 49 (Đức) được tăng cường Trung đoàn xe tăng 5 thuộc Sư đoàn xe tăng "Wiking" lấy từ Quân đoàn bộ binh 11 sang tổ chức phản công, chiếm lại các điểm cao 704 và 768. Pháo binh Đức lập tức được điều đến hai điểm cao này và khống chế Liptovský Mikuláš. Ngày 8 tháng 3, tướng Karl von Le Suire tổ chức một cuộc …

**Bài:** Chiến dịch Tây Carpath (9,006 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân 17 tham gia chiến dịch do ai chỉ huy?  
**Đáp án sinh:** trung tướng bộ binh Friedrich Schulz  
**Kiểm:** trung tướng bộ binh Friedrich Schulz (F1 1.0)  
**Cửa sổ (rút gọn):** Thành phần tham gia chiến dịch gồm có: Tập đoàn quân 17 do trung tướng bộ binh Friedrich Schulz chỉ huy. Quân đoàn bộ binh 59 do các tướng Edgar Röhricht (đến 29 tháng 1 năm 1945), Joachim von Tresckow (đến 1 tháng 2 năm 1945) và Ernst Sieler chỉ huy, gồm có: Sư đoàn bộ binh 68. Sư đoàn bộ binh 75. Sư đoàn bộ binh 253. Sư đoàn bộ binh 259. Quân đoà…

**Bài:** Chiến dịch Tây Carpath (9,006 âm tiết), cửa sổ ở 93% bài  
**Trạng thái:** kept  
**Câu hỏi:** Đại tướng A. Yeryomenko, người thay thế I. Petrov làm tham mưu trưởng Phương diện quân Ukraina 1, giữ chức vụ gì trước đó?  
**Đáp án sinh:** nguyên Tư lệnh Phương diện quân Pribaltic 2  
**Kiểm:** Tư lệnh Phương diện quân Pribaltic 2 (F1 0.93)  
**Cửa sổ (rút gọn):** Petrov làm việc ăn ý với Mekhlis và Petrov không có gì phàn nàn về Mekhlis" nhưng sau chiến dịch, I. Stalin vẫn quyết định thay I. Ngày 25 tháng 3 năm 1945, đại tướng I. Petrov được điều đi làm tham mưu trưởng Phương diện quân Ukraina 1. Thay thế ông là đại tướng A. Yeryomenko, nguyên Tư lệnh Phương diện quân Pribaltic 2. Saldalov, nguyên tham mưu …

**Bài:** Chiến dịch Tây Carpath (9,006 âm tiết), cửa sổ ở 91% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người thay thế đại tướng I. Petrov làm Tư lệnh Phương diện quân Ukraina 4?  
**Đáp án sinh:** đại tướng A. Yeryomenko  
**Kiểm:** đại tướng A. Yeryomenko (F1 1.0)  
**Cửa sổ (rút gọn):** Pliyev sang hướng Tây Bắc Budapest dù là do tình huống bắt buộc để tập trung quân giải phóng Budapest nhưng cũng có tác động tiêu cực đến tiến trình của chiến dịch Tây Carpath. Binh lực của 5 tập đoàn quân Liên Xô vốn đã không chiếm ưu thế áp đảo so với quân Đức lại bị dàn mỏng thêm nên khó có thể duy trì các trận tấn công liên tục quá một tuần. Mặ…

**Bài:** Chiến dịch Tây Carpath (9,006 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tướng I. Petrov yêu cầu Tập đoàn quân cận vệ 1 điều các sư đoàn bộ binh nào chi viện cho Tập đoàn quân 38?  
**Đáp án sinh:** 271 và 276  
**Kiểm:** 271 và 276 (F1 1.0)  
**Cửa sổ (rút gọn):** Trong hai ngày tấn công đầu tiên, các sư đoàn Liên Xô đều bị đánh bật trở lại. Để đánh chiếm thành phố này, tướng I. Petrov yêu cầu Tập đoàn quân cận vệ 1 điều các sư đoàn bộ binh 271 và 276 chi viện cho Tập đoàn quân 38. Grechko vẫn phải hoàn thành nhiệm vụ phải đánh chiếm Żywiec trước ngày 3 tháng 2 để cắt đứt con đường rút quân cuối cùng của Quâ…

**Bài:** Chiến dịch Tây Carpath (9,006 âm tiết), cửa sổ ở 8% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là tư lệnh của Phương diện quân Ukraina 4?  
**Đáp án sinh:** đại tướng I. Petrov  
**Kiểm:** đại tướng I. Petrov (F1 1.0)  
**Cửa sổ (rút gọn):** Binh lực và kế hoạch Quân đội Liên Xô và các đồng minh Phương diện quân Ukraina 4 (tư lệnh: đại tướng I. Petrov, tham mưu trưởng: trung tướng F. Korzhenyevich), với quân số tổng cộng 267.500 người, bao gồm: Tập đoàn quân 38 do thượng tướng K. Quân đoàn 52 gồm các sư đoàn 81, 121 và 340. Quân đoàn 67 gồm các sư đoàn 211, 241 và 305. Quân đoàn 101 gồ…

**Bài:** Chiến dịch Tây Carpath (9,006 âm tiết), cửa sổ ở 11% bài  
**Trạng thái:** kept  
**Câu hỏi:** Sư đoàn 76 thuộc lực lượng phòng không bao gồm những trung đoàn nào?  
**Đáp án sinh:** 223, 416, 447, 591  
**Kiểm:** 223, 416, 447, 591 (F1 1.0)  
**Cửa sổ (rút gọn):** Các trung đoàn 805, 839 (lựu pháo); 1506, 1642, 1663 (chống tăng); 5, 6, 83, 96 (súng cối cận vệ); 144, 276, 491, 618 (súng cối); 197 (sơn pháo). Phòng không: Sư đoàn 76 gồm các trung đoàn 223, 416, 447, 591; Trung đoàn độc lập 1954. Thiết giáp: Các trung đoàn xe tăng 8, 12 (cận vệ). Công binh: Lữ đoàn hỗn hợp 39. Tập đoàn quân cận vệ 1 do thượng t…

**Bài:** Chiến dịch Tây Carpath (9,006 âm tiết), cửa sổ ở 67% bài  
**Trạng thái:** answer_not_verbatim  
**Câu hỏi:** Tuyến phòng ngự của quân Đức tại các tuyến sông Poprad và thượng nguồn sông Váh có độ sâu bao nhiêu?  
**Đáp án sinh:** 7 km  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Chiều 12 tháng 2, các sư đoàn bộ binh 211, 340 và Trung đoàn xe tăng cận vệ 1 tiến vào giải phóng Bielsko-Biała. Trong 6 ngày tiếp theo, các sư đoàn của Tập đoàn quân 38 (Liên Xô) cố gắng đột phá sang phía Tây nhưng vẫn phải dừng lại trước tuyến sông Olza do tướng Ferdinand Schörner đã điều đến đây Sư đoàn xe tăng 18 SS và một phần Sư đoàn xe tăng …

**Bài:** Chiến dịch tấn công Moravská–Ostrava (11,786 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thành phố công nghiệp nào đã được Quân đội Liên Xô giải phóng vào ngày 30 tháng 4 năm 1945?  
**Đáp án sinh:** Moravská-Ostrava  
**Kiểm:** Moravská-Ostrava (F1 1.0)  
**Cửa sổ (rút gọn):** Hai mũi tấn công được thực hiện từ ngày 15 tháng 4. Ngày 30 tháng 4 năm 1945, Quân đội Liên Xô giải phóng thành phố công nghiệp Moravská-Ostrava. Trên cánh trái, Tập đoàn quân 18 (Liên Xô) cũng phối hợp với cánh phải của Phương diện quân Ukraina 2 tấn công sang phía Tây, dồn Tập đoàn quân xe tăng 1 (Đức) vào "cái túi" Přerov - Olomouc. 12 giờ trưa …

**Bài:** Chiến dịch tấn công Moravská–Ostrava (11,786 âm tiết), cửa sổ ở 8% bài  
**Trạng thái:** kept  
**Câu hỏi:** Moravská-Ostrava nằm trong một thung lũng lớn, nơi hợp lưu của ba con sông nào?  
**Đáp án sinh:** Odra, Opava và Ostravice  
**Kiểm:** Odra, Opava và Ostravice (F1 1.0)  
**Cửa sổ (rút gọn):** Khu vực tác chiến là một vùng núi già với các đỉnh tròn đặc trưng, độ cao từ 200 đến 425 m. Tuy thấp hơn dãy Carpath chính ở phía Đông nhưng vùng này lại có nhiều khối núi trải rộng từ 2 km ở phía Đông đến 10–15 km ở phía Tây. Moravská-Ostrava nằm trong một thung lũng lớn, nơi hợp lưu của ba con sông Odra, Opava và Ostravice (các chi lưu hợp thành …

**Bài:** Chiến dịch tấn công Moravská–Ostrava (11,786 âm tiết), cửa sổ ở 26% bài  
**Trạng thái:** kept  
**Câu hỏi:** Mũi tấn công chính trong kế hoạch tấn công ban đầu của quân đội Liên Xô do những đơn vị nào phụ trách?  
**Đáp án sinh:** Tập đoàn quân cận vệ số 1 và Tập đoàn quân 38  
**Kiểm:** Tập đoàn quân cận vệ số 1 và Tập đoàn quân 38 (F1 1.0)  
**Cửa sổ (rút gọn):** Công binh: Lữ đoàn cầu cận vệ 22, Lữ đoàn công trình 59, Tiểu đoàn mìn 8 Phòng hóa: Các tiểu súng phun lửa 1 và 37 Quân đoàn xe tăng 31 (phối thuộc Tập đoàn quân 60). Xe tăng: Các lữ đoàn 100, 237, 242 Cơ giới: Lữ đoàn 65 Mô tô: Tiểu đoàn 98 Pháo tự hành: Trung đoàn cận vệ 367 (chống tăng), các trung đoàn 722, 1442 Pháo và súng cối: Các trung đoàn …

**Bài:** Chiến dịch tấn công Moravská–Ostrava (11,786 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn sơn chiến nhẹ 127 gồm các lữ đoàn nào?  
**Đáp án sinh:** các lữ đoàn 3, 69 và 70  
**Kiểm:** các lữ đoàn 3, 69 và 70 (F1 1.0)  
**Cửa sổ (rút gọn):** Phòng hóa: Các đại đội súng phun lửa 9, 26 Tập đoàn quân 38 do thượng tướng K. Quân đoàn 52 gồm các sư đoàn 121, 241 và 305 Quân đoàn 95 gồm Sư đoàn đổ bộ đường không cận vệ 2 các sư đoàn 271 và 351 Quân đoàn 101 gồm các sư đoàn 70 (cận vệ), 140 và 183 Quân đoàn sơn chiến nhẹ 126 gồm các lữ đoàn sơn chiến 31, 32 và 72 Quân đoàn sơn chiến nhẹ 127 gồ…

**Bài:** Chiến dịch tấn công Moravská–Ostrava (11,786 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thành phố công nghiệp nào đã được Quân đội Liên Xô giải phóng vào ngày 30 tháng 4 năm 1945?  
**Đáp án sinh:** Moravská-Ostrava  
**Kiểm:** Moravská-Ostrava (F1 1.0)  
**Cửa sổ (rút gọn):** Hai mũi tấn công được thực hiện từ ngày 15 tháng 4. Ngày 30 tháng 4 năm 1945, Quân đội Liên Xô giải phóng thành phố công nghiệp Moravská-Ostrava. Trên cánh trái, Tập đoàn quân 18 (Liên Xô) cũng phối hợp với cánh phải của Phương diện quân Ukraina 2 tấn công sang phía Tây, dồn Tập đoàn quân xe tăng 1 (Đức) vào "cái túi" Přerov - Olomouc. 12 giờ trưa …

**Bài:** Chiến dịch tấn công Moravská–Ostrava (11,786 âm tiết), cửa sổ ở 35% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tập đoàn quân không quân 4 yểm hộ từ trên không cho Tập đoàn quân xe tăng 1 do ai chỉ huy?  
**Đáp án sinh:** thượng tướng Otto Deßloch  
**Kiểm:** thượng tướng Otto Deßloch (F1 1.0)  
**Cửa sổ (rút gọn):** Quân đoàn bộ binh 11 của tướng Rudolf von Bünau (đến ngày 6 tháng 4) và tướng Friedrich Wiese, gồm Sư đoàn bộ binh trượt tuyết 1, Sư đoàn biệt kích 97, các cụm tác chiến sư đoàn 344 và 371, một phần Sư đoàn xe tăng 5 SS "Wiking" Quân đoàn bộ binh 59 của trung tướng Ernst Sieler gồm các sư đoàn bộ binh 68, 253, các cụm tác chiến sư đoàn bộ binh 75 v…

**Bài:** Chiến dịch tấn công Moravská–Ostrava (11,786 âm tiết), cửa sổ ở 2% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai được cử làm tư lệnh Phương diện quân Ukraina 4 sau khi STAVKA cách chức các tướng I. Korzhenyevich?  
**Đáp án sinh:** Yeryomenko  
**Kiểm:** Yeryomenko (F1 1.0)  
**Cửa sổ (rút gọn):** Tập đoàn quân 18, Quân đoàn bộ binh cận vệ 17 và Quân đoàn Tiệp Khắc 1 chưa kịp chuẩn bị để triển khai các mũi tấn công. Tuyến mặt trận của Phương diện quân Ukraina 4 hầu như không thay đổi so với đầu tháng 3 năm 1945. Giai đoạn thứ hai từ 24 tháng 3 đến 5 tháng 4 năm 1945: Một cuộc tấn công mới được triển khai nhưng tốc độ tấn công vẫn không được …

**Bài:** Chiến dịch tấn công Moravská–Ostrava (11,786 âm tiết), cửa sổ ở 89% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lữ đoàn xe tăng Tiệp Khắc 1 được tặng huân chương gì sau chiến dịch?  
**Đáp án sinh:** Huân chương Suvorov hạng nhì  
**Kiểm:** Huân chương Suvorov hạng nhì (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, sự kiện Phương diện quân Ukraina 4 đánh chiếm Moravská-Ostrava và Žilina đã đe dọa làm thất bại phương án này. Và Bộ chỉ huy Đức không phải chờ đợi lâu. Ngày 6 tháng 5, các chi đội phái đi trước của Quân đoàn xe tăng 31 đánh chiếm Šternberk và tiếp cận ngoại vi Olomouc, những người yêu nước Tiệp Khắc ở Praha đã nổi dậy khởi nghĩa. Sau ch…

**Bài:** Lịch sử tư tưởng kinh tế (18,340 âm tiết), cửa sổ ở 79% bài  
**Trạng thái:** kept  
**Câu hỏi:** Veblen đã chuyển đến thành phố nào vào năm 1918 để bắt đầu làm biên tập viên cho tạp chí The Dial?  
**Đáp án sinh:** New York  
**Kiểm:** New York (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, năm 1911, Veblen gia nhập Đại học Missouri, nơi ông ủng hộ Herbert Davenport, trưởng khoa kinh tế của trường. Veblen ở lại Columbia, Missouri tới năm 1918. Năm đó, ông chuyển sang New York và bắt đầu làm biên tập viên cho tạp chí The Dial, rồi năm 1919, cùng với Charles A. Beard, James Harvey Robinson và John Dewey, ông chung tay thành l…

**Bài:** Lịch sử tư tưởng kinh tế (18,340 âm tiết), cửa sổ ở 58% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vilfredo Pareto là nhà kinh tế người nào nổi tiếng với việc phát triển khái niệm về nền kinh tế cho phép tối đa hóa độ thỏa dụng của mỗi cá nhân?  
**Đáp án sinh:** người Ý  
**Kiểm:** người Ý (F1 1.0)  
**Cửa sổ (rút gọn):** Điều này khiến người sản xuất dịch chuyển sản xuất, tăng đầu tư vào nấm, tăng cung trên thị trường và đạt tới một mức cân bằng mới giữa các sản phẩm, chẳng hạn như giảm giá nấm xuống mức đâu đó giữa hai mức ban đầu. Với nhiều sản phẩm khác trong nền kinh tế, mọi việc cũng sẽ xảy ra như thế, nếu giả định rằng thị trường là cạnh tranh, mọi người lựa …

**Bài:** Lịch sử tư tưởng kinh tế (18,340 âm tiết), cửa sổ ở 28% bài  
**Trạng thái:** kept  
**Câu hỏi:** Jeremy Bentham là người phát triển khái niệm nào?  
**Đáp án sinh:** chủ nghĩa công lợi  
**Kiểm:** chủ nghĩa công lợi (F1 1.0)  
**Cửa sổ (rút gọn):** Điểm chung trong các học thuyết của họ là học thuyết giá trị lao động, đối lập với giá trị xuất phát từ một sự cân bằng giữa cung và cầu. Những nhà kinh tế này trước hết đã chứng kiến sự chuyển đổi kinh tế xã hội do cuộc Cách mạng công nghiệp: sự giảm dân số ở nông thôn, bất ổn, nghèo đói, sự xuất hiện của giai cấp công nhân. Họ đặt câu hỏi về gia …

**Bài:** Lịch sử tư tưởng kinh tế (18,340 âm tiết), cửa sổ ở 26% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Adam Smith, sự phân công lao động bị giới hạn bởi yếu tố nào?  
**Đáp án sinh:** quy mô của các thị trường  
**Kiểm:** quy mô của các thị trường (F1 1.0)  
**Cửa sổ (rút gọn):** Smith tin rằng một thị trường sẽ sinh ra điều mà ông gọi là sự giàu có gia tăng. Điều này bao gồm hàng loạt khái niệm, như sự phân công lao động là động lực cho hiệu quả kinh tế, nhưng nó bị giới hạn bởi quy mô của các thị trường. Cả phân công lao động và mở rộng thị trường đòi hỏi sự tích tụ tư bản lớn bởi những doanh nhân và những nhà lãnh đạo ki…

**Bài:** Lịch sử tư tưởng kinh tế (18,340 âm tiết), cửa sổ ở 81% bài  
**Trạng thái:** kept  
**Câu hỏi:** Adolf Berle đã từ nhiệm cương vị ngoại giao của mình ở hội nghị nào?  
**Đáp án sinh:** Hội nghị hòa bình Paris năm 1919  
**Kiểm:** Hội nghị hòa bình Paris năm 1919 (F1 1.0)  
**Cửa sổ (rút gọn):** Commons cho rằng các chính phủ phải đóng vai trò người trung gian giữa các nhóm xung đột. Bản thân Commons dành nhiều thời gian làm việc trung gian và tư vấn trong các ủy ban công nghiệp của chính phủ. Cuộc Đại khủng hoảng là thời gian có những thay đổi mang tính đảo lộn ở Mỹ. Một trong những đóng góp đầu tiên tìm hiểu tại sao mọi việc lại trở nên …

**Bài:** Lịch sử tư tưởng kinh tế (18,340 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** kept  
**Câu hỏi:** Murray Rothbard gọi nhà nước là gì?  
**Đáp án sinh:** tổ chức của những kẻ ăn cướp trắng trợn có hệ thống  
**Kiểm:** tổ chức của những kẻ ăn cướp trắng trợn có hệ thống (F1 1.0)  
**Cửa sổ (rút gọn):** Xây dựng khái niệm trật tự ngẫu nhiên cho trường phái Áo, ủng hộ thị trường tự do trên cơ sở số nhân tiền tệ và lên án kế hoạch hóa tập trung, Murray Rothbard (1926–1995) thúc đẩy việc hủy bỏ kiểm soát cưỡng ép của chính quyền với xã hội và nền kinh tế. Ông coi quyền lực độc quyền của nhà nước là đe dọa lớn nhất với tự do và sự thịnh vượng trong dà…

**Bài:** Lịch sử tư tưởng kinh tế (18,340 âm tiết), cửa sổ ở 89% bài  
**Trạng thái:** kept  
**Câu hỏi:** Điều kiện nào trong các điều kiện của Arrow gây tranh cãi nhiều nhất?  
**Đáp án sinh:** sự độc lập của các nhân tố thay thế không tương quan  
**Kiểm:** sự độc lập của các nhân tố thay thế không tương quan (F1 1.0)  
**Cửa sổ (rút gọn):** Tác phẩm này mở đường cho học thuyết về lựa chọn xã hội và định lý về sự bất khả của Arrow. Lập luận này gây ra tranh luận lớn trong cách diễn giải những điều kiện khác nhau của định lý và ý nghĩa của nó với nền dân chủ và phổ thông đầu phiếu. Gây tranh cãi nhiều nhất trong bốn (1963) hoặc năm (1950-1951) điều kiện của ông là sự độc lập của các nhâ…

**Bài:** Lịch sử tư tưởng kinh tế (18,340 âm tiết), cửa sổ ở 67% bài  
**Trạng thái:** kept  
**Câu hỏi:** John Maynard Keynes sinh ra ở đâu?  
**Đáp án sinh:** Cambridge  
**Kiểm:** Cambridge (F1 1.0)  
**Cửa sổ (rút gọn):** Năm 1918, Đức mở cuộc tấn công mùa xuân, nhưng thất bại, các nước đồng minh phản công dẫn tới việc hàng triệu người thiệt mạng vì chiến tranh. Trong nội bộ nước Đức diễn ra cuộc Cách mạng Đức, chính quyền lâm thời theo đuổi hòa bình trên cơ sở mười bốn điểm của Wilson. Châu Âu là một đống điêu tàn, về tài chính, vật chất và tâm lý, với một tương la…

**Bài:** Harry Potter (loạt phim) (9,912 âm tiết), cửa sổ ở 88% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Hòn đá Phù thủy đã đạt được bao nhiêu đề cử Giải BAFTA?  
**Đáp án sinh:** bảy  
**Kiểm:** bảy đề cử Giải BAFTA (F1 0.33)  
**Cửa sổ (rút gọn):** Hòn đá Phù thủy đã đạt được bảy đề cử Giải BAFTA, bao gồm Phim Anh hay nhất và Nam diễn viên phụ xuất sắc nhất cho Robbie Coltrane. Bộ phim cũng đã được đề cử cho tám giải thưởng Saturn và chiến thắng cho thiết kế trang phục của nó. Nó cũng được đề cử tại Art Director Guild Awards cho thiết kế sản xuất và nhận được Giải thưởng Nhà phê bình Phim tru…

**Bài:** Harry Potter (loạt phim) (9,912 âm tiết), cửa sổ ở 84% bài  
**Trạng thái:** kept  
**Câu hỏi:** Viện phim Hoa Kỳ đã công nhận toàn bộ loạt phim Harry Potter với giải thưởng nào tại Lễ trao giải Viện Phim Hoa Kỳ năm 2011?  
**Đáp án sinh:** Giải Đặc biệt  
**Kiểm:** Giải Đặc biệt (F1 1.0)  
**Cửa sổ (rút gọn):** Ngoài ra, Viện phim Hoa Kỳ đã công nhận toàn bộ loạt phim với Giải Đặc biệt tại Lễ trao giải Viện Phim Hoa Kỳ năm 2011. Giải thưởng đặc biệt "được trao cho những thành tựu xuất sắc trong hình ảnh chuyển động không phù hợp với tiêu chí của AFI cho những người được vinh danh khác". Trong thông cáo báo chí của mình, Viện gọi các bộ phim là "một loạt p…

**Bài:** Harry Potter (loạt phim) (9,912 âm tiết), cửa sổ ở 6% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo quan điểm của Steven Spielberg, việc kiếm tiền từ bộ phim Harry Potter giống như điều gì?  
**Đáp án sinh:** bắn vịt vào thùng  
**Kiểm:** bắn vịt vào thùng (F1 1.0)  
**Cửa sổ (rút gọn):** với giá 1 triệu bảng Anh (2.000.000 USD). Rowling đưa ra yêu cầu là dàn diễn viên chính phải được giữ nghiêm ngặt là người Anh, tuy nhiên cho phép nhiều diễn viên người Ireland, chẳng hạn như Richard Harris trong vai Dumbledore, và tuyển diễn viên Pháp và Đông Âu trong Harry Potter và Chiếc cốc lửa khi các chi tiết trong sách được chỉ định như vậy.…

**Bài:** Harry Potter (loạt phim) (9,912 âm tiết), cửa sổ ở 95% bài  
**Trạng thái:** kept  
**Câu hỏi:** Bộ phim Harry Potter nào do Alfonso Cuarón đạo diễn được cho là có doanh thu thấp nhất trong loạt phim?  
**Đáp án sinh:** Tên tù nhân ngục Azkaban  
**Kiểm:** Tên tù nhân ngục Azkaban (F1 1.0)  
**Cửa sổ (rút gọn):** Hòn đá phù thủy của Chris Columbus đã trở thành bộ phim Harry Potter có doanh thu cao nhất trên toàn thế giới sau khi hoàn thành ra rạp vào năm 2002, nhưng cuối cùng nó lại đứng đầu là Bảo bối Tử thần – Phần 2 của David Yates, trong khi Tên tù nhân ngục Azkaban của Alfonso Cuarón kiếm được ít nhất. Sáu bộ phim trong loạt phim Harry Potter — Harry P…

**Bài:** Harry Potter (loạt phim) (9,912 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo lời kể của Heyman, ấn tượng đầu tiên của anh về cậu bé có đôi mắt xanh to tròn ngồi đằng sau mình là gì?  
**Đáp án sinh:** Cậu ấy tò mò, vui tính và rất năng động  
**Kiểm:** tò mò, vui tính và rất năng động (F1 0.89)  
**Cửa sổ (rút gọn):** Theo cách nói của Heyman, "Ngồi đằng sau tôi là cậu bé có đôi mắt xanh to tròn này. Tôi nhớ ấn tượng đầu tiên của mình: Cậu ấy tò mò, vui tính và rất năng động. Ngoài ra còn có sự hào phóng và ngọt ngào. Nhưng ở đồng thời anh ta thực sự rất phàm ăn và khao khát kiến ​​thức về bất cứ thứ gì." Radcliffe đã tự khẳng định mình là một diễn viên trong bộ…

**Bài:** Harry Potter (loạt phim) (9,912 âm tiết), cửa sổ ở 86% bài  
**Trạng thái:** kept  
**Câu hỏi:** Loạt phim Harry Potter đã nhận được tổng cộng bao nhiêu đề cử tại Giải thưởng Điện ảnh Viện hàn lâm Anh (BAFTA)?  
**Đáp án sinh:** 24 đề cử  
**Kiểm:** 24 đề cử (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, những người khác lại chỉ ra rằng một số phim trong loạt phim này có đánh giá không đồng đều, trái ngược với ba phim Chúa tể của những chiếc nhẫn, chẳng hạn, đều được giới phê bình đánh giá cao. Điều này một phần được cho là do loạt phim Harry Potter trải qua một số đạo diễn, mỗi người có phong cách đạo diễn riêng, trái ngược với bộ ba Ch…

**Bài:** Harry Potter (loạt phim) (9,912 âm tiết), cửa sổ ở 13% bài  
**Trạng thái:** kept  
**Câu hỏi:** David Heyman đã được xác nhận sẽ đảm nhận vai trò gì cho bộ phim Harry Potter?  
**Đáp án sinh:** sản xuất bộ phim  
**Kiểm:** sản xuất bộ phim (F1 1.0)  
**Cửa sổ (rút gọn):** David Heyman đã được xác nhận sẽ sản xuất bộ phim. Rowling nhận được một lượng lớn quyền kiểm soát sáng tạo cho bộ phim, một sự sắp xếp mà Columbus không bận tâm. ban đầu đã lên kế hoạch phát hành bộ phim đầu tiên vào cuối tuần 4 tháng 7 năm 2001, tạo ra thời hạn sản xuất ngắn đến mức một số đạo diễn được đề xuất ban đầu đã rút lui khỏi tranh chấp.…

**Bài:** Harry Potter (loạt phim) (9,912 âm tiết), cửa sổ ở 71% bài  
**Trạng thái:** kept  
**Câu hỏi:** Bốn tiểu thuyết đầu tiên trong loạt truyện Harry Potter đã được J. Rowling bán bản quyền cho Warner Bros. với giá bao nhiêu?  
**Đáp án sinh:** 1.000.000 bảng Anh  
**Kiểm:** 1.000.000 bảng Anh (F1 1.0)  
**Cửa sổ (rút gọn):** Harry Potter và Bảo bối Tử thần – Phần 1 (2010) phải|nhỏ|Nhà tranh của gia đình Potter từ phần phim cuối cùng.Sau những sự kiện bất ngờ xảy ra vào cuối năm trước, Harry, Ron và Hermione được giao cho nhiệm vụ tìm và phá hủy bí mật trường sinh bất tử của Chúa tể Voldemort – Trường sinh linh giá. Đáng lẽ đây là năm cuối cùng của họ tại Hogwarts, nhưn…

**Bài:** Chiến tranh Punic lần thứ hai (12,498 âm tiết), cửa sổ ở 27% bài  
**Trạng thái:** kept  
**Câu hỏi:** Viên chỉ huy Latin ở địa phương đã phản bội và tạo cơ hội cho người Carthage đánh chiếm kho lương tại đâu?  
**Đáp án sinh:** Clastidium  
**Kiểm:** Clastidium (F1 1.0)  
**Cửa sổ (rút gọn):** Ngay cả trước khi tin tức về thất bại tại sông Ticinus truyền tới Roma, viện nguyên lão đã ra lệnh cho chấp chính quan Sempronius Longus đem đạo quân của ông ta quay trở về từ Sicily, nơi mà nó đang chuẩn bị cho cuộc xâm lược châu Phi, để kết hợp cùng Scipio và đối phó với Hannibal. Hannibal đã ngăn chặn không cho quân đội của Scipio và Sempronius …

**Bài:** Chiến tranh Punic lần thứ hai (12,498 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** Fabius đã làm gì để có tiền trả cho quân địch và nhận lại số tù binh còn lại?  
**Đáp án sinh:** bán các điền trang của mình  
**Kiểm:** bán các điền trang của mình (F1 1.0)  
**Cửa sổ (rút gọn):** Đường lối của Fabius chẳng khác gì cái bóng của Hannibal bằng cách di chuyển theo chiều song song với đà tiến quân của người Carthage trên vùng đồng bằng, để tránh kỵ binh của Hannibal vốn có ưu thế trên địa hình bằng phẳng. Điều này đòi hỏi một sự cẩn trọng tuyệt đối, vì khi đó người Carthage đã cố gắng với tất cả khả năng của mình để phục kích nh…

**Bài:** Chiến tranh Punic lần thứ hai (12,498 âm tiết), cửa sổ ở 70% bài  
**Trạng thái:** kept  
**Câu hỏi:** Năm 211 TCN, Roma đã chống lại mối đe dọa từ Macedonia cùng với liên minh Hy Lạp của những ai?  
**Đáp án sinh:** người Aetolia, Elis, Sparta, Messenia và Attalos I của Pergamon  
**Kiểm:** người Aetolia, Elis, Sparta, Messenia và Attalos I của Pergamon (F1 1.0)  
**Cửa sổ (rút gọn):** Năm 210 TCN: Cuộc viễn chinh đường biển tới Tarentum Năm 210 TCN: Những cuộc tập kích của La Mã ở châu Phi Miền đông Địa Trung Hải và biển Ionia (212-207 TCN) Năm 211 TCN, Roma chống lại mối đe dọa từ Macedonia cùng với một liên minh Hy Lạp của người Aetolia, Elis, Sparta, Messenia và Attalos I của Pergamon, cũng như hai vị vua chư hầu người Ilyria…

**Bài:** Chiến tranh Punic lần thứ hai (12,498 âm tiết), cửa sổ ở 78% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người đã được giao quyền chỉ huy các quân đoàn ở Sicily và được phép tuyển mộ tình nguyện viên cho kế hoạch xâm lược châu Phi?  
**Đáp án sinh:** Scipio Africanus Major  
**Kiểm:** Scipio Africanus Major (F1 1.0)  
**Cửa sổ (rút gọn):** Miền Trung Địa Trung Hải (206-202 TCN) Mang chiến tranh đến châu Phi Năm 205 TCN, Mago đặt chân lên đất Ý. Ông ta đến nơi vào thời điểm vừa diễn ra trận Crotona (ngày nay là Crotone) và tới năm sau, ông ta đã bị đánh bại trong cuộc đột kích thung lũng Po năm 203TCN. Đồng thời, Scipio Africanus Major đã được giao quyền chỉ huy của các quân đoàn ở Si…

**Bài:** Chiến tranh Punic lần thứ hai (12,498 âm tiết), cửa sổ ở 54% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là thuộc cấp của Hannibal đã xây dựng được một đội quân ở vùng Samnium?  
**Đáp án sinh:** Hanno  
**Kiểm:** Hanno (F1 1.0)  
**Cửa sổ (rút gọn):** Bản chất chiến dịch của Hannibal ở Ý là sử dụng các nguồn lực tại chỗ để chống lại người La Mã và chiêu mộ thêm binh lính từ những cư dân địa phương. Hanno, thuộc cấp của ông đã có xây dựng được một đội quân ở vùng Samnium, nhưng người La Mã đã chặn đạo quân mới được chiêu mộ này trong trận Beneventum (214 TCN) và tiêu diệt nó trước khi nó có thể n…

**Bài:** Chiến tranh Punic lần thứ hai (12,498 âm tiết), cửa sổ ở 63% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người đã phát minh ra các cỗ máy chiến tranh trong cuộc vây hãm Syracuse?  
**Đáp án sinh:** Archimedes  
**Kiểm:** Archimedes (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, bến cảng đã bị phong tỏa và những con tàu chiến phải vận chuyển bằng đường bộ để có thể đưa ra biển hạ thủy. Trận Capua (212 TN) là một sự bế tắc, vì không bên nào có thể đánh bại đối phương. Người La Mã đã quyết định rút quân và từ bỏ cuộc vây hãm Capua. Kết quả là, kỵ binh Capua đã được tăng cường bằng một nửa lực lượng kỵ binh Numidia…

**Bài:** Chiến tranh Punic lần thứ hai (12,498 âm tiết), cửa sổ ở 50% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thành công lớn nhất mà Hannibal giành được là thành phố nào của Ý?  
**Đáp án sinh:** Capua  
**Kiểm:** Capua (F1 1.0)  
**Cửa sổ (rút gọn):** Thành công lớn nhất mà ông giành được đó là thành phố lớn thứ hai của Ý, Capua, khi quân đội của Hannibal hành quân vào vùng Campania trong năm 216 TCN. Cư dân của Capua đã có quyền công dân La Mã một cách giới hạn và tầng lớp quý tộc của nó đã liên kết với những người La Mã thông qua hôn nhân và tình bạn, nhưng với tham vọng có thể trở thành thành…

**Bài:** Chiến tranh Punic lần thứ hai (12,498 âm tiết), cửa sổ ở 79% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người đã chiếm giữ một phần lớn vương quốc của Syphax với sự giúp đỡ từ người La Mã?  
**Đáp án sinh:** Masinissa  
**Kiểm:** Masinissa (F1 1.0)  
**Cửa sổ (rút gọn):** Các quân đoàn ở Sicily chủ yếu là những người sống sót sau trận Cannae, nhưng họ không được cho phép về nhà cho đến khi chiến tranh đã kết thúc. Scipio cũng một trong những người sống sót và đã từng cùng chiến đấu với họ trong suốt cuộc vây hãm Syracuse, nhưng không giống như những người lính bình thường, sau đó ông đã được cho phép về nhà, và tiếp…

**Bài:** Hậu cung nhà Thanh (20,405 âm tiết), cửa sổ ở 95% bài  
**Trạng thái:** kept  
**Câu hỏi:** Loại trang sức đầu nào của phụ nữ quý tộc nhà Thanh được hình thành và đạt đỉnh điểm vào thời Càn Long?  
**Đáp án sinh:** Điền tử  
**Kiểm:** Điền tử (F1 1.0)  
**Cửa sổ (rút gọn):** Loại Cát phục quan này, có thể thấy giống với mũ nam giới, đầu là dạng mũ chóp lông đỏ, có thể tùy theo cấp bậc mà có điểm trang sức. Song trong các tranh họa thời kỳ này cũng có người không đội mũ mà chỉ biện tóc, tùy ý cài thêm hai ba loại trang sức. Lại có người dùng khăn đen phủ đầu, cài trâm. Sau này, loại khăn đó hình thành và đỉnh điểm ở thờ…

**Bài:** Hậu cung nhà Thanh (20,405 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo quy tắc của đời Thanh, khái niệm "Hán" trong quy định "Mãn-Hán không thể liên hôn" cụ thể chỉ đến đối tượng nào?  
**Đáp án sinh:** Hán nhân  
**Kiểm:** Hán nhân (F1 1.0)  
**Cửa sổ (rút gọn):** Phim truyện về triều Thanh đặc biệt rất hay nhầm lẫn giữa hai khái niệm này. Đời Thanh có quy tắc「Mãn-Hán không thể liên hôn」 , trong đó "Hán" chính là nói đến Hán nhân, không phải người Hán Quân Bát kỳ. Ngoài ra, những người có thể có gốc Hán mà được phân vào Bao y, cũng đều là "Kỳ nhân", không còn là "Hán nhân" nữa. Giữa Kỳ phân và Bao y đôi khi …

**Bài:** Hậu cung nhà Thanh (20,405 âm tiết), cửa sổ ở 3% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, Trát Lỗ Đặc Bác Nhĩ Tế Cát Đặc thị được sách lập làm chức vị gì vào năm Thiên Thông thứ 6?  
**Đáp án sinh:** Đông cung Phúc tấn  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Nhàn tản Phụ nhân (闲散妇人; Sula hehesi); Trên thực tế, lúc đó trong hậu cung sinh hoạt tuy rằng đồng dạng thuộc về cấp bậc Thứ phi, nhưng là căn cứ xưng hô bất đồng mà cũng có địa vị cao thấp khác nhau. Tỷ như nói “Ajige fujin” thân phận liền phải so cao hơn các “Buya sargan”, nhưng các “Ajige fujin” vẫn như cũ không thể bị xếp vào hàng Trắc Phúc tấn…

**Bài:** Hậu cung nhà Thanh (20,405 âm tiết), cửa sổ ở 0% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, danh xưng chung của các Thê thiếp của Nỗ Nhĩ Cáp Xích sau khi ông xưng Đại hãn là gì?  
**Đáp án sinh:** Chúng Phúc tấn  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Hậu cung Nhà Thanh (chữ Hán: 清朝後宮; "Thanh triều Hậu cung") là quy định và trật tự của hậu cung dưới thời nhà Thanh trong lịch sử Trung Quốc. Ngoài bản thân Hoàng đế là chủ nhân, bên cạnh đó còn có Hoàng thái hậu, Hoàng hậu cùng Phi tần, Thái giám và Cung nữ, tất cả đều tham gia vào sự vận động cuộc sống sinh hoạt hằng ngày trong cung. Triều đại nhà…

**Bài:** Hậu cung nhà Thanh (20,405 âm tiết), cửa sổ ở 29% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo quy định của nhà Minh, vị Hoàng thái hậu nào được gọi là Hoàng thái hậu mà không có tôn hiệu?  
**Đáp án sinh:** Hoàng sinh mẫu  
**Kiểm:** Hoàng sinh mẫu (F1 1.0)  
**Cửa sổ (rút gọn):** Lịch sử Thanh cung chỉ có 2 vị Thái hoàng thái hậu, là Hiếu Trang Văn Hoàng hậu cùng Hiếu Khâm Hiển Hoàng hậu (tức Từ Hi Hoàng thái hậu). Trong hậu cung, với vai trò là trưởng bối và là bà nội của Hoàng đế, Thái hoàng thái hậu có bối phận cao nhất đương thời, khi Hiếu Trang Văn Hoàng hậu là Thái hoàng thái hậu thì ý chỉ của bà được xem là tối cao n…

**Bài:** Hậu cung nhà Thanh (20,405 âm tiết), cửa sổ ở 49% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo quy định trong cung đình nhà Thanh, hình phạt cao nhất dành cho cung nữ phạm đại tội bất nghịch là gì?  
**Đáp án sinh:** đuổi khỏi cung  
**Kiểm:** đuổi khỏi cung (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy thân phận hầu hạ, nhưng người Bao y trong xã hội đời Thanh đều là "Lương dân", cho nên không thể tự tiện lăng nhục. Theo quy định trong cung đình nhà Thanh, các cung nữ nếu bị tội thì sẽ bị phạt quỳ, phạt trượng đánh, nếu phạm đại tội bất nghịch thì cao lắm là đuổi khỏi cung, không thể tự ý giết chết. Dù cho bị phạt, thì có một quy tắc chính là…

**Bài:** Hậu cung nhà Thanh (20,405 âm tiết), cửa sổ ở 82% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thải thuế của Hoàng hậu thường có màu gì?  
**Đáp án sinh:** xanh biếc  
**Kiểm:** xanh biếc (F1 1.0)  
**Cửa sổ (rút gọn):** Triều quan của Hoàng quý phi, Quý phi: lệ như của Hoàng hậu, mùa Đông dùng da Huân chồn, mùa hạ dùng Nhung xanh, đại khái như Hoàng hậu. Nhưng đuôi chim Địch sức 192 viên, kết thành 3 hàng dây rũ. Quý phi dây rũ dùng màu Kim hoàng sắc. Triều quan của Phi: trên đỉnh chỉ có 2 tầng, mỗi tầng cách 1 viên Đông châu và một con Kim phượng, trên thân Kim p…

**Bài:** Hậu cung nhà Thanh (20,405 âm tiết), cửa sổ ở 92% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo quy định về Cát phục, màu sắc của Long bào dành cho Thái hậu, Hoàng hậu và Hoàng quý phi là gì?  
**Đáp án sinh:** màu Minh hoàng  
**Kiểm:** Minh hoàng (F1 0.8)  
**Cửa sổ (rút gọn):** Áo thể viên lĩnh (cổ tròn), ống tay áo dạng Mã đề tụ, khai vạt trái phải, thân áo dài, lĩnh khâm (viền cổ áo) có viền hoa văn. Đại để khá tương đồng với Long bào của phái nam trong hoàng thất. Hoa văn của áo thường là Mãn địa văn (满地纹; hình hoa văn phủ khắp áo) và Đoàn văn (团纹; hình hoa văn ổ). Thời sơ kỳ, áo bào của Đế-Hậu cùng dạng đoàn long, sau…

**Bài:** Bitcoin (10,671 âm tiết), cửa sổ ở 37% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, quá trình khai thác Bitcoin được ngữ cảnh hóa tốt nhất về mặt khai thác đối tượng nào?  
**Đáp án sinh:** các khối tiền điện tử  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Để có thể được cả mạng lưới chấp nhận, khối mới cần phải chứa bằng chứng công việc (proof-of-work). Proof-of-work yêu cầu thợ đào tìm kiếm một số nonce, mà khi nội dung của khối được hash (hàm băm mật mã học) cùng nonce, kết quả tạo ra một số nhỏ hơn số target của mạng lưới (số target càng nhỏ thì độ khó càng cao). Nói cách khác: Proof-of-work rất …

**Bài:** Bitcoin (10,671 âm tiết), cửa sổ ở 48% bài  
**Trạng thái:** kept  
**Câu hỏi:** Đoạn script trong giao dịch Bitcoin được thiết kế theo đặc điểm nào để tránh vòng lặp vô hạn?  
**Đáp án sinh:** không Turing-complete  
**Kiểm:** không Turing-complete (F1 1.0)  
**Cửa sổ (rút gọn):** Điển hình: Ví trên nền tảng Web dễ sử dụng nhất, bao gồm: Coinbase, Blockchain.info, BitGo, Xapo; Ví phần mềm: Armory, Bitcoin Core; Ví cho thiết bị di động: breadwallet, Blockchain.info; Ví phần cứng: Ledger Nano S, Trezor; Hoặc bạn có thể tự in ví giấy cho mình để cất trong tủ an toàn từ một trong các ví trên. Một giao dịch là một sự dịch chuyển …

**Bài:** Bitcoin (10,671 âm tiết), cửa sổ ở 9% bài  
**Trạng thái:** kept  
**Câu hỏi:** Đại lý mua, bán Bitcoin đầu tiên tại Việt Nam ra đời vào tháng 12 năm 2013 có tên gọi là gì?  
**Đáp án sinh:** Bitcoin Vietnam  
**Kiểm:** Bitcoin Vietnam (F1 1.0)  
**Cửa sổ (rút gọn):** Bitcoin bắt đầu thu hút dư luận từ năm 2012, khi có rất nhiều bài báo nhắc đến nó. Năm 2013, một số dịch vụ lớn như OKCupid, Baidu, Reddit, Humble Bundle, Foodler và Gyft bắt đầu sử dụng nó. Tại Canada đã có máy ATM mua bán Bitcoin đầu tiên trên thế giới. Tháng 12 năm 2013, tại Việt Nam, đại lý mua, bán Bitcoin đầu tiên ra đời với tên gọi là Bitcoi…

**Bài:** Bitcoin (10,671 âm tiết), cửa sổ ở 71% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo các nhà kinh tế, các ngân hàng trung ương nên dành bao nhiêu phần trăm dự trữ ngoại hối cho Bitcoin để phòng hộ rủi ro tiền tệ?  
**Đáp án sinh:** từ 0.01% tới 5%  
**Kiểm:** từ 0.01% tới 5% (F1 1.0)  
**Cửa sổ (rút gọn):** Các nhà kinh tế khuyến cáo các ngân hàng trung ương nên dành từ 0.01% tới 5% dự trữ ngoại hối của mình cho Bitcoin để phòng hộ các rủi ro về tiền tệ. Các doanh nghiệp chấp nhận Bitcoin Trong năm 2016, số lượng các doanh nghiệp chấp nhận Bitcoin đã vượt qua 122.000. Tính đến tháng 12 năm 2014, các công ty lớn chấp nhận thanh toán bằng Bitcoin bao gồ…

**Bài:** Bitcoin (10,671 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** Giao dịch đặc biệt nào được đưa vào thanh toán để nhận phần thưởng khai thác Bitcoin?  
**Đáp án sinh:** coinbase  
**Kiểm:** coinbase (F1 1.0)  
**Cửa sổ (rút gọn):** Quá trình khai thác Bitcoin được ngữ cảnh hóa tốt nhất về mặt khai thác các khối tiền điện tử, trái ngược với các đơn vị đơn lẻ, chẳng hạn như một Bitcoin (BTC). Lý do rất đơn giản: Bitcoin mới chỉ được khai thác bất cứ khi nào một khối mới trên chuỗi khối Bitcoin được xác thực. nhỏ|Độ khó của việc đào Bitcoin Cứ mỗi 2016 khối được tạo ra (mất khoả…

**Bài:** Bitcoin (10,671 âm tiết), cửa sổ ở 44% bài  
**Trạng thái:** kept  
**Câu hỏi:** Việc sở hữu Bitcoin được định nghĩa là sự nắm giữ thành phần nào của một địa chỉ Bitcoin?  
**Đáp án sinh:** khoá riêng tư  
**Kiểm:** khoá riêng tư (F1 1.0)  
**Cửa sổ (rút gọn):** vì khó cạnh tranh được với các mỏ đào ASIC chuyên nghiệp. Giới đào mỏ trong nước hoạt động tương đối khép kín vì tính chất nhạy cảm của Bitcoin và một phần trong số họ sử dụng nguồn điện không hợp pháp và không đóng thuế thu nhập. Mỗi tài khoản Bitcoin được biểu diễn dưới dạng 1 ví Bitcoin. Mỗi ví Bitcoin bao gồm địa chỉ Bitcoin công khai (hash của…

**Bài:** Bitcoin (10,671 âm tiết), cửa sổ ở 59% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lightning Network đã được đưa vào thử nghiệm với phiên bản 1.0 từ thời điểm nào?  
**Đáp án sinh:** tháng 12 năm 2017  
**Kiểm:** tháng 12 năm 2017 (F1 1.0)  
**Cửa sổ (rút gọn):** Lightning Network đã được đưa vào thử nghiệm với phiên bản 1.0 từ tháng 12 năm 2017 với giao dịch đầu tiên tại Bitrefill, và được chính thức triển khai trong năm 2018. Taproot bao gồm việc đưa vào sử dụng chữ ký Schnorr thay cho thuật toán ECDSA, với các đặc tính toán học như cung cấp mức độ đúng đắn cao, xác minh nhanh, và tránh được malleability.…

**Bài:** Bitcoin (10,671 âm tiết), cửa sổ ở 55% bài  
**Trạng thái:** kept  
**Câu hỏi:** Phần mềm Bitcoin nguyên thủy có tên gọi là gì?  
**Đáp án sinh:** Bitcoin Core  
**Kiểm:** Bitcoin Core (F1 1.0)  
**Cửa sổ (rút gọn):** Vì vậy, kể cả trong trường hợp tôi bị xe buýt đâm, dự án vẫn sẽ rõ ràng được tiếp tục". Khóa báo động này sau đó đã được chính Gavin hủy bỏ để biến Bitcoin thành một mạng lưới hoàn toàn phân quyền. Việc quản lý một cách phân quyền đã mang tới nhiều tranh cãi về con đường mà Bitcoin sẽ được phát triển trong tương lai. Phần mềm Bitcoin nguyên thủy vớ…

**Bài:** Thiên kiến xác nhận (10,353 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo nghiên cứu của Philip E. Tetlock, nhóm chuyên gia nào được cho là ít chính xác hơn nhiều do thiên kiến xác nhận?  
**Đáp án sinh:** nhóm nhím  
**Kiểm:** nhóm nhím (F1 1.0)  
**Cửa sổ (rút gọn):** Những tiên đoán rằng các hội thẩm sẽ trở nên càng cực đoan thêm trong hành động của mình khi họ thấy thêm bằng chứng mới đã được quan sát thấy trong những thí nghiệm bằng phiên xử mô phỏng. Cả các hệ thống công lý kiểu trọng tài hay kiểu thẩm tra đều chịu ảnh hưởng của thiên kiến xác nhận. Thiên kiến xác nhận có thể là một nhân tố trong việc tạo nê…

**Bài:** Thiên kiến xác nhận (10,353 âm tiết), cửa sổ ở 10% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thí nghiệm do nhóm nào tại Đại học Stanford tiến hành để minh họa cho thiên kiến xác nhận?  
**Đáp án sinh:** Một nhóm ở Đại học Stanford  
**Kiểm:** Một nhóm ở Đại học Stanford (F1 1.0)  
**Cửa sổ (rút gọn):** Vì thế, việc tìm kiếm bằng chứng để ủng hộ cho giả thuyết sẽ có khả năng thành công. Một sự minh họa cho điều này, đó là cách diễn đạt câu hỏi có tính chất gợi ý để thay đổi câu trả lời. Ví dụ, khi người ta hỏi "cuộc sống của bạn có hạnh phúc không?" thì sẽ nhận được câu trả lời "hài lòng" nhiều hơn là khi hỏi "cuộc sống của bạn có bất hạnh không?"…

**Bài:** Thiên kiến xác nhận (10,353 âm tiết), cửa sổ ở 26% bài  
**Trạng thái:** kept  
**Câu hỏi:** Những người tham gia thí nghiệm đã đánh giá cảm xúc của họ khi nghe tin O.J. Simpson được tha bổng vào những thời điểm nào sau vụ xử?  
**Đáp án sinh:** một tuần, hai tháng, và một năm sau vụ xử  
**Kiểm:** một tuần, hai tháng, và một năm sau vụ xử (F1 1.0)  
**Cửa sổ (rút gọn):** Một thí nghiệm khác xác nhận rằng những thay đổi trong trạng thái cảm xúc cũng có thể ảnh hưởng tới việc hồi tưởng ký ức. Những người tham gia trong thí nghiệm này đánh giá họ cảm thấy ra sao khi lần đầu tiên họ nghe tin O.J. Simpson đã được tòa tha bổng vụ án giết người. Họ mô tả các phản ứng cảm xúc của họ và sự tin tưởng liên quan tới phán quyết…

**Bài:** Thiên kiến xác nhận (10,353 âm tiết), cửa sổ ở 20% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hiệu ứng ghi nhớ thông tin có lọc lựa để củng cố kỳ vọng của con người còn được gọi là gì?  
**Đáp án sinh:** hồi tưởng chọn lọc  
**Kiểm:** hồi tưởng chọn lọc (F1 1.0)  
**Cửa sổ (rút gọn):** Cách diễn giải thiên lệch không giới hạn trong những chủ đề chịu ảnh hưởng mạnh bởi cảm xúc. Trong một thí nghiệm khác, các đối tượng tham gia nghe một câu chuyện kể về một vụ trộm. Họ phải đánh giá mức độ quan trọng bằng chứng của các mệnh đề lập luận ủng hộ hay chống lại việc một nhân vật cụ thể nào phải chịu trách nhiệm. Khi họ đặt giả thuyết rằ…

**Bài:** Thiên kiến xác nhận (10,353 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhà tâm lý học người Anh nào đã đặt ra thuật ngữ 'confirmation bias' (thiên kiến xác nhận)?  
**Đáp án sinh:** Peter Cathcart Wason  
**Kiểm:** Peter Cathcart Wason (F1 1.0)  
**Cửa sổ (rút gọn):** Nghiên cứu của Wason về kiểm tra giả thuyết Nhà tâm lý học người Anh Peter Cathcart Wason là người đặt ra thuật ngữ "confirmation bias" (thiên kiến xác nhận). Trong một thí nghiệm công bố năm 1960, ông yêu cầu những người tham gia xác định quy luật áp dụng cho các bộ ba số. Vào lúc bắt đầu, những người tham gia được cho biết rằng bộ số (2,4,6) phù …

**Bài:** Thiên kiến xác nhận (10,353 âm tiết), cửa sổ ở 45% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Theo Robert Maccoun, việc xử lý những bằng chứng gây tranh cãi nhất xảy ra thông qua tổ hợp của những cơ chế nào?  
**Đáp án sinh:** một tổ hợp các cơ chế "lạnh" (nhận thức) và "nóng" (có động lực)  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Klayman và Ra hỗ trợ phân tích của họ bằng cách trích dẫn một thí nghiệm sử dụng các nhãn "DAX" và "MED" thay cho "phù hợp với quy luật" và "không phù hợp với quy luật". Điều này tránh việc rằng mục đích bài tập là tìm một quy tắc có xác suất thấp. Những người tham gia có tỉ lệ thành công lớn hơn hẳn với phiên bản thí nghiệm này. Dưới ảnh hưởng của…

**Bài:** Thiên kiến xác nhận (10,353 âm tiết), cửa sổ ở 53% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Jennifer Lerner và Philip Tetlock, suy nghĩ khám phá xem xét một cách trung lập nhiều quan điểm và tìm cách phỏng đoán điều gì đối với mỗi một lập trường?  
**Đáp án sinh:** tất cả những phản đối có thể  
**Kiểm:** tất cả những phản đối có thể (F1 1.0)  
**Cửa sổ (rút gọn):** Đánh giá quá cao lòng trung thực của người bạn đó cũng có thể gây tổn thất, nhưng ít hơn. Trong trường hợp này, thành ra là hợp lý để tìm kiếm, đánh giá hoặc ghi nhớ bằng chứng về lòng trung thực của họ theo một cách thiên vị. Khi ai đó gây ra một ấn tượng ban đầu là hướng ngoại hoặc hướng nội, các câu hỏi phù hợp với ấn tượng đó bắt gặp như là nhi…

**Bài:** Thiên kiến xác nhận (10,353 âm tiết), cửa sổ ở 9% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thí nghiệm do nhóm nào tại Đại học Stanford tiến hành để kiểm tra cách diễn dịch thông tin của những người có quan điểm khác nhau về án tử hình?  
**Đáp án sinh:** Một nhóm ở Đại học Stanford  
**Kiểm:** Một nhóm ở Đại học Stanford (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên, khi kết hợp với các kết quả khác, cách chọn phép thử này có thể dẫn đến sự củng cố niềm tin hoặc giả định hiện có, bất chấp vào những phép thử đó là đúng hay sai. Trong những tình huống thực tế, bằng chứng thường phức tạp và rối rắm. Ví dụ, khi ta có nhiều quan niệm mâu thuẫn với nhau về một người nào đó, thì những quan niệm này có thể đ…

**Bài:** Chiến dịch Praha (13,512 âm tiết), cửa sổ ở 7% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tổng quân số của lực lượng do Petrov làm tham mưu trưởng là bao nhiêu người?  
**Đáp án sinh:** 806.400 người  
**Kiểm:** 806.400 người (F1 1.0)  
**Cửa sổ (rút gọn):** Petrov làm tham mưu trưởng. Tổng quân số 806.400 người. Tập đoàn quân cận vệ 3 do thượng tướng V. Quân đoàn 21 gồm các sư đoàn 58, 197, 253. Quân đoàn 76 gồm các sư đoàn 149, 287. Quân đoàn 120 gồm các sư đoàn 106, 127. Các sư đoàn trực thuộc 329 và 389. Pháo nòng dài: Các lữ đoàn cận vệ 1, cận vệ 40. Lựu pháo: Các lữ đoàn cận vệ 2 và 1528. Hỏa tiễ…

**Bài:** Chiến dịch Praha (13,512 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** kept  
**Câu hỏi:** Thành phố lớn cuối cùng ở châu Âu được giải phóng vào ngày 9 tháng 5 năm 1945 là thành phố nào?  
**Đáp án sinh:** Praha  
**Kiểm:** Praha (F1 1.0)  
**Cửa sổ (rút gọn):** Toàn bộ quân đội Đức Quốc xã tại Tiệp Khắc đều hoặc bị tiêu diệt, hoặc bị quân đội Liên Xô và quân đội Hoa Kỳ bắt làm tù binh. Toàn bộ vũ khí và phương tiện chiến tranh của nước Đức Quốc xã trong khu vực đều bị phá hủy hoặc thu giữ. Praha là thành phố lớn cuối cùng ở châu Âu được giải phóng ngày 9 tháng 5 năm 1945. Ngày này trở thành ngày quốc khán…

**Bài:** Chiến dịch Praha (13,512 âm tiết), cửa sổ ở 78% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tổng số quân Đức bị bắt ở Tiệp Khắc trong toàn bộ chiến dịch lên đến bao nhiêu người?  
**Đáp án sinh:** 859.400 người  
**Kiểm:** 859.400 người (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 10 tháng 5 có hơn 20.000 quân Đức ra hàng. Ngày 11 tháng 5,con số này tăng vọt lên khoảng 130.000 tù binh. Ngày 12 tháng 5, con số này là 185.900 người, trong các ngày từ 13 đến 15 tháng 5, vẫn còn khoảng 31.230 sĩ quan và binh lính Đức ở phía Đông đầu hàng quân đội Liên Xô. Tổng số quân Đức bị bắt ở Tiệp Khắc trong toàn bộ chiến dịch lên đến …

**Bài:** Chiến dịch Praha (13,512 âm tiết), cửa sổ ở 26% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn cận vệ 6 gồm các sư đoàn nào?  
**Đáp án sinh:** các sư đoàn cận vệ 1 và 8  
**Kiểm:** các sư đoàn cận vệ 1 và 8 (F1 1.0)  
**Cửa sổ (rút gọn):** Xe tăng: các lữ đoàn cận vệ 61, 62, 63; Trung đoàn xe tăng hạng nặng cận vệ 72. Pháo tự hành: Trung đoàn 1222. Cơ giới: Lữ đoàn cận vệ 29, Tiểu đoàn trinh sát cận vệ 7. Pháo binh: Trung đoàn 1689 (nòng dài), các trung đoàn cận vệ 248 và 299 (súng cối), Trung đoàn phòng không cận vệ 359. Các đơn vị trực thuộc: Thiết giáp: Lữ đoàn cận vệ 68, Lữ đoàn …

**Bài:** Chiến dịch Praha (13,512 âm tiết), cửa sổ ở 92% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hơn 10.000 quân nhân Liên Xô, Tiệp Khắc, Romania và Ba Lan được tặng thưởng huy chương nào sau Chiến dịch Praha?  
**Đáp án sinh:** Huy chương Vì sự giải phóng Praha  
**Kiểm:** Huy chương Vì sự giải phóng Praha (F1 1.0)  
**Cửa sổ (rút gọn):** Chiến dịch này cũng là một trong những chiến dịch có số lượng binh lực, vũ khí, phương tiện chiến tranh cùng tham gia vào hàng lớn nhất trong Chiến tranh thế giới thứ hai ở châu Âu. Quân đội Liên Xô, Romania và Tiệp Khắc có 181 sư đoàn và 19 lữ đoàn bộ binh, 3 tập đoàn quân xe tăng, 4 quân đoàn xe tăng và 2 quân đoàn cơ giới độc lập, 11 sư đoàn và …

**Bài:** Chiến dịch Praha (13,512 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn 20 bao gồm những đơn vị nào?  
**Đáp án sinh:** các sư đoàn cận vệ 48, 55 và sư đoàn 20  
**Kiểm:** các sư đoàn cận vệ 48, 55 và sư đoàn 20 (F1 1.0)  
**Cửa sổ (rút gọn):** Quân đoàn 20 gồm các sư đoàn cận vệ 48, 55 và sư đoàn 20. Quân đoàn 128 gồm các sư đoàn 61, 130 và 152. Pháo binh: Lữ đoàn lựu pháo 157, Trung đoàn pháo chống tăng 530, Trung đoàn súng cối cận vệ 133, Sư đoàn phòng không 33 (các trung đoàn 1378, 1710, 1715 và 1718), Trung đoàn phòng không 607. Công binh: Lữ đoàn hỗn hợp 36. Tập đoàn quân 31 được đi…

**Bài:** Chiến dịch Praha (13,512 âm tiết), cửa sổ ở 28% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đoàn cận vệ 6 bao gồm những sư đoàn cận vệ nào?  
**Đáp án sinh:** sư đoàn cận vệ 1 và 8  
**Kiểm:** các sư đoàn cận vệ 1 và 8 (F1 0.93)  
**Cửa sổ (rút gọn):** Quân đoàn cận vệ 6 gồm các sư đoàn cận vệ 1 và 8. Sư đoàn ném bom ban đêm 208. Quân đoàn cận vệ 1 gồm các sư đoàn cường kích cận vệ 8, 9 và Sư đoàn tiêm kích cận vệ 12. Quân đoàn cận vệ 2 gồm các sư đoàn cường kích cận vệ 5, 6 và Sư đoàn tiêm kích cận vệ 11. Quân đoàn 3 gồm các sư đoàn cường kích 307, 308 và Sư đoàn tiêm kích 181. Các trung đoàn cư…

**Bài:** Chiến dịch Praha (13,512 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân Đức đã ký hiệp nghị đầu hàng ở đâu vào rạng sáng ngày 7 tháng 5?  
**Đáp án sinh:** Reims  
**Kiểm:** Reims (F1 1.0)  
**Cửa sổ (rút gọn):** Quân Đức chống cự đặc biệt ác liệt tại khu phòng thủ Olomouc vì đây là "cái miệng" của "cái túi" Přerov. Mất Olomouc đồng nghĩa vời việc ba quân đoàn Đức sẽ mất con đường cuối cùng thoát sang phía Tây. Trong ngày tấn công đầu tiên, các tập đoàn quân của Phương diện quân Ukraina 4 chỉ tiến lên được từ 8 đến 12 km trên cao nguyên Bohemia. Trên hướng …

**Bài:** Giuse Nguyễn Chí Linh (11,369 âm tiết), cửa sổ ở 64% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tổng giám mục Nguyễn Chí Linh đã chủ sự nghi lễ nào tại Đất Thánh vào giữa tháng 10 năm 2018?  
**Đáp án sinh:** lễ đặt tượng Đức Mẹ La Vang  
**Kiểm:** lễ đặt tượng Đức Mẹ La Vang (F1 1.0)  
**Cửa sổ (rút gọn):** Khi được hỏi về những khó khăn của giáo hội Công giáo Việt Nam về vấn đề bổ nhiệm giám mục, vị chủ tịch Hội đồng giám mục Việt Nam chia sẻ việc bổ nhiệm ở Việt Nam theo cơ chế Tòa Thánh đề cử và Việt Nam có quyền phủ quyết ứng viên, tuy vậy tình hình ngày càng tốt đẹp hơn do các bên tế nhị tôn trọng lẫn nhau, chỉ gặp một số khó khăn khi bổ nhiệm cá…

**Bài:** Giuse Nguyễn Chí Linh (11,369 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Chủng sinh Nguyễn Chí Linh theo học tại Giáo hoàng Học viện Thánh Piô X, Đà Lạt từ năm nào?  
**Đáp án sinh:** 1970  
**Kiểm:** năm 1970 (F1 0.67)  
**Cửa sổ (rút gọn):** Riêng về con đường tu học của chủng sinh Linh, từ năm 1970, chủng sinh này theo học Giáo hoàng Học viện Thánh Piô X, Đà Lạt và học tại đây cho đến năm 1977, khi học viện này đóng cửa. Học cùng lớp Giáo hoàng Học viện này, sau này còn có ba giám mục khác là Cosma Hoàng Văn Đạt, Mátthêu Nguyễn Văn Khôi và Giuse Nguyễn Năng. Sau đó, vì hoàn cảnh không…

**Bài:** Giuse Nguyễn Chí Linh (11,369 âm tiết), cửa sổ ở 95% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, Mátthêu Nguyễn Văn Khôi hiện đang giữ chức vụ gì tại Giáo phận Quy Nhơn?  
**Đáp án sinh:** Giám mục chính tòa Giáo phận Quy Nhơn  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Năm 2010, Mátthêu Nguyễn Văn Khôi, hiện đang là Giám mục chính tòa Giáo phận Quy Nhơn. Năm 2015, Phêrô Huỳnh Văn Hai, hiện đang là Giám mục chính tòa Giáo phận Vĩnh Long. Năm 2016, Emmanuel Nguyễn Hồng Sơn, hiện đang là Giám mục chính tòa Giáo phận Bà Rịa. Danh sách giám mục người Việt Danh sách giám mục Việt Nam còn sống theo tuổi ĐGM Giuse Nguyễn…

**Bài:** Giuse Nguyễn Chí Linh (11,369 âm tiết), cửa sổ ở 72% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người được các giám mục tiếp tục chọn làm Chủ tịch Hội đồng Giám mục trong nhiệm kỳ 2019–2022?  
**Đáp án sinh:** Tổng giám mục Nguyễn Chí Linh  
**Kiểm:** Tổng giám mục Nguyễn Chí Linh (F1 1.0)  
**Cửa sổ (rút gọn):** Đồng ký tên trong thư này có Chủ tịch Ủy ban Giáo lý Đức Tin Gioan Đỗ Văn Ngân. Tháng 8 năm 2019, phái đoàn giáo sĩ Công giáo do Tổng giám mục Nguyễn Chí Linh dẫn đầu tham gia Hội nghị Thủ tướng Chính phủ và các chức sắc tôn giáo, có dịp tiếp xúc với thủ tướng Nguyễn Xuân Phúc. Tại hội nghị, về phía Công giáo có bài tham luận về 5 chương trình chín…

**Bài:** Giuse Nguyễn Chí Linh (11,369 âm tiết), cửa sổ ở 60% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là chủ phong nghi thức truyền chức trong lễ tấn phong giám mục Nguyễn Đức Cường?  
**Đáp án sinh:** Tổng giám mục Giuse Nguyễn Chí Linh  
**Kiểm:** Tổng giám mục Giuse Nguyễn Chí Linh (F1 1.0)  
**Cửa sổ (rút gọn):** Ông chính thức tổ chức buổi chia tay với Giáo phận Thanh Hóa vào ngày 10 tháng 6. Lễ tấn phong giám mục Nguyễn Đức Cường được cử hành vào ngày 27 tháng 6 năm 2018. Chủ phong nghi thức truyền chức là Tổng giám mục Giuse Nguyễn Chí Linh và hai vị phụ phong, gồm Giuse Nguyễn Năng, giám mục Giáo phận Phát Diệm và Giám mục Phó Giáo phận Đà Lạt Đa Minh N…

**Bài:** Giuse Nguyễn Chí Linh (11,369 âm tiết), cửa sổ ở 71% bài  
**Trạng thái:** kept  
**Câu hỏi:** Tổng giám mục Nguyễn Chí Linh đã được các giám mục tiếp tục chọn làm Chủ tịch Hội đồng Giám mục trong nhiệm kỳ nào?  
**Đáp án sinh:** 2019–2022  
**Kiểm:** 2019–2022 (F1 1.0)  
**Cửa sổ (rút gọn):** Từ ngày 21 đến ngày 24 tháng 2 năm 2019, với tư cách Chủ tịch Hội đồng Giám mục Việt Nam, Tổng giám mục Nguyễn Chí Linh đến Vatican tham gia hội nghị về Bảo vệ trẻ em trong Giáo hội, với đa số nghị phụ là Chủ tịch Hội đồng Giám mục trên toàn thế giới. Trong biến cố hỏa hoạn Nhà thờ Đức Bà Paris, với cương vị Chủ tịch Hội đồng Giám mục Việt Nam, Tổn…

**Bài:** Giuse Nguyễn Chí Linh (11,369 âm tiết), cửa sổ ở 7% bài  
**Trạng thái:** kept  
**Câu hỏi:** Linh mục Nguyễn Chí Linh được cử đi du học tại Paris, Pháp trong khoảng thời gian nào?  
**Đáp án sinh:** từ năm 1995 đến năm 2003  
**Kiểm:** từ năm 1995 đến năm 2003 (F1 1.0)  
**Cửa sổ (rút gọn):** Ngày 30 tháng 12 năm 1992, Phó tế Nguyễn Chí Linh được giám mục Phaolô Nguyễn Văn Hòa, giám mục Giáo phận Nha Trang truyền chức linh mục, tại nhà thờ Phan Rang, giáo phận Nha Trang. Sau khi được truyền chức linh mục, vị linh mục trẻ được giám mục giáo phận bổ nhiệm làm linh mục phó giáo xứ Phước Thiện, giáo phận Nha Trang và đảm nhận chức vụ này đế…

**Bài:** Giuse Nguyễn Chí Linh (11,369 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** kept  
**Câu hỏi:** Giám mục Nguyễn Chí Linh cho biết khó khăn của giáo phận Thanh Hóa là thiếu những yếu tố nào?  
**Đáp án sinh:** nhân sự và tài chính  
**Kiểm:** nhân sự và tài chính (F1 1.0)  
**Cửa sổ (rút gọn):** Nhận phỏng vấn trong dịp giáo phận Thanh Hóa kỷ niệm 75 năm thành lập, nhắc đến thông tin về những ưu tiên trong các công tác mục vụ, ông cho biết đó là vấn đề đào tạo nhân sự: linh mục, tu sĩ và giáo dân. Khó khăn của giáo phận Thanh Hóa là thiếu nhân sự và tài chính. Giám mục Linh khuyến khích hợp nhất, hỗ trợ người khó khăn như cấp học bổng cho …

**Bài:** Chiến tranh La Mã-Ba Tư (9,961 âm tiết), cửa sổ ở 80% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào thế kỷ thứ 7, nước đệm cuối cùng giữa La Mã và Sassanid là vương quốc của dân tộc nào?  
**Đáp án sinh:** người Lakhmid Ả Rập  
**Kiểm:** người Lakhmid Ả Rập (F1 1.0)  
**Cửa sổ (rút gọn):** Shapur cũng đã cho xây dựng một hệ thống thành trì dựa trên mô hình của hệ thống limes của người La Mã mà người Sassanid rất hâm mộ. Vào thời điểm nhà Sassanid khai quốc, một số nước đệm tồn tại giữa hai đế quốc. Các nước này đều bị sáp nhập vào đại quốc theo thời gian và vào thế kỷ thứ 7, nước đệm cuối cùng là vương quốc của người Lakhmid Ả Rập củ…

**Bài:** Chiến tranh La Mã-Ba Tư (9,961 âm tiết), cửa sổ ở 26% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hoàng đế La Mã nào đã dẫn quân đánh Ardashir trong năm 232 và cuối cùng đã đẩy lui ông ta?  
**Đáp án sinh:** Alexander Severus  
**Kiểm:** Alexander Severus (F1 1.0)  
**Cửa sổ (rút gọn):** Để đổi lấy một nền hòa bình, ông này phải chịu trách nhiệm bồi thường chiến phí cho những thiệt hại mà Hoàng Đế Caracalla gây ra. Những xung đột thời kỳ đầu Chiến tranh tiếp tục tiếp diễn nhà Parthia diệt vong và hoàng đế Ardashir I khai lập nên đế quốc Sassanid. Ardashir tiến hành nhiều cuộc tấn công vào Lưỡng Hà và Syria trong năm 230 và yêu cầu …

**Bài:** Chiến tranh La Mã-Ba Tư (9,961 âm tiết), cửa sổ ở 3% bài  
**Trạng thái:** kept  
**Câu hỏi:** Quân đội của người Hồi giáo Ả Rập đã chinh phục toàn bộ đế quốc nào?  
**Đáp án sinh:** Đế chế Sassanid  
**Kiểm:** Đế chế Sassanid (F1 1.0)  
**Cửa sổ (rút gọn):** Cuộc chiến tranh kéo dài và leo thang vào thế kỷ thứ 6 và 7 đã khiến hai nước suy kiệt và dễ bị tổn thương khi phải đối mặt với sự xuất hiện và trỗi dậy đột ngột của Khalifah Ả Rập, chính lực lượng này đã xua quân chinh phạt cả hai đế quốc chỉ một vài năm sau khi cuộc chiến tranh La Mã-Ba Tư kết thúc. Hưởng lợi từ tình trạng suy yếu của các đối thủ…

**Bài:** Chiến tranh La Mã-Ba Tư (9,961 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào năm 64 TCN, Pompey đã chinh phục vùng lãnh thổ nào của người Seleukos?  
**Đáp án sinh:** Syria  
**Kiểm:** Syria (F1 1.0)  
**Cửa sổ (rút gọn):** Mặc dù phải chịu khuất phục trước các vua nhà Seleukos trong một thời gian, nhưng họ đã tách ra trong thế kỷ thứ 2 TCN và thành lập một vương quốc độc lập và vương quốc này liên tục mở rộng lãnh thổ bằng cái giá của những kẻ đã thống trị họ trước đây. Trong tiến trình từ thế kỷ 3 đến 1 TCN, người Parthia đã chinh phục Ba Tư, Lưỡng Hà và Armenia. Dư…

**Bài:** Chiến tranh La Mã-Ba Tư (9,961 âm tiết), cửa sổ ở 22% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hadrianus đã trao trả lại vùng Lưỡng Hà cho người Parthia vì ông cho rằng việc tái thiết lập Euphrates làm ranh giới là vì lợi ích của ai?  
**Đáp án sinh:** La Mã  
**Kiểm:** La Mã (F1 1.0)  
**Cửa sổ (rút gọn):** Tuy nhiên ngay sau khi lên nối ngôi Hoàng đế, Hadrianus đã cho trao trả lại vùng Lưỡng Hà cho người Parthia, vì ông cho rằng, việc tái thiết lập Euphrates làm ranh giới là vì lợi ích của La Mã. Hadrianus cho trở lại hiện trạng status quo ante bellum và trao trả các vùng lãnh thổ ở Armenia, Lưỡng Hà và Adiabene cho những nhà cai trị cùng với các vị …

**Bài:** Chiến tranh La Mã-Ba Tư (9,961 âm tiết), cửa sổ ở 55% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vua Hormizd IV đã bãi bỏ chế độ quân chủ ở vùng nào và biến nơi đó thành một tỉnh Ba Tư?  
**Đáp án sinh:** Iberia Caucasus  
**Kiểm:** Iberia Caucasus (F1 1.0)  
**Cửa sổ (rút gọn):** Năm 575, Khosrau I đã cố gắng kết hợp cuộc xâm lược ở Armenia vào cuộc thảo luận về một nền hòa bình vĩnh viễn. Ông đã tiến hành xâm lược vùng Anatolia và chiếm thành phố Sebasteia, nhưng sau một trận chiến ở gần Melitene, quân đội Ba Tư đã bị hứng chịu tổn thất nặng nề trong khi phải rút lui qua vùng Euphrates dưới những cuộc tấn công du kích của …

**Bài:** Chiến tranh La Mã-Ba Tư (9,961 âm tiết), cửa sổ ở 18% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Hoàng đế La Mã nào đã chinh phạt Armenia và Lưỡng Hà trong thời gian từ năm 114 đến 115?  
**Đáp án sinh:** Hoàng đế Traianus  
**Kiểm:** Traianus (F1 0.5)  
**Cửa sổ (rút gọn):** Tuy nhiên, người La Mã và người Ba Tư liên tục cạnh tranh quyền kiểm soát và ảnh hưởng với nhau tại Armenia vài thập kỷ sau đó. Quyết định đặt con trai của mình lên ngôi vua Armenia đang bị bỏ trống của vua Parthia Artabanus II đã gây ra một cuộc chiến với La Mã trong năm 36 CN, cuộc chiến chỉ kết thúc khi Artabanus tuyên bố từ bỏ ảnh hưởng của ngư…

**Bài:** Chiến tranh La Mã-Ba Tư (9,961 âm tiết), cửa sổ ở 93% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người dịch tác phẩm Chronicon Paschale?  
**Đáp án sinh:** Earnest Cary  
**Kiểm:** Earnest Cary (F1 1.0)  
**Cửa sổ (rút gọn):** Dịch bởi Earnest Cary.Chronicon Paschale. See the original text in Google books Eutropius, Abridgment of Roman History. Herodian, History of the Roman Empire. Xem văn bản gốc trong Thư viện Latinh. Xem văn bản gốc trong Thư viện Latinh. Procopius, History of the Wars, Quyển II. Sozomen, Ecclesiastical History, Quyển II. Hartranft, Philip Schaff & H…

**Bài:** Trận Yarmouk (10,793 âm tiết), cửa sổ ở 54% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người chỉ huy cánh trái của quân Byzantine trong trận chiến được mô tả?  
**Đáp án sinh:** Qanateer  
**Kiểm:** Qanateer (F1 1.0)  
**Cửa sổ (rút gọn):** Ông ra lệnh cho quân đội của mình chuẩn bị cho các cuộc tấn công bất ngờ. Người Byzantine không biết rằng, Khalid cũng đã chuẩn bị cho phương án này bằng cách đặt một lực lượng tiền tuyến mạnh mẽ ở phía trước ngay trong buổi đêm để tấn công bất ngờ, chính vì vậy người Hồi giáo đã có đủ thời gian để chuẩn bị cho trận chiến. Tại phía trung tâm, người…

**Bài:** Trận Yarmouk (10,793 âm tiết), cửa sổ ở 30% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai sẽ nhận nhiệm vụ chỉ huy lực lượng kỵ binh tinh nhuệ cơ động trong trường hợp Khalid quá bận rộn trong việc lãnh đạo quân đội?  
**Đáp án sinh:** Dharar ibn al-Azwar  
**Kiểm:** Dharar ibn al-Azwar (F1 1.0)  
**Cửa sổ (rút gọn):** ở trung tâm, cánh trái và cánh phải đều có các chiến đoàn kỵ binh được sử dụng như là lực lượng dự trữ cho các cuộc phản công trong trường hợp họ bị đẩy trở lại bởi người Byzantine. Đằng sau cánh trung tâm là lực lượng kỵ binh tinh nhuệ cơ động nằm dưới sự chỉ huy của cá nhân Khalid. Trong trường hợp Khalid quá bận rộn trong việc lãnh đạo quân đội,…

**Bài:** Trận Yarmouk (10,793 âm tiết), cửa sổ ở 60% bài  
**Trạng thái:** kept  
**Câu hỏi:** Khalid đã ra lệnh cho Dharar ibn al-Azwar tấn công vỗ mặt vào đội quân của ai?  
**Đáp án sinh:** Dairjan  
**Kiểm:** Dairjan (F1 1.0)  
**Cửa sổ (rút gọn):** <blockquote>Hỡi những người chạy đã bỏ chạy từ người phụ nữ chung thủy Ai có cả vẻ đẹp và đức hạnh; Và rời bỏ cô để theo ngoại đạo, Trong sự căm thù và cái xấu vô đạo, Bị chiếm hữu, ô nhục và đổ nát.</blockquote> Sự kiện này làm máu của các chiến binh Hồi giáo đang rút lui sôi lên và họ quay trở lại chiến trường. Giai đoạn 3: Sau khi cố gắng để ổn …

**Bài:** Trận Yarmouk (10,793 âm tiết), cửa sổ ở 77% bài  
**Trạng thái:** kept  
**Câu hỏi:** Khalid đã cử ai cùng với 500 kỵ binh để chiếm cây cầu chiến lược tại Ayn al Dhakar vào ban đêm?  
**Đáp án sinh:** Dharar  
**Kiểm:** Dharar (F1 1.0)  
**Cửa sổ (rút gọn):** Tuyến đường phía Bắc đã bị chặn bởi kỵ binh của người Hồi giáo. Tuy nhiên, đoạn khe núi sâu trên  của Wadi-ur-Raqqad ở phía tây có một cây cầu chiến lược quan trọng nhất tại Ayn al Dhakar. Khalid cử Dharar cùng với 500 kỵ binh để chiếm cây cầu vào ban đêm. Dharar di chuyển xung quanh sườn phía bắc của Đế chế Byzantine và chiếm được cây cầu. Sự cơ đ…

**Bài:** Trận Yarmouk (10,793 âm tiết), cửa sổ ở 17% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Quân tiếp viện được gửi tới vùng Caesarea dưới sự chỉ huy của ai?  
**Đáp án sinh:** Constantinus III, con trai của Heraclius  
**Kiểm:** Constantinus III (F1 0.25)  
**Cửa sổ (rút gọn):** Bằng cách buộc các tín đồ Hồi giáo phải rút lui, hoặc bằng cách tiêu diệt từng lực lượng Hồi giáo riêng biệt, ông sẽ thực hiện được mục tiêu chiến lược của mình là chiếm lại các vùng lãnh thổ đã bị mất. Quân tiếp viện tiếp tục được gửi tới vùng Caesarea dưới sự chỉ huy của Constantinus III, con trai của Heraclius có lẽ để gây sức ép vào đạo quân củ…

**Bài:** Trận Yarmouk (10,793 âm tiết), cửa sổ ở 9% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người kế nhiệm Khalip Abu Bakr và đã xác định mở rộng ảnh hưởng của Đế chế Hồi giáo vào Syria?  
**Đáp án sinh:** Umar  
**Kiểm:** Umar (F1 1.0)  
**Cửa sổ (rút gọn):** Khalip Abu Bakr đã qua đời trong năm 634. Umar, người kế nhiệm ông đã xác định là mở rộng hơn nữa ảnh hưởng của Đế chế Hồi giáo vào Syria. Mặc dù các chiến dịch trước đó của Khalid đã thành công, ông vẫn bị thay thế bởi Abu Ubaidah. Chiếm được phía nam Palestina, lực lượng Hồi giáo tiếp tục tiến lên con đường thương mại và đên Tiberias và Baalbek, …

**Bài:** Trận Yarmouk (10,793 âm tiết), cửa sổ ở 95% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Nafziger, cuốn sách nào của ông đã đưa ra kết luận về trận chiến Yarmouk?  
**Đáp án sinh:** Islam at war  
**Kiểm:** Islam at war (F1 1.0)  
**Cửa sổ (rút gọn):** Có vẻ như đây là một sự thiếu quyết tâm trong số các chỉ huy của Đế quốc, mặc dù sự kiện này có thể đã bị gây ra bởi những khó khăn trong việc chỉ huy quân đội vì các xung đột nội bộ. Hơn nữa, nhiều rất nhiều lính Ả Rập Thiên chúa giáo chỉ là lính nghĩa vụ, trong khi quân đội Hồi giáo Ả Rập bao gồm một phần lớn là các cựu binh. Chiến lược ban đầu c…

**Bài:** Trận Yarmouk (10,793 âm tiết), cửa sổ ở 73% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Vahan gửi sứ giả đến doanh trại người Hồi giáo vào sáng sớm ngày 19 tháng 8 năm 636 để yêu cầu điều gì?  
**Đáp án sinh:** một cuộc ngưng chiến vài ngày để có thể tiến hành một cuộc đàm phán mới  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Ikrimah bảo vệ cuộc rút lui của người Hồi giáo với bốn trăm kỵ binh của mình bằng cách tấn công vỗ mặt vào người Byzantine, trong khi các đội quân khác tổ chức lại chính họ để phản công và giành lại các vị trí mà họ đã bị mất. Toàn bộ người của Ikrimah hoặc bị thương nặng hoặc chết trong ngày hôm đó. Ikrimah-một người bạn thời thơ ấu của Khalid nằm…

**Bài:** Lịch sử Bắc Kinh (20,717 âm tiết), cửa sổ ở 88% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai đã cho phát hành một loạt tác phẩm tuyên truyền để chỉ trích di sản của Chu Ân Lai sau khi ông qua đời?  
**Đáp án sinh:** Diêu Văn Nguyên  
**Kiểm:** Diêu Văn Nguyên (F1 1.0)  
**Cửa sổ (rút gọn):** Sau khi Chu Ân Lai qua đời vào ngày 8 tháng 1 năm 1976, Diêu Văn Nguyên cho phát hành một loạt tác phẩm tuyên truyền để chỉ trích di sản của Chu Ân Lai, khiến dư luận phổ biến không chấp thuận. Ngày 20 tháng 3 năm 1976, học sinh trường tiểu học Ngưu Phòng đặt vòng hoa tại Bia kỉ niệm Anh hùng Nhân dân tại quảng trường Thiên An Môn nhằm tưởng nhớ Ch…

**Bài:** Lịch sử Bắc Kinh (20,717 âm tiết), cửa sổ ở 91% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo nguyên tắc chỉ đạo của Hồ Diệu Bang vào tháng 4 năm 1980, Bắc Kinh cần phải trở thành một trung tâm giao lưu quốc tế để hỗ trợ điều gì?  
**Đáp án sinh:** sự mở cửa của Trung Quốc với thế giới  
**Kiểm:** sự mở cửa của Trung Quốc với thế giới (F1 1.0)  
**Cửa sổ (rút gọn):** Quy hoạch đô thị tại Bắc Kinh phát triển theo một xu hướng mới so với thời đại Mao Trạch Đông. Vào tháng 4 năm 1980, khi xem xét tài trợ cho cơ sở hạ tầng, Hồ Diệu Bang đặt ra các nguyên tắc chỉ đạo cho sự phát triển của Bắc Kinh: Với vai trò là trung tâm chính trị của quốc gia, Bắc Kinh cần phải trở thành một trung tâm giao lưu quốc tế để hỗ trợ s…

**Bài:** Lịch sử Bắc Kinh (20,717 âm tiết), cửa sổ ở 48% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Viện Cảnh sát Bắc Kinh được thành lập vào năm nào?  
**Đáp án sinh:** 1901  
**Kiểm:** năm 1901 (F1 0.67)  
**Cửa sổ (rút gọn):** Gánh nặng bồi thường chiến phí khiến triều đình Thanh phải gia tăng thu thuế và khiến quốc lực tiếp tục suy yếu. Sau khởi nghĩa Nghĩa Hòa Đoàn, triều đình Thanh đẩy nhanh tốc độ cải cách và dễ dàng tiếp nhận ảnh hưởng của ngoại quốc. Các kỳ thi khoa cử kéo dài hàng thế kỷ bị bãi bỏ vào năm 1905, thay thế chúng là hệ thống giảng dạy và văn bằng theo…

**Bài:** Lịch sử Bắc Kinh (20,717 âm tiết), cửa sổ ở 94% bài  
**Trạng thái:** kept  
**Câu hỏi:** Đường vành đai 2 tại Bắc Kinh được xây dựng trên nền của công trình kiến trúc nào?  
**Đáp án sinh:** tường thành thời Minh  
**Kiểm:** tường thành thời Minh (F1 1.0)  
**Cửa sổ (rút gọn):** Sân vận động Công nhân là địa điểm chính của Á vận hội. Đường vành đai 2 được xây dựng tứ thập niên 1960 trên nền của tường thành thời Minh, cuối cùng hoàn thành vào năm 1992. Đường vành đai 3 hoàn tất vào năm 1993. Việc xây dựng ba tuyến đường vành đai khác được bắt đầu trong thập niên 1990, và lần lượt hoàn thành vào năm 2001 (đường vành đai 4), …

**Bài:** Lịch sử Bắc Kinh (20,717 âm tiết), cửa sổ ở 18% bài  
**Trạng thái:** kept  
**Câu hỏi:** Hoàng đế Kim nào đã chuyển quốc đô từ Thượng Kinh đến Yên Kinh vào năm 1153?  
**Đáp án sinh:** Hoàn Nhan Lượng  
**Kiểm:** Hoàn Nhan Lượng (F1 1.0)  
**Cửa sổ (rút gọn):** Chúng bao gồm đường Tam Miếu (三庙街), một trong các đường phố cổ nhất tại Bắc Kinh và Ngưu Nhai Lễ bái tự được hình thành vào năm 996, và Thiên Ninh tự, được xây dựng từ năm 1100 đến năm 1119. Dưới sự cai quản của triều Liêu, dân số nội thành Nam Kinh tăng từ 22.000 vào năm 938 lên 150.000 vào năm 1113 (và dân số khu vực xung quanh tăng từ 100.000 lê…

**Bài:** Lịch sử Bắc Kinh (20,717 âm tiết), cửa sổ ở 98% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Luận án tiến sĩ nào của Đại học Columbia có mã số DA9333861 và tập trung vào cơ sở hạ tầng đô thị của Bắc Kinh từ năm 1900 đến 1928?  
**Đáp án sinh:** Beijing Transforms: Urban Infrastructure, Public Works, and Social Change in the Chinese Capital, 1900-1928  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Lonely Planet Beijing City Guide (2007) excerpt and text search The Dragons of Tiananmen: Beijing as a Sacred City. Peking: Temples and City Life, 1400-1900. "Beijing Transforms: Urban Infrastructure, Public Works, and Social Change in the Chinese Capital, 1900-1928." PhD dissertation Columbia U. DA9333861 Fulltext: ProQuest Dissertations & Theses …

**Bài:** Lịch sử Bắc Kinh (20,717 âm tiết), cửa sổ ở 89% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lăng của Mao Trạch Đông được đặt tại đâu?  
**Đáp án sinh:** quảng trường Thiên An Môn  
**Kiểm:** quảng trường Thiên An Môn (F1 1.0)  
**Cửa sổ (rút gọn):** Mao Trạch Đông qua đời tại Bắc Kinh vào ngày 9 tháng 9 năm 1976, và lăng của ông tại quảng trường Thiên An Môn được hoàn thành một năm sau đó. Chưa đầy một tháng sau khi Mao Trạch Đông qua đời, vào ngày 7 tháng 10 năm 1976, Uông Đông Hưng cho bắt giữ Tứ nhân bang tại Trung Nam Hải trong một cuộc chính biến không đổ máu. Đặng Tiểu Bình được phục hồi…

**Bài:** Lịch sử Bắc Kinh (20,717 âm tiết), cửa sổ ở 43% bài  
**Trạng thái:** kept  
**Câu hỏi:** Năm 1790, Nam phủ đã mời các đoàn kịch nào từ An Huy đến biểu diễn cho Càn Long Đế?  
**Đáp án sinh:** Huy kịch  
**Kiểm:** Huy kịch (F1 1.0)  
**Cửa sổ (rút gọn):** Sau khi Trung Hoa Dân Quốc dời đô đến Nam Kinh, Quốc ngữ thôi hành ủy viên hội tái khẳng định lấy phương ngữ Bắc Kinh làm chuẩn cho Quốc ngữ vào năm 1932. Cộng hòa Nhân dân Trung Hoa cũng làm điều tương tự vào năm 1955. Nhà Thanh duy trì nguồn cung cấp lương thực tương đối ổn định cho cư dân kinh thành vào cuối thế kỷ XVII và đầu thế kỷ XVIII. Hệ t…

**Bài:** Paul Heyman Guy (nhóm đô vật chuyên nghiệp) (11,774 âm tiết), cửa sổ ở 90% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Ai là người đã pin Axel trong trận đấu được nhắc đến ở đầu đoạn trích?  
**Đáp án sinh:** R-Truth  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Và anh bị pin bởi R-Truth. Trên 11 tháng 10 trong SmackDown, Axel một lần nữa bảo vệ thành công Intercontinental Championship trước R-Truth. Tại Hell in a Cell, Axel đã được lên kế hoạch có trận tranh đai đối đầu với Big E Langston, tuy nhiên trận đấu đã bị hủy bỏ do chấn thương hông của Curtis. Sau khi Heyman tuyên bố ở Raw ngày 11 tháng 11 rằng R…

**Bài:** Paul Heyman Guy (nhóm đô vật chuyên nghiệp) (11,774 âm tiết), cửa sổ ở 97% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo bình chọn của PWI 500 năm 2012, đô vật nào được xếp hạng #1 trong top 500 đô vật đấu đơn?  
**Đáp án sinh:** Punk  
**Kiểm:** Punk (F1 1.0)  
**Cửa sổ (rút gọn):** "Swiss Made" by CFO$ (21 tháng 4 năm 2014 - 21 Tháng 7 năm 2014) - Cesaro Các đai vô địch và danh hiệuPro Wrestling Illustrated''PWI xếp hạng Punk #1 trong top 500 đô vật đấu đơn do PWI 500 bình chọn năm  2012 PWI xếp Ryback hạng #13 trong top 500 đô vật đấu đơn theo PWI 500 năm 2013 PWI xếp Curtis Axel hạng #47 trong top 500 đô vật đấu đơn theo PW…

**Bài:** Paul Heyman Guy (nhóm đô vật chuyên nghiệp) (11,774 âm tiết), cửa sổ ở 15% bài  
**Trạng thái:** kept  
**Câu hỏi:** Heyman đã dùng vật gì để đập vào người CM Punk hai lần tại sự kiện Money in the Bank?  
**Đáp án sinh:** chiếc thang  
**Kiểm:** chiếc thang (F1 1.0)  
**Cửa sổ (rút gọn):** Họ làm hòa sau đó. Thù với CM Punk và quản lý với nhiều Superstars (2013–2014) Tại Money in the Bank, Heyman phản bội Punk khi ông dùng chiếc thang đập vào người Punk hai lần khiến anh chấn thương. Heyman đi cùng với Axel trong trận đấu với Punk trên Raw ngày 5 tháng 8 cho đến khi Lesnar xuất hiện và tấn công Punk. Sau đó, Heyman thách thức Punk ch…

**Bài:** Paul Heyman Guy (nhóm đô vật chuyên nghiệp) (11,774 âm tiết), cửa sổ ở 44% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trọng tài đã không nhìn thấy bộ phận nào của Jey không chạm sàn khi bị đè đếm trong trận đấu tranh đai SmackDown Tag Team Championship?  
**Đáp án sinh:** vai Jey  
**Kiểm:** vai Jey (F1 1.0)  
**Cửa sổ (rút gọn):** Trong SmackDown ngày 4 tháng 6, The Usos tái hợp và đấu với The Mysterious (Rey Mysterio và Dominik Mysterio) tranh đai SmackDown Tag Team Championship; nhưng kết quả trận đấu gây tranh cãi, do trọng tài đã không nhìn thấy vai Jey không chạm sàn khi bị đè đếm. Usos tái đấu cùng đêm đó, nhưng trong trận đấu, Reigns bất ngờ can thiệp và tấn công Myst…

**Bài:** Paul Heyman Guy (nhóm đô vật chuyên nghiệp) (11,774 âm tiết), cửa sổ ở 91% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhóm The Shield gồm những thành viên nào khi debut vào ngày 18 tháng 11 năm 2012?  
**Đáp án sinh:** Dean Ambrose, Roman Reigns, và Seth Rollins  
**Kiểm:** Dean Ambrose, Roman Reigns, và Seth Rollins (F1 1.0)  
**Cửa sổ (rút gọn):** Có nhiều mối nghi ngờ rằng Paul Heyman đứng đằng sau điều khiển nhóm, khi The Shield debut vào ngày 18 tháng 11 năm 2012 tại WWE Survivor Series, nhóm gồm có Dean Ambrose, Roman Reigns, và Seth Rollins tấn công vào Main Event, trận Triple Threat giữa CM Punk, John Cena, và Ryback cho WWE Championship. Họ powerbombed Ryback lên chiếc bàn bình luận, …

**Bài:** Paul Heyman Guy (nhóm đô vật chuyên nghiệp) (11,774 âm tiết), cửa sổ ở 34% bài  
**Trạng thái:** kept  
**Câu hỏi:** Lesnar đã bảo toàn đai vô địch trước ai tại Royal Rumble vào ngày 27 tháng 1 năm 2019?  
**Đáp án sinh:** Finn Bálor  
**Kiểm:** Finn Bálor (F1 1.0)  
**Cửa sổ (rút gọn):** Sau khi giành đai, Lesnar được dự định đấu với AJ Styles tại Survivor Series trong trận đấu không tranh đai. Tuy nhiên, năm ngày trước Survivor Series, Styles đã thua và mất đai vô địch của mình vào tay Daniel Bryan trong SmackDown. Tại Survivor Series, Lesnar thắng. Lesnar sau đó bảo toàn đai trước Finn Bálor tại Royal Rumble vào ngày 27 tháng 1 n…

**Bài:** Paul Heyman Guy (nhóm đô vật chuyên nghiệp) (11,774 âm tiết), cửa sổ ở 85% bài  
**Trạng thái:** kept  
**Câu hỏi:** Axel giành được WWE Intercontinental Championship tại pay-per-view nào?  
**Đáp án sinh:** WWE Payback  
**Kiểm:** WWE Payback (F1 1.0)  
**Cửa sổ (rút gọn):** Sau đó, Triple H yêu cầu trận đấu được quay lại, như lần đầu tiên Vince McMahon đã trở lại và kết thúc trận đấu và cho Triple H thua cuộc, mặc dù Triple H không có bất cứ trục trặc gì. Axel giành được WWE Intercontinental Championship tại pay-per-view WWE Payback khi anh đánh bại Wade Barrett và The Miz trong một trận đấu tay ba. Tối hôm sau trên R…

**Bài:** Paul Heyman Guy (nhóm đô vật chuyên nghiệp) (11,774 âm tiết), cửa sổ ở 78% bài  
**Trạng thái:** kept  
**Câu hỏi:** Punk đã bảo vệ đai WWE Championship trước ai tại sự kiện Royal Rumble ngày 27 tháng 1 năm 2013?  
**Đáp án sinh:** The Rock  
**Kiểm:** The Rock (F1 1.0)  
**Cửa sổ (rút gọn):** Tại Royal Rumble ngày 27 tháng 1 năm 2013, Punk đã bảo vệ đai WWE Championship trước The Rock trong một trận đấu với quy định rằng nếu The Shield can thiệp, Punk sẽ bị tước danh hiệu. Punk ban đầu được pin The Rock bảo vệ thành công chiếc đai sau khi The Shield đẩy The Rock vào chiếc bàn, trong khi đó trường quay đã bị tắt đèn. Vince McMahon xuất h…

**Bài:** Chiến dịch phòng ngự chiến lược Leningrad (12,706 âm tiết), cửa sổ ở 85% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Quân đội Liên Xô đã chặn đứng cuộc tấn công của quân đội Đức Quốc xã trên hướng thành phố Leningrad và hướng Demyansk nhờ vào biện pháp nào?  
**Đáp án sinh:** những biện pháp động viên lực lượng dự bị huy động từ các quân khu trong nội địa  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Chiến dịch phòng ngự chiến lược Leningrad của quân đội đã không đạt được mục tiêu đề ra. Thành phố Leningrad bị quân đội Đức Quốc xã bao vây và phải trải qua gần 900 ngày sau, vòng vây đó mới bị phá vỡ. Quá nửa quân số tham gia chiến dịch (so với quân số ban đầu) đã thương vong. Chỉ nhờ vào những biện pháp động viên lực lượng dự bị huy động từ các …

**Bài:** Chiến dịch phòng ngự chiến lược Leningrad (12,706 âm tiết), cửa sổ ở 13% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là người chỉ huy Tập đoàn quân 16?  
**Đáp án sinh:** thượng tướng Ernst Busch  
**Kiểm:** thượng tướng Ernst Busch (F1 1.0)  
**Cửa sổ (rút gọn):** Tập đoàn quân 16 do thượng tướng Ernst Busch chỉ huy; thành phần gồm có: Quân đoàn bộ binh 1 do trung tướng Kuno-Hans von Both chỉ huy; trong biên chế có các sư đoàn bộ binh 11, 21 và 126. Quân đoàn bộ binh 2 do trung tướng Walter Graf von Brockdorff-Ahlefeldt chỉ huy; trong biên chế có các sư đoàn bộ binh 12, 32 và 123. Quân đoàn bộ binh 10 do tru…

**Bài:** Chiến dịch phòng ngự chiến lược Leningrad (12,706 âm tiết), cửa sổ ở 55% bài  
**Trạng thái:** kept  
**Câu hỏi:** Vào ngày 17 tháng 8, Quân đoàn xe tăng 41 (Đức) đã đánh chiếm đầu mối giao thông đường sắt quan trọng ở đâu?  
**Đáp án sinh:** Volosovo  
**Kiểm:** Volosovo (F1 1.0)  
**Cửa sổ (rút gọn):** Nó không nằm ở Luga, nơi quân đội Liên Xô đã huy động đến Sư đoàn xe tăng 24 và 3 sư đoàn bộ binh trấn giữ, mà nằm ở phía Nam "Cụm phòng thủ Kingisepp", nơi chỉ có Quân đoàn bộ binh 4 mới thành lập vội vã chỉ gồm Sư đoàn xe tăng 1 khá yếu (chỉ có 58 xe tăng hoạt động được), Sư đoàn bảo vệ bờ biển của Hạm đội Baltic và Sư đoàn học viên trường quân s…

**Bài:** Chiến dịch phòng ngự chiến lược Leningrad (12,706 âm tiết), cửa sổ ở 91% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ai là Tổng tham mưu trưởng lục quân Đức Quốc xã đã viết vào ngày 18 tháng 9 năm 1941 về việc chuyển lực lượng xe tăng về hướng Moskva?  
**Đáp án sinh:** trung tướng Franz Halder  
**Kiểm:** trung tướng Franz Halder (F1 1.0)  
**Cửa sổ (rút gọn):** Sau khi bao vây Leningrad, quân đội Đức Quốc xã còn rộng đường tiến đánh trên hướng Volkhov - Tikhvin, đe dọa tiến vào sau Tập đoàn quân 7 của Phương diện quân Karelia đang phòng ngự chống lại các cuộc tấn công của quân đội Phần Lan trên eo đất giữa hồ Ladoga và hồ Onega. Mặc dù không chiếm được thành phố Leningrad nhưng Tổng hành dinh quân đội Đức…

**Bài:** Chiến dịch phòng ngự chiến lược Leningrad (12,706 âm tiết), cửa sổ ở 83% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Sự kiện nào đã khiến Leningrad hoàn toàn bị cắt rời khỏi đất lớn và chỉ còn liên lạc được qua hồ Ladoga?  
**Đáp án sinh:** các sư đoàn xe tăng của Tập đoàn quân xe tăng 4 (Đức) đã chọc thủng phòng tuyến của quân đội Liên Xô ở chỗ tiếp giáp giữa Tập đoàn quân 55 (Phương diện quân Leningrad) và Tập đoàn quân 54 (Phương diện quân Tây Bắc) tại khu vực Kolpino - Mga, tiến ra bờ hồ Ladoga, đánh chiếm "cái cổ chai" Shlisselburg  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Quân đội Đức Quốc xã bao vây Leningrad Kết thúc chiến dịch, mặc dù các tập đoàn quân 11, 27 và 34 (Liên Xô) đã chặn được Tập đoàn quân 16 (Đức) tại khu vực phía Đông Demyansk, loại trừ một phần nguy cơ đứt đoạn giữa Phương diện quân Tây Bắc (tái lập) và Phương diện quân Tây nhưng điều đó là không đủ để chặn các đòn tấn công của Quân đội Đức Quốc xã…

**Bài:** Chiến dịch phòng ngự chiến lược Leningrad (12,706 âm tiết), cửa sổ ở 20% bài  
**Trạng thái:** question_refers_to_text  
**Câu hỏi:** Theo đoạn trích, Hitler quyết định chọn mục tiêu Kiev và Ukraina trước vì những nguồn lực nào?  
**Đáp án sinh:** những cánh đồng lúa mì bao la, các khu khai thác khoáng sản và những khu công nghiệp ở Ukraina  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Trong 3 mục tiêu của Kế hoạch Barbarossa, Hitler quyết định chọn mục tiêu Kiev và Ukraina trước vì những cánh đồng lúa mì bao la, các khu khai thác khoáng sản và những khu công nghiệp ở Ukraina chính là nguồn lực vậy chất nuôi dưỡng chiến tranh. Mục tiêu tiếp theo là Moskva, trái tim của đất nước Xô Viết. Mục tiêu Leningrad tụt xuống đứng hàng thứ …

**Bài:** Chiến dịch phòng ngự chiến lược Leningrad (12,706 âm tiết), cửa sổ ở 4% bài  
**Trạng thái:** answer_not_verbatim  
**Câu hỏi:** Sư đoàn bộ binh 58 thuộc Quân đoàn bộ binh 38 (Đức) chỉ còn cách khu vực nội đô Leningrad bao xa về phía Tây Nam trên khu vực Pulkovo?  
**Đáp án sinh:** 5 km  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Khozin lần lượt chỉ huy. Phần còn lại của Phương diện quân Bắc gồm các tập đoàn quân 7, 14, các đơn vị độc lập chiến đấu ở vùng cực và Karelia được đổi thành Phương diện quân Karelia do thượng tướng V. Sau chiến dịch, Quân đội Đức Quốc xã tiếp tục phát huy chiến quả, tấn công sâu thêm trên hướng Tây Bắc Liên Xô từ 180 km (trên hướng Demyansk, 240 k…

**Bài:** Chiến dịch phòng ngự chiến lược Leningrad (12,706 âm tiết), cửa sổ ở 82% bài  
**Trạng thái:** answer_length  
**Câu hỏi:** Sự kiện nào đã diễn ra vào ngày 22 tháng 8 năm 1941 khiến Leningrad hoàn toàn bị cắt rời khỏi đất lớn?  
**Đáp án sinh:** các sư đoàn xe tăng của Tập đoàn quân xe tăng 4 (Đức) đã chọc thủng phòng tuyến của quân đội Liên Xô ở chỗ tiếp giáp giữa Tập đoàn quân 55 (Phương diện quân Leningrad) và Tập đoàn quân 54 (Phương diện quân Tây Bắc) tại khu vực Kolpino - Mga, tiến ra bờ hồ Ladoga, đánh chiếm "cái cổ chai" Shlisselburg  
**Kiểm:** - (F1 -)  
**Cửa sổ (rút gọn):** Đối diện với họ là Sư đoàn bộ binh 32 (Đức). Trên vùng hồ Orekhov đến Ostakovo có các sư đoàn bộ binh 4, 23, 28 (tuyến 1), 33, 183 và sư đoàn kỵ binh 46 (tuyến 2) phòng thủ. Quân đội Đức Quốc xã bao vây Leningrad Kết thúc chiến dịch, mặc dù các tập đoàn quân 11, 27 và 34 (Liên Xô) đã chặn được Tập đoàn quân 16 (Đức) tại khu vực phía Đông Demyansk, …

**Bài:** Breaking Bad (14,855 âm tiết), cửa sổ ở 40% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhân vật Jack Welker trong phim Breaking Bad là chú của ai và giữ vị trí gì trong băng đảng Aryan Brotherhood?  
**Đáp án sinh:** Chú của Todd và là thủ lĩnh của Aryan Brotherhood  
**Kiểm:** Chú của Todd và là thủ lĩnh của Aryan Brotherhood (F1 1.0)  
**Cửa sổ (rút gọn):** David Costabile trong vai Gale Boetticher – Nhà hóa học được Gus Fring thuê để làm việc cùng với Walter. Daniel Moncada và Luis Moncada trong vai Leonel và Marco Salamanca – Hai gã sát thủ lầm lì nhưng tàn nhẫn của băng đảng Juarez, là anh em họ của Tuco Salamanca và cháu trai của Hector Salamanca. Emily Rios trong vai Andrea Cantillo – Bạn gái thứ…

**Bài:** Breaking Bad (14,855 âm tiết), cửa sổ ở 45% bài  
**Trạng thái:** kept  
**Câu hỏi:** Walter đã thuê luật sư nào để móc nối với nhà buôn ma túy cấp cao Gus?  
**Đáp án sinh:** Saul  
**Kiểm:** Saul (F1 1.0)  
**Cửa sổ (rút gọn):** Các đầu nậu phân phối của Jesse ngày càng trở nên không an toàn, Walter đành phải thuê gã luật sư vô lại Saul, móc nối với nhà buôn ma túy cấp cao Gus, bằng cách chào hàng lô hàng mới nhất của ông. Jesse thì đang bắt đầu hẹn hò với chủ trọ của anh là Jane, và cô này thì tái nghiện heroin. Nhận thấy Jesse không đáng tin cậy, Walter từ chối trả anh m…

**Bài:** Breaking Bad (14,855 âm tiết), cửa sổ ở 38% bài  
**Trạng thái:** kept  
**Câu hỏi:** Trong phim Breaking Bad, nhân vật Tuco Salamanca được mô tả là tên trùm ma túy Mexico mắc chứng gì?  
**Đáp án sinh:** rối loạn nhân cách chống đối xã hội  
**Kiểm:** rối loạn nhân cách chống đối xã hội (F1 1.0)  
**Cửa sổ (rút gọn):** Charles Baker trong vai Skinny Pete – Bạn của Jesse. Rodney Rush trong vai Christian "Combo" Ortega – Cũng là bạn và đồng bọn của Jesse. Jessica Hecht và Adam Godley trong vai Gretchen và Elliodt Schwartz – Đồng sở hữu của Grey Matter, một công ty mà họ đồng sáng lập cùng với Walter, người đã rời bỏ doanh nghiệp trước khi nó phát đạt. Gretchen từng…

**Bài:** Breaking Bad (14,855 âm tiết), cửa sổ ở 77% bài  
**Trạng thái:** kept  
**Câu hỏi:** Pittsburgh Post-Gazette đã đánh giá Breaking Bad là loạt phim như thế nào trong năm 2011?  
**Đáp án sinh:** loạt phim hay nhất 2011  
**Kiểm:** loạt phim hay nhất 2011 (F1 1.0)  
**Cửa sổ (rút gọn):** Pittsburgh Post-Gazette tiếp tục xem Breaking Bad là loạt phim hay nhất 2011, đồng thời lưu ý rằng "Breaking Bad là phim truyền hình hiếm hoi chưa từng mắc bất cứ lỗi kể chuyện nghiêm trọng nào". Bài đánh giá của The A.V. Club về tập phim cuối mùa tóm gọn là một "kết thúc tuyệt vời phù hợp với mùa phim diễn ra với tốc độ chậm, khởi đầu và tiếp diễn…

**Bài:** Breaking Bad (14,855 âm tiết), cửa sổ ở 19% bài  
**Trạng thái:** kept  
**Câu hỏi:** Theo Gilligan, Nelson đã xem xét các kịch bản để đảm bảo những cuộc đối thoại hóa học luôn chính xác và điều gì?  
**Đáp án sinh:** hợp thời  
**Kiểm:** hợp thời (F1 1.0)  
**Cửa sổ (rút gọn):** Chúng tôi nhận được trợ giúp ở bất cứ vấn đề nào mình cần, cho dù đó là hóa học, kỹ thuật điện hay vật lý. Chúng tôi cố gắng làm mọi thứ thật chính xác. Cố vấn không phải lúc nào cũng túc trực trên phim trường, nên phải cho chạy trước một số cảnh nhất định cần các chuyên gia.Gilligan nói: "Vì Walter White phải trao đổi với các học sinh của mình, tô…

**Bài:** Breaking Bad (14,855 âm tiết), cửa sổ ở 46% bài  
**Trạng thái:** kept  
**Câu hỏi:** Mùa 3 của Breaking Bad chính thức lên sóng vào ngày nào?  
**Đáp án sinh:** 21 tháng 3 năm 2010  
**Kiểm:** ngày 21 tháng 3 năm 2010 (F1 0.91)  
**Cửa sổ (rút gọn):** Ông này vì quá đau xót do mất con nên đã vướng phải sai sót nghiêm trọng trong lúc làm việc. Ngày 2 tháng 4 năm 2009, AMC công bố kế hoạch sản xuất mùa ba của Breaking Bad với 13 tập phim. Mùa 3 chính thức lên sóng ngày 21 tháng 3 năm 2010 và kết thúc vào ngày 13 tháng 6 năm 2010. Mùa phim có phiên bản hoàn chỉnh trên DVD mã vùng 1 và Blu-ray mã vù…

**Bài:** Breaking Bad (14,855 âm tiết), cửa sổ ở 36% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhân vật Lydia Rodarte-Quayle trong Breaking Bad được thủ vai bởi diễn viên nào?  
**Đáp án sinh:** Laura Fraser  
**Kiểm:** Laura Fraser (F1 1.0)  
**Cửa sổ (rút gọn):** Mike được so sánh với Winston Wolf do Harvey Keitel thủ vai trong Pulp Fiction, nhưng Banks thì bày tỏ rằng mình không nghĩ tới việc so kè với vai diễn Winston Wolf: "Thành thật thì tôi ngay lập tức cố gắng gạt điều đó ra khỏi tâm trí của mình. Trên khắp thế giới này, bạn sẽ nghi ngờ về sự tồn tại của rất nhiều 'người dọn dẹp', dù là họ làm việc ch…

**Bài:** Breaking Bad (14,855 âm tiết), cửa sổ ở 80% bài  
**Trạng thái:** kept  
**Câu hỏi:** Bryan Cranston đã giành giải Primetime Emmy cho nam diễn viên xuất sắc trong loạt phim chính kịch vào những năm nào?  
**Đáp án sinh:** 2008, 2009, 2010 và 2014  
**Kiểm:** 2008, 2009, 2010 và 2014 (F1 1.0)  
**Cửa sổ (rút gọn):** Với màn hóa thân Walter White, Bryan Cranston đã giật giải Primetime Emmy cho nam diễn viên xuất sắc trong loạt phim chính kịch tới 4 lần (2008, 2009, 2010 và 2014). Cranston còn đoạt giải TCA cho thành tựu cá nhân trong phim chính kịch vào năm 2009 và giải Vệ tinh cho nam diễn viên xuất sắc nhất trong phim truyền hình chính kịch vào các năm 2008, …

**Bài:** Inkigayo (7,704 âm tiết), cửa sổ ở 80% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhóm nhạc nào đã giành vị trí thứ nhất với bài hát 'Beautiful' vào ngày 5 tháng 12 năm 2010?  
**Đáp án sinh:** BEAST  
**Kiểm:** BEAST (F1 1.0)  
**Cửa sổ (rút gọn):** 2010.09.19 - Không phát sóng (2NE16th - Can't Nobody1st) 2010.09.26 - 2NE17th - Can't Nobody2nd 2010.10.03 - 2NE18th - Can't Nobody3rd 2010.10.10 - Không phát sóng (2NE19th - Go Away1st) 2010.10.17 - SHINee9th - Hello1st 2010.10.24 - 2PM9th - I'll be back1st 2010.10.31 - Ga-In1st - Irreversible 1st 2010.11.07 - Girls' Generation15th - 훗 (Hoot)1st 2…

**Bài:** Inkigayo (7,704 âm tiết), cửa sổ ở 9% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ca khúc nào của H.O.T. đã đạt vị trí thứ nhất trên bảng xếp hạng vào ngày 29 tháng 11 năm 1998?  
**Đáp án sinh:** 빛 (Hope)  
**Kiểm:** 빛 (Hope) (F1 1.0)  
**Cửa sổ (rút gọn):** 1998.09.20 - Kim Hyun-jung5th - 혼자한 사랑 (Lonely Love)1st 1998.09.27 - Sechs Kies2nd - 무모한 사랑 (Reckless Love)1st 1998.10.04 - Uhm Jung-hwa1st - 포이즌 (Poison)1st 1998.10.11 - Sechs Kies3rd - 무모한 사랑 (Reckless Love)2nd 1998.10.18 - H.O.T.1st - 열맞춰 (Line Up)1st 1998.10.25 - Không phát sóng 1998.11.01 - H.O.T.2nd - 열맞춰 (Line Up)2nd 1998.11.08 - Turbo4th - …

**Bài:** Inkigayo (7,704 âm tiết), cửa sổ ở 6% bài  
**Trạng thái:** kept  
**Câu hỏi:** Ca khúc nào của nhóm S.E.S. được phát hành vào ngày 01 tháng 03 năm 1998?  
**Đáp án sinh:** I'm Your Girl  
**Kiểm:** I'm Your Girl (F1 1.0)  
**Cửa sổ (rút gọn):** 1998.02.08 - Turbo2nd - 회상 (December)2nd 1998.02.15 - Turbo3rd - 회상 (December)3rd 1998.02.22 - S.E.S.1st - I'm Your Girl1st 1998.03.01 - S.E.S.2nd - I'm Your Girl2nd 1998.03.08 - Park Jin-young1st - HONEY1st 1998.03.15 - Park Jin-young2nd - HONEY2nd 1998.03.22 - Shin Seung-hoon1st - 지킬수 없는 약속 (A Promise I Can't Follow)1st 1998.03.29 - Shin Seung-ho…

**Bài:** Inkigayo (7,704 âm tiết), cửa sổ ở 5% bài  
**Trạng thái:** kept  
**Câu hỏi:** Giải thưởng Mutizen Song được trao cho đối tượng nào trong chương trình?  
**Đáp án sinh:** bài hát chiến thắng  
**Kiểm:** bài hát chiến thắng (F1 1.0)  
**Cửa sổ (rút gọn):** Cuối chương trình, giải thưởng Mutizen Song ("Mutizen" là sự kết hợp của "music" (âm nhạc) và "netizen" (cư dân mạng)) sẽ được trao cho bài hát chiến thắng. Hệ thống này đã thay thế bảng xếp hạng đếm ngược được sử dụng trong hầu hết các chương trình âm nhạc. Một bài hát chỉ có thể chiến thắng 3 lần. Hệ thống này bị hủy bỏ vào ngày 10 tháng 7 năm 20…

**Bài:** Inkigayo (7,704 âm tiết), cửa sổ ở 61% bài  
**Trạng thái:** check_disagrees  
**Câu hỏi:** Nhóm nhạc nào đã đạt vị trí thứ 9 với bài hát '아리랑 (Arirang)' vào ngày 29 tháng 4 năm 2007?  
**Đáp án sinh:** SG Wannabe9th  
**Kiểm:** SG Wannabe (F1 0.5)  
**Cửa sổ (rút gọn):** 2007.04.08 - Ivy2nd - 유혹의 소나타 (Sonata of Temptation)2nd 2007.04.15 - Không phát sóng 2007.04.22 - Ivy3rd - 유혹의 소나타 (Sonata of Temptation)3rd 2007.04.29 - SG Wannabe9th - 아리랑 (Arirang)1stTháng 52007.05.06 - SG Wannabe10th - 아리랑 (Arirang)2nd 2007.05.13 - SG Wannabe11th - 아리랑 (Arirang)3rd 2007.05.20 - Younha1st - 비밀번호 486 (Secret Number 486)1st 2007.0…

**Bài:** Inkigayo (7,704 âm tiết), cửa sổ ở 32% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhóm nhạc nào đã ra mắt ca khúc 'Sea Of Love' vào ngày 14 tháng 7 năm 2002?  
**Đáp án sinh:** Fly to the Sky  
**Kiểm:** Fly to the Sky (F1 1.0)  
**Cửa sổ (rút gọn):** 2002.03.31 - Fin.K.L15th - 영원 (Forever)1stTháng 42002.04.07 - Fin.K.L16th - 영원 (Forever)2nd 2002.04.14 - Fin.K.L17th - 영원 (Forever)3rd 2002.04.21 - Shinhwa10th - Perfect Man1st 2002.04.28 - Shinhwa11th - Perfect Man2ndTháng 52002.05.05 - Shinhwa12th - Perfect Man3rd 2002.05.12 - BoA1st - No.11st 2002.05.19 - BoA2nd - No.12nd 2002.05.26 - BoA3rd - N…

**Bài:** Inkigayo (7,704 âm tiết), cửa sổ ở 3% bài  
**Trạng thái:** kept  
**Câu hỏi:** Bảng xếp hạng âm nhạc trực tuyến có tên cũ là gì?  
**Đáp án sinh:** Mobile Ranking  
**Kiểm:** Mobile Ranking (F1 1.0)  
**Cửa sổ (rút gọn):** Tháng 8 - Teen Top Tháng 9 - Go Eun (고은) Tháng 10 - Bohemian (보헤미안) Tháng 11 - Bebe Mignon (베베미뇽) Tháng 12 - One Way Bảng xếp hạng âm nhạc trực tuyến Có tên cũ là Mobile Ranking, bảng xếp hạng âm nhạc trực tuyến (Digital Music Charts) cho thấy mức độ nổi tiếng của các bài hát thông qua số lượt tải về trên điện thoại cũng như trên các trang web âm n…

**Bài:** Inkigayo (7,704 âm tiết), cửa sổ ở 66% bài  
**Trạng thái:** kept  
**Câu hỏi:** Nhóm nhạc nào đã giành vị trí thứ nhất với ca khúc 'L.O.V.E' vào ngày 2 tháng 3 năm 2008?  
**Đáp án sinh:** Brown Eyed Girls  
**Kiểm:** Brown Eyed Girls (F1 1.0)  
**Cửa sổ (rút gọn):** 2008.01.27 - Haha1st - 너는 내운명 (You Are My Destiny)1stTháng 22008.02.03 - Girls' Generation3rd - Kissing You1st 2008.02.10 - Không phát sóng 2008.02.17 - Girls' Generation4th - Kissing You2nd 2008.02.24 - Park Ji Heon1st - 보고 싶은 날엔 (The Day I Miss You)1stTháng 32008.03.02 - Brown Eyed Girls1st - L.O.V.E1st 2008.03.09 - Brown Eyed Girls2nd - L.O.V.E2…
