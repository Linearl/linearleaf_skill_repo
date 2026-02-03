import re
from datetime import datetime, timedelta
from pathlib import Path

import akshare as ak
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = BASE_DIR / "analysis"
REPORT_DIR = BASE_DIR / "report"
OUT_FILE = REPORT_DIR / "03_汇总_结论表.md"

pattern = re.compile(r"03_(.+)_(\d{6})_(.+)\.md")


def _pick(text: str, label: str) -> str:
    m2 = re.search(rf"- \*\*{label}\*\*：([^\n]+)", text)
    return m2.group(1).strip() if m2 else ""


def _to_float(series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def analyze_price(code: str) -> tuple[str, str, str, str]:
    end = datetime.now().strftime("%Y%m%d")
    start = (datetime.now() - timedelta(days=200)).strftime("%Y%m%d")
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
    high20 = df["最高"].rolling(20).max().iloc[-1]
    low20 = df["最低"].rolling(20).min().iloc[-1]
    high60 = df["最高"].rolling(60).max().iloc[-1]
    low60 = df["最低"].rolling(60).min().iloc[-1]

    if pd.isna(ma20) or pd.isna(ma60):
        return "数据不足", "观望", "-", "-"

    if close >= ma20 >= ma60:
        trend = "上行"
        strategy = "回撤至MA20/MA60分批"
    elif close >= ma60 and close < ma20:
        trend = "震荡偏弱"
        strategy = "等站回MA20或放量突破"
    else:
        trend = "弱势"
        strategy = "观望，待企稳放量"

    target_low = round(float(ma60), 2)
    target_high = round(float(high60), 2)
    support = round(float(low60 if pd.notna(low60) else low20), 2)
    resistance = round(float(high20 if pd.notna(high20) else high60), 2)
    target = f"{target_low}-{target_high}"
    levels = f"{support}/{resistance}"
    return trend, strategy, target, levels


rows = []
for path in sorted(ANALYSIS_DIR.glob("03_*.md")):
    if path.name == OUT_FILE.name:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = pattern.match(path.name)
    track = code = name = ""
    if m:
        track, code, name = m.group(1), m.group(2), m.group(3)

    auth = _pick(text, "业务真实性")
    timing = _pick(text, "择时建议")
    risk = _pick(text, "最大风险")
    trend, strategy, target, levels = analyze_price(code)
    rows.append(
        (
            track,
            code,
            name,
            auth,
            timing,
            risk,
            trend,
            strategy,
            target,
            levels,
            path.name,
        )
    )

lines = [
    "# Step3 汇总结论表（20260119）",
    "",
    "| 赛道 | 代码 | 名称 | 业务真实性 | 择时建议 | 最大风险 | 近期走势 | 入场策略（参考） | 预期价格区间（参考） | 支撑/压力 | 报告 |",
    "|---|---|---|---|---|---|---|---|---|---|---|",
]

for (
    track,
    code,
    name,
    auth,
    timing,
    risk,
    trend,
    strategy,
    target,
    levels,
    fname,
) in rows:
    link = f"[{fname}]({fname})"
    lines.append(
        "| "
        + " | ".join(
            [
                track,
                code,
                name,
                auth or "未填",
                timing or "未填",
                risk or "未填",
                trend,
                strategy,
                target,
                levels,
                link,
            ]
        )
        + " |"
    )

REPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote summary: {OUT_FILE}")
