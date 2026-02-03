import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import akshare as ak
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
STEP3_TOOLS = BASE_DIR.parent / "step3" / "tools"
if str(STEP3_TOOLS) not in sys.path:
    sys.path.insert(0, str(STEP3_TOOLS))

from step3_cninfo_reports_and_notes import STOCKS

ANALYSIS_DIR = BASE_DIR / "analysis"

POS_KW = [
    "中标",
    "签约",
    "订单",
    "扩产",
    "增长",
    "同比增长",
    "业绩预增",
    "回购",
    "分红",
    "合作",
    "发布",
    "落地",
    "获批",
    "新产品",
    "涨停",
    "增持",
    "上调",
]

NEG_KW = [
    "下滑",
    "亏损",
    "减持",
    "处罚",
    "诉讼",
    "风险",
    "质疑",
    "终止",
    "裁员",
    "停产",
    "事故",
    "暴跌",
    "违约",
]


def _score(title: str, content: str, kws: list[str]) -> int:
    text = f"{title} {content}"
    return sum(1 for kw in kws if kw in text)


def _parse_time(value: str) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt)
        except Exception:
            continue
    try:
        return pd.to_datetime(value, errors="coerce").to_pydatetime()
    except Exception:
        return None


def fetch_news(code: str) -> pd.DataFrame:
    df = ak.stock_news_em(symbol=code)
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.copy()
    df["发布时间"] = df["发布时间"].apply(lambda x: str(x) if x is not None else "")
    df["_dt"] = df["发布时间"].apply(_parse_time)
    df = df[df["_dt"].notna()].sort_values("_dt", ascending=False)
    return df


def build_report(stock, df: pd.DataFrame, days: int = 60) -> str:
    cutoff = datetime.now() - timedelta(days=days)
    recent = df[df["_dt"] >= cutoff].copy()

    def _top(df_in: pd.DataFrame, kws: list[str], n: int = 5) -> list[dict]:
        rows = []
        for _, r in df_in.iterrows():
            title = str(r.get("新闻标题", ""))
            content = str(r.get("新闻内容", ""))
            score = _score(title, content, kws)
            if score > 0:
                rows.append((score, r))
        rows.sort(key=lambda x: (x[0], x[1].get("_dt")), reverse=True)
        out = []
        for _, r in rows[:n]:
            out.append(
                {
                    "time": r.get("发布时间", ""),
                    "title": r.get("新闻标题", ""),
                    "source": r.get("文章来源", ""),
                    "link": r.get("新闻链接", ""),
                }
            )
        return out

    positives = _top(recent, POS_KW, n=6)
    negatives = _top(recent, NEG_KW, n=6)

    def _fmt(items: list[dict]) -> str:
        if not items:
            return "- （无明显匹配条目；需人工补充）"
        lines = []
        for it in items:
            link = it["link"] or ""
            title = it["title"] or ""
            source = it["source"] or ""
            time = it["time"] or ""
            lines.append(f"- {time}｜{source}｜[{title}]({link})")
        return "\n".join(lines)

    total = len(recent)
    return f"""# 04｜新闻与事件：{stock.track}｜{stock.name}（{stock.code}）

> 窗口：近 {days} 天；来源：东方财富个股新闻（akshare.stock_news_em）

---

## A. 近期新闻概览

- 新闻条数：{total}
- 正向催化候选：{len(positives)}
- 负向风险候选：{len(negatives)}

---

## B. 正向催化（候选）

{_fmt(positives)}

---

## C. 负向风险（候选）

{_fmt(negatives)}

---

## D. 备注

- 以上为自动筛选，需人工复核事件真实性与影响级别。
"""


def main() -> int:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    for stock in STOCKS:
        print(f"==> {stock.track} {stock.code} {stock.name}")
        try:
            df = fetch_news(stock.code)
            content = build_report(stock, df, days=60)
            out = (
                ANALYSIS_DIR
                / f"04_新闻与事件_{stock.track}_{stock.code}_{stock.name}.md"
            )
            out.write_text(content, encoding="utf-8")
        except Exception as e:
            out = (
                ANALYSIS_DIR
                / f"04_新闻与事件_{stock.track}_{stock.code}_{stock.name}.md"
            )
            out.write_text(
                f"# 04｜新闻与事件：{stock.track}｜{stock.name}（{stock.code}）\n\n- 获取失败：{e}\n",
                encoding="utf-8",
            )

    print("\nDone")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
