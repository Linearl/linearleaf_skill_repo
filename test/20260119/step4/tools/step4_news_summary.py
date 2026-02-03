from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = BASE_DIR / "analysis"
REPORT_DIR = BASE_DIR / "report"
OUT_FILE = REPORT_DIR / "04_汇总_新闻表.md"

pattern = re.compile(r"04_新闻与事件_(.+)_(\d{6})_(.+)\.md")

rows = []
for path in sorted(ANALYSIS_DIR.glob("04_新闻与事件_*.md")):
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = pattern.match(path.name)
    track = code = name = ""
    if m:
        track, code, name = m.group(1), m.group(2), m.group(3)

    total = re.search(r"新闻条数：\s*(\d+)", text)
    pos = re.search(r"正向催化候选：\s*(\d+)", text)
    neg = re.search(r"负向风险候选：\s*(\d+)", text)
    total_v = total.group(1) if total else ""
    pos_v = pos.group(1) if pos else ""
    neg_v = neg.group(1) if neg else ""
    link = f"[{path.name}]({path.name})"
    rows.append((track, code, name, total_v, pos_v, neg_v, link))

lines = [
    "# Step4 汇总新闻表（20260119）",
    "",
    "| 赛道 | 代码 | 名称 | 近60天新闻数 | 正向候选 | 负向候选 | 报告 |",
    "|---|---|---|---|---|---|---|",
]

for track, code, name, total_v, pos_v, neg_v, link in rows:
    lines.append(
        f"| {track} | {code} | {name} | {total_v or '未填'} | {pos_v or '未填'} | {neg_v or '未填'} | {link} |"
    )

REPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote summary: {OUT_FILE}")
