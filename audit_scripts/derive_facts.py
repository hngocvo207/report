#!/usr/bin/env python3
"""Tính các số suy ra dùng trong docs, từ output audit và kết quả gốc của leakage_fix.

Chạy từ gốc repo Dynamic_Fusion:
    python3 docs/research/audit_scripts/derive_facts.py > docs/research/audit_scripts/derive_facts.log
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RES = ROOT / "Dataset/inductive_model/leakage_fix/results"
a = json.load(open(HERE / "audit_data_out.json"))
d = json.load(open(HERE / "audit_degree_artifact_out.json"))


def pct(x, y):
    return round(100 * x / y, 2)


print("zero_value_edges_pct", pct(a["val_zero"], a["n_edges"]))
print("duplicate_edges_pct", pct(a["duplicate_edges(src,dst,ts,val)"], a["n_edges"]))
print("train_nodes_T_after_t1_pct", pct(a["train_nodes_T_after_t1"], a["split_train"]["nodes"]))
print("val_nodes_T_after_t2_pct", pct(a["val_nodes_T_after_t2"], a["split_val"]["nodes"]))
deg = a["degree_at_Tv_median"]
print("normal_deg1_at_Tv_pct", round(100 * deg["normal_frac_deg1"], 2))
print("phisher_deg1_at_Tv_pct", round(100 * deg["phisher_frac_deg1"], 2))
hop = a["degree_by_hop_and_label(full timeline)"]
print("normal_hop2_deg1_pct", round(100 * hop["y0_hop2"]["frac_deg1"], 2))
print("normal_hop2_share_of_normals_pct",
      pct(hop["y0_hop2"]["nodes"], sum(v["nodes"] for k, v in hop.items() if k.startswith("y0"))))
print("test_subset_deg_ge2_kept_pct", round(100 * d["test_subset_deg_ge2"]["frac_nodes_kept"], 2))
print("test_phishers_removed_by_deg_ge2", 233 - d["test_subset_deg_ge2"]["phishers"])

for t in ("gnn_in", "gnn_bidir", "gnn_in_g3", "gnn_bidir_g3"):
    r = json.load(open(RES / f"{t}.json"))["runs"]
    va = [x["val"]["auprc"] for x in r]
    thr = [x["val"]["threshold"] for x in r]
    print(f"{t}_val_auprc_mean {np.mean(va):.4f}")
    print(f"{t}_val_threshold_min {min(thr):.3f} max {max(thr):.3f}")
g = json.load(open(RES / "gbm_new23_temporal.json"))
print("gbm_new23_val_auprc_mean %.4f" % np.mean([x["val"]["auprc"] for x in g["per_seed"]]))
