#!/usr/bin/env python3
"""Audit dữ liệu cho bộ docs nghiên cứu (chỉ đọc, không ghi gì ngoài stdout và audit_data_out.json).

Chạy từ gốc repo Dynamic_Fusion:
    python3 docs/research/audit_scripts/audit_data.py

Kiểm tra:
  1. shape, dtype, NaN/inf của mảng cạnh, mảng nút, đặc trưng new18/new23/old23
  2. tính nhất quán nodes.npy / address_to_index / labels / partition / t_first
  3. phân phối nhãn theo tập, địa chỉ trùng giữa các tập
  4. self-loop, cạnh trùng (src, dst, ts, val), khoảng thời gian cạnh theo tập của nút nguồn
  5. bất biến temporal: out/in-degree của new18 bằng số cạnh có ts <= T_v (đếm lại độc lập)
  6. scaler của old23 được fit trên tập nào (đọc meta)
  7. rủi ro thu thập BFS: bậc của nút theo khoảng cách tới phisher và theo nhãn
"""
from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
LF = ROOT / "Dataset" / "inductive_model" / "leakage_fix"
sys.path.insert(0, str(LF))
from common import (ARR, FEAT_DIR, G12_COLS, G3_COLS, OLD_FEATURES, SPLIT_DIR,  # noqa: E402
                    load_edges, load_nodes_labels_partition, prediction_time)

out: dict = {}


def p(k, v):
    out[k] = v
    print(f"{k}: {v}", flush=True)


def ts_h(t):
    import datetime
    return datetime.datetime.fromtimestamp(int(t), tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


# 1-2. arrays and consistency
src, dst, ts, val = load_edges()
nodes, y, part, t_first = load_nodes_labels_partition()
n, m = len(nodes), len(src)
p("n_nodes", n)
p("n_edges", m)
p("edge_dtypes", {"src": str(src.dtype), "dst": str(dst.dtype), "ts": str(ts.dtype), "val": str(val.dtype)})
p("ts_missing(<0)", int((ts < 0).sum()))
p("ts_min", ts_h(ts.min()))
p("ts_max", ts_h(ts.max()))
p("val_nan_or_inf", int((~np.isfinite(val)).sum()))
p("val_negative", int((val < 0).sum()))
p("val_zero", int((val == 0).sum()))
p("val_max", float(val.max()))
p("self_loops", int((src == dst).sum()))
key = np.stack([src.astype(np.int64), dst.astype(np.int64), ts, val.view(np.int64)], 1)
uniq = np.unique(key, axis=0).shape[0]
p("duplicate_edges(src,dst,ts,val)", int(m - uniq))
del key
pair = np.unique(src.astype(np.int64) * n + dst)
p("distinct_pairs", int(len(pair)))
del pair

with open(SPLIT_DIR / "address_to_index.pkl", "rb") as f:
    a2i = pickle.load(f)
p("a2i_matches_nodes_order", bool(all(a2i[nodes[i]] == i for i in range(0, n, 997))))

# t_first equals min incident edge timestamp
mn = np.full(n, np.iinfo(np.int64).max)
np.minimum.at(mn, src, ts)
np.minimum.at(mn, dst, ts)
p("t_first_equals_min_edge_ts", bool(np.array_equal(mn, t_first)))

# 3. labels per split, overlap
for s in ("train", "val", "test"):
    msk = part == s
    p(f"split_{s}", {"nodes": int(msk.sum()), "phishers": int(y[msk].sum()),
                     "tfirst_min": ts_h(t_first[msk].min()), "tfirst_max": ts_h(t_first[msk].max())})
p("split_other_labels", sorted(set(np.unique(part)) - {"train", "val", "test"}))
addr = {s: set(nodes[part == s]) for s in ("train", "val", "test")}
p("address_overlap", {"train&val": len(addr["train"] & addr["val"]), "train&test": len(addr["train"] & addr["test"]),
                      "val&test": len(addr["val"] & addr["test"])})
del addr
cfg = json.load(open(SPLIT_DIR / "split_config.json"))
t1, t2 = cfg["t1_train_val_cutoff"], cfg["t2_val_test_cutoff"]
p("t1_human", cfg["t1_human"])
p("t2_human", cfg["t2_human"])
p("val_window_days", round((t2 - t1) / 86400, 2))
ph_list = [a.strip() for a in open(ROOT / "raw_data/MulDiGraph/phisher_account_muldi.txt") if a.strip()]
p("phisher_list_equals_labels", bool(set(ph_list) == set(nodes[y == 1])))

# 4. edge time ranges by split of the source node; edges into the future relative to t1/t2
for s in ("train", "val", "test"):
    e = part[src] == s
    p(f"edges_from_{s}", {"n": int(e.sum()), "ts_min": ts_h(ts[e].min()), "ts_max": ts_h(ts[e].max())})
p("edges_le_t1", int((ts <= t1).sum()))
p("edges_le_t2", int((ts <= t2).sum()))

# 5. temporal invariant re-count
T = prediction_time(t_first, int(ts.max()))
od = np.bincount(src[ts <= T[src]], minlength=n)
idg = np.bincount(dst[ts <= T[dst]], minlength=n)
g12 = np.load(FEAT_DIR / "groups12_tfirst30d.npz")
p("new18_out_degree_equals_recount", bool(np.array_equal(od, g12["out_degree"])))
p("new18_in_degree_equals_recount", bool(np.array_equal(idg, g12["in_degree"])))
X18 = np.stack([np.asarray(g12[c], float) for c in G12_COLS], 1)
p("new18_shape", list(X18.shape))
p("new18_nan_inf", int((~np.isfinite(X18)).sum()))
g3 = np.load(FEAT_DIR / "group3_tfirst30d.npz")
X3 = np.stack([np.asarray(g3[c], float) for c in G3_COLS], 1)
p("g3_new_shape", list(X3.shape))
p("g3_new_nan_inf", int((~np.isfinite(X3)).sum()))
truncated = (t_first + 30 * 86400) > ts.max()
p("test_nodes_window_truncated", {"n": int((truncated & (part == "test")).sum()),
                                  "frac": round(float((truncated & (part == "test")).sum() / (part == "test").sum()), 4),
                                  "phishers": int((truncated & (part == "test") & (y == 1)).sum())})
# train nodes whose window reaches past t1 (into val period) and past t2 (into test period)
tr = part == "train"
p("train_nodes_T_after_t1", int((tr & (T > t1)).sum()))
p("train_nodes_T_after_t2", int((tr & (T > t2)).sum()))
va = part == "val"
p("val_nodes_T_after_t2", int((va & (T > t2)).sum()))
# full-timeline vs T_v: how many edges after T_v exist for test nodes (what the old features saw extra)
fut = (ts > T[src]) & (part[src] == "test")
p("test_src_edges_after_Tv", int(fut.sum()))

# 6. old23 scaler provenance
meta = json.load(open(ROOT / "Dataset/inductive_model/data/node_features_all23.scaler.json"))
p("old23_scaler_keys", list(meta.keys())[:8])
import torch  # noqa: E402
old = torch.load(OLD_FEATURES, weights_only=False)
p("old23_shape", list(old.shape))
p("old23_nan_inf", int((~torch.isfinite(old)).sum()))

# 7. BFS collection artefact: total degree (full timeline) by hop distance to nearest phisher and label
deg = np.bincount(src, minlength=n) + np.bincount(dst, minlength=n)
und_s = np.concatenate([src, dst]); und_d = np.concatenate([dst, src])
dist = np.full(n, 99, dtype=np.int64)
dist[y == 1] = 0
frontier = np.where(y == 1)[0]
for k in range(1, 4):
    fm = np.zeros(n, bool); fm[frontier] = True
    nb = np.unique(und_d[fm[und_s]])
    nb = nb[dist[nb] == 99]
    dist[nb] = k
    frontier = nb
rows = {}
for lab in (0, 1):
    for k in (0, 1, 2, 3, 99):
        msk = (y == lab) & (dist == k)
        if msk.sum() == 0:
            continue
        d = deg[msk]
        rows[f"y{lab}_hop{k}"] = {"nodes": int(msk.sum()), "deg_median": float(np.median(d)),
                                  "deg_mean": round(float(d.mean()), 2), "frac_deg1": round(float((d == 1).mean()), 4)}
p("degree_by_hop_and_label(full timeline)", rows)
# same at T_v (what new18 sees)
degT = od + idg
p("degree_at_Tv_median", {"phisher": float(np.median(degT[y == 1])), "normal": float(np.median(degT[y == 0])),
                           "normal_frac_deg1": round(float((degT[y == 0] == 1).mean()), 4),
                           "phisher_frac_deg1": round(float((degT[y == 1] == 1).mean()), 4)})

json.dump(out, open(Path(__file__).with_name("audit_data_out.json"), "w"), indent=2, default=str)
print("wrote audit_data_out.json")
