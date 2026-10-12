#!/usr/bin/env python3
"""Checker cho bộ docs nghiên cứu. Dùng: python3 check_research_docs.py <repo_root> [docs_dir]"""
import re, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
DOCS = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT / "docs" / "research"
REQUIRED = ["00_OVERVIEW.md", "01_PROBLEM_AND_DATA.md", "02_SPLIT_AND_LEAKAGE_AUDIT.md",
            "03_MODEL_PROPOSAL.md", "04_PUBLIC_CODE_AND_REPRODUCIBILITY.md",
            "05_EXPERIMENT_PLAN.md", "06_EVIDENCE_AND_OPEN_ISSUES.md"]
TAGS = ["Đã xác minh", "Suy luận", "Đề xuất", "Chưa xác định"]
METRIC = re.compile(r"\b(F1|AUC|ROC|PR-AUC|AP|accuracy|precision|recall|MCC|loss|acc)\b[^\n]{0,40}?\d+[.,]?\d*", re.I)
SOURCE = re.compile(r"(\bE\d+\b|đã xác minh|nguồn:|\.log|\.csv|\.json|\.txt|\.py|\.ipynb|chưa chạy|TBD|https?://)", re.I)
HYPE = re.compile(r"\b(SOTA|state[- ]of[- ]the[- ]art|novel|đột phá|vượt trội|tốt nhất|hoàn hảo)\b", re.I)
FLUFF = ["như chúng ta đã biết", "trong thời đại", "có thể nói rằng", "không thể phủ nhận",
         "đóng vai trò vô cùng", "vô cùng quan trọng", "hết sức quan trọng", "ngày nay",
         "nhìn chung thì", "tóm lại là", "đáng chú ý là"]
PATH = re.compile(r"`([^`\s]+?\.(?:py|ipynb|yaml|yml|json|csv|md|txt|log|sh|toml|cfg|pt|pkl|npy|npz|parquet))(?::L?\d+(?:-L?\d+)?)?`")
IO_HEADER = "| Thành phần | Input | Biến đổi | Output | Mục đích | Rủi ro cần kiểm tra |"
PUNCT = {"→": "mũi tên", "—": "gạch dài", "…": "dấu ba chấm", ";": "chấm phẩy"}
UPPER_TAG = re.compile(r"\[(ĐÃ XÁC MINH|SUY LUẬN|ĐỀ XUẤT|CHƯA XÁC ĐỊNH)")
REFER = re.compile(r"(bảng|hình) (dưới đây|sau đây|bên dưới|trên đây)", re.I)

res = []  # (level, msg)
def add(level, msg): res.append((level, msg))

texts = {}
for name in REQUIRED:
    p = DOCS / name
    if not p.exists():
        add("FAIL", f"Thiếu file {name}")
    else:
        texts[name] = p.read_text(encoding="utf-8")

for name, t in texts.items():
    lines = t.splitlines()
    in_code = False
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        prose = re.sub(r"`[^`]*`", "", ln)
        for ch, label in PUNCT.items():
            if ch in prose:
                add("WARN", f"{name}:{i} có {label} '{ch}' trong văn bản (thay bằng chữ hoặc dấu phẩy)")
        if UPPER_TAG.search(prose):
            add("WARN", f"{name}:{i} nhãn viết hoa toàn bộ '{UPPER_TAG.search(prose).group(0)}', viet.py sẽ báo M5 (viết thành [Đã xác minh, E1])")
        if REFER.search(prose):
            add("WARN", f"{name}:{i} dẫn chiếu kiểu '{REFER.search(prose).group(0)}', hãy gọi theo số (Bảng 1, Hình 2)")
        if prose.lstrip().startswith("#") and prose.rstrip().endswith("?"):
            add("WARN", f"{name}:{i} tiêu đề là câu hỏi, hãy dùng cụm danh từ")
        if METRIC.search(ln) and not SOURCE.search(ln):
            add("FAIL", f"{name}:{i} số liệu metric không có nguồn: {ln.strip()[:90]}")
        if HYPE.search(ln) and "đã xác minh" not in ln.lower() and not ln.lstrip().startswith(">"):
            add("WARN", f"{name}:{i} từ khẳng định mạnh chưa có bằng chứng: {HYPE.search(ln).group(0)}")
        low = ln.lower()
        for f in FLUFF:
            if f in low:
                add("WARN", f"{name}:{i} câu dẫn rườm rà: '{f}'")
    for m in PATH.finditer(t):
        rel = m.group(1)
        if not (ROOT / rel).exists() and not (DOCS / rel).exists():
            add("FAIL", f"{name}: đường dẫn không tồn tại `{rel}`")
    if name not in ("00_OVERVIEW.md", "06_EVIDENCE_AND_OPEN_ISSUES.md") and not any(f"[{tag.lower()}" in t.lower() for tag in TAGS):
        add("WARN", f"{name}: không có nhãn mức độ xác minh nào")

# Mã bằng chứng: mọi E<n> dùng trong 00-05 phải có dòng trong bảng của 06
ev = texts.get("06_EVIDENCE_AND_OPEN_ISSUES.md", "")
defined = set(re.findall(r"^\|\s*(E\d+)\s*\|", ev, re.M))
for name, t in texts.items():
    if name.startswith("06"):
        continue
    for eid in sorted(set(re.findall(r"\b(E\d+)\b", t)) - defined):
        add("FAIL", f"{name}: mã bằng chứng {eid} không có trong bảng của 06")

ov = texts.get("00_OVERVIEW.md")
if ov is not None:
    if PATH.search(ov):
        add("WARN", "00_OVERVIEW.md chứa đường dẫn file, bản tổng quan phải đọc độc lập (chuyển sang 06)")
    words = len(re.findall(r"\w+", ov))
    add("FAIL" if words > 1100 else "PASS", f"00_OVERVIEW.md dài {words} từ (giới hạn ~1100)")

pd = texts.get("01_PROBLEM_AND_DATA.md")
if pd is not None:
    add("PASS" if IO_HEADER in pd else "FAIL", "01: bảng input/output đúng cột")
    add("PASS" if "```mermaid" in pd else "FAIL", "01: có sơ đồ luồng dữ liệu (khối mermaid)")

# Đoạn văn lặp giữa các file
def paras(t):
    for p in re.split(r"\n\s*\n", t):
        w = re.findall(r"\w+", p.lower())
        if len(w) >= 25 and not p.lstrip().startswith("|"):
            yield p.strip()[:60], set(w)
items = [(n, h, s) for n, t in texts.items() for h, s in paras(t)]
for a in range(len(items)):
    for b in range(a + 1, len(items)):
        if items[a][0] == items[b][0]:
            continue
        sa, sb = items[a][2], items[b][2]
        if len(sa & sb) / len(sa | sb) > 0.7:
            add("WARN", f"Ý lặp giữa {items[a][0]} và {items[b][0]}: '{items[a][1]}…'")

for name, t in texts.items():
    counts = ", ".join(f"{tag}={t.lower().count('[' + tag.lower())}" for tag in TAGS)
    add("INFO", f"{name}: {counts}")

order = {"FAIL": 0, "WARN": 1, "PASS": 2, "INFO": 3}
for lv, msg in sorted(res, key=lambda x: order[x[0]]):
    print(f"[{lv}] {msg}")
nf = sum(1 for lv, _ in res if lv == "FAIL"); nw = sum(1 for lv, _ in res if lv == "WARN")
print(f"\nTổng: {nf} FAIL, {nw} WARN")
sys.exit(1 if nf else 0)
