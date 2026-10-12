# Chia tập và rò rỉ dữ liệu

Số liệu theo định dạng quốc tế. Mã bằng chứng tra trong file 06. Định nghĩa tập, T_v và các bộ đặc trưng nằm ở file 01, mục 3 và 4.

## 1. Kết luận

Giao thức V3-sạch loại được rò rỉ dữ liệu (data leakage) qua đặc trưng và qua đồ thị. Rò rỉ dữ liệu ở đây nghĩa là mô hình thấy thông tin mà lúc dự đoán thật chưa có, nên điểm số cao hơn thực tế. Bằng chứng gồm ba phần [Đã xác minh, E6, E9]. Code cắt mọi giao dịch sau T_v. Bộ đặc trưng mới tái tạo đúng bộ cũ khi bỏ ràng buộc thời gian. Script audit đếm lại độc lập bậc nút tại T_v và khớp với bộ mới.

Bốn rủi ro còn lại chưa được loại trừ.

- Dữ liệu được thu thập bằng tìm kiếm theo chiều rộng (breadth-first search, BFS) quanh tài khoản lừa đảo. Cách thu thập BFS làm phần lớn tài khoản thường có bậc 1 (mục 3).
- Cửa sổ đặc trưng của 93.62% tài khoản tập kiểm định kéo dài sang giai đoạn kiểm tra (mục 4).
- Dữ liệu không có thời điểm gán nhãn.
- Tập kiểm tra chỉ có 233 tài khoản lừa đảo. Chênh lệch dưới khoảng 0.05 diện tích dưới đường Precision-Recall (area under the precision-recall curve, AUPRC) giữa hai mô hình chưa có ý nghĩa thống kê [Suy luận, E15].

Loại bỏ địa chỉ trùng giữa các tập là điều kiện cần, chưa đủ. Pipeline cũ không có địa chỉ trùng nhưng vẫn rò rỉ qua đặc trưng toàn thời gian, qua đồ thị đầy đủ và qua sampler dùng nhãn (mục 2).

## 2. Các giao thức đã dùng trong dự án

Dự án đã chạy kết quả trên bốn giao thức khác nhau. Số liệu giữa các giao thức không so sánh trực tiếp được vì tập kiểm tra khác nhau. Bảng 1 tóm tắt bốn giao thức.

Bảng 1. Bốn giao thức đánh giá trong repo

| Giao thức | Quy tắc chia | Tập kiểm tra | Rò rỉ còn lại | Bằng chứng |
|---|---|---|---|---|
| Chia cũ | Mốc là phân vị 80% của mọi giao dịch, tập kiểm tra gồm cả tài khoản vắt qua mốc | 811,704 tài khoản | Đặc trưng toàn thời gian, đồ thị đầy đủ khi chấm | E21 |
| V3 | Theo t_first, mốc t1 và t2 (file 01, Bảng 2) | 487,855 tài khoản, 233 lừa đảo | Tùy pipeline: đặc trưng cũ, đồ thị đầy đủ khi chấm, sampler dùng nhãn | E3, E17 |
| V3-sạch | V3 cộng ràng buộc T_v cho đặc trưng, đồ thị và lấy mẫu | Như V3 | Không phát hiện rò rỉ qua đặc trưng hay đồ thị | E6, E9 |
| Chia ngẫu nhiên | Chia ngẫu nhiên theo nút, phân tầng theo nhãn, cùng kích thước V3 | Thay đổi theo seed | Đồ thị huấn luyện chứa cạnh tương lai | E29 |

Ba lỗi của pipeline cũ đã được đo bằng thí nghiệm, không chỉ suy luận từ code.

- Đặc trưng toàn thời gian làm AUPRC của gradient boosting (GBM) tăng từ 0.360 ± 0.004 lên 0.417 ± 0.007 [Đã xác minh, E14]. Chênh lệch 0.057 tương đương mức giảm khoảng 14% tính trên 0.417 khi bỏ rò rỉ. Phần rò rỉ nằm chủ yếu ở nhóm 1 và 2: AUPRC tăng từ 0.303 ± 0.015 lên 0.368 ± 0.020 khi chỉ dùng 18 cột này [Đã xác minh, E14].
- Chấm tập kiểm định trên đồ thị đầy đủ làm việc chọn checkpoint kém ổn định. Khi chỉ đổi đồ thị chấm tập kiểm định sang snapshot tại t2, AUPRC kiểm tra tăng từ 0.387 ± 0.057 lên 0.425 ± 0.024 [Đã xác minh, E17].
- Kết quả 0.538 của mô hình dùng 7 đặc trưng chọn lọc có rò rỉ khi chọn đặc trưng: bước xếp hạng đặc trưng dùng nhãn của một phần tập kiểm định V3. Chạy lại đúng cấu hình đó với 5 seed (giá trị khởi tạo ngẫu nhiên) chỉ cho 0.422 ± 0.046 [Đã xác minh, E18].

## 3. Thiên lệch do cách thu thập dữ liệu

Audit này phát hiện một rủi ro chưa có trong báo cáo nào của repo: bậc nút phản ánh vị trí của tài khoản trong vùng thu thập BFS, không chỉ hành vi của tài khoản. Tại T_v, 68.06% tài khoản thường có bậc 1, trong khi chỉ 3.95% tài khoản lừa đảo có bậc 1 [Đã xác minh, E23]. Bậc trung vị tại T_v là 1.0 với tài khoản thường và 11.0 với tài khoản lừa đảo.

Nguyên nhân có khả năng cao là BFS dừng ở bước thứ hai. Tài khoản thường cách tài khoản lừa đảo đúng 2 bước chiếm 87.66% số tài khoản thường. Trong nhóm này, 59.74% có bậc 1 trên toàn thời gian [Đã xác minh, E23]. Tài khoản thường kề trực tiếp tài khoản lừa đảo có bậc trung vị 12.0, gần bằng 13.0 của tài khoản lừa đảo. Cạnh của tài khoản ở rìa vùng thu thập có thể đã bị cắt bớt [Suy luận, E23].

Rủi ro này làm ROC-AUC mất giá trị so sánh, nhưng chưa làm sai AUPRC của các mô hình đã kiểm tra. Bảng 2 so sánh một baseline chỉ dùng bậc nút với GBM sạch (seed 0) trên toàn tập kiểm tra và trên tập con chỉ gồm tài khoản có bậc ít nhất 2 tại T_v.

Bảng 2. Ảnh hưởng của tài khoản bậc 1 lên metric

| Mô hình | Tập chấm | AUPRC | ROC-AUC |
|---|---|---:|---:|
| Chỉ dùng bậc nút | Toàn tập kiểm tra | 0.0123 | 0.9372 |
| Chỉ dùng bậc nút | Bậc ít nhất 2 (99581 tài khoản, 223 lừa đảo) | - | 0.8103 |
| GBM, bộ mới 23 cột | Toàn tập kiểm tra | 0.3638 | 0.9762 |
| GBM, bộ mới 23 cột | Bậc ít nhất 2 | 0.3845 | 0.9692 |

Ba điểm rút ra từ Bảng 2 [Đã xác minh, E23].

- Riêng bậc nút đã cho ROC-AUC 0.9372. ROC-AUC từ 0.976 đến 0.982 của các mô hình (E14, E15) vì thế chủ yếu phản ánh việc loại nhóm tài khoản bậc 1 dễ đoán.
- Riêng bậc nút chỉ cho AUPRC 0.0123, nên AUPRC của GBM không đến từ bậc nút.
- Tập con bậc ít nhất 2 giữ 20.41% tài khoản kiểm tra và 223 trên 233 tài khoản lừa đảo. GBM giữ được AUPRC trên tập con này.

Audit chưa kiểm tra mạng nơ-ron đồ thị (graph neural network, GNN) trên tập con bậc ít nhất 2. Repo không lưu xác suất kiểm tra của GNN [Chưa xác định: cần lưu xác suất kiểm tra của GNN rồi chấm lại trên tập con, vì GNN dựa vào cấu trúc nhiều hơn GBM].

## 4. Đánh giá từng loại rò rỉ

Bảng 3 phân tích riêng từng loại rò rỉ cho giao thức V3-sạch, đồng thời ghi lại tình trạng của pipeline cũ để đối chiếu.

Bảng 3. Kết luận theo từng loại rò rỉ

| Loại | Câu hỏi kiểm tra | Kết luận cho V3-sạch | Nhóm | Bằng chứng |
|---|---|---|---|---|
| Trùng mẫu | Ba tập có trùng địa chỉ không? | Không trùng địa chỉ nào. Mốc t_first giữa các tập đúng thứ tự | Đã loại trừ | E4 |
| Temporal, đặc trưng | Đặc trưng có dùng giao dịch sau T_v không? | Không. Pipeline cũ có, và đã đo được mức tăng 0.057 AUPRC | Đã loại trừ | E6, E8, E14 |
| Temporal, đồ thị | Cấu trúc có dùng giao dịch sau T_v không? | Không với GNN mới. Pipeline cũ và FraudGT chấm trên đồ thị đầy đủ, trong đó 19.0% giao dịch chạm tập kiểm tra xảy ra sau T_v | Đã loại trừ ở mức code | E9, E26 |
| Temporal, chồng cửa sổ | Cửa sổ T_v có vượt sang giai đoạn của tập sau không? | 9.64% tài khoản huấn luyện có T_v sau t1. 93.62% tài khoản kiểm định có T_v sau t2. Không tài khoản huấn luyện nào có T_v sau t2 | Còn rủi ro | E25 |
| Temporal, nhãn | Nhãn có được gán sau thời điểm dự đoán không? | Dữ liệu không ghi thời điểm gán nhãn | Chưa biết | E32 |
| Đặc trưng, chuẩn hóa | Chuẩn hóa hay chọn đặc trưng có fit trên tập kiểm định, kiểm tra không? | Không. GNN lấy trung bình và độ lệch chuẩn từ tập huấn luyện. GBM không cần chuẩn hóa. Pipeline cũ chọn 7 đặc trưng bằng nhãn có lẫn tập kiểm định | Đã loại trừ | E11, E18 |
| Đặc trưng, mốc chia | Mốc chia có dùng thông tin của tập kiểm tra không? | Có. t1, t2 là phân vị trên t_first của mọi tài khoản lừa đảo, gồm cả tài khoản kiểm tra | Còn rủi ro nhỏ | E3 |
| Đồ thị | Truyền thông điệp (message passing) có đi qua cạnh bị cấm không? | Chỉ đi qua cặp có giao dịch đầu không muộn hơn T_v. Cạnh tới tài khoản kiểm định, kiểm tra quan sát được trước T_v là hợp lệ | Đã loại trừ ở mức code | E9 |
| Nhãn | Nhãn có lọt vào đầu vào không? | Không với GNN mới. Sampler cũ cấp nhiều láng giềng hơn cho chính tài khoản lừa đảo | Đã loại trừ | E10, E16 |
| Phụ thuộc mẫu | Mẫu liên kết chặt có bị tách sang nhiều tập không? | Có: 89.3% tài khoản lừa đảo kiểm tra có láng giềng thuộc tập kiểm tra, so với 23.8% tài khoản thường. Tín hiệu này quan sát được tại T_v với 70.8% tài khoản lừa đảo | Còn rủi ro | E26 |
| Giao thức | Inductive hay transductive? Tài khoản chưa thấy được xử lý thế nào? | Inductive theo nhóm t_first. Mỗi tài khoản được chấm trên snapshot riêng tại T_v. Mô hình cũ tri_model là transductive | Đã xác minh | E9, E20 |

Inductive nghĩa là mô hình chấm được tài khoản chưa xuất hiện lúc huấn luyện. Transductive nghĩa là mô hình học một biểu diễn riêng cho từng tài khoản đã biết, nên không chấm được tài khoản mới.

Ba nhóm rủi ro được tách như sau.

- Đã xác minh có rò rỉ, chỉ ở pipeline cũ: đặc trưng toàn thời gian, đồ thị đầy đủ khi chấm, sampler dùng nhãn, chọn đặc trưng bằng nhãn có lẫn tập kiểm định, nhánh văn bản dùng toàn bộ lịch sử (E8, E16, E17, E18, E19, E26).
- Còn rủi ro trong V3-sạch: thiên lệch thu thập qua bậc nút, chồng cửa sổ giữa các tập, mốc chia dùng nhãn của cả ba tập, phụ thuộc mẫu qua láng giềng kiểm tra (E3, E23, E25, E26).
- Chưa biết: thời điểm gán nhãn và mức độ đầy đủ của nhãn (E32).

## 5. Checklist chất lượng đầu vào

Bảng 4 ghi từng mục kiểm tra, kết quả hiện có và tiêu chí đạt. Các mục có kết quả đều do script audit chạy lại trên dữ liệu thật (E1, E24).

Bảng 4. Checklist chất lượng đầu vào cho V3-sạch

| Mục | Mục đích | Cách kiểm tra | Kết quả hiện có | Tiêu chí đạt/không đạt | Vấn đề còn mở |
|---|---|---|---|---|---|
| Shape, dtype, giá trị thiếu | Phát hiện lỗi đọc dữ liệu | Đếm NaN, inf, thời điểm thiếu trên mảng cạnh và ma trận đặc trưng | 0 thời điểm thiếu, 0 NaN và inf trong đặc trưng mới (E1) | Đạt khi tất cả bằng 0 | Không |
| Phân phối đặc trưng | Phát hiện đuôi dài, giá trị lạ | Thống kê theo cột | GNN dùng log có dấu cho cả 18 cột (E11) | Không có cột hằng số trên tập huấn luyện | Chưa có báo cáo phân phối theo tập |
| Nhất quán địa chỉ, chỉ số, nhãn | Tránh lệch hàng giữa các file | So thứ tự địa chỉ, so danh sách lừa đảo với nhãn | Khớp hoàn toàn (E2) | Đạt khi khớp hoàn toàn | Không |
| Hướng cạnh, self-loop, cạnh trùng | Hiểu cấu trúc đồ thị | Đếm trên mảng cạnh | 5,926 self-loop, 1,491,279 cạnh trùng hoàn toàn (E24) | Có giải thích cho từng loại | Chưa rõ nguồn gốc cạnh trùng và cạnh giá trị 0 |
| Thời gian của cạnh | Kiểm tra mốc chia | So t_first với thời điểm cạnh nhỏ nhất | t_first khớp thời điểm cạnh nhỏ nhất của mọi tài khoản (E4) | Đạt khi khớp hoàn toàn | Không |
| Đặc trưng chỉ dùng thông tin trước T_v | Chặn rò rỉ temporal | Đếm lại độc lập bậc tại T_v, tái tạo bộ cũ khi bỏ ràng buộc | Khớp hoàn toàn, lệch 0 (E6) | Đạt khi khớp hoàn toàn | Mới đếm lại bậc vào và bậc ra, chưa đếm lại các cột còn lại |
| Tiền xử lý chỉ fit trên tập huấn luyện | Chặn rò rỉ qua chuẩn hóa | Đọc code chuẩn hóa | Chỉ dùng tập huấn luyện (E11) | Đạt khi không có tập khác | Không |
| Mất cân bằng dữ liệu theo tập | Chọn metric và ngưỡng | Đếm nhãn theo tập | 0.034%, 0.065%, 0.048% (file 01, Bảng 2) | Ghi rõ, dùng AUPRC | Ngưỡng chọn ở tỷ lệ 0.065% áp lên tập có tỷ lệ 0.048% |
| Seed và khả năng tái lập | Ước lượng độ dao động | Chạy 5 seed, bootstrap 1000 lần | Có cho GBM, GNN (E14, E15) | Báo cáo trung bình và độ lệch chuẩn | Mã nguồn pipeline sạch chưa được git theo dõi (E30) |
| Đồ thị không chứa cạnh bị cấm | Chặn rò rỉ qua cấu trúc | Đọc code lấy mẫu | Chỉ cặp có giao dịch đầu không muộn hơn T_v (E9) | Có kiểm tra tự động khi chạy | Chưa có assert lúc chạy, mới kiểm ở mức code |
| Thiên lệch thu thập | Tránh mô hình học vị trí trong BFS | So metric trên tập con bậc ít nhất 2 | GBM giữ AUPRC (E23) | AUPRC trên tập con không giảm quá độ lệch giữa các seed | Chưa chấm GNN trên tập con |

Code chạy được hay metric cao không chứng minh dữ liệu hợp lệ hay giao thức hợp lệ. Bảng 4 kiểm tra dữ liệu. Bảng 3 kiểm tra giao thức. Việc mô hình dự đoán tốt đến đâu được trình bày ở file 03.

## 6. Giao thức chia tập đề xuất

### 6.1. Phương án chính V3-sạch có kiểm tra bổ sung

Phương án chính giữ V3-sạch và thêm bốn kiểm tra [Đề xuất]. Lý do chọn: V3-sạch mô phỏng đúng kịch bản triển khai, khi hệ thống chấm một tài khoản mới sau 30 ngày hoạt động. Toàn bộ code của V3-sạch đã chạy được và đã có kết quả 5 seed.

| Yếu tố | Nội dung |
|---|---|
| Câu hỏi nghiên cứu | Sau 30 ngày kể từ giao dịch đầu tiên, mô hình có xếp hạng đúng tài khoản mới chưa từng thấy theo nguy cơ lừa đảo không? |
| Đơn vị chia | Tài khoản, theo t_first |
| Mốc thời gian | t1, t2 giữ như V3 để so sánh được với kết quả đã có |
| Địa chỉ trùng | Không thể xảy ra vì mỗi tài khoản có đúng một t_first |
| Giao dịch tương lai | Cắt tại T_v cho tài khoản đích, láng giềng và đặc trưng của láng giềng |
| Snapshot đồ thị | Riêng cho từng tài khoản đích tại T_v |
| Được quan sát tại thời điểm dự đoán | Mọi giao dịch không muộn hơn T_v thuộc bất kỳ tập nào, nhãn của tập huấn luyện |
| Ưu điểm | Mô phỏng đúng triển khai, đã có code và kết quả |
| Giới hạn | 233 tài khoản lừa đảo kiểm tra, một mốc thời gian duy nhất |
| Chi phí | Thấp: các kiểm tra bổ sung không cần tính lại đặc trưng |

Bốn kiểm tra bổ sung:

1. Cắt cửa sổ đặc trưng của tập kiểm định tại t2. Phương án khác là giữ nguyên và ghi rõ là giới hạn. Đây là quyết định cần mentor phê duyệt (file 00).
2. Báo cáo AUPRC trên tập con bậc ít nhất 2 cho mọi mô hình, kèm AUPRC trên toàn tập.
3. So sánh hai mô hình bằng bootstrap ghép cặp trên cùng tập kiểm tra, không chỉ so độ lệch chuẩn qua seed.
4. Thêm các assert lúc chạy. Mọi cạnh được lấy mẫu phải có thời điểm không muộn hơn T_v của tài khoản đích. Nhãn chỉ được lấy từ tập huấn luyện.

### 6.2. Phương án thay thế đánh giá cuốn chiếu theo thời gian

Phương án này chia nhiều lần với mốc tăng dần, ví dụ 3 cặp mốc theo phân vị t_first của tài khoản lừa đảo [Đề xuất]. Mỗi lần huấn luyện trên mọi tài khoản trước mốc và kiểm tra trên cửa sổ ngay sau mốc.

- Câu hỏi trả lời: hiệu năng có ổn định qua các giai đoạn thời gian không, hay phụ thuộc vào một cửa sổ kiểm tra cụ thể?
- Ưu điểm: tổng số tài khoản lừa đảo dùng để đánh giá tăng lên, đo được concept drift (phân phối dữ liệu thay đổi theo thời gian).
- Giới hạn: các lần chia dùng chung dữ liệu huấn luyện nên kết quả không độc lập. Giai đoạn đầu có ít tài khoản lừa đảo.
- Chi phí: thấp. Đặc trưng tại T_v không phụ thuộc cách chia nên không cần tính lại. Chỉ cần huấn luyện lại GBM và GNN.
- Kiểm tra: mỗi lần chia đều qua các assert ở mục 6.1.

### 6.3. Phương án thay thế chia ngẫu nhiên có ràng buộc T_v

Phương án này chia ngẫu nhiên theo tài khoản nhưng vẫn chấm mỗi tài khoản trên snapshot tại T_v [Đề xuất]. Mục đích là so sánh được với các bài báo dùng chia ngẫu nhiên, như LMAE4Eth và FraudGT.

- Câu hỏi trả lời: chênh lệch giữa số liệu của dự án và số tự công bố của các bài báo đến từ giao thức hay từ kiến trúc?
- Ưu điểm: tách được ảnh hưởng của giao thức khỏi ảnh hưởng của mô hình.
- Giới hạn: không mô phỏng triển khai thật. Tập huấn luyện chứa tài khoản xuất hiện sau tài khoản kiểm tra.
- Chi phí: thấp, đã có code chia ngẫu nhiên cho GBM (E29).
- Kiểm tra: tỷ lệ lừa đảo bằng nhau giữa các tập, cùng kích thước với V3.

Kết quả hiện có cho thấy chia ngẫu nhiên không lạc quan hơn chia theo thời gian trên bộ dữ liệu này. GBM với bộ mới 23 cột đạt 0.308 ± 0.011 khi chia ngẫu nhiên, so với 0.360 ± 0.004 khi chia theo thời gian [Đã xác minh, E29]. Vì vậy không nên mặc định chia theo thời gian luôn cho số thấp hơn.
