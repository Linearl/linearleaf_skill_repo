"""HTML 合并稿质量门禁校验脚本。

用于在阶段 D.2 对合并后的 HTML 进行自动化门禁检查，重点覆盖：
1) 标题格式一致性（{主题}-合并(v-XX)）
2) 页序连续性与 active 唯一性
3) 单页信息密度与总体信息量
4) 重复骨架过多（模板化回归）
5) 与标杆文件的信息密度/信息量对齐
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

SLIDE_PATTERN: str = r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>.*?</section>'
OPEN_SECTION_PATTERN: str = r"<section\b([^>]*)>"
DATA_INDEX_PATTERN: str = r'data-index="(\d+)"'
ACTIVE_CLASS_PATTERN: str = r'class="[^"]*\bslide\b[^"]*\bactive\b[^"]*"'
TITLE_PATTERN_DEFAULT: str = r'.+-合并\(v-\d{2}\)$'

BLOCK_TAGS: Sequence[str] = (
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "li",
    "tr",
    "blockquote",
    "pre",
    "dd",
    "dt",
    "td",
    "th",
)

LAYOUT_CLASS_PREFIXES: Sequence[str] = (
    "layout-",
    "mode-",
    "view-",
    "template-",
    "skeleton-",
)

LAYOUT_CLASS_KEYWORDS: Sequence[str] = (
    "grid",
    "matrix",
    "timeline",
    "compare",
    "flow",
    "cards",
    "kpi",
    "dashboard",
)

IGNORED_SECTION_CLASSES: Sequence[str] = (
    "slide",
    "active",
)

PAGE_TYPE_RULES: Dict[str, Tuple[str, ...]] = {
    "compare": ("对比", "比较", "差异", "vs", "A/B"),
    "process": ("流程", "步骤", "路径", "方法", "闭环"),
    "action": ("行动", "执行", "清单", "下一步", "落地"),
}

FORBIDDEN_VISIBLE_TEXTS: Sequence[str] = (
    "页面模式类型",
    "背景呈现策略",
    "界面元素布局",
    "示例锚点",
    "执行约束",
    "中间章节组织模式",
    "演讲备注",
    "过渡句",
)


@dataclass
class Issue:
    """单条校验问题。"""

    level: str
    message: str


@dataclass
class DeckMetrics:
    """HTML 关键指标。"""

    title: str
    slide_count: int
    active_count: int
    data_index_values: List[int]
    total_text_chars: int
    total_block_count: int
    avg_text_chars_per_slide: float
    avg_blocks_per_slide: float
    max_consecutive_same_layout: int
    dominant_layout_ratio: float
    layout_signatures: List[str]
    layout_frequencies: Dict[str, int]
    repeated_layout_runs: List[Tuple[int, int, int, str]]
    page_type_counts: Dict[str, int]


@dataclass
class ValidationResult:
    """门禁结果。"""

    issues: List[Issue] = field(default_factory=list)
    metrics: Optional[DeckMetrics] = None
    benchmark_metrics: Optional[DeckMetrics] = None

    @property
    def has_errors(self) -> bool:
        return any(item.level == "ERROR" for item in self.issues)

    def add(self, level: str, message: str) -> None:
        self.issues.append(Issue(level=level, message=message))


def extract_title(html: str) -> str:
    """提取文档标题。"""

    match: Optional[re.Match[str]] = re.search(
        r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL
    )
    if match is None:
        return ""
    return match.group(1).strip()


def extract_slides(html: str) -> List[str]:
    """提取所有 slide section。"""

    return re.findall(SLIDE_PATTERN, html, re.IGNORECASE | re.DOTALL)


def strip_tags(text: str) -> str:
    """去掉 HTML 标签并规整空白。"""

    no_script: str = re.sub(
        r"<script\b[^>]*>.*?</script>", " ", text, flags=re.IGNORECASE | re.DOTALL
    )
    no_style: str = re.sub(
        r"<style\b[^>]*>.*?</style>", " ", no_script, flags=re.IGNORECASE | re.DOTALL
    )
    no_tag: str = re.sub(r"<[^>]+>", " ", no_style)
    normalized: str = re.sub(r"\s+", " ", no_tag)
    return normalized.strip()


def count_information_blocks(slide_html: str) -> int:
    """统计单页信息块数量。"""

    block_count: int = 0
    for tag in BLOCK_TAGS:
        pattern: str = rf"<{tag}\b[^>]*>(.*?)</{tag}>"
        for matched in re.findall(pattern, slide_html, re.IGNORECASE | re.DOTALL):
            content: str = strip_tags(matched)
            if content:
                block_count += 1

    return block_count


def parse_section_classes(slide_html: str) -> List[str]:
    """解析 section 的 class tokens。"""

    open_tag_match: Optional[re.Match[str]] = re.search(
        OPEN_SECTION_PATTERN,
        slide_html,
        re.IGNORECASE,
    )
    if open_tag_match is None:
        return []

    open_attrs: str = open_tag_match.group(1)
    class_match: Optional[re.Match[str]] = re.search(
        r'class="([^"]+)"',
        open_attrs,
        re.IGNORECASE,
    )
    if class_match is None:
        return []

    return [token.strip() for token in class_match.group(1).split() if token.strip()]


def infer_layout_signature(slide_html: str) -> str:
    """推断页面骨架签名，用于检测连续重复模板。"""

    classes: List[str] = parse_section_classes(slide_html)
    layout_tokens: List[str] = []

    for token in classes:
        lowered: str = token.lower()
        if lowered in IGNORED_SECTION_CLASSES or lowered.startswith("bg-"):
            continue
        if any(lowered.startswith(prefix) for prefix in LAYOUT_CLASS_PREFIXES):
            layout_tokens.append(lowered)
            continue
        if any(keyword in lowered for keyword in LAYOUT_CLASS_KEYWORDS):
            layout_tokens.append(lowered)

    if layout_tokens:
        return "class:" + "+".join(sorted(set(layout_tokens)))

    inner_tags: List[str] = re.findall(
        r"<(h1|h2|h3|p|ul|ol|table|div|article|aside|blockquote|pre)\b",
        slide_html,
        re.IGNORECASE,
    )
    if not inner_tags:
        return "tags:none"

    limited: List[str] = [tag.lower() for tag in inner_tags[:6]]
    return "tags:" + "-".join(limited)


def classify_page_types(slide_html: str) -> Dict[str, int]:
    """识别页面类型命中（对比/流程/行动）。"""

    text: str = strip_tags(slide_html).lower()
    counters: Dict[str, int] = {"compare": 0, "process": 0, "action": 0}

    for page_type, keywords in PAGE_TYPE_RULES.items():
        if any(keyword.lower() in text for keyword in keywords):
            counters[page_type] = 1

    return counters


def extract_data_indexes(slides: Sequence[str]) -> List[int]:
    """提取 data-index 数组。"""

    indexes: List[int] = []
    for slide in slides:
        match: Optional[re.Match[str]] = re.search(DATA_INDEX_PATTERN, slide)
        if match is not None:
            indexes.append(int(match.group(1)))
    return indexes


def max_consecutive_repeat(values: Sequence[str]) -> int:
    """返回最大连续重复长度。"""

    if not values:
        return 0

    max_run: int = 1
    current_run: int = 1
    previous: str = values[0]

    for value in values[1:]:
        if value == previous:
            current_run += 1
        else:
            max_run = max(max_run, current_run)
            current_run = 1
            previous = value
    max_run = max(max_run, current_run)
    return max_run


def dominant_ratio(values: Sequence[str]) -> float:
    """返回最常见骨架占比。"""

    if not values:
        return 0.0

    freq: Dict[str, int] = {}
    for value in values:
        freq[value] = freq.get(value, 0) + 1

    top: int = max(freq.values())
    return top / len(values)


def layout_frequencies(values: Sequence[str]) -> Dict[str, int]:
    """统计各骨架签名频次。"""

    freq: Dict[str, int] = {}
    for value in values:
        freq[value] = freq.get(value, 0) + 1
    return freq


def collect_repeated_layout_runs(values: Sequence[str]) -> List[Tuple[int, int, int, str]]:
    """收集连续重复骨架区间（start, end, length, signature）。"""

    if not values:
        return []

    runs: List[Tuple[int, int, int, str]] = []
    start: int = 0

    while start < len(values):
        end: int = start
        while end + 1 < len(values) and values[end + 1] == values[start]:
            end += 1

        run_length: int = end - start + 1
        if run_length >= 2:
            runs.append((start, end, run_length, values[start]))

        start = end + 1

    return runs


def analyze_html(html: str) -> DeckMetrics:
    """提取整份 HTML 指标。"""

    slides: List[str] = extract_slides(html)
    title: str = extract_title(html)
    active_count: int = len(re.findall(ACTIVE_CLASS_PATTERN, html, re.IGNORECASE))
    data_indexes: List[int] = extract_data_indexes(slides)

    total_chars: int = 0
    total_blocks: int = 0
    layout_signatures: List[str] = []
    page_type_counts: Dict[str, int] = {"compare": 0, "process": 0, "action": 0}

    for slide in slides:
        text: str = strip_tags(slide)
        total_chars += len(text)
        total_blocks += count_information_blocks(slide)
        layout_signatures.append(infer_layout_signature(slide))

        classified: Dict[str, int] = classify_page_types(slide)
        for key in page_type_counts:
            page_type_counts[key] += classified[key]

    slide_count: int = len(slides)
    avg_chars: float = (total_chars / slide_count) if slide_count else 0.0
    avg_blocks: float = (total_blocks / slide_count) if slide_count else 0.0
    signature_freq: Dict[str, int] = layout_frequencies(layout_signatures)
    repeated_runs: List[Tuple[int, int, int, str]] = collect_repeated_layout_runs(
        layout_signatures
    )

    return DeckMetrics(
        title=title,
        slide_count=slide_count,
        active_count=active_count,
        data_index_values=data_indexes,
        total_text_chars=total_chars,
        total_block_count=total_blocks,
        avg_text_chars_per_slide=avg_chars,
        avg_blocks_per_slide=avg_blocks,
        max_consecutive_same_layout=max_consecutive_repeat(layout_signatures),
        dominant_layout_ratio=dominant_ratio(layout_signatures),
        layout_signatures=layout_signatures,
        layout_frequencies=signature_freq,
        repeated_layout_runs=repeated_runs,
        page_type_counts=page_type_counts,
    )


def check_data_index_continuity(metrics: DeckMetrics, result: ValidationResult) -> None:
    """检查 data-index 从 0 连续递增。"""

    if metrics.slide_count == 0:
        result.add("ERROR", "未找到任何 slide 页面。")
        return

    indexes: List[int] = metrics.data_index_values
    if len(indexes) != metrics.slide_count:
        result.add(
            "ERROR",
            f"data-index 数量({len(indexes)})与 slide 数量({metrics.slide_count})不一致。",
        )
        return

    expected: List[int] = list(range(metrics.slide_count))
    if indexes != expected:
        result.add(
            "ERROR",
            f"data-index 不连续或顺序错误，期望 {expected[:8]}...，实际 {indexes[:8]}...",
        )


def compare_with_benchmark(
    metrics: DeckMetrics,
    benchmark: DeckMetrics,
    min_density_ratio: float,
    min_info_ratio: float,
    result: ValidationResult,
) -> None:
    """对齐标杆文件密度与信息量。"""

    if benchmark.avg_blocks_per_slide <= 0:
        result.add("WARN", "标杆文件平均信息块为 0，已跳过密度对齐检查。")
    else:
        density_ratio: float = metrics.avg_blocks_per_slide / benchmark.avg_blocks_per_slide
        if density_ratio < min_density_ratio:
            result.add(
                "ERROR",
                (
                    "信息密度未达到标杆："
                    f"当前={metrics.avg_blocks_per_slide:.2f}，"
                    f"标杆={benchmark.avg_blocks_per_slide:.2f}，"
                    f"比例={density_ratio:.3f} < 阈值={min_density_ratio:.3f}"
                ),
            )

    if benchmark.total_text_chars <= 0:
        result.add("WARN", "标杆文件文本信息量为 0，已跳过信息量对齐检查。")
    else:
        info_ratio: float = metrics.total_text_chars / benchmark.total_text_chars
        if info_ratio < min_info_ratio:
            result.add(
                "ERROR",
                (
                    "总体信息量未达到标杆："
                    f"当前={metrics.total_text_chars} chars，"
                    f"标杆={benchmark.total_text_chars} chars，"
                    f"比例={info_ratio:.3f} < 阈值={min_info_ratio:.3f}"
                ),
            )


def run_validation(
    html_path: Path,
    title_pattern: str,
    min_avg_blocks: float,
    max_consecutive_layout: int,
    max_dominant_layout_ratio: float,
    benchmark_html: Optional[Path],
    benchmark_density_ratio: float,
    benchmark_info_ratio: float,
) -> ValidationResult:
    """执行门禁校验。"""

    content: str = html_path.read_text(encoding="utf-8")
    metrics: DeckMetrics = analyze_html(content)
    visible_text: str = strip_tags(content)

    result = ValidationResult(metrics=metrics)

    if not metrics.title:
        result.add("ERROR", "缺少 <title> 或 title 为空。")
    elif re.fullmatch(title_pattern, metrics.title) is None:
        result.add(
            "ERROR",
            f"标题不符合格式要求，当前='{metrics.title}'，期望正则='{title_pattern}'",
        )

    if metrics.active_count != 1:
        result.add("ERROR", f"active slide 数量必须为 1，当前为 {metrics.active_count}。")

    check_data_index_continuity(metrics, result)

    if metrics.avg_blocks_per_slide < min_avg_blocks:
        result.add(
            "ERROR",
            (
                "单页信息密度过低："
                f"平均信息块={metrics.avg_blocks_per_slide:.2f} < 阈值={min_avg_blocks:.2f}"
            ),
        )

    if metrics.max_consecutive_same_layout > max_consecutive_layout:
        result.add(
            "ERROR",
            (
                "重复骨架过多："
                f"最大连续同骨架页数={metrics.max_consecutive_same_layout} > 阈值={max_consecutive_layout}"
            ),
        )

    if metrics.dominant_layout_ratio > max_dominant_layout_ratio:
        result.add(
            "ERROR",
            (
                "模板集中度过高："
                f"主导骨架占比={metrics.dominant_layout_ratio:.3f} > 阈值={max_dominant_layout_ratio:.3f}"
            ),
        )

    for forbidden_text in FORBIDDEN_VISIBLE_TEXTS:
        if forbidden_text in visible_text:
            result.add(
                "ERROR",
                f"检测到流程元信息泄露到可见文本：'{forbidden_text}'",
            )

    if metrics.page_type_counts["compare"] < 1:
        result.add("ERROR", "缺少对比页（compare）。")
    if metrics.page_type_counts["process"] < 1:
        result.add("ERROR", "缺少流程页（process）。")
    if metrics.page_type_counts["action"] < 1:
        result.add("ERROR", "缺少行动页（action）。")

    if benchmark_html is not None:
        benchmark_content: str = benchmark_html.read_text(encoding="utf-8")
        benchmark_metrics: DeckMetrics = analyze_html(benchmark_content)
        result.benchmark_metrics = benchmark_metrics
        compare_with_benchmark(
            metrics=metrics,
            benchmark=benchmark_metrics,
            min_density_ratio=benchmark_density_ratio,
            min_info_ratio=benchmark_info_ratio,
            result=result,
        )

    return result


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(description="HTML 合并稿质量门禁校验脚本")
    parser.add_argument("--input", required=True, help="合并后的 HTML 文件路径")
    parser.add_argument(
        "--title-pattern",
        default=TITLE_PATTERN_DEFAULT,
        help="标题正则，默认要求：{主题}-合并(v-XX)",
    )
    parser.add_argument(
        "--min-average-blocks",
        type=float,
        default=2.0,
        help="平均每页最少信息块数量（平衡档默认 2.0）",
    )
    parser.add_argument(
        "--max-consecutive-same-layout",
        type=int,
        default=2,
        help="允许连续复用同一骨架的最大页数",
    )
    parser.add_argument(
        "--max-dominant-layout-ratio",
        type=float,
        default=0.45,
        help="单一骨架在全稿中的最大占比",
    )
    parser.add_argument(
        "--benchmark-html",
        default="",
        help="标杆 HTML 文件路径（可选）",
    )
    parser.add_argument(
        "--benchmark-density-ratio",
        type=float,
        default=1.0,
        help="相对标杆平均信息块的最低比例",
    )
    parser.add_argument(
        "--benchmark-info-ratio",
        type=float,
        default=1.0,
        help="相对标杆总体文本信息量的最低比例",
    )
    parser.add_argument(
        "--report-json",
        default="",
        help="可选：输出 JSON 报告路径",
    )
    return parser.parse_args()


def metrics_to_dict(metrics: DeckMetrics) -> Dict[str, object]:
    """将指标对象转换为 JSON 可序列化结构。"""

    return {
        "title": metrics.title,
        "slide_count": metrics.slide_count,
        "active_count": metrics.active_count,
        "data_index_values": metrics.data_index_values,
        "total_text_chars": metrics.total_text_chars,
        "total_block_count": metrics.total_block_count,
        "avg_text_chars_per_slide": round(metrics.avg_text_chars_per_slide, 4),
        "avg_blocks_per_slide": round(metrics.avg_blocks_per_slide, 4),
        "max_consecutive_same_layout": metrics.max_consecutive_same_layout,
        "dominant_layout_ratio": round(metrics.dominant_layout_ratio, 4),
        "layout_frequencies": metrics.layout_frequencies,
        "repeated_layout_runs": [
            {
                "start": start,
                "end": end,
                "length": length,
                "signature": signature,
            }
            for start, end, length, signature in metrics.repeated_layout_runs
        ],
        "page_type_counts": metrics.page_type_counts,
    }


def main() -> None:
    """脚本入口。"""

    args = parse_args()
    html_path: Path = Path(args.input).expanduser().resolve()
    if not html_path.exists():
        raise FileNotFoundError(f"输入文件不存在: {html_path}")

    benchmark_path: Optional[Path] = None
    if args.benchmark_html:
        benchmark_path = Path(args.benchmark_html).expanduser().resolve()
        if not benchmark_path.exists():
            raise FileNotFoundError(f"标杆文件不存在: {benchmark_path}")

    result: ValidationResult = run_validation(
        html_path=html_path,
        title_pattern=args.title_pattern,
        min_avg_blocks=args.min_average_blocks,
        max_consecutive_layout=args.max_consecutive_same_layout,
        max_dominant_layout_ratio=args.max_dominant_layout_ratio,
        benchmark_html=benchmark_path,
        benchmark_density_ratio=args.benchmark_density_ratio,
        benchmark_info_ratio=args.benchmark_info_ratio,
    )

    if result.metrics is None:
        raise RuntimeError("门禁执行失败：未生成指标。")

    print(f"校验文件: {html_path}")
    print("\n[核心指标]")
    print(f"- 标题: {result.metrics.title}")
    print(f"- slide 数量: {result.metrics.slide_count}")
    print(f"- active 数量: {result.metrics.active_count}")
    print(f"- 平均信息块/页: {result.metrics.avg_blocks_per_slide:.2f}")
    print(f"- 平均文本字符/页: {result.metrics.avg_text_chars_per_slide:.1f}")
    print(f"- 总体文本字符: {result.metrics.total_text_chars}")
    print(f"- 最大连续同骨架页数: {result.metrics.max_consecutive_same_layout}")
    print(f"- 主导骨架占比: {result.metrics.dominant_layout_ratio:.3f}")
    print(
        "- 页面类型计数: "
        f"compare={result.metrics.page_type_counts['compare']}, "
        f"process={result.metrics.page_type_counts['process']}, "
        f"action={result.metrics.page_type_counts['action']}"
    )

    if result.metrics.layout_frequencies:
        print("- Top 骨架频次:")
        top_signatures: List[Tuple[str, int]] = sorted(
            result.metrics.layout_frequencies.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:3]
        for signature, count in top_signatures:
            print(f"  · {count} 页: {signature}")

    repeated_runs: List[Tuple[int, int, int, str]] = [
        item for item in result.metrics.repeated_layout_runs if item[2] >= 3
    ]
    if repeated_runs:
        print("- 连续重复区间(长度≥3):")
        for start, end, length, signature in repeated_runs:
            print(f"  · index {start}-{end} (len={length}): {signature}")

    if result.benchmark_metrics is not None:
        print("\n[标杆对齐]")
        print(f"- 标杆文件标题: {result.benchmark_metrics.title}")
        print(
            "- 标杆平均信息块/页: "
            f"{result.benchmark_metrics.avg_blocks_per_slide:.2f}"
        )
        print(
            "- 标杆总体文本字符: "
            f"{result.benchmark_metrics.total_text_chars}"
        )

    if result.issues:
        print(f"\n发现 {len(result.issues)} 个问题:")
        for issue in result.issues:
            prefix: str = "❌" if issue.level == "ERROR" else "⚠️"
            print(f"  {prefix} [{issue.level}] {issue.message}")

    report_json: Dict[str, object] = {
        "input": str(html_path),
        "metrics": metrics_to_dict(result.metrics),
        "issues": [
            {"level": item.level, "message": item.message} for item in result.issues
        ],
    }

    if result.benchmark_metrics is not None:
        report_json["benchmark"] = {
            "path": str(benchmark_path),
            "metrics": metrics_to_dict(result.benchmark_metrics),
        }

    if args.report_json:
        report_path: Path = Path(args.report_json).expanduser().resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(report_json, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\n已写入报告: {report_path}")

    if result.has_errors:
        print("\n❌ HTML 门禁失败。")
        raise SystemExit(1)

    print("\n✅ HTML 门禁通过。")


if __name__ == "__main__":
    main()
