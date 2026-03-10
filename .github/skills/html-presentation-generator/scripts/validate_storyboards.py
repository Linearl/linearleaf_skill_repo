from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

FORBIDDEN_PATTERNS: List[str] = [
    r"（轻）",
    r"（重）",
    r"这一页不做什么",
    r"页内主题：",
]

REQUIRED_PATTERNS: List[Tuple[str, str]] = [
    ("页眉主题字段", r"页眉主题："),
    ("演讲备注", r"### 演讲备注"),
    ("过渡句", r"过渡句："),
    ("附录A", r"## 附录A：页码映射表（分镜页 -> HTML data-index）"),
    ("附录B", r"## 附录B：分镜质量检查清单"),
]


def check_file(path: Path) -> Dict[str, List[str]]:
    """校验单个分镜稿文件并返回问题列表。"""

    text: str = path.read_text(encoding="utf-8")
    issues: List[str] = []

    for p in FORBIDDEN_PATTERNS:
        if re.search(p, text):
            issues.append(f"命中禁用模式: {p}")

    for label, p in REQUIRED_PATTERNS:
        if not re.search(p, text):
            issues.append(f"缺少必需内容: {label}")

    if "行动页" in text and "口播版三步法" not in text:
        issues.append("含行动页但缺少口播版三步法")

    return {"file": [str(path)], "issues": issues}


def main() -> None:
    """执行目录内三份分镜稿校验并输出结果。"""

    workspace: Path = Path(__file__).resolve().parents[4]
    docs_dir: Path = workspace / "组内分享" / "docs"
    files: List[Path] = sorted(docs_dir.glob("01-00-0*-*分镜稿.md"))

    if not files:
        raise FileNotFoundError(f"未找到分镜稿文件: {docs_dir}")

    total_issues: int = 0
    for file_path in files:
        result = check_file(file_path)
        issues = result["issues"]
        if issues:
            total_issues += len(issues)
            print(f"[FAIL] {file_path}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"[PASS] {file_path}")

    if total_issues > 0:
        raise SystemExit(1)

    print("ALL_PASS")


if __name__ == "__main__":
    main()
