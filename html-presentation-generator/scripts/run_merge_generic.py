from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Sequence, Tuple


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(
        description="合并 3 个或以上 HTML 分片并重排页码。"
    )
    parser.add_argument(
        "--parts",
        nargs="+",
        required=True,
        help="输入分片 HTML 路径，至少 3 个。",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="合并后的输出 HTML 路径。",
    )
    return parser.parse_args()


def split_template(html: str) -> Tuple[str, str, str]:
    """把模板 HTML 分割为 deck 前缀、deck 区域与后缀。"""

    deck_start: int = html.find('<div class="deck">')
    if deck_start < 0:
        raise ValueError('未找到 <div class="deck">。')

    deck_open_end: int = html.find(">", deck_start)
    if deck_open_end < 0:
        raise ValueError("deck 开始标签不完整。")

    deck_close_match: re.Match[str] | None = re.search(
        r"</div>\s*(?:<!--.*?-->\s*)?<script>",
        html[deck_open_end + 1 :],
        re.DOTALL,
    )
    if deck_close_match is None:
        raise ValueError("未找到 deck 结束标签。")

    deck_close_start: int = deck_open_end + 1 + deck_close_match.start()
    prefix: str = html[: deck_open_end + 1]
    deck_region: str = html[deck_open_end + 1 : deck_close_start]
    suffix: str = html[deck_close_start:]
    return prefix, deck_region, suffix


def extract_slides(deck_region: str) -> List[str]:
    """从 deck 区域提取所有 slide section。"""

    pattern: re.Pattern[str] = re.compile(
        r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>.*?</section>',
        re.DOTALL,
    )
    slides: List[str] = [
        match.group(0).strip() for match in pattern.finditer(deck_region)
    ]
    if not slides:
        raise ValueError("未在 deck 区域中提取到任何 slide。")
    return slides


def rewrite_slide_class(slide: str, is_active: bool) -> str:
    """清理旧 active 标记，并按需设置新的 active。"""

    def replace_class(match: re.Match[str]) -> str:
        tokens: List[str] = [
            token for token in match.group(1).split() if token != "active"
        ]
        if is_active:
            tokens.append("active")
        return f'class="{" ".join(tokens)}"'

    return re.sub(r'class="([^"]+)"', replace_class, slide, count=1)


def rewrite_data_index(slide: str, index: int) -> str:
    """重写 section 的 data-index。"""

    cleaned: str = re.sub(r'\sdata-index="\d+"', "", slide, count=1)
    return re.sub(
        r"(<section\b[^>]*?)>", rf'\1 data-index="{index}">', cleaned, count=1
    )


def rewrite_slide_number(slide: str, index: int, total: int) -> str:
    """重写 slide-header 中的静态页码。"""

    number_text: str = f"{index + 1:02d} / {total:02d}"

    def replace_number(match: re.Match[str]) -> str:
        return f"{match.group(1)}{number_text}{match.group(2)}"

    return re.sub(
        r'(<span class="number">)\s*\d+\s*/\s*\d+\s*(</span>)',
        replace_number,
        slide,
        count=1,
    )


def normalize_slides(slides: Sequence[str]) -> List[str]:
    """标准化 slides 的 active、data-index 与页码。"""

    total: int = len(slides)
    normalized: List[str] = []
    for idx, slide in enumerate(slides):
        current: str = rewrite_slide_class(slide, is_active=(idx == 0))
        current = rewrite_data_index(current, idx)
        current = rewrite_slide_number(current, idx, total)
        normalized.append(current)
    return normalized


def update_nav_hint(html: str, total: int) -> str:
    """更新底部总页数文案。"""

    updated: str = re.sub(r"共\s*\d+\s*页", f"共 {total} 页", html, count=1)
    updated = re.sub(
        r"const total = slides\.length;",
        f"const total = {total};",
        updated,
        count=1,
    )
    return updated


def resolve_paths(raw_paths: Sequence[str]) -> List[Path]:
    """把命令行传入路径解析为绝对路径。"""

    return [Path(item).expanduser().resolve() for item in raw_paths]


def merge_html(parts: Sequence[Path], output_path: Path) -> int:
    """执行分片合并并返回总页数。"""

    template_html: str = parts[0].read_text(encoding="utf-8")
    prefix, _, suffix = split_template(template_html)

    all_slides: List[str] = []
    for part in parts:
        html: str = part.read_text(encoding="utf-8")
        _, deck_region, _ = split_template(html)
        all_slides.extend(extract_slides(deck_region))

    normalized_slides: List[str] = normalize_slides(all_slides)
    total: int = len(normalized_slides)
    slides_text: str = "\n\n".join(normalized_slides)
    merged_html: str = f"{prefix}\n{slides_text}\n{suffix.lstrip()}"
    merged_html = update_nav_hint(merged_html, total)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(merged_html, encoding="utf-8")
    return total


def main() -> None:
    """脚本入口。"""

    args = parse_args()
    part_paths: List[Path] = resolve_paths(args.parts)
    if len(part_paths) < 3:
        raise ValueError("--parts 至少需要 3 个 HTML 文件。")

    missing: List[Path] = [path for path in part_paths if not path.exists()]
    if missing:
        missing_text: str = "\n".join(str(path) for path in missing)
        raise FileNotFoundError(f"以下分片文件不存在：\n{missing_text}")

    output_path: Path = Path(args.output).expanduser().resolve()
    total: int = merge_html(part_paths, output_path)
    print(f"合并完成：{output_path}")
    print(f"总页数：{total} 页（来源分片：{len(part_paths)} 个）")


if __name__ == "__main__":
    main()
