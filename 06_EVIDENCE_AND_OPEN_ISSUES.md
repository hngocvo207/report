# Bằng chứng và vấn đề còn mở

File này là phụ lục kỹ thuật. File này được phép chứa đường dẫn và lệnh, nên cảnh báo A1 của checker ngôn ngữ trên file này là miễn có chủ đích. Đường dẫn tính từ gốc repo Dynamic_Fusion. Mọi con số dùng trong 00 đến 06 có trong fact sheet `docs/research/audit_scripts/facts.md`.

## 1. Phạm vi kiểm toán

Kiểm toán đọc sâu pipeline V3-sạch, bước chia tập, bước tạo mảng cạnh và nhãn, cùng các file kết quả và log của pipeline đó. Các phần còn lại chỉ được kiểm kê và xác minh claim chính: tri_model, bi_model, nhánh E2, các bản sao trong `Dataset/dataset_check/`, các bước trung gian của `Dataset/fullscale_features/` và log tái hiện LMAE4Eth. Danh sách chi tiết nằm trong `docs/research/.audit_progress.md`. Báo cáo này không khẳng định đã đọc toàn bộ repo.

## 2. Bảng bằng chứng

Bảng 1 liệt kê mọi mã bằng chứng dùng trong 00 đến 05.

Bảng 1. Mã bằng chứng

| Mã | Nhận định | File:dòng, hàm | Mức xác minh |
|---|---|---|---|
| E1 | Quy mô dữ liệu, khoảng thời gian, không có thời điểm thiếu | `Dataset/fullscale_features/00_graph_to_arrays.py:33-84`, `main`. Output: `docs/research/audit_scripts/audit_data.log` | Đã xác minh, chạy lại |
| E2 | Nhãn là isp bằng 1, danh sách tài khoản lừa đảo trùng khớp nhãn, danh sách cũ bị bỏ | `Dataset/mg_temporal_pipeline.py:82`. `Dataset/fullscale_features/13_export_phisher_list.py:12-16`. `docs/research/audit_scripts/audit_data.log` | Đã xác minh, chạy lại |
| E3 | Chia theo t_first, mốc là phân vị trên t_first của mọi tài khoản lừa đảo | `Dataset/mg_temporal_pipeline_v3_no_overlap.py:76-98`, `main` | Đã xác minh, đọc code |
| E4 | Không trùng địa chỉ, ranh giới t_first đúng, t_first bằng thời điểm cạnh nhỏ nhất, cửa sổ tập kiểm định | `docs/research/audit_scripts/audit_data.py`, output `docs/research/audit_scripts/audit_data.log` | Đã xác minh, chạy lại |
| E5 | Định nghĩa T_v | `Dataset/inductive_model/leakage_fix/common.py:77-78`, `prediction_time` | Đã xác minh, đọc code |
| E6 | Nhóm 1 và 2 cắt tại T_v, tái tạo bản cũ với sai lệch 0, bậc vào và ra khớp phép đếm độc lập | `Dataset/inductive_model/leakage_fix/f01_groups12_tfirst.py:45-53`, `groups12`. `Dataset/inductive_model/leakage_fix/logs/f01_nocut.log`. `docs/research/audit_scripts/audit_data.log` | Đã xác minh, chạy lại |
| E7 | Nhóm 3 tính trên vùng lân cận 2 bước chỉ gồm giao dịch tới T_v, chạy song song nhiều tiến trình | `Dataset/inductive_model/leakage_fix/f02_group3_tfirst.py:67-95`, `ball_depth2`, `induced` | Đã xác minh, đọc code |
| E8 | Bộ đặc trưng cũ tính trên toàn thời gian | `Dataset/inductive_model/TEST_CONNECTIVITY_LEAKAGE_AUDIT.md` mục 6. Gián tiếp qua E6: bộ mới không cắt thời gian tái tạo đúng bộ cũ | Đã xác minh |
| E9 | Lấy mẫu láng giềng chỉ qua cặp có giao dịch đầu tới T_v, trọng số cộng dồn tới T_v, đặc trưng láng giềng tại min(T_u, T_v), không dùng nhãn, không có thuộc tính cạnh ngoài trọng số n-gram | `Dataset/inductive_model/leakage_fix/f05_temporal_graph.py:38-55`, `ngram_edge_weights`. Cùng file `:142-189`, `features`, `sample_neighbors`. `Dataset/inductive_model/leakage_fix/f06_gnn_temporal.py:42-71`, `Sampler.batch` | Đã xác minh, đọc code |
| E10 | Hàm mất mát chỉ dùng nhãn tập huấn luyện | `Dataset/inductive_model/leakage_fix/f06_gnn_temporal.py:161-175`, `run_seed` | Đã xác minh, đọc code |
| E11 | Chuẩn hóa từ tập huấn luyện, log có dấu cho 18 cột | `Dataset/inductive_model/leakage_fix/f06_gnn_temporal.py:120-129`, `Runner.__init__` | Đã xác minh, đọc code |
| E12 | Chọn checkpoint, siêu tham số và ngưỡng trên tập kiểm định | `Dataset/inductive_model/leakage_fix/f06_gnn_temporal.py:179-190`. `Dataset/inductive_model/leakage_fix/f03_gbm.py:85-93` | Đã xác minh, đọc code |
| E13 | Thứ hạng bốn biến thể mạng nơ-ron đồ thị (graph neural network, GNN) theo tập kiểm định trùng thứ hạng theo tập kiểm tra | `docs/research/audit_scripts/derive_facts.log` | Đã xác minh, chạy lại |
| E14 | Kết quả gradient boosting (GBM) với bốn bộ đặc trưng | `Dataset/inductive_model/leakage_fix/results/gbm_new23_temporal.json` và ba file gbm cùng thư mục. Đối chiếu với `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` mục 5.1 | Đã xác minh, số khớp |
| E15 | Kết quả bốn biến thể GNN time-aware | `Dataset/inductive_model/leakage_fix/results/gnn_bidir_g3.json` và ba file gnn cùng thư mục. Log `Dataset/inductive_model/leakage_fix/logs/f06_gnn.log` | Đã xác minh, số khớp |
| E16 | Sampler cũ cấp ngân sách láng giềng theo nhãn của chính nút | `Dataset/inductive_model/model/label_aware_sampler.py:58-61`, `_budget_fn` | Đã xác minh, đọc code |
| E17 | Pipeline cũ chấm tập kiểm định trên đồ thị đầy đủ, ảnh hưởng đã đo | `Dataset/inductive_model/train_eval/train_graph_only_hypothesis.py:248-277`. `Dataset/inductive_model/leakage_fix/f07_valgraph_fix.py`. `Dataset/inductive_model/leakage_fix/results/valgraph_fix_all23.json` | Đã xác minh |
| E18 | Kết quả 0.538 có rò rỉ khi chọn đặc trưng và không tái lập được | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` mục 4. `Dataset/inductive_model/leakage_fix/results/valgraph_fix_k7.json` | Đã xác minh từ kết quả, chưa đọc lại code xếp hạng đặc trưng |
| E19 | Corpus văn bản của E2 dùng toàn bộ lịch sử, kết quả E2 trên V3 | `Dataset/inductive_model/data_prep/e2_v3split_corpus.py:4-7`. `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` mục 6.1 | Đã xác minh, đọc code |
| E20 | tri_model học một hàng tham số cho mỗi tài khoản trong vocab, nên transductive | `Dataset/tri_model/ETH_GBert.py:45-56`, `VocabGraphConvolution`. `Dataset/tri_model/train1.py:240` | Đã xác minh, đọc code |
| E21 | Kết quả trên cách chia cũ: tri_model, E2, graph-only, kết hợp GBM với graph-only | `MODEL_RESULTS_SUMMARY.md` mục 1 và mục 2. Số gốc nằm ở các báo cáo ngoài repo `../tổng_hợp_markdown/` | Suy luận, chưa đối chiếu với log gốc |
| E22 | Baseline ngẫu nhiên và khoảng cách, tỷ lệ tài khoản thường trong 2 bước | `Dataset/inductive_model/leakage_fix/f04_distance_baseline.py:60-123`. `Dataset/inductive_model/leakage_fix/results/distance_baseline.json` | Đã xác minh, số khớp |
| E23 | Bậc nút phân theo khoảng cách và nhãn, baseline chỉ dùng bậc, tập con bậc ít nhất 2 | `docs/research/audit_scripts/audit_data.py` mục 7. `docs/research/audit_scripts/audit_degree_artifact.py`. Log `docs/research/audit_scripts/audit_degree_artifact.log`, `docs/research/audit_scripts/derive_facts.log` | Đã xác minh, chạy mới |
| E24 | Cạnh giá trị 0, cạnh trùng hoàn toàn, self-loop | `docs/research/audit_scripts/audit_data.log` | Đã xác minh, chạy mới |
| E25 | Cửa sổ T_v của tập huấn luyện vượt t1, của tập kiểm định vượt t2 | `docs/research/audit_scripts/audit_data.log`. Quyết định thiết kế ghi trong `Dataset/inductive_model/leakage_fix/common.py:4-10` | Đã xác minh, chạy mới |
| E26 | Tỷ lệ giao dịch chạm tập kiểm tra xảy ra sau T_v, phụ thuộc nhãn của láng giềng kiểm tra | `Dataset/inductive_model/TEST_CONNECTIVITY_LEAKAGE_AUDIT.md` mục 3 và mục 7 | Đã xác minh theo báo cáo có assert, chưa chạy lại |
| E27 | FraudGT: dữ liệu, kết quả, 60 epoch, đánh giá mỗi 2 epoch | `Dataset/inductive_model/leakage_fix/results/summary.json`. `Dataset/inductive_model/leakage_fix/fraudgt/results/v3/ETH-SparseNodeGT/config.yaml`. `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` mục 5.5 | Đã xác minh, số khớp |
| E28 | LMAE4Eth tái hiện, TLmGNN chưa chạy | `../LMAE4Eth/repro/full_run.log:621-623`. `MODEL_RESULTS_SUMMARY.md` mục 3.2 | Đã xác minh cho LMAE4Eth, suy luận cho TLmGNN |
| E29 | Chia ngẫu nhiên so với chia theo thời gian | `Dataset/inductive_model/leakage_fix/f03_gbm.py:49-61`, `make_split`. `Dataset/inductive_model/leakage_fix/results/gbm_new23_random.json`. `Dataset/inductive_model/leakage_fix/results/random_vs_temporal_breakdown.json` | Đã xác minh, số khớp |
| E30 | Thư mục pipeline sạch chưa được git theo dõi, PyG không có trong danh sách phụ thuộc | `git status --short Dataset/inductive_model` trả về dòng chưa theo dõi. `requirements.txt` | Đã xác minh, chạy lệnh |
| E31 | License, ngày push, file license của repo công khai | `docs/research/audit_scripts/public_repos.sh`, output `docs/research/audit_scripts/public_repos.log` | Đã xác minh qua GitHub API |
| E32 | Dữ liệu không có thời điểm gán nhãn | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` mục 1.1. Script audit chỉ thấy thuộc tính isp được dùng | Suy luận, chưa liệt kê hết thuộc tính nút của đồ thị gốc |
| E33 | Giao dịch đầu của mỗi tài khoản có trọng số n-gram bằng 0, pipeline mới chuẩn hóa bằng 1 cộng log | `Dataset/inductive_model/leakage_fix/f06_gnn_temporal.py:106-109`, `norm_weights` | Đã xác minh, đọc code |
| E34 | Sweep siêu tham số của graph-only cũ chọn theo tập kiểm định | `Dataset/inductive_model/train_eval/sweep_graph_only_v2.py:86-94` | Đã xác minh, đọc code |
| E35 | Trọng số cặp khi không giới hạn thời gian khớp ma trận kề gốc ở phần lớn cặp | `Dataset/inductive_model/leakage_fix/f05_temporal_graph.py:192-214`, `check`. `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` mục 5.2 | Đã xác minh theo log, chưa chạy lại |
| E36 | Ngưỡng F1-score chọn trên tập kiểm định của GNN sát giá trị tối đa của xác suất | `docs/research/audit_scripts/derive_facts.log`. Lấy mẫu âm theo tỷ lệ 3:1 ở `Dataset/inductive_model/leakage_fix/f06_gnn_temporal.py:169` | Đã xác minh, chạy lại |
| E37 | Định nghĩa AUPRC, Precision@100, Recall@1000, ngưỡng F1-score tối ưu trên tập kiểm định, bootstrap phân tầng giữ nguyên tỷ lệ lớp | `Dataset/inductive_model/leakage_fix/evalutil.py:8-53`, `best_f1_threshold`, `metrics`, `bootstrap_ci` | Đã xác minh, đọc code |

## 3. Mâu thuẫn giữa tài liệu cũ và code

Bảng 2 ghi các mâu thuẫn tìm thấy. Không file Markdown cũ nào bị sửa.

Bảng 2. Mâu thuẫn giữa tài liệu cũ và code hoặc dữ liệu

| Tài liệu cũ | Claim | Thực tế | Bằng chứng |
|---|---|---|---|
| `README.md` | Dự án có train.py, dev.tsv, file LICENSE theo MIT | Không có các file này ở gốc repo. Mã huấn luyện nằm trong `Dataset/tri_model/train1.py` | E30, E31 |
| `README.md` | Mô hình vượt các benchmark về accuracy, F1-score, recall | Trên toàn bộ tập kiểm tra cũ, tri_model chỉ đạt diện tích dưới đường Precision-Recall (area under the precision-recall curve, AUPRC) 0.124. README không nêu giao thức đánh giá | E21 |
| `Dataset/inductive_model/FINAL_REPORT_FOR_MENTOR.md` | Nhóm 1 và 2 rủi ro thấp, chỉ nhóm 3 rò rỉ thật | Rò rỉ nằm chủ yếu ở nhóm 1 và 2: GBM 0.368 so với 0.303 | E14 |
| `Dataset/inductive_model/FINAL_REPORT_FOR_MENTOR.md` | Dùng đồ thị đầy đủ khi suy luận là chủ đích, không phải rò rỉ | 19.0% giao dịch chạm tập kiểm tra xảy ra sau T_v | E26 |
| `Dataset/inductive_model/FINAL_REPORT_FOR_MENTOR.md` | Bản cắt thời gian của nhóm 3 chưa từng chạy | Đã chạy xong sau đó, bộ mới 23 cột tồn tại và không có NaN | E7, E4 |
| `CONTEXT_SUMMARY.md` | Giữ địa chỉ gửi và nhận trong văn bản là bản sửa lỗi | Sau đó địa chỉ của chính tài khoản bị xác định là nguyên nhân nhánh mô hình ngôn ngữ tiền huấn luyện học thuộc địa chỉ | `Dataset/inductive_model/BERT_debug.md` mục 1 |
| `MODEL_RESULTS_SUMMARY.md` | GNN time-aware sạch rò rỉ hoàn toàn | Sạch qua đặc trưng và đồ thị. Còn chồng cửa sổ giữa các tập, thiên lệch thu thập, thiếu thời điểm gán nhãn | E23, E25, E32 |
| `MODEL_RESULTS_SUMMARY.md` | Graph-only 7 đặc trưng đạt 0.538 | Chạy lại 5 seed đạt 0.422 ± 0.046, có rò rỉ khi chọn đặc trưng | E18 |
| `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` | FraudGT chạy 60 epoch | Khớp: config 60 epoch, file thống kê ít dòng hơn vì chỉ đánh giá mỗi 2 epoch. Không mâu thuẫn | E27 |

## 4. Câu hỏi còn thiếu bằng chứng

| Câu hỏi | Vì sao quan trọng | Cách kiểm tra |
|---|---|---|
| Cạnh giá trị 0 và cạnh trùng hoàn toàn là gì? | Chúng chiếm 67.54% và 11.0% số cạnh, chi phối đặc trưng tần suất | Đối chiếu mô tả bộ dữ liệu của XBlock, lấy mẫu vài cạnh tra trên trình duyệt khối |
| Nhãn được gán khi nào và theo quy trình nào? | Quyết định bài toán phát hiện sớm có nghĩa hay không | Tìm tài liệu gốc của MulDiGraph, liệt kê mọi thuộc tính nút |
| GNN có giữ AUPRC trên tập con bậc ít nhất 2 không? | GNN dựa vào cấu trúc nhiều hơn GBM | Thí nghiệm X0 ở file 05 |
| Rò rỉ qua đồ thị đầy đủ làm AUPRC của GNN tăng bao nhiêu? | Chưa được đo riêng | Thí nghiệm X8 ở file 05 |
| Điều khoản sử dụng dữ liệu XBlock | Quyết định có công bố được đặc trưng dẫn xuất không | Đọc trực tiếp trang XBlock hoặc liên hệ nhóm tác giả |
| Kho mã PhishEye có license gì? | Ứng viên baseline có đánh giá theo thời gian | Mở kho mã ẩn danh của bài báo |

## 5. Lệnh tái lập

Chạy từ gốc repo. Môi trường ảo trong repo không có torch. Lần audit này dùng Python hệ thống có torch. Thứ tự lệnh theo `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` mục 8.

```bash
python3 Dataset/fullscale_features/00_graph_to_arrays.py
python3 Dataset/mg_temporal_pipeline.py
python3 Dataset/mg_temporal_pipeline_v3_no_overlap.py
cd Dataset/inductive_model/leakage_fix
python f01_groups12_tfirst.py --no-cutoff && python f01_groups12_tfirst.py
python f02_group3_tfirst.py --check-full 100 && python f02_group3_tfirst.py --workers 16
python f03_gbm.py --features old23 old18 new18 new23; python f03b_gbm_fixed_hp.py
python f04_distance_baseline.py
python f05_temporal_graph.py --build --check
python f06_gnn_temporal.py; python f06_gnn_temporal.py --bidir --k1 10 --k2 5
python f06_gnn_temporal.py --g3; python f06_gnn_temporal.py --g3 --bidir --k1 10 --k2 5
python f07_valgraph_fix.py --topk 0; python f07_valgraph_fix.py --topk 7
python f08_random_vs_temporal.py; python f09_collect.py
cd ../../..
python3 docs/research/audit_scripts/audit_data.py
python3 docs/research/audit_scripts/audit_degree_artifact.py
python3 docs/research/audit_scripts/derive_facts.py
bash docs/research/audit_scripts/public_repos.sh
```

Biến thể hai chiều dùng fanout 10 và 5 thay cho mặc định 15 và 10. Repo không ghi lý do chọn [Chưa xác định: cần hỏi tác giả fanout này được chọn theo tập kiểm định hay theo giới hạn bộ nhớ].

## 6. Hành động tiếp theo

1. Đưa thư mục pipeline sạch và kết quả vào git, thêm PyG vào danh sách phụ thuộc (E30).
2. Chạy X0, X1, X2 ở file 05 vì chi phí thấp nhất.
3. Thêm assert thời gian vào bộ lấy mẫu và bộ tính đặc trưng.
4. Gỡ bản sao FraudGT khỏi mọi nhánh sẽ công khai. Cách khác là xin phép tác giả (E31).
5. Xác minh điều khoản dữ liệu XBlock trước khi công bố đặc trưng dẫn xuất.

## 7. Trạng thái từng nhiệm vụ

| Nhiệm vụ | Trạng thái | Lý do | Bước tiếp |
|---|---|---|---|
| A1. Truy vết dữ liệu | Đã làm | Có sơ đồ luồng dữ liệu và bảng input/output ở file 01 | Liệt kê hết thuộc tính nút của đồ thị gốc |
| A2. Đánh giá cách chia | Đã làm | Bảng rò rỉ ở file 02, mục 4 | Chạy X0 và X8 |
| A3. Giao thức đề xuất | Đã làm | Một phương án chính, hai phương án thay thế ở file 02, mục 6 | Mentor chọn có cắt cửa sổ tập kiểm định tại t2 không |
| A4. Checklist đầu vào | Đã làm một phần | Script audit có kiểm tra in ra kết quả, chưa có assert hay unit test | Chuyển các kiểm tra thành assert |
| B. Đề xuất mô hình | Đã làm | File 03 | Chạy X3 |
| C. Mã nguồn công khai | Đã làm | License và ngày push tra qua API | Xác minh PhishEye và điều khoản XBlock |
| D. Bảng input/output | Đã làm | File 01, mục 6 | Không |
| Kiểm tra tái lập toàn bộ pipeline | Chưa làm | Bước nhóm 3 tốn thời gian tính, audit chỉ chạy lại phần kiểm tra | Chạy lại toàn bộ trên máy sạch sau khi đưa code vào git |

## 8. Giới hạn của các checker

- Checker nội dung chỉ kiểm tra hình thức: nguồn của metric, mã E, đường dẫn tồn tại, dấu câu, độ dài file 00. Checker này không kiểm tra lập luận có đúng không.
- Checker ngôn ngữ đối chiếu con số với fact sheet. Checker này không biết con số đó có được dùng đúng ngữ cảnh hay không.
- Checker ngôn ngữ đưa cảnh báo mức xem lại ở ba chỗ mà báo cáo giữ nguyên có chủ đích.
  - Tên riêng như tên license và tên file README bị coi là viết tắt chưa giải nghĩa.
  - Một cột AUPRC trộn số chữ số thập phân. Nguồn ghi 0.0005 và 0.360 với độ chính xác khác nhau, báo cáo không làm tròn.
  - Đường dẫn trên file này. File 06 là phụ lục kỹ thuật nên được miễn.
- Fact sheet bỏ qua số nguyên từ 0 đến 10 vì checker coi đó là số đếm cấu trúc.
