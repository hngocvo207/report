#!/usr/bin/env bash
# Tra license, lần push gần nhất và số issue mở của các repo công khai qua GitHub API (không cần token).
# Chạy: bash docs/research/audit_scripts/public_repos.sh > docs/research/audit_scripts/public_repos.log
echo "queried_at $(date -u +%Y-%m-%dT%H:%MZ)"
for r in dcszhang/Dynamic_Feature lmae4eth/LMAE4Eth lincozz/TLmGNN junhongmit/FraudGT pyg-team/pytorch_geometric dmlc/dgl scikit-learn/scikit-learn lightgbm-org/LightGBM dmlc/xgboost twitter-research/tgn yule-BUAA/DyGLib shenyangHuang/TGB THUDM/GraphMAE git-disl/BERT4ETH PonderLY/PC-GNN; do
  curl -sL -m 20 "https://api.github.com/repos/$r" | python3 -c "import sys,json; d=json.load(sys.stdin); print('$r', '| license', (d.get('license') or {}).get('spdx_id'), '| pushed', (d.get('pushed_at') or '')[:10], '| open_issues', d.get('open_issues_count'), '| archived', d.get('archived'))"
  echo "  license_files: $(curl -sL -m 20 "https://api.github.com/repos/$r/contents/" | python3 -c "import sys,json; print([x['name'] for x in json.load(sys.stdin) if 'lic' in x['name'].lower() or 'copying' in x['name'].lower()])" 2>/dev/null)"
done
