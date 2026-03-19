"""提取 HTML 讲稿中各页标题，用于快速校验页序。

从合并后的 HTML 文件中提取所有 slide 的 data-index 与标题文本，
输出为表格或 JSON 格式，便于与分镜稿进行页序对照。

用法：
    python scripts/extract_slide_titles.py \
        --input merged.html \
        [--format table|json]

说明：
    从 V1 PowerShell 脚本重写为 Python，统一技术栈。
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import List, Tuple


def extract_titles(html: str) -> List[Tuple[int, str]]:
    """提取每个 slide 的 data-index 和标题。"""

    # data-index 从 section 标签提取
    slide_pattern: re.Pattern[str] = re.compile(
        r'<section\b[^>]*data-index="(\d+)"[^>]*>(.*?)</section>',
        re.DOTALL,
    )

    # 标题从 slide-header 中的 h2 或 eyebrow/title 提取
    title_patterns: List[re.Pattern[str]] = [
        re.compile(r"<h2[^>]*>(.*?)</h2>", re.DOTALL),
        re.compile(r'<div[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</div>', re.DOTALL),
        re.compile(r'<span[^>]*class="[^"]*eyebrow[^"]*"[^>]*>(.*?)</span>', re.DOTALL),
    ]

    results: List[Tuple[int, str]] = []
    for match in slide_pattern.finditer(html):
        data_index: int = int(match.group(1))
        section_content: str = match.group(2)

        title: str = "(无标题)"
        for pattern in title_patterns:
            title_match: re.Match[str] | None = pattern.search(section_content)
            if title_match:
                raw_title: str = title_match.group(1)
                clean_title: str = re.sub(r"<[^>]+>", "", raw_title).strip()
                if clean_title:
                    title = clean_title
                    break

        results.append((data_index, title))

    results.sort(key=lambda x: x[0])
    return results


def format_table(titles: List[Tuple[int, str]]) -> str:
    """格式化为表格文本。"""

    lines: List[str] = [
        f"{'data-index':>10}  {'标题'}",
        f"{'─' * 10}  {'─' * 40}",
    ]
    for idx, title in titles:
        lines.append(f"{idx:>10}  {title}")

    lines.append(f"\n总页数: {len(titles)}")
    return "\n".join(lines)


def format_json(titles: List[Tuple[int, str]]) -> str:
    """格式化为 JSON。"""

    data: List[dict[str, int | str]] = [
        {"data_index": idx, "title": title} for idx, title in titles
    ]
    return json.dumps(data, ensure_ascii=False, indent=2)


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(description="提取 HTML 讲稿中各页标题。")
    parser.add_argument(
        "--input",
        required=True,
        help="输入 HTML 文件路径。",
    )
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="输出格式（默认 table）。",
    )
    return parser.parse_args()


def main() -> None:
    """脚本入口。"""

    args = parse_args()
    input_path: Path = Path(args.input).expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")

    html: str = input_path.read_text(encoding="utf-8")
    titles: List[Tuple[int, str]] = extract_titles(html)

    if not titles:
        print("未提取到任何 slide。请检查 HTML 结构是否包含 data-index 属性。")
        raise SystemExit(1)

    if args.format == "json":
        print(format_json(titles))
    else:
        print(format_table(titles))

    # data-index 连续性检查
    indices: List[int] = [idx for idx, _ in titles]
    expected: List[int] = list(range(len(titles)))
    if indices != expected:
        print(f"\n⚠️ 警告: data-index 不连续！实际: {indices}, 期望: {expected}")


if __name__ == "__main__":
    main()
