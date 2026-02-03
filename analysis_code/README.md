# Analysis Code Skill

> 🌍 **语言版本**: [English](#english) | [中文](#中文)

---

## 中文

### 📋 概述

这是一个基于 VS Code Agent Skills 标准的代码分析技能，将原有的 `analysis_system` 工作流重构为符合 [agentskills.io](https://agentskills.io/) 规范的可复用技能包。

### 🎯 功能特点

- **系统化分析**: 采用"总-分-总"结构化分析方法
- **多维度评估**: 支持代码质量、技术债务、性能、架构等多个维度
- **自动化工具**: 包含代码指标收集器等自动化工具
- **模板驱动**: 提供完整的分析报告模板
- **可扩展**: 支持自定义分析维度和输出格式

### 📁 目录结构

```
analysis_code/
├── SKILL.md              # 技能定义文件（Agent Skills 标准）
├── README.md             # 本说明文档
├── templates/            # 分析模板
│   ├── master-analysis-plan.md    # 总体分析计划
│   ├── round-plan.md              # 轮次分析计划
│   ├── round-analysis-report.md   # 轮次分析报告
│   ├── final-analysis-report.md   # 最终分析报告
│   ├── executive-summary.md       # 执行摘要
│   └── lessons-learned.md         # 经验总结
├── tools/                # 分析工具
│   ├── code-metrics-collector.py  # 代码指标收集器
│   └── README.md                  # 工具说明
└── examples/             # 使用示例
    ├── README.md                  # 示例说明
    └── sample-analysis-task.md    # 示例分析任务
```

### 🚀 使用方法

#### 1. 启用 Agent Skills

确保在 VS Code 设置中启用了 Agent Skills：
```json
{
  "chat.useAgentSkills": true
}
```

#### 2. 触发分析

在 Copilot Chat 中使用自然语言请求代码分析：

```
帮我分析这个项目的代码质量
```

```
我需要对 src/core 模块进行技术债务评估
```

```
准备重构前，帮我评估一下这个模块的风险
```

#### 3. 手动使用工具

```powershell
# 收集代码指标
python tools/code-metrics-collector.py --project-path "项目路径"

# 生成 Markdown 报告
python tools/code-metrics-collector.py -p "项目路径" -f markdown -o report.md
```

### 📊 分析流程

```
阶段一：总体规划（总）
├── 需求解析
├── 信息确认 ← 暂停点
├── 创建分析计划
└── 初始化环境

阶段二：循环分析（分）← 可多轮迭代
├── 创建轮次目录
├── 制定轮次计划
├── 收集项目数据
├── 执行分析
├── 量化评估
├── 记录结果
├── 生成建议
└── 轮次评估 ← 暂停点（决策下一步）

阶段三：汇总报告（总）
├── 评估完成度
├── 生成最终报告
└── 归档
```

### 🔗 与原 analysis_system 的关系

本技能是对原 `analysis_system` 工作流的重构：

| 对比项 | analysis_system | analysis_code skill |
|--------|----------------|---------------------|
| 标准 | 自定义工作流格式 | Agent Skills 开放标准 |
| 加载方式 | 手动引用模板 | Copilot 按需自动加载 |
| 可移植性 | VS Code 内使用 | 跨 AI 工具使用 |
| 位置 | `analysis_system/` | `.github/skills/analysis_code/` |

原 `analysis_system` 仍然保留，可供需要更详细控制的场景使用。

---

## English

### 📋 Overview

This is a code analysis skill based on the VS Code Agent Skills standard, refactoring the original `analysis_system` workflow into a reusable skill package compliant with [agentskills.io](https://agentskills.io/) specification.

### 🎯 Features

- **Systematic Analysis**: Uses "Plan-Execute-Summarize" structured approach
- **Multi-dimensional Assessment**: Supports code quality, technical debt, performance, architecture dimensions
- **Automated Tools**: Includes code metrics collector and other automation tools
- **Template-driven**: Provides complete analysis report templates
- **Extensible**: Supports custom analysis dimensions and output formats

### 📁 Directory Structure

```
analysis_code/
├── SKILL.md              # Skill definition (Agent Skills standard)
├── README.md             # This documentation
├── templates/            # Analysis templates
├── tools/                # Analysis tools
└── examples/             # Usage examples
```

### 🚀 Usage

#### 1. Enable Agent Skills

Enable Agent Skills in VS Code settings:
```json
{
  "chat.useAgentSkills": true
}
```

#### 2. Trigger Analysis

Use natural language in Copilot Chat:

```
Analyze the code quality of this project
```

```
I need a technical debt assessment for the src/core module
```

#### 3. Manual Tool Usage

```powershell
# Collect code metrics
python tools/code-metrics-collector.py --project-path "project_path"

# Generate Markdown report
python tools/code-metrics-collector.py -p "project_path" -f markdown -o report.md
```

---

## 📚 相关资源 | Related Resources

- [Agent Skills 标准](https://agentskills.io/)
- [VS Code Agent Skills 文档](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [原 analysis_system 文档](../../../analysis_system/README.md)

---

*版本: 1.0.0 | 基于 Copilot 工作流系统 analysis_system*
