# Linearleaf Agent Skills

<p align="center">
  <img src="https://img.shields.io/badge/VS%20Code-Agent%20Skills-blue?logo=visualstudiocode" alt="VS Code Agent Skills">
  <img src="https://img.shields.io/badge/Standard-agentskills.io-green" alt="Agent Skills Standard">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

<p align="center">
  <strong>🚀 专业级 VS Code Agent Skills 技能包 | Professional VS Code Agent Skills Collection</strong>
</p>

<p align="center">
  <a href="#中文">中文</a> | <a href="#english">English</a>
</p>

---

## 中文

### 📖 概述

Linearleaf Agent Skills 是一套符合 [Agent Skills 开放标准](https://agentskills.io/) 的专业技能包，为 GitHub Copilot 和 Claude Code 提供系统化的代码分析、调试、重构、文件整理、版本对比和技能构建能力。

> 🔄 **项目演进**: 本项目是 [copilot_workflows](https://github.com/Linearl/copilot_workflows) 的 Agent Skills 标准化重构版本，提供更好的 AI 集成体验。

### 🎯 可用技能

| 技能 | 说明 | 触发示例 |
|------|------|----------|
| 🔍 [analysis_code](analysis_code/) | 系统化代码分析 | "分析这段代码"、"代码质量评估" |
| 🐛 [debug_code](debug_code/) | 系统化代码调试 | "帮我调试"、"修复这个错误" |
| 🔧 [refactor_code](refactor_code/) | 系统化代码重构 | "重构代码"、"架构改进" |
| 📁 [file_organize](file_organize/) | 系统化文件整理 | "整理文件"、"清理目录" |
| 📊 [version_compare](version_compare/) | 系统化版本对比 | "版本对比"、"变更分析" |
| 💰 [invest_analysis](invest_analysis/) | A股投资分析 | "分析这个板块"、"财报验证" |
| 🏗️ [skill_builder](skill_builder/) | **元技能** - 创建新技能 | "创建技能"、"设计技能" |

### 🚀 快速开始

#### 1. 安装

**方式1：克隆整个仓库**
```bash
git clone https://github.com/Linearl/linearleaf_skill_repo.git
```

**方式2：作为 Git 子模块**
```bash
git submodule add https://github.com/Linearl/linearleaf_skill_repo.git .skills
```

**方式3：直接复制技能**
将所需的技能目录（如 `analysis_code/`、`debug_code/` 等）复制到您的项目中。

#### 2. 启用 Agent Skills

在 VS Code 设置中启用：

```json
{
  "chat.useAgentSkills": true
}
```

#### 3. 使用

技能会根据您的请求自动加载。直接向 Copilot 描述您的需求即可！

### 📚 技能详情

#### 🔍 analysis_code - 代码分析技能

提供总-分-总结构的系统化代码分析能力：
- 代码质量评估
- 性能分析
- 架构审查
- 技术债务识别

#### 🐛 debug_code - 调试技能

6步调试循环的系统化调试方法：
- 问题定义
- 假设形成
- 验证测试
- 根因分析
- 修复实施
- 验证确认

#### 🔧 refactor_code - 重构技能

三层级计划体系的系统化重构：
- 整体重构计划
- 阶段详细规划
- 任务执行管理
- P0-P3 优先级控制

#### 📁 file_organize - 文件整理技能

三种整理方式：
- 优先级导向整理
- 类型导向整理
- 时间线导向整理

#### 📊 version_compare - 版本对比技能

系统化版本对比和变更分析：
- 版本差异分析
- 变更影响评估
- 更新日志生成

#### 🏗️ skill_builder - 技能构建器

**元技能** - 用于创建新的 Agent Skills：
- IPD 驱动的技能设计流程
- 技能设计模式库
- 质量保证检查清单

#### 💰 invest_analysis - 投资分析技能

系统化 A 股投资研究框架：
- 赛道筛选和热点挖掘
- 产业链深度分析
- 财报验证和去伪
- 择时分析和风险评估
- 跨模型验证

### 🔗 相关链接

- [Agent Skills 开放标准](https://agentskills.io/)
- [VS Code Agent Skills 文档](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [原工作流项目 (已停止维护)](https://github.com/Linearl/copilot_workflows)

---

## English

### 📖 Overview

Linearleaf Agent Skills is a collection of professional skill packages compliant with the [Agent Skills open standard](https://agentskills.io/), providing GitHub Copilot and Claude Code with systematic capabilities for code analysis, debugging, refactoring, file organization, version comparison, and skill building.

> 🔄 **Project Evolution**: This project is the Agent Skills standardized version of [copilot_workflows](https://github.com/Linearl/copilot_workflows), offering a better AI integration experience.

### 🎯 Available Skills

| Skill | Description | Trigger Examples |
|-------|-------------|------------------|
| 🔍 [analysis_code](analysis_code/) | Systematic code analysis | "analyze this code", "code quality assessment" |
| 🐛 [debug_code](debug_code/) | Systematic debugging | "help me debug", "fix this error" |
| 🔧 [refactor_code](refactor_code/) | Systematic refactoring | "refactor code", "improve architecture" |
| 📁 [file_organize](file_organize/) | Systematic file organization | "organize files", "clean up directory" |
| 📊 [version_compare](version_compare/) | Systematic version comparison | "compare versions", "change analysis" |
| 💰 [invest_analysis](invest_analysis/) | A-share investment analysis | "analyze this sector", "verify financial report" |
| 🏗️ [skill_builder](skill_builder/) | **Meta-skill** - Create new skills | "create skill", "design skill" |

### 🚀 Quick Start

#### 1. Installation

**Option 1: Clone the entire repository**
```bash
git clone https://github.com/Linearl/linearleaf_skill_repo.git
```

**Option 2: As Git submodule**
```bash
git submodule add https://github.com/Linearl/linearleaf_skill_repo.git .skills
```

**Option 3: Copy specific skills**
Copy the skill directories you need (e.g., `analysis_code/`, `debug_code/`) to your project.

#### 2. Enable Agent Skills

Enable in VS Code settings:

```json
{
  "chat.useAgentSkills": true
}
```

#### 3. Usage

Skills are automatically loaded based on your requests. Just describe your needs to Copilot!

### 📚 Skill Details

#### 🔍 analysis_code - Code Analysis Skill

Provides systematic code analysis with overview-detail-summary structure:
- Code quality assessment
- Performance analysis
- Architecture review
- Technical debt identification

#### 🐛 debug_code - Debugging Skill

6-step debugging cycle methodology:
- Problem definition
- Hypothesis formation
- Verification testing
- Root cause analysis
- Fix implementation
- Validation confirmation

#### 🔧 refactor_code - Refactoring Skill

Three-tier planning system for systematic refactoring:
- Overall refactoring plan
- Stage detailed planning
- Task execution management
- P0-P3 priority control

#### 📁 file_organize - File Organization Skill

Three organization approaches:
- Priority-oriented organization
- Type-oriented organization
- Timeline-oriented organization

#### 📊 version_compare - Version Comparison Skill

Systematic version comparison and change analysis:
- Version difference analysis
- Change impact assessment
- Update log generation

#### 🏗️ skill_builder - Skill Builder

**Meta-skill** - For creating new Agent Skills:
- IPD-driven skill design process
- Skill design pattern library
- Quality assurance checklist
#### 💰 invest_analysis - Investment Analysis

Systematic A-share investment research framework:
- Sector selection and trend identification
- Supply chain deep analysis
- Financial report verification
- Timing analysis and risk assessment
- Cross-model validation
### 🔗 Related Links

- [Agent Skills Open Standard](https://agentskills.io/)
- [VS Code Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Original Workflow Project (Deprecated)](https://github.com/Linearl/copilot_workflows)

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

<p align="center">
  <strong>Made with ❤️ by Linearleaf</strong>
</p>
