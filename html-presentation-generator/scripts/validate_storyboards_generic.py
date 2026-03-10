from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from validate_storyboards import check_file


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(description="按 glob 规则校验一组分镜稿文件。")
    parser.add_argument(
        "--root",
        default="组内分享/docs",
        help="glob 的根目录（默认：组内分享/docs，相对工作区）。",
    )
    parser.add_argument(
        "--glob",
        default="01-00-0*-*分镜稿.md",
        help="在 root 目录下匹配分镜稿的 glob 规则。",
    )
    return parser.parse_args()


def resolve_workspace_root() -> Path:
    """定位工作区根目录。"""

    return Path(__file__).resolve().parents[4]


def resolve_root_dir(raw_root: str) -> Path:
    """解析 root 参数，支持相对工作区和绝对路径。"""

    candidate: Path = Path(raw_root).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    workspace: Path = resolve_workspace_root()
    return (workspace / candidate).resolve()


def main() -> None:
    """执行通用分镜稿校验并输出结果。"""

    args = parse_args()
    root_dir: Path = resolve_root_dir(args.root)
    files: List[Path] = sorted(root_dir.glob(args.glob))

    if not files:
        raise FileNotFoundError(f"未找到分镜稿文件：{root_dir} -> {args.glob}")

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
