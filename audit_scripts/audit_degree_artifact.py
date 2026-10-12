#!/usr/bin/env python3
"""Kiểm tra rủi ro thiên lệch do cách thu thập dữ liệu (BFS quanh phisher) qua bậc của nút.

Chạy từ gốc repo Dynamic_Fusion:
    python3 docs/research/audit_scripts/audit_degree_artifact.py

1. Baseline không huấn luyện: điểm = tổng bậc của nút tại T_v (chỉ giao dịch <= T_v).
2. GBM new23 (seed 0, xác suất test đã lưu): AUPRC trên toàn tập test và trên tập con
   chỉ gồm nút có bậc tại T_v >= 2 (loại phần lớn nút ở rìa vùng thu thập).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
LF = ROOT / "Dataset" / "inductive_model" / "leakage_fix"
sys.path.insert(0, str(LF))
from common import RES_DIR, load_edges, load_nodes_labels_partition, prediction_time  # noqa: E402
from evalutil import metrics  # noqa: E402

src, dst, ts, _ = load_edges()
_, y, part, t_first = load_nodes_labels_partition()
n = len(y)
T = prediction_time(t_first, int(ts.max()))
deg = np.bincount(src[ts <= T[src]], minlength=n) + np.bincount(dst[ts <= T[dst]], minlength=n)

out = {}
te = np.where(part == "test")[0]
va = np.where(part == "val")[0]
out["degree_only_test"] = metrics(y[te], deg[te].astype(float))
out["degree_only_val"] = metrics(y[va], deg[va].astype(float))
sub = te[deg[te] >= 2]
out["test_subset_deg_ge2"] = {"nodes": int(len(sub)), "phishers": int(y[sub].sum()),
                              "frac_nodes_kept": round(len(sub) / len(te), 4)}
for feat in ("new23", "new18", "old23"):
    f = RES_DIR / f"gbm_{feat}_temporal_testprob_seed0.npy"
    if f.exists():
        p = np.load(f)
        assert len(p) == len(te)
        keep = deg[te] >= 2
        out[f"gbm_{feat}_seed0_full_test"] = metrics(y[te], p)
        out[f"gbm_{feat}_seed0_deg_ge2"] = metrics(y[te][keep], p[keep])
        out[f"degree_only_deg_ge2"] = metrics(y[te][keep], deg[te][keep].astype(float))
for k, v in out.items():
    print(k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()})
json.dump(out, open(Path(__file__).with_name("audit_degree_artifact_out.json"), "w"), indent=2)
