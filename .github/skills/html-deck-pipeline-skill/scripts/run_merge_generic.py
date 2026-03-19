"""合并多个 HTML 分片并重排页码（结构鲁棒版）。

特性：
- 通过 HTMLParser 定位 deck 容器，不依赖脆弱的正则切段。
- 提取 deck 的直属 section.slide，避免误抓嵌套内容。
- 自动重写 active、data-index、页码显示与 live region 文案。
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

VERSION_PATTERN: str = r"^v-\d{2}$"
STYLE_BLOCK_PATTERN: str = r"<style\b[^>]*>(.*?)</style>"


@dataclass
class SelectorSpec:
    """容器选择器解析结构。"""

    tag: Optional[str] = None
    element_id: Optional[str] = None
    classes: List[str] = field(default_factory=list)


@dataclass
class ElementNode:
    """HTML 元素位置信息。"""

    tag: str
    attrs: Dict[str, str]
    start: int
    open_end: int
    close_start: Optional[int] = None
    end: Optional[int] = None
    children: List["ElementNode"] = field(default_factory=list)


class HtmlLocator(HTMLParser):
    """记录元素在原文中的绝对偏移。"""

    def __init__(self, html: str) -> None:
        super().__init__(convert_charrefs=False)
        self.html: str = html
        self.line_offsets: List[int] = self._build_line_offsets(html)
        self.roots: List[ElementNode] = []
        self.stack: List[ElementNode] = []

    @staticmethod
    def _build_line_offsets(html: str) -> List[int]:
        offsets: List[int] = [0]
        for line in html.splitlines(keepends=True):
            offsets.append(offsets[-1] + len(line))
        return offsets

    def _absolute_pos(self) -> int:
        line, column = self.getpos()
        return self.line_offsets[line - 1] + column

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        start: int = self._absolute_pos()
        text: str = self.get_starttag_text()
        node = ElementNode(
            tag=tag.lower(),
            attrs={name.lower(): value or "" for name, value in attrs},
            start=start,
            open_end=start + len(text),
        )
        if self.stack:
            self.stack[-1].children.append(node)
        else:
            self.roots.append(node)
        self.stack.append(node)

    def handle_startendtag(
        self, tag: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        start: int = self._absolute_pos()
        text: str = self.get_starttag_text()
        node = ElementNode(
            tag=tag.lower(),
            attrs={name.lower(): value or "" for name, value in attrs},
            start=start,
            open_end=start + len(text),
            close_start=start + len(text),
            end=start + len(text),
        )
        if self.stack:
            self.stack[-1].children.append(node)
        else:
            self.roots.append(node)

    def handle_endtag(self, tag: str) -> None:
        close_start: int = self._absolute_pos()
        tag_name: str = tag.lower()
        match: Optional[re.Match[str]] = re.match(
            rf"</\s*{re.escape(tag_name)}\b[^>]*>",
            self.html[close_start:],
            re.IGNORECASE,
        )
        close_end: int = close_start + len(match.group(0)) if match else close_start

        for index in range(len(self.stack) - 1, -1, -1):
            node = self.stack[index]
            if node.tag == tag_name:
                node.close_start = close_start
                node.end = close_end
                del self.stack[index:]
                return


def parse_selector(selector: str) -> SelectorSpec:
    """解析容器选择器（支持 div.deck/.deck/#id/<div class="deck">）。"""

    cleaned: str = selector.strip()
    if cleaned.startswith("<") and cleaned.endswith(">"):
        cleaned = cleaned[1:-1].strip()

    if 'class="' in cleaned:
        tag: str = cleaned.split()[0].lower()
        class_match = re.search(r'class="([^"]+)"', cleaned)
        id_match = re.search(r'id="([^"]+)"', cleaned)
        return SelectorSpec(
            tag=tag,
            element_id=id_match.group(1) if id_match else None,
            classes=class_match.group(1).split() if class_match else [],
        )

    match = re.match(r"^(?P<tag>[a-zA-Z0-9_-]+)?(?P<rest>.*)$", cleaned)
    tag = match.group("tag").lower() if match and match.group("tag") else None
    rest = match.group("rest") if match else cleaned
    classes = re.findall(r"\.([a-zA-Z0-9_-]+)", rest)
    id_match = re.search(r"#([a-zA-Z0-9_-]+)", rest)

    return SelectorSpec(
        tag=tag, element_id=id_match.group(1) if id_match else None, classes=classes
    )


def matches_selector(node: ElementNode, selector: SelectorSpec) -> bool:
    """判断节点是否匹配选择器。"""

    if selector.tag and node.tag != selector.tag:
        return False
    if selector.element_id and node.attrs.get("id") != selector.element_id:
        return False
    class_tokens: List[str] = node.attrs.get("class", "").split()
    return all(class_name in class_tokens for class_name in selector.classes)


def find_first_match(
    nodes: Sequence[ElementNode], selector: SelectorSpec
) -> Optional[ElementNode]:
    """深度优先查找第一个匹配节点。"""

    for node in nodes:
        if matches_selector(node, selector):
            return node
        child = find_first_match(node.children, selector)
        if child is not None:
            return child
    return None


def direct_slide_nodes(deck_node: ElementNode) -> List[ElementNode]:
    """获取 deck 容器直属 slide。"""

    slides: List[ElementNode] = []
    for child in deck_node.children:
        if child.tag != "section" or child.end is None:
            continue
        class_tokens = child.attrs.get("class", "").split()
        if "slide" in class_tokens:
            slides.append(child)
    return slides


def locate_deck_regions(html: str, selector_text: str) -> Tuple[str, str, str]:
    """返回 deck 前缀、tail、后缀。"""

    parser = HtmlLocator(html)
    parser.feed(html)

    selector = parse_selector(selector_text)
    deck = find_first_match(parser.roots, selector)
    if deck is None or deck.close_start is None or deck.end is None:
        raise ValueError(f"未找到容器选择器：{selector_text}")

    slides = direct_slide_nodes(deck)
    if not slides:
        raise ValueError("未在 deck 容器中找到直属 slide。")

    prefix = html[: deck.open_end] + html[deck.open_end : slides[0].start]
    tail = html[slides[-1].end : deck.close_start]
    suffix = html[deck.close_start :]
    return prefix, tail, suffix


def extract_slides(html: str, selector_text: str) -> List[str]:
    """提取 HTML 的直属 slide 文本。"""

    parser = HtmlLocator(html)
    parser.feed(html)

    selector = parse_selector(selector_text)
    deck = find_first_match(parser.roots, selector)
    if deck is None:
        raise ValueError(f"未找到容器选择器：{selector_text}")

    slides = direct_slide_nodes(deck)
    if not slides:
        raise ValueError("未在容器内提取到任何 slide。")

    return [
        html[item.start : item.end].strip() for item in slides if item.end is not None
    ]


def rewrite_slide_class(slide: str, *, is_active: bool) -> str:
    """重写 class 中 active。"""

    def _replace(match: re.Match[str]) -> str:
        tokens = [token for token in match.group(1).split() if token != "active"]
        if is_active:
            tokens.append("active")
        return f'class="{" ".join(tokens)}"'

    return re.sub(r'class="([^"]+)"', _replace, slide, count=1)


def rewrite_data_index(slide: str, index: int) -> str:
    """重写 data-index。"""

    cleaned = re.sub(r'\sdata-index="\d+"', "", slide, count=1)
    return re.sub(
        r"(<section\b[^>]*?)>", rf'\1 data-index="{index}">', cleaned, count=1
    )


def rewrite_slide_number(slide: str, index: int, total: int, fmt: str) -> str:
    """重写页码显示。"""

    number_text = fmt.format(current=index + 1, total=total)
    updated = re.sub(
        r'(<span class="(?:number|num)">)\s*\d+\s*/\s*\d+\s*(</span>)',
        lambda match: f"{match.group(1)}{number_text}{match.group(2)}",
        slide,
        count=1,
    )
    return updated


def first_page_text(page_format: str, total: int) -> str:
    """返回首页页码文本。"""

    return page_format.format(current=1, total=total)


def normalize_slides(slides: Sequence[str], page_format: str) -> List[str]:
    """统一 active/index/页码。"""

    total = len(slides)
    result: List[str] = []
    for index, slide in enumerate(slides):
        current = rewrite_slide_class(slide, is_active=(index == 0))
        current = rewrite_data_index(current, index)
        current = rewrite_slide_number(current, index, total, page_format)
        result.append(current)
    return result


def update_nav_text(html: str, total: int, page_format: str) -> str:
    """更新合并稿中的 live region 与页码摘要。"""

    first_page = first_page_text(page_format, total)

    updated = re.sub(
        r'(<[^>]+id="liveRegion"[^>]*>)\s*(?:当前)?第\s*\d+\s*页，共\s*\d+\s*页(?:\s*[—-]\s*[^<]+)?\s*(</[^>]+>)',
        rf"\1当前第 1 页，共 {total} 页\2",
        html,
        count=1,
    )
    updated = re.sub(
        r'(<span id="pageNum"[^>]*class="page-num"[^>]*>)[^<]+(</span>)',
        rf"\g<1>{first_page}\g<2>",
        updated,
        count=1,
    )
    updated = re.sub(
        r"const total = \d+;", "const total = slides.length;", updated, count=1
    )
    return updated


def resolve_paths(raw_paths: Sequence[str]) -> List[Path]:
    """解析输入路径。"""

    return [Path(item).expanduser().resolve() for item in raw_paths]


def infer_topic_from_output(output_path: Path) -> str:
    """从输出文件名推断主题名。"""

    stem: str = output_path.stem
    if stem.endswith("-合并"):
        return stem[: -len("-合并")]
    return stem


def infer_version_from_paths(output_path: Path, parts: Sequence[Path]) -> str:
    """从路径层级中推断版本号（如 v-02）。"""

    candidates: List[str] = []
    for path in [output_path] + list(parts):
        candidates.extend(
            item for item in path.parts if re.match(VERSION_PATTERN, item)
        )

    for candidate in candidates:
        if re.match(VERSION_PATTERN, candidate):
            return candidate
    return "v-01"


def normalize_title(
    html: str,
    output_path: Path,
    parts: Sequence[Path],
    title_topic: str,
    title_version: str,
    title_template: str,
) -> str:
    """统一设置文档标题。"""

    topic: str = (
        title_topic.strip()
        if title_topic.strip()
        else infer_topic_from_output(output_path)
    )
    version: str = (
        title_version.strip()
        if title_version.strip()
        else infer_version_from_paths(output_path, parts)
    )
    final_title: str = title_template.format(topic=topic, version=version)

    if re.search(r"<title>.*?</title>", html, re.IGNORECASE | re.DOTALL):
        return re.sub(
            r"<title>.*?</title>",
            f"<title>{final_title}</title>",
            html,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )

    if "</head>" in html:
        return html.replace("</head>", f"  <title>{final_title}</title>\n</head>", 1)

    return f"<title>{final_title}</title>\n" + html


def extract_style_blocks(html: str) -> List[str]:
    """提取 style 块内容。"""

    return [
        item.strip()
        for item in re.findall(STYLE_BLOCK_PATTERN, html, re.IGNORECASE | re.DOTALL)
        if item.strip()
    ]


def merge_style_blocks(template_html: str, part_htmls: Sequence[str]) -> str:
    """将所有分片中的 style 合并注入模板首个 style。"""

    merged_blocks: List[str] = []
    seen: set[str] = set()
    for html in part_htmls:
        for block in extract_style_blocks(html):
            if block in seen:
                continue
            seen.add(block)
            merged_blocks.append(block)

    if not merged_blocks:
        return template_html

    merged_css: str = "\n\n/* --- merged styles from parts --- */\n\n".join(
        merged_blocks
    )

    if re.search(STYLE_BLOCK_PATTERN, template_html, re.IGNORECASE | re.DOTALL):
        return re.sub(
            STYLE_BLOCK_PATTERN,
            lambda match: f"<style>\n{merged_css}\n</style>",
            template_html,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )

    if "</head>" in template_html:
        return template_html.replace(
            "</head>", f"<style>\n{merged_css}\n</style>\n</head>", 1
        )

    return f"<style>\n{merged_css}\n</style>\n" + template_html


def part_sort_key(path: Path) -> Tuple[int, str]:
    """按前缀编号排序（01-开头.html）。"""

    match = re.match(r"^(\d{2})-", path.stem)
    if match:
        return int(match.group(1)), path.name.lower()

    part_match = re.search(r"part(\d{2})", path.stem, re.IGNORECASE)
    if part_match:
        return int(part_match.group(1)), path.name.lower()

    return 9999, path.name.lower()


def merge_html(
    parts: Sequence[Path],
    output_path: Path,
    container_selector: str,
    page_format: str,
    title_topic: str,
    title_version: str,
    title_template: str,
) -> int:
    """执行合并并返回总页数。"""

    part_htmls: List[str] = [part.read_text(encoding="utf-8") for part in parts]
    template_html = merge_style_blocks(part_htmls[0], part_htmls)
    prefix, tail, suffix = locate_deck_regions(template_html, container_selector)

    all_slides: List[str] = []
    for part_html in part_htmls:
        all_slides.extend(extract_slides(part_html, container_selector))

    normalized = normalize_slides(all_slides, page_format)
    total = len(normalized)
    merged = f"{prefix}\n{'\n\n'.join(normalized)}\n{tail}{suffix.lstrip()}"
    merged = update_nav_text(merged, total, page_format)
    merged = normalize_title(
        html=merged,
        output_path=output_path,
        parts=parts,
        title_topic=title_topic,
        title_version=title_version,
        title_template=title_template,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(merged, encoding="utf-8")
    return total


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(
        description="合并 2 个或以上 HTML 分片并重排页码。"
    )
    parser.add_argument(
        "--parts", nargs="+", required=True, help="输入分片 HTML 文件。"
    )
    parser.add_argument("--output", required=True, help="合并输出 HTML 文件。")
    parser.add_argument(
        "--container-selector",
        default="div.deck",
        help="容器选择器（默认 div.deck）。",
    )
    parser.add_argument(
        "--page-format",
        default="{current:02d} / {total:02d}",
        help="页码格式（默认 {current:02d} / {total:02d}）。",
    )
    parser.add_argument(
        "--title-topic",
        default="",
        help="可选：标题中的主题名（为空则从输出文件名推断）。",
    )
    parser.add_argument(
        "--title-version",
        default="",
        help="可选：标题中的版本号（为空则从路径推断，如 v-02）。",
    )
    parser.add_argument(
        "--title-template",
        default="{topic}-合并({version})",
        help="标题模板，默认 {topic}-合并({version})。",
    )
    return parser.parse_args()


def main() -> None:
    """脚本入口。"""

    args = parse_args()
    part_paths = sorted(resolve_paths(args.parts), key=part_sort_key)

    if len(part_paths) < 2:
        raise ValueError("--parts 至少需要 2 个 HTML 文件。")

    missing = [path for path in part_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "以下分片文件不存在：\n" + "\n".join(str(item) for item in missing)
        )

    output_path = Path(args.output).expanduser().resolve()
    total = merge_html(
        parts=part_paths,
        output_path=output_path,
        container_selector=args.container_selector,
        page_format=args.page_format,
        title_topic=args.title_topic,
        title_version=args.title_version,
        title_template=args.title_template,
    )

    print(f"合并完成：{output_path}")
    print(f"总页数：{total} 页（来源分片：{len(part_paths)} 个）")


if __name__ == "__main__":
    main()
