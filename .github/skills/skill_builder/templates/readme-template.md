# README 模板 | README Template

此模板用于创建 Agent Skill 的 README.md 文件。

---

## 模板内容 | Template Content

```markdown
# [技能名称] | [Skill Name]

<p align="center">
  <strong>[技能图标] [技能简短描述] | [Short Description]</strong>
</p>

## 📖 概述 | Overview

[技能的详细说明，比 SKILL.md 中的 Overview 更详细]

### 背景 | Background

[为什么需要这个技能？解决什么问题？]

### 设计理念 | Design Philosophy

[技能的设计原则和理念]

## 🎯 适用场景 | Use Cases

| 场景 | 说明 |
|------|------|
| [场景1] | [说明] |
| [场景2] | [说明] |
| [场景3] | [说明] |

## 🔧 核心功能 | Core Features

### 1. [功能1名称]

[功能说明]

### 2. [功能2名称]

[功能说明]

### 3. [功能3名称]

[功能说明]

## 📂 目录结构 | Directory Structure

\`\`\`
[skill_name]/
├── SKILL.md                     # 主技能定义
├── README.md                    # 本文档
├── templates/
│   ├── [template-1].md          # [模板1说明]
│   └── [template-2].md          # [模板2说明]
├── tools/                       # (如有)
│   └── [tool].py                # [工具说明]
└── examples/
    └── README.md                # 使用示例
\`\`\`

## 🚀 快速开始 | Quick Start

### 基本使用 | Basic Usage

\`\`\`markdown
@copilot [触发技能的示例请求]
\`\`\`

### 高级使用 | Advanced Usage

\`\`\`markdown
@copilot [更复杂的请求示例]

[额外参数或上下文]
\`\`\`

## 📋 工作流程 | Workflow

\`\`\`mermaid
graph LR
    A[步骤1] --> B[步骤2]
    B --> C[步骤3]
    C --> D[步骤4]
\`\`\`

### 阶段说明 | Phase Details

| 阶段 | 描述 | 输出 |
|------|------|------|
| [阶段1] | [描述] | [输出] |
| [阶段2] | [描述] | [输出] |

## 🔗 相关技能 | Related Skills

- `[skill_1]` - [关系说明]
- `[skill_2]` - [关系说明]

## 📚 参考资源 | References

- [资源1](链接)
- [资源2](链接)

## 📜 更新日志 | Changelog

### v[版本号]
- [更新内容1]
- [更新内容2]
```

---

## 使用说明 | Usage Instructions

### README vs SKILL.md

| 内容 | SKILL.md | README.md |
|------|----------|-----------|
| 主要目的 | AI 加载和执行 | 人类阅读理解 |
| 详细程度 | 精确指令 | 背景说明 |
| 格式要求 | 严格结构化 | 灵活友好 |
| 必须性 | 必需 | 推荐 |

### 最佳实践 | Best Practices

1. **开头使用居中的标题和描述** - 视觉吸引
2. **使用 emoji 分类章节** - 提高可读性
3. **包含目录结构图** - 帮助理解组织
4. **提供快速开始示例** - 降低使用门槛
5. **包含更新日志** - 跟踪变化
