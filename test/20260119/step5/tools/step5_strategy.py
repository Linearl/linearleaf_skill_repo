from datetime import datetime, timedelta
from pathlib import Path

import akshare as ak
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
STEP3_REPORT = BASE_DIR.parent / "step3" / "report" / "03_汇总_结论表.md"
STEP4_REPORT = BASE_DIR.parent / "step4" / "report" / "04_汇总_新闻表.md"
REPORT_DIR = BASE_DIR / "report"
OUT_FILE = REPORT_DIR / "05_汇总_介入策略表.md"


def _parse_table(path: Path) -> list[list[str]]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    rows = []
    for line in lines:
        if not line.startswith("|"):
            continue
        if line.startswith("|---"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if cols and cols[0] == "赛道":
            continue
        rows.append(cols)
    return rows


def _to_float(series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def analyze_price(code: str) -> tuple[str, str, str, str]:
    end = datetime.now().strftime("%Y%m%d")
    start = (datetime.now() - timedelta(days=400)).strftime("%Y%m%d")
    try:
        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date=start,
            end_date=end,
            adjust="qfq",
        )
    except Exception:
        return "数据缺失", "观望", "-", "-"

    if df is None or df.empty:
        return "数据缺失", "观望", "-", "-"

    df = df.copy()
    df["收盘"] = _to_float(df["收盘"])
    df["最高"] = _to_float(df["最高"])
    df["最低"] = _to_float(df["最低"])
    df = df.dropna(subset=["收盘", "最高", "最低"])
    if df.empty:
        return "数据缺失", "观望", "-", "-"

    close = df["收盘"].iloc[-1]
    ma20 = df["收盘"].rolling(20).mean().iloc[-1]
    ma60 = df["收盘"].rolling(60).mean().iloc[-1]
    ma250 = df["收盘"].rolling(250).mean().iloc[-1]
    high60 = df["最高"].rolling(60).max().iloc[-1]
    low60 = df["最低"].rolling(60).min().iloc[-1]
    high250 = df["最高"].rolling(250).max().iloc[-1]
    low250 = df["最低"].rolling(250).min().iloc[-1]

    if pd.isna(ma20) or pd.isna(ma60) or pd.isna(ma250):
        return "数据不足", "观望", "-", "-"

    if close >= ma20 >= ma60 >= ma250:
        trend = "强势"
        strategy = "回撤至MA20/MA60分批"
    elif close >= ma60 >= ma250:
        trend = "震荡偏强"
        strategy = "等站回MA20或放量突破"
    elif close >= ma250 and close < ma60:
        trend = "震荡偏弱"
        strategy = "等待企稳再评估"
    else:
        trend = "弱势"
        strategy = "观望，待MA60/MA250收复"

    target = f"{round(float(ma250),2)}-{round(float(high250),2)}"
    levels = f"{round(float(low250),2)}/{round(float(high60 if pd.notna(high60) else high250),2)}"
    return trend, strategy, target, levels


step3_rows = _parse_table(STEP3_REPORT)
step4_rows = _parse_table(STEP4_REPORT)

step4_map = {}
for row in step4_rows:
    if len(row) < 7:
        continue
    track, code, name, total_news, pos_cnt, neg_cnt, report = row[:7]
    step4_map[code] = (total_news, pos_cnt, neg_cnt, report)

lines = [
    "# Step5 汇总介入策略表（20260119）",
    "",
    "| 赛道 | 代码 | 名称 | 财报结论 | 主要风险 | 新闻数量 | 正向/负向 | 走势 | 策略（参考） | 预期区间（参考） | 支撑/压力 | Step3报告 | Step4报告 |",
    "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
]

for row in step3_rows:
    if len(row) < 7:
        continue
    track, code, name, auth, timing, risk, report = row[:7]
    total_news, pos_cnt, neg_cnt, report4 = step4_map.get(code, ("", "", "", ""))
    trend, strategy, target, levels = analyze_price(code)
    lines.append(
        "| "
        + " | ".join(
            [
                track,
                code,
                name,
                auth or "未填",
                risk or "未填",
                total_news or "未填",
                f"{pos_cnt or '0'}/{neg_cnt or '0'}",
                trend,
                strategy,
                target,
                levels,
                report,
                report4 or "-",
            ]
        )
        + " |"
    )

REPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote strategy: {OUT_FILE}")
