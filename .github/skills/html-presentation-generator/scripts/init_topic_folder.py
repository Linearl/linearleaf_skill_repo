from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class TopicConfig:
    """专题初始化参数。"""

    topic_folder: str
    topic_code: str
    topic_title: str
    part_names: List[str]
    plan_code: str
    source: Path | None
    dry_run: bool


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(
        description="初始化专题目录（输入原稿副本/分镜稿/测试记录/HTML输出）。"
    )
    parser.add_argument(
        "--topic-folder",
        required=True,
        help="专题目录名，例如：4.03主题开发",
    )
    parser.add_argument(
        "--topic-code",
        required=True,
        help="专题编号，例如：03-00（两段两位数字）。",
    )
    parser.add_argument(
        "--topic-title",
        required=True,
        help="专题标题，例如：GitHub Copilot在日常开发中的正确打开方式",
    )
    parser.add_argument(
        "--parts",
        default="基础篇,进阶篇,收官篇",
        help="分镜分段名称，逗号分隔，默认：基础篇,进阶篇,收官篇",
    )
    parser.add_argument(
        "--plan",
        default="方案A",
        help="HTML 方案代号，默认：方案A",
    )
    parser.add_argument(
        "--source",
        default="",
        help="输入原稿路径（可选）。提供后会复制到 00-input。",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅打印将执行的动作，不落盘。",
    )
    return parser.parse_args()


def resolve_workspace_root() -> Path:
    """定位工作区根目录。"""

    return Path(__file__).resolve().parents[4]


def to_config(args: argparse.Namespace) -> TopicConfig:
    """将参数转为配置对象并做基础清洗。"""

    names: List[str] = [item.strip() for item in args.parts.split(",") if item.strip()]
    source_text: str = str(args.source).strip()
    source_path: Path | None = (
        Path(source_text).expanduser().resolve() if source_text else None
    )
    return TopicConfig(
        topic_folder=str(args.topic_folder).strip(),
        topic_code=str(args.topic_code).strip(),
        topic_title=str(args.topic_title).strip(),
        part_names=names,
        plan_code=str(args.plan).strip(),
        source=source_path,
        dry_run=bool(args.dry_run),
    )


def validate_config(config: TopicConfig) -> None:
    """校验配置合法性。"""

    if not re.fullmatch(r"\d{2}-\d{2}", config.topic_code):
        raise ValueError("--topic-code 必须是 NN-NN 格式，例如 02-00")

    if not config.topic_folder:
        raise ValueError("--topic-folder 不能为空")

    if not config.topic_title:
        raise ValueError("--topic-title 不能为空")

    if not config.part_names:
        raise ValueError("--parts 至少要有一个分段名称")

    if config.source is not None and not config.source.exists():
        raise FileNotFoundError(f"输入原稿不存在：{config.source}")


@dataclass(frozen=True)
class TopicPaths:
    """专题路径集合。"""

    topic_dir: Path
    input_dir: Path
    storyboard_dir: Path
    html_dir: Path
    test_dir: Path


def build_paths(config: TopicConfig) -> TopicPaths:
    """根据配置构建专题目录路径。"""

    root: Path = resolve_workspace_root()
    docs_dir: Path = root / "组内分享" / "docs"
    topic_dir: Path = docs_dir / config.topic_folder
    return TopicPaths(
        topic_dir=topic_dir,
        input_dir=topic_dir / "00-input",
        storyboard_dir=topic_dir / "10-storyboards",
        html_dir=topic_dir / "20-html",
        test_dir=topic_dir / "90-tests",
    )


def ensure_dirs(paths: TopicPaths, dry_run: bool) -> None:
    """创建目录结构。"""

    targets: List[Path] = [
        paths.topic_dir,
        paths.input_dir,
        paths.storyboard_dir,
        paths.html_dir,
        paths.test_dir,
    ]
    for target in targets:
        if dry_run:
            print(f"[DRY-RUN] mkdir -p {target}")
            continue
        target.mkdir(parents=True, exist_ok=True)


def write_file_if_missing(path: Path, content: str, dry_run: bool) -> None:
    """仅在文件不存在时写入模板。"""

    if path.exists():
        print(f"[SKIP] 已存在：{path}")
        return

    if dry_run:
        print(f"[DRY-RUN] create {path}")
        return

    path.write_text(content, encoding="utf-8")
    print(f"[CREATE] {path}")


def build_main_doc_name(config: TopicConfig) -> str:
    """生成输入原稿副本文件名。"""

    return f"{config.topic_code}-{config.topic_title}-组内分享.md"


def build_storyboard_name(config: TopicConfig, index: int, part_name: str) -> str:
    """生成分镜稿文件名。"""

    return f"{config.topic_code}-{index:02d}-{part_name}-分镜稿.md"


def build_test_name(config: TopicConfig) -> str:
    """生成测试记录文件名。"""

    current: str = date.today().strftime("%Y%m%d")
    return f"{config.topic_code}-90-技能测试记录_{current}.md"


def build_part_html_name(config: TopicConfig, index: int) -> str:
    """生成分片 HTML 文件名。"""

    return f"{config.topic_code}-{config.plan_code}-part{index}.html"


def build_merged_html_name(config: TopicConfig) -> str:
    """生成合并 HTML 文件名。"""

    return f"{config.topic_code}-{config.plan_code}-合并.html"


def copy_source(config: TopicConfig, paths: TopicPaths) -> None:
    """复制输入原稿到专题目录。"""

    if config.source is None:
        return

    target: Path = paths.input_dir / build_main_doc_name(config)
    if config.source.resolve() == target.resolve():
        print(f"[SKIP] 源文件与目标相同：{target}")
        return

    if target.exists():
        print(f"[SKIP] 原稿副本已存在：{target}")
        return

    if config.dry_run:
        print(f"[DRY-RUN] copy {config.source} -> {target}")
        return

    shutil.copy2(config.source, target)
    print(f"[COPY] {config.source} -> {target}")


def create_storyboard_templates(config: TopicConfig, paths: TopicPaths) -> None:
    """创建分镜稿模板文件。"""

    for idx, part_name in enumerate(config.part_names, start=1):
        file_name: str = build_storyboard_name(config, idx, part_name)
        target: Path = paths.storyboard_dir / file_name
        content: str = (
            f"# {config.topic_code}-{idx:02d}-{part_name} 分镜稿\n\n"
            "## 第1页：\n"
            "- 页面目标：\n"
            "- 页面完整文案：\n"
            "- 演讲备注：\n"
        )
        write_file_if_missing(target, content, config.dry_run)


def create_test_template(config: TopicConfig, paths: TopicPaths) -> None:
    """创建测试记录模板。"""

    target: Path = paths.test_dir / build_test_name(config)
    content: str = (
        f"# {config.topic_code} 专题技能测试记录\n\n"
        "## 校验项\n"
        "- [ ] 分镜稿规则校验通过\n"
        "- [ ] HTML 分片输出完成\n"
        "- [ ] HTML 合并成功\n"
        "- [ ] 页序与关键页检查通过\n"
    )
    write_file_if_missing(target, content, config.dry_run)


def create_html_placeholders(config: TopicConfig, paths: TopicPaths) -> None:
    """创建 HTML 占位文件（仅创建空文件）。"""

    for idx in range(1, len(config.part_names) + 1):
        target: Path = paths.html_dir / build_part_html_name(config, idx)
        write_file_if_missing(target, "", config.dry_run)

    merged: Path = paths.html_dir / build_merged_html_name(config)
    write_file_if_missing(merged, "", config.dry_run)


def print_summary(config: TopicConfig, paths: TopicPaths) -> None:
    """输出初始化摘要。"""

    print("\n=== 专题目录初始化完成 ===")
    print(f"专题目录：{paths.topic_dir}")
    print(f"专题编号：{config.topic_code}")
    print(f"分镜分段：{', '.join(config.part_names)}")
    print(f"HTML 方案：{config.plan_code}")
    print("目录结构：00-input / 10-storyboards / 20-html / 90-tests")


def main() -> None:
    """脚本入口。"""

    args = parse_args()
    config: TopicConfig = to_config(args)
    validate_config(config)

    paths: TopicPaths = build_paths(config)
    ensure_dirs(paths, config.dry_run)
    copy_source(config, paths)
    create_storyboard_templates(config, paths)
    create_test_template(config, paths)
    create_html_placeholders(config, paths)
    print_summary(config, paths)


if __name__ == "__main__":
    main()
