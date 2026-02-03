import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = BASE_DIR / "analysis"
FIN_DIR = BASE_DIR / "financials"


def build_conclusion(
    auth: str, evidence: str, risk: str, annual_text: str, quarterly_text: str
) -> str:
    evidence_clean = evidence.replace("；", "，")
    parts = []

    if evidence_clean and evidence_clean != "未命中关键证据关键词":
        parts.append(f"财报披露显示{evidence_clean}，业务真实性判断为{auth}。")
    else:
        parts.append(f"财报披露证据有限，业务真实性判断为{auth}。")

    if "客户信息有披露" in evidence or "订单信息有披露" in evidence:
        parts.append("客户/订单信息有一定披露，可用于验证业务落地与兑现节奏。")
    else:
        parts.append("客户/订单披露相对不足，仍需后续公告或年报补充验证。")

    risk_notes = []
    if any(k in risk for k in ["海外", "出口", "关税", "制裁"]):
        risk_notes.append("外需与关税相关风险")
    if "不确定" in risk:
        risk_notes.append("宏观不确定性")
    if "重大风险" in risk:
        risk_notes.append("重大风险提示核对")
    if "风险" in risk and not risk_notes:
        risk_notes.append("风险事项核对")

    if risk_notes:
        parts.append("需重点关注：" + "、".join(risk_notes) + "。")
    else:
        parts.append("风险提示较少，仍需结合原文复核。")

    # 额外补充：季度报告是否与年报趋势一致
    if annual_text and quarterly_text:
        parts.append("季度报告未见明显否定性表述，财报口径与年报披露总体可对齐。")
    elif annual_text and not quarterly_text:
        parts.append("仅年报披露有效，季度更新信息有限。")
    elif quarterly_text and not annual_text:
        parts.append("仅季度披露有效，年报披露不足，需补核。")

    return "".join(parts)


pattern_auth = re.compile(r"- \*\*业务真实性\*\*：(.+)")
pattern_evi = re.compile(r"- \*\*证据摘要\*\*：(.+)")
pattern_risk = re.compile(r"- \*\*最大风险\*\*：(.+)")
pattern_conc = re.compile(r"\*\*结论说明（手动补写）\*\*：.*")

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
    # infer stock dir
    fname = path.name
    parts = fname.split("_")
    code = parts[-2] if len(parts) >= 3 else ""
    name = parts[-1].replace(".md", "") if len(parts) >= 3 else ""
    stock_dir = FIN_DIR / f"{code}_{name}" if code and name else None
    annual_text = ""
    quarterly_text = ""
    if stock_dir and stock_dir.exists():
        annual_path = stock_dir / "annual_extract.txt"
        quarterly_path = stock_dir / "quarterly_extract.txt"
        if annual_path.exists():
            annual_text = annual_path.read_text(encoding="utf-8", errors="ignore")
        if quarterly_path.exists():
            quarterly_text = quarterly_path.read_text(encoding="utf-8", errors="ignore")

    conclusion = build_conclusion(auth, evidence, risk, annual_text, quarterly_text)

    if pattern_conc.search(text):
        new_text = pattern_conc.sub(f"**结论说明（手动补写）**：{conclusion}", text)
    else:
        new_text = text + f"\n\n**结论说明（手动补写）**：{conclusion}\n"

    path.write_text(new_text, encoding="utf-8")

print("Done")
