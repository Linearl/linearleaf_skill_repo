# Debug Code Skill

> 🌍 **语言版本**: [English](#english) | [中文](#中文)

---

## 中文

### 📋 概述

这是一个基于 VS Code Agent Skills 标准的代码调试技能，将原有的 `debug-system` 工作流重构为符合 [agentskills.io](https://agentskills.io/) 规范的可复用技能包。

### 🎯 功能特点

- **系统化调试**: 采用6步调试循环（计划→分析→修正→执行→检查→记录）
- **多轮迭代**: 支持复杂问题的多轮渐进式调试
- **人工确认**: 关键节点暂停等待用户确认
- **Bug管理**: 集成Bug追踪和状态管理
- **经验沉淀**: 记录调试过程和经验教训

### 📁 目录结构

```
debug_code/
├── SKILL.md              # 技能定义文件（Agent Skills 标准）
├── README.md             # 本说明文档
├── templates/            # 调试模板
│   ├── debug-round-record.md  # 调试轮次记录
│   ├── bug-detail.md          # Bug详细报告
│   ├── bug-list.md            # Bug清单管理
│   ├── debug-summary.md       # 调试总结
│   ├── lessons-learned.md     # 经验教训
│   └── task-index.md          # 任务索引
└── examples/             # 使用示例
    └── README.md         # 示例说明
```

### 🚀 使用方法

#### 1. 启用 Agent Skills

确保在 VS Code 设置中启用了 Agent Skills：
```json
{
  "chat.useAgentSkills": true
}
```

#### 2. 触发调试

在 Copilot Chat 中使用自然语言描述问题：

```
我的程序报错 TypeError，帮我调试一下
```

```
这个函数运行结果不对，需要排查问题
```

```
数据库连接失败，帮我找出原因
```

### 📊 调试流程

```
6步调试循环:

📋 计划 ──→ 🔍 分析 ──→ 💡 修正
   ↑                        ↓
   │                        ↓
📊 记录 ←── ✅ 检查 ←── ⚙️ 执行
   │
   ↓
🎯 下轮目标 ← 暂停点（需用户确认）
```

### 🔑 关键暂停点

1. **步骤3**: 确认问题信息后暂停
2. **6.6记录**: 规划下轮目标后暂停
3. **步骤7**: 完成决策前暂停

### 🔗 与原 debug-system 的关系

| 对比项 | debug-system | debug_code skill |
|--------|--------------|------------------|
| 标准 | 自定义工作流格式 | Agent Skills 开放标准 |
| 加载方式 | 手动引用模板 | Copilot 按需自动加载 |
| 可移植性 | VS Code 内使用 | 跨 AI 工具使用 |
| 位置 | `debug-system/` | `.github/skills/debug_code/` |

---

## English

### 📋 Overview

This is a code debugging skill based on the VS Code Agent Skills standard, refactoring the original `debug-system` workflow into a reusable skill package compliant with [agentskills.io](https://agentskills.io/) specification.

### 🎯 Features

- **Systematic Debugging**: 6-step debug cycle (Plan→Analyze→Design→Execute→Verify→Document)
- **Multi-round Iteration**: Support progressive debugging for complex issues
- **Human Confirmation**: Pause at key points for user confirmation
- **Bug Management**: Integrated bug tracking and status management
- **Experience Capture**: Record debugging process and lessons learned

### 📁 Directory Structure

```
debug_code/
├── SKILL.md              # Skill definition (Agent Skills standard)
├── README.md             # This documentation
├── templates/            # Debug templates
└── examples/             # Usage examples
```

### 🚀 Usage

#### 1. Enable Agent Skills

Enable in VS Code settings:
```json
{
  "chat.useAgentSkills": true
}
```

#### 2. Trigger Debugging

Use natural language in Copilot Chat:

```
My program throws a TypeError, help me debug
```

```
This function returns wrong results, need to investigate
```

### 📊 Debug Flow

```
6-step Debug Cycle:

📋 Plan ──→ 🔍 Analyze ──→ 💡 Design
   ↑                          ↓
   │                          ↓
📊 Document ←── ✅ Verify ←── ⚙️ Execute
```

---

## 📚 相关资源 | Related Resources

- [Agent Skills 标准](https://agentskills.io/)
- [VS Code Agent Skills 文档](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [原 debug-system 文档](../../../debug-system/README.md)

---

*版本: 1.0.0 | 基于 Copilot 工作流系统 debug-system*
