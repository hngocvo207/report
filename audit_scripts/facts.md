# Fact sheet cho bộ docs nghiên cứu

Mọi con số dùng trong 00 đến 06 và nguồn của nó. Đường dẫn tính từ gốc repo Dynamic_Fusion. Số chép nguyên văn từ nguồn. Số suy ra được tính bằng script và ghi vào log của script đó.

## Dữ liệu và chia tập

| Dữ kiện | Giá trị | Nguồn |
|---|---|---|
| Số nút (tài khoản) | 2,973,489 | `docs/research/audit_scripts/audit_data.log` |
| Số giao dịch | 13,551,303 | `docs/research/audit_scripts/audit_data.log` |
| Số cặp (gửi, nhận) phân biệt | 5,355,155 | `docs/research/audit_scripts/audit_data.log` |
| Thời điểm giao dịch đầu tiên | 2015-08-07 | `docs/research/audit_scripts/audit_data.log` |
| Thời điểm giao dịch cuối | 2019-01-19 | `docs/research/audit_scripts/audit_data.log` |
| Số phisher (isp bằng 1) | 1165 | `data/preprocessed/Dataset_MG_v3_no_overlap/split_config.json` |
| Tỷ lệ phisher toàn bộ | 0.039% | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Train: số nút | 2,217,282 | `docs/research/audit_scripts/audit_data.log` |
| Train: số phisher | 757 | `docs/research/audit_scripts/audit_data.log` |
| Val: số nút | 268,352 | `docs/research/audit_scripts/audit_data.log` |
| Val: số phisher | 175 | `docs/research/audit_scripts/audit_data.log` |
| Test: số nút | 487,855 | `docs/research/audit_scripts/audit_data.log` |
| Test: số phisher | 233 | `docs/research/audit_scripts/audit_data.log` |
| Tỷ lệ phisher val | 0.065% | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Tỷ lệ phisher test | 0.048% | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Mốc t1 | 2018-05-18 | `docs/research/audit_scripts/audit_data.log` |
| Mốc t2 | 2018-06-18 | `docs/research/audit_scripts/audit_data.log` |
| Phân vị chọn mốc trên t_first của phisher | 0.65 và 0.80 | `data/preprocessed/Dataset_MG_v3_no_overlap/split_config.json` |
| Độ dài cửa sổ val (ngày) | 31.48 | `docs/research/audit_scripts/audit_data.log` |
| Cửa sổ quan sát sau giao dịch đầu tiên (ngày) | 30 | `Dataset/inductive_model/leakage_fix/common.py` |
| Số giao dịch có ts không quá t1 | 10,238,978 | `docs/research/audit_scripts/audit_data.log` |
| Số giao dịch có ts không quá t2 | 11,413,288 | `docs/research/audit_scripts/audit_data.log` |
| Self-loop | 5,926 | `docs/research/audit_scripts/audit_data.log` |
| Cạnh trùng hoàn toàn (src, dst, ts, val) | 1,491,279 | `docs/research/audit_scripts/audit_data.log` |
| Tỷ lệ cạnh trùng hoàn toàn | 11.0% | `docs/research/audit_scripts/derive_facts.log` |
| Số giao dịch giá trị 0 | 9,152,968 | `docs/research/audit_scripts/audit_data.log` |
| Tỷ lệ giao dịch giá trị 0 | 67.54% | `docs/research/audit_scripts/derive_facts.log` |
| Giá trị giao dịch lớn nhất | 800000.0 | `docs/research/audit_scripts/audit_data.log` |
| Nút test bị cụt cửa sổ vì chạm cuối dữ liệu | 12414 | `docs/research/audit_scripts/audit_data.log` |
| Tỷ lệ nút test bị cụt cửa sổ | 2.5% | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Nút train có T_v sau t1 | 213744 | `docs/research/audit_scripts/audit_data.log` |
| Tỷ lệ nút train có T_v sau t1 | 9.64% | `docs/research/audit_scripts/derive_facts.log` |
| Nút val có T_v sau t2 | 251241 | `docs/research/audit_scripts/audit_data.log` |
| Tỷ lệ nút val có T_v sau t2 | 93.62% | `docs/research/audit_scripts/derive_facts.log` |
| Giao dịch gửi từ nút test xảy ra sau T_v | 150303 | `docs/research/audit_scripts/audit_data.log` |
| Tỷ lệ giao dịch chạm test xảy ra sau T_v | 19.0% | `Dataset/inductive_model/TEST_CONNECTIVITY_LEAKAGE_AUDIT.md` |
| Tỷ lệ nút test có ít nhất 1 giao dịch như vậy | 7.9% | `Dataset/inductive_model/TEST_CONNECTIVITY_LEAKAGE_AUDIT.md` |
| Phisher test có láng giềng test | 89.3% | `Dataset/inductive_model/TEST_CONNECTIVITY_LEAKAGE_AUDIT.md` |
| Nút thường test có láng giềng test | 23.8% | `Dataset/inductive_model/TEST_CONNECTIVITY_LEAKAGE_AUDIT.md` |
| Phisher nhận giao dịch từ test, chỉ tính đến T_v | 70.8% | `Dataset/inductive_model/TEST_CONNECTIVITY_LEAKAGE_AUDIT.md` |
| Nút thường trong 2 bước tới một phisher (train, val, test) | 91%, 80%, 82% | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Số địa chỉ trong danh sách phisher cũ | 5,480 | `Dataset/fullscale_features/13_export_phisher_list.py` |
| Địa chỉ chung giữa danh sách cũ và nhãn isp | 963 | `Dataset/fullscale_features/13_export_phisher_list.py` |

## Thiên lệch thu thập qua bậc nút (audit mới)

| Dữ kiện | Giá trị | Nguồn |
|---|---|---|
| Bậc trung vị của phisher tại T_v | 11.0 | `docs/research/audit_scripts/audit_data.log` |
| Bậc trung vị của nút thường tại T_v | 1.0 | `docs/research/audit_scripts/audit_data.log` |
| Nút thường có bậc 1 tại T_v | 68.06% | `docs/research/audit_scripts/derive_facts.log` |
| Phisher có bậc 1 tại T_v | 3.95% | `docs/research/audit_scripts/derive_facts.log` |
| Nút thường cách phisher 2 bước: số nút | 2605666 | `docs/research/audit_scripts/audit_data.log` |
| Nút thường cách phisher 2 bước: tỷ lệ trong nút thường | 87.66% | `docs/research/audit_scripts/derive_facts.log` |
| Nút thường cách phisher 2 bước có bậc 1 (toàn thời gian) | 59.74% | `docs/research/audit_scripts/derive_facts.log` |
| Bậc trung vị nút thường kề phisher (toàn thời gian) | 12.0 | `docs/research/audit_scripts/audit_data.log` |
| Bậc trung vị phisher (toàn thời gian) | 13.0 | `docs/research/audit_scripts/audit_data.log` |
| Baseline chỉ dùng bậc: test AUPRC | 0.0123 | `docs/research/audit_scripts/audit_degree_artifact.log` |
| Baseline chỉ dùng bậc: test ROC-AUC | 0.9372 | `docs/research/audit_scripts/audit_degree_artifact.log` |
| Tập test con bậc ít nhất 2: số nút | 99581 | `docs/research/audit_scripts/audit_degree_artifact.log` |
| Tập test con bậc ít nhất 2: số phisher | 223 | `docs/research/audit_scripts/audit_degree_artifact.log` |
| Tập test con bậc ít nhất 2: tỷ lệ nút giữ lại | 20.41% | `docs/research/audit_scripts/derive_facts.log` |
| GBM new23 seed 0: AUPRC toàn test | 0.3638 | `docs/research/audit_scripts/audit_degree_artifact.log` |
| GBM new23 seed 0: AUPRC tập con bậc ít nhất 2 | 0.3845 | `docs/research/audit_scripts/audit_degree_artifact.log` |
| GBM new23 seed 0: ROC-AUC toàn test | 0.9762 | `docs/research/audit_scripts/audit_degree_artifact.log` |
| GBM new23 seed 0: ROC-AUC tập con bậc ít nhất 2 | 0.9692 | `docs/research/audit_scripts/audit_degree_artifact.log` |
| Baseline chỉ dùng bậc: ROC-AUC tập con bậc ít nhất 2 | 0.8103 | `docs/research/audit_scripts/audit_degree_artifact.log` |

## Kết quả protocol V3-clean và V3

| Dữ kiện | Giá trị | Nguồn |
|---|---|---|
| Ngẫu nhiên: AUPRC | 0.0005 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Khoảng cách tới phisher train: AUPRC | 0.0010 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Khoảng cách tới phisher train: ROC-AUC | 0.664 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GBM old23 temporal: AUPRC | 0.417 ± 0.007 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GBM old18 temporal: AUPRC | 0.368 ± 0.020 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GBM new18 temporal: AUPRC | 0.303 ± 0.015 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GBM new23 temporal: AUPRC | 0.360 ± 0.004 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GBM new23 temporal: CI 95% seed 0 | 0.299 đến 0.429 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GBM new23: ROC-AUC, P@100, F1 tại ngưỡng val | 0.976, 0.68, 0.416 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GBM new23 random split: AUPRC | 0.308 ± 0.011 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Random trừ temporal, new18, lr cố định | −0.078 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GNN time-aware chỉ payer: AUPRC | 0.483 ± 0.040 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GNN time-aware hai chiều: AUPRC | 0.509 ± 0.049 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GNN time-aware chỉ payer + G3: AUPRC | 0.459 ± 0.035 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GNN time-aware hai chiều + G3: AUPRC | 0.531 ± 0.036 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GNN hai chiều + G3: CI 95% seed 0 | 0.489 đến 0.608 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| GNN hai chiều + G3: ROC-AUC, P@100, Recall@1000, F1 | 0.982, 0.75, 0.79, 0.589 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Val AUPRC trung bình: chỉ payer, hai chiều, payer + G3, hai chiều + G3 | 0.4154, 0.4726, 0.4048, 0.4908 | `docs/research/audit_scripts/derive_facts.log` |
| GBM new23: val AUPRC trung bình | 0.3790 | `docs/research/audit_scripts/derive_facts.log` |
| Ngưỡng F1 chọn trên val của GNN hai chiều + G3 | 0.971 đến 1.000 | `docs/research/audit_scripts/derive_facts.log` |
| Graph-only cũ, val trên full graph: AUPRC | 0.387 ± 0.057 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Graph-only cũ, val trên snapshot t2: AUPRC | 0.425 ± 0.024 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Graph-only top-7 đã công bố (1 lần chạy) | 0.538 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Graph-only top-7 chạy lại 5 seed | 0.422 ± 0.046 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| E2 BERT + GraphSAGE trên V3: AUPRC | 0.243 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| FraudGT trên split V3: AUPRC | 0.332 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| FraudGT trên split riêng của FraudGT: AUPRC | 0.214 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| FraudGT: số epoch | 60 | `Dataset/inductive_model/leakage_fix/fraudgt/results/v3/ETH-SparseNodeGT/config.yaml` |
| FraudGT: epoch bắt đầu overfit | 17 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Số lần resample bootstrap | 1000 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Cặp có trọng số khớp bản gốc tại T vô cùng | 96% | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |

## Cấu hình mô hình

| Dữ kiện | Giá trị | Nguồn |
|---|---|---|
| GNN: fanout mặc định | 15, 10 | `Dataset/inductive_model/leakage_fix/f06_gnn_temporal.py` |
| GNN: hidden, epoch tối đa, patience | 64, 150, 30 | `Dataset/inductive_model/leakage_fix/f06_gnn_temporal.py` |
| GNN: batch size | 32 | `Dataset/inductive_model/leakage_fix/f06_gnn_temporal.py` |
| GNN hai chiều: fanout | 10, 5 | `Dataset/inductive_model/leakage_fix/run_after_group3.sh` |
| GBM: số vòng tối đa | 300 | `Dataset/inductive_model/leakage_fix/f03_gbm.py` |

## Pipeline cũ và tái hiện bài báo

| Dữ kiện | Giá trị | Nguồn |
|---|---|---|
| Bài báo Dynamic Feature Fusion: weighted F1 công bố | 94.71% | `MODEL_RESULTS_SUMMARY.md` |
| tri_model bounded: F1 lớp dương overall | 0.623 | `MODEL_RESULTS_SUMMARY.md` |
| tri_model full-scale: F1 lớp dương, AUPRC overall | 0.055, 0.124 | `MODEL_RESULTS_SUMMARY.md` |
| Test cũ: số tài khoản ngoài vocab | 801,704 / 811,704 | `MODEL_RESULTS_SUMMARY.md` |
| Tỷ lệ tài khoản test ngoài vocab | 98.8% | `MODEL_RESULTS_SUMMARY.md` |
| Vocab GCN của tri_model | 35,000 | `MODEL_RESULTS_SUMMARY.md` |
| E2 fusion và graph-only trên split cũ: AUPRC | 0.144, 0.303 | `MODEL_RESULTS_SUMMARY.md` |
| Ensemble GBM + graph-only trên split cũ | 0.474 | `MODEL_RESULTS_SUMMARY.md` |
| LMAE4Eth tái hiện, random split: F1 | 0.2799 | `../LMAE4Eth/repro/full_run.log` |
| LMAE4Eth bài báo: F1 | 0.8960 | `../LMAE4Eth/repro/full_run.log` |

## Mã nguồn công khai (tra ngày 2026-10-11)

| Dữ kiện | Giá trị | Nguồn |
|---|---|---|
| Ngày push gần nhất: Dynamic_Feature, LMAE4Eth, TLmGNN, FraudGT | 2025-01-19, 2025-12-12, 2025-05-02, 2025-06-05 | `docs/research/audit_scripts/public_repos.log` |
| Ngày push gần nhất: TGN, DyGLib, TGB | 2024-05-28, 2023-09-28, 2026-07-27 | `docs/research/audit_scripts/public_repos.log` |
| Ngày push gần nhất: GraphMAE, BERT4ETH, PC-GNN | 2023-04-12, 2024-06-21, 2021-12-26 | `docs/research/audit_scripts/public_repos.log` |
| Ngày push gần nhất: PyG, scikit-learn, LightGBM | 2026-10-06, 2026-10-10, 2026-10-11 | `docs/research/audit_scripts/public_repos.log` |
| Số issue mở: PyG | 1373 | `docs/research/audit_scripts/public_repos.log` |

## Bổ sung khi viết

| Dữ kiện | Giá trị | Nguồn |
|---|---|---|
| Số cột đặc trưng nhóm 1 và 2 | 18 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Tổng số cột đặc trưng | 23 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| AUPRC giảm khi bỏ rò rỉ đặc trưng (GBM, bộ 23 cột) | 0.057 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Mức giảm tương đối | 14% | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Chia ngẫu nhiên thấp hơn chia theo thời gian (AUPRC) | 0.05 đến 0.08 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Lệch lớn nhất khi tái tạo bộ đặc trưng cũ không cắt thời gian | 0 | `Dataset/inductive_model/leakage_fix/logs/f01_nocut.log` |
| Tỷ lệ phisher tập huấn luyện | 0.034% | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
| Cửa sổ tần suất dài (ngày) | 180 | `Dataset/inductive_model/leakage_fix/f05_temporal_graph.py` |
| Chênh lệch AUPRC khi thêm nhóm 3 vào GNN hai chiều | 0.022 | `Dataset/inductive_model/leakage_fix/PROGRESS_REPORT.md` |
