from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Tuple


def resolve_paths() -> Tuple[Path, Path]:
    """解析并返回工作区根目录与合并脚本路径。"""

    skill_dir: Path = Path(__file__).resolve().parent
    workspace_root: Path = skill_dir.parents[4]
    merge_script: Path = workspace_root / "组内分享" / "merge_scheme_c_parts.py"
    return workspace_root, merge_script


def main() -> None:
    """运行项目合并脚本并打印结果。"""

    workspace_root, merge_script = resolve_paths()
    if not merge_script.exists():
        raise FileNotFoundError(f"未找到合并脚本：{merge_script}")

    result = subprocess.run(
        ["python", str(merge_script)],
        cwd=str(workspace_root),
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    print(result.stdout.strip())


if __name__ == "__main__":
    main()
