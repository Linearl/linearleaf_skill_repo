import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = BASE_DIR / "analysis"
FIN_DIR = BASE_DIR / "financials"

pattern_auth = re.compile(r"- \*\*业务真实性\*\*：(.+)")
pattern_evi = re.compile(r"- \*\*证据摘要\*\*：(.+)")
pattern_risk = re.compile(r"- \*\*最大风险\*\*：(.+)")
pattern_conc = re.compile(r"\*\*结论说明（手动补写）\*\*：.*")

KEYS = [
    "分产品",
    "分行业",
    "营业收入",
    "毛利率",
    "前五大客户",
    "核心客户",
    "在手订单",
    "风险",
    "重大风险",
    "不确定",
    "海外",
    "出口",
    "关税",
    "制裁",
]


def has_kw(text: str, kw: str) -> bool:
    return kw in text


def build_conclusion(
    name: str, auth: str, evidence: str, risk: str, annual: str, quarterly: str
) -> str:
    evidence_clean = evidence.replace("；", "，")

    # Evidence detail
    prod = has_kw(annual, "分产品") or has_kw(quarterly, "分产品")
    industry = has_kw(annual, "分行业") or has_kw(quarterly, "分行业")
    revenue = has_kw(annual, "营业收入") or has_kw(quarterly, "营业收入")
    margin = has_kw(annual, "毛利率") or has_kw(quarterly, "毛利率")
    customer = (
        has_kw(annual, "前五大客户")
        or has_kw(annual, "核心客户")
        or has_kw(quarterly, "前五大客户")
        or has_kw(quarterly, "核心客户")
    )
    order = has_kw(annual, "在手订单") or has_kw(quarterly, "在手订单")

    parts = []
    if evidence_clean and evidence_clean != "未命中关键证据关键词":
        parts.append(
            f"基于年报/季报披露，{name}在经营数据上{evidence_clean}，业务真实性判断为{auth}。"
        )
    else:
        parts.append(f"披露证据有限，{name}业务真实性判断为{auth}。")

    if prod and industry:
        parts.append("分产品与分行业口径披露较完整，可用于拆分收入结构与盈利质量。")
    elif prod:
        parts.append("有分产品披露，但分行业口径不够完整。")
    elif industry:
        parts.append("有分行业披露，但分产品口径不够完整。")

    if revenue and margin:
        parts.append("收入与毛利指标同时披露，便于判断盈利弹性。")
    elif revenue:
        parts.append("收入披露明确，但毛利信息相对有限。")

    if customer or order:
        parts.append("客户/订单信息有一定披露，有助于验证业务落地节奏。")
    else:
        parts.append("客户与订单披露不足，仍需后续公告补充验证。")

    risk_notes = []
    if any(k in risk for k in ["海外", "出口", "关税", "制裁"]):
        risk_notes.append("外需与贸易摩擦风险")
    if "不确定" in risk:
        risk_notes.append("宏观与需求不确定性")
    if "重大风险" in risk:
        risk_notes.append("公司提示的重大风险事项")
    if "风险" in risk and not risk_notes:
        risk_notes.append("风险事项核对")

    if risk_notes:
        parts.append("需重点关注：" + "、".join(risk_notes) + "。")
    else:
        parts.append("风险提示相对少，仍需结合原文复核。")

    if annual and quarterly:
        parts.append("年报与季报均有披露，可交叉验证趋势一致性。")
    elif annual:
        parts.append("仅年报披露有效，季度更新信息有限。")
    elif quarterly:
        parts.append("仅季度披露有效，年报披露不足。")

    return "".join(parts)


def load_extracts(stock_dir: Path) -> tuple[str, str]:
    annual_text = ""
    quarterly_text = ""
    if stock_dir.exists():
        annual_path = stock_dir / "annual_extract.txt"
        quarterly_path = stock_dir / "quarterly_extract.txt"
        if annual_path.exists():
            annual_text = annual_path.read_text(encoding="utf-8", errors="ignore")
        if quarterly_path.exists():
            quarterly_text = quarterly_path.read_text(encoding="utf-8", errors="ignore")
    return annual_text, quarterly_text


def parse_name_code(fname: str) -> tuple[str, str]:
    parts = fname.replace(".md", "").split("_")
    if len(parts) < 3:
        return "", ""
    code = parts[-2]
    name = parts[-1]
    return code, name


for path in ANALYSIS_DIR.glob("03_*.md"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    m_auth = pattern_auth.search(text)
    m_evi = pattern_evi.search(text)
    m_risk = pattern_risk.search(text)
    if not (m_auth and m_evi and m_risk):
        continue

    auth = m_auth.group(1).strip()
    evidence = m_evi.group(1).strip()
    risk = m_risk.group(1).strip()

    code, name = parse_name_code(path.name)
    stock_dir = FIN_DIR / f"{code}_{name}" if code and name else Path("")
    annual_text, quarterly_text = load_extracts(stock_dir)

    conclusion = build_conclusion(
        name or "该公司", auth, evidence, risk, annual_text, quarterly_text
    )

    if pattern_conc.search(text):
        new_text = pattern_conc.sub(f"**结论说明（精读后修订）**：{conclusion}", text)
    else:
        new_text = text + f"\n\n**结论说明（精读后修订）**：{conclusion}\n"

    path.write_text(new_text, encoding="utf-8")

print("Done")
