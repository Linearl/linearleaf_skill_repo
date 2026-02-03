# Copilot Agent Skills

> 🌍 **语言版本**: [English](#english) | [中文](#中文)

---

## 中文

### 📋 概述

本目录包含符合 [Agent Skills 开放标准](https://agentskills.io/) 的技能包，用于增强 GitHub Copilot 的专业能力。

### 🎯 什么是 Agent Skills？

Agent Skills 是一种开放标准，允许你创建可被 AI 代理（如 GitHub Copilot）按需加载的专业能力包。与自定义指令不同，技能可以包含：

- 📝 详细的操作指令
- 📜 脚本和工具
- 📚 示例和模板
- 📁 相关资源文件

### 📁 可用技能

| 技能 | 说明 | 状态 |
|------|------|------|
| [analysis_code](analysis_code/) | 系统化代码分析技能 | ✅ 可用 |
| [debug_code](debug_code/) | 系统化代码调试技能 | ✅ 可用 |
| [refactor_code](refactor_code/) | 系统化代码重构技能 | ✅ 可用 |
| [file_organize](file_organize/) | 系统化文件整理技能 | ✅ 可用 |
| [version_compare](version_compare/) | 系统化版本对比技能 | ✅ 可用 |
| [skill_builder](skill_builder/) | 🏗️ **元技能** - 用于创建 Agent Skills 的技能 | ✅ 可用 |

### 🚀 使用方法

#### 1. 启用 Agent Skills

在 VS Code 设置中启用：

```json
{
  "chat.useAgentSkills": true
}
```

#### 2. 自动触发

技能会根据你的请求自动加载。例如：

- 请求"代码分析"时 → 自动加载 `analysis_code` 技能
- 请求"调试"、"错误修复"时 → 自动加载 `debug_code` 技能
- 请求"重构"、"架构改进"时 → 自动加载 `refactor_code` 技能
- 请求"文件整理"、"目录清理"时 → 自动加载 `file_organize` 技能
- 请求"版本对比"、"变更分析"、"更新日志"时 → 自动加载 `version_compare` 技能
- 请求"创建技能"、"设计技能"、"转换为技能"时 → 自动加载 `skill_builder` 技能

#### 3. 三级加载机制

Agent Skills 使用渐进式加载：

1. **Level 1 - 技能发现**: Copilot 始终知道有哪些技能可用
2. **Level 2 - 指令加载**: 匹配请求时加载 SKILL.md 的指令
3. **Level 3 - 资源访问**: 按需访问技能目录中的其他文件

### 🔄 与原工作流系统的关系

本 Skills 目录是对原 Copilot 工作流系统的 Agent Skills 标准化重构：

| 原工作流 | 对应技能 | 说明 |
|----------|----------|------|
| analysis_system | analysis_code | ✅ 代码分析技能 |
| debug-system | debug_code | ✅ 调试技能 |
| refactor_system | refactor_code | ✅ 重构技能 |
| file-organize-system | file_organize | ✅ 文件整理技能 |
| version-comparison-system | version_compare | ✅ 版本对比技能 |
| workflow-builder-system | skill_builder | ✅ **元技能** - 创建技能的技能 |

原工作流系统仍然可用，Skills 版本提供更好的 AI 集成体验。

> 💡 **特别说明**: `skill_builder` 不是简单的 workflow-builder 移植，而是重新定位为"用于创建 Agent Skills 的元技能"，帮助用户设计和构建新的技能包。

### 📚 相关链接

- [Agent Skills 标准](https://agentskills.io/)
- [VS Code Agent Skills 文档](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Copilot 工作流系统主页](../../README.md)

---

## English

### 📋 Overview

This directory contains skill packages compliant with the [Agent Skills open standard](https://agentskills.io/) to enhance GitHub Copilot's specialized capabilities.

### 🎯 What are Agent Skills?

Agent Skills is an open standard that allows you to create specialized capability packages that AI agents (like GitHub Copilot) can load on-demand. Unlike custom instructions, skills can include:

- 📝 Detailed operational instructions
- 📜 Scripts and tools
- 📚 Examples and templates
- 📁 Related resource files

### 📁 Available Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [analysis_code](analysis_code/) | Systematic code analysis skill | ✅ Available |
| [debug_code](debug_code/) | Systematic code debugging skill | ✅ Available |
| [refactor_code](refactor_code/) | Systematic code refactoring skill | ✅ Available |
| [file_organize](file_organize/) | Systematic file organization skill | ✅ Available |
| [version_compare](version_compare/) | Systematic version comparison skill | ✅ Available |
| [skill_builder](skill_builder/) | 🏗️ **Meta-Skill** - Skill for creating Agent Skills | ✅ Available |

### 🚀 Usage

#### 1. Enable Agent Skills

Enable in VS Code settings:

```json
{
  "chat.useAgentSkills": true
}
```

#### 2. Automatic Triggering

Skills are automatically loaded based on your requests. For example:

- Requesting "code analysis" → auto-loads `analysis_code` skill
- Requesting "debug help", "fix errors" → auto-loads `debug_code` skill
- Requesting "refactoring", "architecture improvement" → auto-loads `refactor_code` skill
- Requesting "file organization", "directory cleanup" → auto-loads `file_organize` skill
- Requesting "version comparison", "change analysis", "update log" → auto-loads `version_compare` skill
- Requesting "create skill", "design skill", "convert to skill" → auto-loads `skill_builder` skill

### 📚 Related Links

- [Agent Skills Standard](https://agentskills.io/)
- [VS Code Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Copilot Workflows System Home](../../README.md)

---

*版本: 1.0.0 | Copilot 工作流系统 Skills 扩展*
