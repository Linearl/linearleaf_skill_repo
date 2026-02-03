import os
import re
import sys
import json
import time
import random
import pathlib
from dataclasses import dataclass
from typing import Iterable, Optional
from urllib.parse import parse_qs, urlparse

import requests
import akshare as ak
from pypdf import PdfReader


BASE_DIR = pathlib.Path(__file__).resolve().parents[1]  # .../test/1/step3
REPORTS_DIR = BASE_DIR / "financials"
OUT_DIR = BASE_DIR / "analysis"

CNINFO_HOME = "http://www.cninfo.com.cn"
CNINFO_BULLETIN_DETAIL = "http://www.cninfo.com.cn/new/announcement/bulletin_detail"
CNINFO_STATIC = "https://static.cninfo.com.cn/"


@dataclass(frozen=True)
class Stock:
    track: str
    code: str
    name: str

    @property
    def column(self) -> str:
        # Rough mapping: Shenzhen for 0/3, Shanghai for 6/688
        return "szse" if self.code.startswith(("0", "3")) else "sse"


TARGETS_FILE = BASE_DIR.parent / "step2" / "02_标的清单.yaml"


def load_targets(path: pathlib.Path) -> list[Stock]:
    if not path.exists():
        raise FileNotFoundError(f"targets yaml not found: {path}")
    text = path.read_text(encoding="utf-8", errors="ignore")
    items: list[dict] = []
    current: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.strip().startswith("#"):
            continue
        if line.lstrip().startswith("- "):
            if current:
                items.append(current)
                current = {}
            line = line.lstrip()[2:]
            if ":" in line:
                k, v = line.split(":", 1)
                current[k.strip()] = v.strip().strip('"')
        elif ":" in line:
            k, v = line.split(":", 1)
            current[k.strip()] = v.strip().strip('"')
    if current:
        items.append(current)

    stocks: list[Stock] = []
    for it in items:
        name = it.get("name", "").strip()
        track = it.get("track", "").strip()
        code = it.get("code", "").strip()
        if not (name and track and code):
            continue
        stocks.append(Stock(track, code, name))
    return stocks


STOCKS: list[Stock] = load_targets(TARGETS_FILE)


def _headers() -> dict[str, str]:
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Origin": CNINFO_HOME,
        "Referer": CNINFO_HOME + "/",
    }


def get_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(_headers())
    # Prime cookies
    s.get(CNINFO_HOME, timeout=20)
    return s


def _parse_cninfo_detail_url(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    q = {k: (v[0] if v else "") for k, v in parse_qs(parsed.query).items()}
    return {
        "stockCode": q.get("stockCode", ""),
        "announcementId": q.get("announcementId", ""),
        "orgId": q.get("orgId", ""),
        "announcementTime": q.get("announcementTime", ""),
        "detailUrl": url,
    }


def query_latest_reports(session: requests.Session, stock: Stock) -> dict[str, dict]:
    """Return selected disclosures for annual + Q3 (or latest quarterly) reports.

    Uses AkShare to fetch disclosure list (stable) then cninfo bulletin_detail API
    to resolve the actual PDF URL.
    """

    def _date_range(years: int = 4) -> tuple[str, str]:
        # Use local time to build a safe range.
        end = time.strftime("%Y%m%d", time.localtime())
        y = int(end[:4]) - years
        start = f"{y}{end[4:]}"
        return start, end

    start_date, end_date = _date_range(5)

    def _fetch_category(category: str) -> list[dict]:
        try:
            df = ak.stock_zh_a_disclosure_report_cninfo(
                symbol=stock.code,
                market="沪深京",
                category=category,
                start_date=start_date,
                end_date=end_date,
            )
        except Exception:
            return []
        if df is None or df.empty:
            return []
        rows = df.to_dict(orient="records")
        out: list[dict] = []
        for r in rows:
            title = str(r.get("公告标题", ""))
            if not title:
                continue
            link = str(r.get("公告链接", ""))
            if not link:
                continue
            out.append(
                {
                    "announcementTitle": title,
                    "announcementTime": str(r.get("公告时间", "")),
                    "detailUrl": link,
                    **_parse_cninfo_detail_url(link),
                }
            )
        # newest first
        out.sort(key=lambda x: str(x.get("announcementTime", "")), reverse=True)
        return out

    def _pick_first(rows: list[dict], match_fn) -> Optional[dict]:
        for r in rows:
            if match_fn(str(r.get("announcementTitle", ""))):
                return r
        return None

    annual_rows = _fetch_category("年报")
    annual = _pick_first(
        annual_rows,
        lambda t: "年度报告" in t and "摘要" not in t and "英文" not in t,
    )

    q3_rows = _fetch_category("三季报")
    quarterly = _pick_first(q3_rows, lambda t: "摘要" not in t)
    if quarterly is None:
        # Fallback: latest quarterly among half-year / Q1
        half_rows = _fetch_category("半年报")
        q1_rows = _fetch_category("一季报")
        cand = [
            r
            for r in (half_rows + q1_rows)
            if "摘要" not in str(r.get("announcementTitle", ""))
        ]
        cand.sort(key=lambda x: str(x.get("announcementTime", "")), reverse=True)
        quarterly = cand[0] if cand else None

    selected = {"annual": annual, "quarterly": quarterly}
    return {k: v for k, v in selected.items() if v}


def safe_filename(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|]", "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:180]


def download_pdf(
    session: requests.Session, stock: Stock, a: dict, dest_dir: pathlib.Path
) -> pathlib.Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    announce_id = str(a.get("announcementId", "")).strip()
    announce_time = str(a.get("announcementTime", "")).strip()
    if not announce_id or not announce_time:
        raise ValueError("missing announcementId/announcementTime")

    detail = session.post(
        CNINFO_BULLETIN_DETAIL,
        params={
            "announceId": announce_id,
            "flag": "true" if stock.column == "szse" else "false",
            "announceTime": announce_time,
        },
        timeout=30,
    )
    detail.raise_for_status()
    payload = detail.json() if detail.content else {}
    ann = payload.get("announcement") if isinstance(payload, dict) else None
    if not isinstance(ann, dict):
        raise ValueError("bulletin_detail missing announcement")

    adjunct_url = str(ann.get("adjunctUrl", "")).lstrip("/")
    if not adjunct_url:
        raise ValueError("bulletin_detail missing adjunctUrl")

    t = str(ann.get("announcementTitle") or a.get("announcementTitle") or "report")
    url = CNINFO_STATIC + adjunct_url
    fn = safe_filename(f"{stock.code}_{stock.name}_{t}.pdf")
    out = dest_dir / fn
    if out.exists() and out.stat().st_size > 0:
        return out

    r = session.get(url, timeout=60)
    r.raise_for_status()
    out.write_bytes(r.content)
    # gentle throttling
    time.sleep(0.8 + random.random() * 0.8)
    return out


def extract_text(pdf_path: pathlib.Path, max_pages: int = 40) -> str:
    reader = PdfReader(str(pdf_path))
    texts: list[str] = []
    for i, page in enumerate(reader.pages[:max_pages]):
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        if txt:
            texts.append(txt)
    return "\n".join(texts)


def extract_snippets(
    text: str, keywords: Iterable[str], window: int = 120
) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for kw in keywords:
        out[kw] = []
        for m in re.finditer(re.escape(kw), text):
            start = max(0, m.start() - window)
            end = min(len(text), m.end() + window)
            snippet = text[start:end].replace("\n", " ")
            snippet = re.sub(r"\s+", " ", snippet).strip()
            if snippet and snippet not in out[kw]:
                out[kw].append(snippet)
            if len(out[kw]) >= 3:
                break
    return out


def select_existing_reports(stock_dir: pathlib.Path) -> dict[str, pathlib.Path]:
    if not stock_dir.exists():
        return {}
    pdfs = list(stock_dir.glob("*.pdf"))
    if not pdfs:
        return {}

    def _match(
        files: list[pathlib.Path], includes: list[str], excludes: list[str]
    ) -> list[pathlib.Path]:
        out: list[pathlib.Path] = []
        for p in files:
            name = p.name
            if any(k in name for k in includes) and not any(
                x in name for x in excludes
            ):
                out.append(p)
        return out

    annuals = _match(pdfs, ["年度报告"], ["摘要", "英文"])
    q3s = _match(pdfs, ["第三季度报告", "三季度报告"], ["摘要"])
    quarterlies = _match(pdfs, ["季度报告"], ["摘要"])

    def _latest(cands: list[pathlib.Path]) -> Optional[pathlib.Path]:
        if not cands:
            return None
        return max(cands, key=lambda p: p.stat().st_mtime)

    annual = _latest(annuals)
    quarterly = _latest(q3s) or _latest(quarterlies)
    selected: dict[str, pathlib.Path] = {}
    if annual:
        selected["annual"] = annual
    if quarterly:
        selected["quarterly"] = quarterly
    return selected


def make_note_md(
    stock: Stock,
    reports: dict[str, pathlib.Path],
    extracts: dict[str, dict[str, list[str]]],
) -> str:
    files_list = (
        "\n".join([f"- {p.name}" for p in reports.values()])
        if reports
        else "- （未下载成功）"
    )

    kw_focus = [
        "主营业务",
        "分产品",
        "分行业",
        "营业收入",
        "毛利率",
        "前五大客户",
        "核心客户",
        "在手订单",
        "风险",
        "不确定",
        "重大风险",
        "海外",
        "出口",
        "关税",
        "制裁",
    ]

    def fmt_snips(section: str) -> str:
        sn = extracts.get(section, {})
        lines: list[str] = []
        for kw in kw_focus:
            if kw not in sn or not sn[kw]:
                continue
            for s in sn[kw]:
                lines.append(f"- 关键词【{kw}】：{s}")
        return (
            "\n".join(lines)
            if lines
            else "- （未从前若干页提取到明显关键词命中；建议在PDF内搜索上述关键词）"
        )

    def summarize_evidence() -> tuple[str, list[str], str]:
        annual = extracts.get("annual", {})
        quarterly = extracts.get("quarterly", {})

        def _has(kw: str) -> bool:
            return bool(annual.get(kw) or quarterly.get(kw))

        evidence_bits: list[str] = []
        if _has("分产品") or _has("分行业"):
            evidence_bits.append("分产品/分行业结构有披露")
        if _has("营业收入") or _has("毛利率"):
            evidence_bits.append("收入/毛利指标有披露")
        if _has("前五大客户") or _has("核心客户"):
            evidence_bits.append("客户信息有披露")
        if _has("在手订单"):
            evidence_bits.append("订单信息有披露")

        if len(evidence_bits) >= 2:
            auth = "偏强（有财报证据支撑）"
        elif len(evidence_bits) == 1:
            auth = "待核验（证据有限）"
        else:
            auth = "偏弱（未见关键证据）"

        risk_hits = []
        for kw in ("重大风险", "风险", "不确定", "海外", "出口", "关税", "制裁"):
            if _has(kw):
                risk_hits.append(kw)
        if risk_hits:
            risk = "已披露风险需核对：" + "、".join(risk_hits)
        else:
            risk = "未见明显风险关键词（需人工复核）"

        return auth, evidence_bits, risk

    auth_level, evidence_bits, risk_summary = summarize_evidence()
    evidence_text = (
        "；".join(evidence_bits) if evidence_bits else "未命中关键证据关键词"
    )

    track = stock.track
    conclusion_text = (
        "【手动补写】请基于财报原文仔细研读后，给出业务真实性判断与关键风险说明。"
    )

    return f"""# 03｜深度去伪：{track}｜{stock.name}（{stock.code}）

> 目标：用财报/公告验证“是否真有业务与收入”，输出基于证据的结论。

---

## A. 已下载财报（本地留档）

保存目录：`投资prompt/test/20260119/step3/financials/{stock.code}_{stock.name}/`

{files_list}

---

## B. 去伪：这家公司相关业务是概念还是实质？

**判定方法（以财报为准）**
- 看“分行业/分产品收入”是否出现对应业务，并能对应到收入与毛利
- 看是否披露客户/订单/量产节奏（而非只有“布局/研发/拟开展”）
- 看现金流与应收：是否出现“收入增长但回款差”的风险

**从财报文本抽取的线索（节选）**
{fmt_snips('annual')}

---

## C. 去全球化与地缘政治风险清单（必须单独过一遍）

| 风险点 | 对公司可能影响 | 我建议的核验办法 |
|------|---------------|------------------|
| 出口/海外收入占比 | 关税/限制可能压缩利润 | 看“境外收入占比”“主要客户地区” |
| 供应链受限 | 关键器件进口受限/成本上升 | 看“供应商集中度”“采购来源” |
| 重大客户集中 | 单一客户变化带来业绩波动 | 看“前五大客户/应收集中度” |

**财报文本抽取线索（节选）**
{fmt_snips('quarterly')}

---

## D. 结论（基于财报证据）

- **业务真实性**：{auth_level}
- **证据摘要**：{evidence_text}
- **最大风险**：{risk_summary}

**结论说明（手动补写）**：{conclusion_text}
"""


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []

    selected_codes: Optional[set[str]] = None
    if len(sys.argv) > 1 and sys.argv[1].strip():
        selected_codes = {c.strip() for c in sys.argv[1].split(",") if c.strip()}

    for stock in STOCKS:
        if selected_codes is not None and stock.code not in selected_codes:
            continue
        print(f"==> {stock.track} {stock.code} {stock.name}")
        stock_dir = REPORTS_DIR / f"{stock.code}_{stock.name}"
        report_paths: dict[str, pathlib.Path] = {}
        extracts: dict[str, dict[str, list[str]]] = {}
        picked = select_existing_reports(stock_dir)
        if not picked:
            failures.append(f"{stock.code} {stock.name}: no local PDFs")
        for kind, pdf_path in picked.items():
            try:
                report_paths[kind] = pdf_path

                text = extract_text(pdf_path, max_pages=40)
                keywords = [
                    "主营业务",
                    "分产品",
                    "分行业",
                    "营业收入",
                    "毛利率",
                    "前五大客户",
                    "核心客户",
                    "在手订单",
                    "风险",
                    "不确定",
                    "重大风险",
                    "海外",
                    "出口",
                    "关税",
                    "制裁",
                ]
                extracts[kind] = extract_snippets(text, keywords)

                # Save extracted text for manual search
                (stock_dir / f"{kind}_extract.txt").write_text(
                    text, encoding="utf-8", errors="ignore"
                )
            except Exception as e:
                failures.append(f"{stock.code} {stock.name} {kind}: {e}")

        # Write per-stock markdown note
        out_md = OUT_DIR / f"03_{stock.track}_{stock.code}_{stock.name}.md"
        out_md.write_text(make_note_md(stock, report_paths, extracts), encoding="utf-8")

    if failures:
        (BASE_DIR / "tools" / "step3_failures.json").write_text(
            json.dumps(failures, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print("\nSome failures occurred; see tools/step3_failures.json")

    print("\nDone")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
