#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码指标收集工具 (Agent Skills 版本)

用于自动收集 Python 项目的基础代码指标，支持多种输出格式

使用方法:
    python code-metrics-collector.py --project-path /path/to/project
    python code-metrics-collector.py --project-path /path/to/project --output metrics.json
    python code-metrics-collector.py --project-path /path/to/project --format markdown

输出格式:
    - json: 结构化 JSON 数据 (默认)
    - markdown: Markdown 格式的报告
    - summary: 简洁的控制台摘要
"""

import os
import ast
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class FileMetrics:
    """单个文件的指标"""

    file_path: str
    lines_of_code: int
    blank_lines: int
    comment_lines: int
    function_count: int
    class_count: int
    import_count: int
    max_complexity: int
    avg_complexity: float
    long_functions: List[str]  # 超过50行的函数名


@dataclass
class ProjectMetrics:
    """项目整体指标"""

    project_path: str
    analysis_time: str
    total_files: int
    python_files: int
    total_lines: int
    code_lines: int
    blank_lines: int
    comment_lines: int
    total_functions: int
    total_classes: int
    total_imports: int
    avg_file_length: float
    max_file_length: int
    complexity_distribution: Dict[str, int]
    quality_score: float  # 0-100 的质量评分
    issues: List[Dict[str, Any]]  # 发现的问题


class ComplexityAnalyzer(ast.NodeVisitor):
    """计算圈复杂度的AST访问器"""

    def __init__(self):
        self.complexity = 1  # 基础复杂度为1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        # and/or 操作增加复杂度
        self.complexity += len(node.values) - 1
        self.generic_visit(node)


class CodeMetricsCollector:
    """代码指标收集器"""

    def __init__(self, verbose: bool = False):
        self.logger = self._setup_logger(verbose)
        self.issues = []

    def _setup_logger(self, verbose: bool) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def analyze_file(self, file_path: Path) -> Optional[FileMetrics]:
        """分析单个Python文件"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            lines = content.split("\n")
            total_lines = len(lines)

            # 统计代码行、空行、注释行
            code_lines = 0
            blank_lines = 0
            comment_lines = 0

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    blank_lines += 1
                elif stripped.startswith("#"):
                    comment_lines += 1
                else:
                    code_lines += 1

            # 解析AST
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                self.logger.warning(f"语法错误 {file_path}: {e}")
                self.issues.append(
                    {
                        "type": "syntax_error",
                        "file": str(file_path),
                        "message": str(e),
                        "severity": "high",
                    }
                )
                return None

            # 统计函数、类、导入
            function_count = 0
            class_count = 0
            import_count = 0
            complexities = []
            long_functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_count += 1
                    # 计算函数复杂度
                    analyzer = ComplexityAnalyzer()
                    analyzer.visit(node)
                    complexities.append(analyzer.complexity)

                    # 检查函数长度
                    func_lines = (
                        node.end_lineno - node.lineno
                        if hasattr(node, "end_lineno")
                        else 0
                    )
                    if func_lines > 50:
                        long_functions.append(node.name)
                        self.issues.append(
                            {
                                "type": "long_function",
                                "file": str(file_path),
                                "function": node.name,
                                "lines": func_lines,
                                "severity": "medium",
                            }
                        )

                    # 检查高复杂度
                    if analyzer.complexity > 10:
                        self.issues.append(
                            {
                                "type": "high_complexity",
                                "file": str(file_path),
                                "function": node.name,
                                "complexity": analyzer.complexity,
                                "severity": (
                                    "medium" if analyzer.complexity <= 20 else "high"
                                ),
                            }
                        )

                elif isinstance(node, ast.ClassDef):
                    class_count += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_count += 1

            # 检查文件过长
            if total_lines > 500:
                self.issues.append(
                    {
                        "type": "long_file",
                        "file": str(file_path),
                        "lines": total_lines,
                        "severity": "low",
                    }
                )

            # 计算复杂度统计
            max_complexity = max(complexities) if complexities else 0
            avg_complexity = (
                sum(complexities) / len(complexities) if complexities else 0
            )

            return FileMetrics(
                file_path=str(file_path),
                lines_of_code=code_lines,
                blank_lines=blank_lines,
                comment_lines=comment_lines,
                function_count=function_count,
                class_count=class_count,
                import_count=import_count,
                max_complexity=max_complexity,
                avg_complexity=round(avg_complexity, 2),
                long_functions=long_functions,
            )

        except Exception as e:
            self.logger.error(f"分析文件失败 {file_path}: {e}")
            return None

    def collect_project_metrics(
        self, project_path: Path, exclude_patterns: List[str] = None
    ) -> ProjectMetrics:
        """收集项目级别的指标"""
        python_files = []
        exclude_patterns = exclude_patterns or [
            ".venv",
            "__pycache__",
            ".git",
            "node_modules",
        ]

        # 查找所有Python文件
        for py_file in project_path.rglob("*.py"):
            # 排除特定目录
            if not any(pattern in str(py_file) for pattern in exclude_patterns):
                python_files.append(py_file)

        self.logger.info(f"找到 {len(python_files)} 个Python文件")

        # 分析每个文件
        file_metrics = []
        for py_file in python_files:
            metrics = self.analyze_file(py_file)
            if metrics:
                file_metrics.append(metrics)

        # 计算项目级别指标
        total_files = len(file_metrics)
        total_lines = sum(
            m.lines_of_code + m.blank_lines + m.comment_lines for m in file_metrics
        )
        code_lines = sum(m.lines_of_code for m in file_metrics)
        blank_lines = sum(m.blank_lines for m in file_metrics)
        comment_lines = sum(m.comment_lines for m in file_metrics)
        total_functions = sum(m.function_count for m in file_metrics)
        total_classes = sum(m.class_count for m in file_metrics)
        total_imports = sum(m.import_count for m in file_metrics)

        # 计算平均值
        avg_file_length = total_lines / total_files if total_files > 0 else 0
        max_file_length = (
            max(
                (m.lines_of_code + m.blank_lines + m.comment_lines)
                for m in file_metrics
            )
            if file_metrics
            else 0
        )

        # 复杂度分布
        all_complexities = [
            m.max_complexity for m in file_metrics if m.max_complexity > 0
        ]

        complexity_distribution = {
            "low": sum(1 for c in all_complexities if 1 <= c <= 10),
            "medium": sum(1 for c in all_complexities if 11 <= c <= 20),
            "high": sum(1 for c in all_complexities if 21 <= c <= 50),
            "very_high": sum(1 for c in all_complexities if c > 50),
        }

        # 计算质量评分 (简化版)
        quality_score = self._calculate_quality_score(
            code_lines, comment_lines, complexity_distribution, total_functions
        )

        return ProjectMetrics(
            project_path=str(project_path),
            analysis_time=datetime.now().isoformat(),
            total_files=total_files,
            python_files=len(python_files),
            total_lines=total_lines,
            code_lines=code_lines,
            blank_lines=blank_lines,
            comment_lines=comment_lines,
            total_functions=total_functions,
            total_classes=total_classes,
            total_imports=total_imports,
            avg_file_length=round(avg_file_length, 2),
            max_file_length=max_file_length,
            complexity_distribution=complexity_distribution,
            quality_score=quality_score,
            issues=self.issues,
        )

    def _calculate_quality_score(
        self,
        code_lines: int,
        comment_lines: int,
        complexity_dist: Dict[str, int],
        total_functions: int,
    ) -> float:
        """计算代码质量评分 (0-100)"""
        score = 100.0

        # 注释覆盖率评分 (目标 > 15%)
        comment_ratio = comment_lines / code_lines if code_lines > 0 else 0
        if comment_ratio < 0.10:
            score -= 15
        elif comment_ratio < 0.15:
            score -= 5

        # 复杂度评分
        if total_functions > 0:
            high_complexity_ratio = (
                complexity_dist.get("high", 0) + complexity_dist.get("very_high", 0)
            ) / total_functions
            if high_complexity_ratio > 0.2:
                score -= 20
            elif high_complexity_ratio > 0.1:
                score -= 10

        # 问题数量扣分
        high_issues = sum(1 for i in self.issues if i.get("severity") == "high")
        medium_issues = sum(1 for i in self.issues if i.get("severity") == "medium")
        score -= high_issues * 5
        score -= medium_issues * 2

        return max(0, min(100, round(score, 1)))

    def save_json(self, metrics: ProjectMetrics, output_path: Path):
        """保存指标到JSON文件"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(asdict(metrics), f, indent=2, ensure_ascii=False)
        self.logger.info(f"JSON指标已保存到: {output_path}")

    def save_markdown(self, metrics: ProjectMetrics, output_path: Path):
        """保存指标到Markdown文件"""
        md_content = self._generate_markdown_report(metrics)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        self.logger.info(f"Markdown报告已保存到: {output_path}")

    def _generate_markdown_report(self, metrics: ProjectMetrics) -> str:
        """生成Markdown格式的报告"""
        quality_emoji = (
            "🟢"
            if metrics.quality_score >= 80
            else "🟡" if metrics.quality_score >= 60 else "🔴"
        )

        report = f"""# 代码指标分析报告

> 生成时间: {metrics.analysis_time}  
> 项目路径: `{metrics.project_path}`

## 📊 整体评估

| 指标 | 数值 | 说明 |
|------|------|------|
| **质量评分** | {quality_emoji} {metrics.quality_score}/100 | 综合质量评分 |
| Python文件数 | {metrics.python_files} | 分析的文件数量 |
| 总代码行数 | {metrics.code_lines} | 不含空行和注释 |
| 函数数量 | {metrics.total_functions} | - |
| 类数量 | {metrics.total_classes} | - |

## 📈 代码统计

| 指标 | 数值 |
|------|------|
| 总行数 | {metrics.total_lines} |
| 代码行 | {metrics.code_lines} |
| 注释行 | {metrics.comment_lines} |
| 空白行 | {metrics.blank_lines} |
| 平均文件长度 | {metrics.avg_file_length} 行 |
| 最大文件长度 | {metrics.max_file_length} 行 |

## 🔍 复杂度分布

| 复杂度等级 | 函数数量 | 说明 |
|------------|----------|------|
| 🟢 低 (1-10) | {metrics.complexity_distribution['low']} | 良好 |
| 🟡 中 (11-20) | {metrics.complexity_distribution['medium']} | 可接受 |
| 🟠 高 (21-50) | {metrics.complexity_distribution['high']} | 需要关注 |
| 🔴 极高 (>50) | {metrics.complexity_distribution['very_high']} | 需要重构 |

## ⚠️ 发现的问题

"""
        if metrics.issues:
            report += "| 严重度 | 类型 | 文件 | 详情 |\n"
            report += "|--------|------|------|------|\n"
            for issue in metrics.issues[:20]:  # 最多显示20个
                severity_emoji = (
                    "🔴"
                    if issue["severity"] == "high"
                    else "🟡" if issue["severity"] == "medium" else "🟢"
                )
                detail = (
                    issue.get("function", "")
                    or issue.get("message", "")
                    or f"{issue.get('lines', '')} 行"
                )
                report += f"| {severity_emoji} {issue['severity']} | {issue['type']} | `{Path(issue['file']).name}` | {detail} |\n"

            if len(metrics.issues) > 20:
                report += f"\n*还有 {len(metrics.issues) - 20} 个问题未显示...*\n"
        else:
            report += "✅ 未发现明显问题\n"

        report += f"""
---

*由 analysis_code skill 的 code-metrics-collector 工具生成*
"""
        return report

    def print_summary(self, metrics: ProjectMetrics):
        """打印控制台摘要"""
        quality_indicator = (
            "🟢"
            if metrics.quality_score >= 80
            else "🟡" if metrics.quality_score >= 60 else "🔴"
        )

        print(f"\n{'='*50}")
        print(f"📊 代码分析摘要")
        print(f"{'='*50}")
        print(f"项目路径: {metrics.project_path}")
        print(f"分析时间: {metrics.analysis_time}")
        print(f"质量评分: {quality_indicator} {metrics.quality_score}/100")
        print(f"{'='*50}")
        print(f"Python文件: {metrics.python_files}")
        print(f"代码行数: {metrics.code_lines}")
        print(f"函数数量: {metrics.total_functions}")
        print(f"类数量: {metrics.total_classes}")
        print(f"平均文件长度: {metrics.avg_file_length} 行")
        print(f"{'='*50}")
        print(f"复杂度分布:")
        print(f"  🟢 低: {metrics.complexity_distribution['low']}")
        print(f"  🟡 中: {metrics.complexity_distribution['medium']}")
        print(f"  🟠 高: {metrics.complexity_distribution['high']}")
        print(f"  🔴 极高: {metrics.complexity_distribution['very_high']}")
        print(f"{'='*50}")

        if metrics.issues:
            high_count = sum(1 for i in metrics.issues if i["severity"] == "high")
            medium_count = sum(1 for i in metrics.issues if i["severity"] == "medium")
            low_count = sum(1 for i in metrics.issues if i["severity"] == "low")
            print(f"发现问题: 🔴高{high_count} 🟡中{medium_count} 🟢低{low_count}")
        else:
            print("发现问题: ✅ 无")
        print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Python项目代码指标收集工具 (Agent Skills 版本)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --project-path ./my_project
  %(prog)s --project-path ./my_project --output metrics.json
  %(prog)s --project-path ./my_project --format markdown --output report.md
        """,
    )
    parser.add_argument(
        "--project-path", "-p", type=str, required=True, help="项目根目录路径"
    )
    parser.add_argument("--output", "-o", type=str, default=None, help="输出文件路径")
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        choices=["json", "markdown", "summary"],
        default="summary",
        help="输出格式 (默认: summary)",
    )
    parser.add_argument(
        "--exclude",
        "-e",
        type=str,
        nargs="*",
        default=[".venv", "__pycache__", ".git", "node_modules"],
        help="排除的目录模式",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细日志")

    args = parser.parse_args()

    # 验证项目路径
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"❌ 错误: 项目路径不存在: {project_path}")
        return 1

    if not project_path.is_dir():
        print(f"❌ 错误: 项目路径不是目录: {project_path}")
        return 1

    # 收集指标
    collector = CodeMetricsCollector(verbose=args.verbose)
    metrics = collector.collect_project_metrics(project_path, args.exclude)

    # 输出结果
    if args.format == "json":
        output_path = Path(args.output) if args.output else Path("metrics.json")
        collector.save_json(metrics, output_path)
        collector.print_summary(metrics)
    elif args.format == "markdown":
        output_path = Path(args.output) if args.output else Path("analysis_report.md")
        collector.save_markdown(metrics, output_path)
        collector.print_summary(metrics)
    else:  # summary
        collector.print_summary(metrics)
        if args.output:
            collector.save_json(metrics, Path(args.output))

    return 0


if __name__ == "__main__":
    exit(main())
