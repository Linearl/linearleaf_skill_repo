# Linearleaf Agent Skills

![VS Code Agent Skills](https://img.shields.io/badge/VS%20Code-Agent%20Skills-blue?logo=visualstudiocode)
![Agent Skills Standard](https://img.shields.io/badge/Standard-agentskills.io-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

🚀 专业级 VS Code Agent Skills 技能包

语言：**中文** | [English (README.md)](README.md)

---

## 📖 概述

Linearleaf Agent Skills 是一套符合 [Agent Skills 开放标准](https://agentskills.io/) 的专业技能包，为 GitHub Copilot 和 Claude Code 提供系统化的代码分析、调试、重构、文件整理、版本对比、HTML 演示文稿生成和技能构建能力。

> 🔄 **项目演进**：本项目是 [copilot_workflows](https://github.com/Linearl/copilot_workflows) 的 Agent Skills 标准化重构版本。

## 🧭 方法哲学（来自 AUTHOR_NOTE）

我们并不是在发明一套全新的协作逻辑，而是在把人类社会长期有效的组织实践迁移到 AI 协作中：

- **Workflow 是方法论内核**：保障复杂任务可控、可复盘、可沉淀；
- **Skill 是标准化外壳**：通过动态加载机制提升接入效率，减少手动唤醒；
- **多智能体协作依赖工作空间**：通过团队 workspace + 智能体 subspace，以文档代通信，降低协作带宽消耗。

👉 详细说明请见：[`AUTHOR_NOTE.md`](AUTHOR_NOTE.md)

## 🎯 可用技能

| 技能 | 说明 | 触发示例 |
| --- | --- | --- |
| 🔍 [analysis_code](analysis_code/) | 系统化代码分析 | "分析这段代码"、"代码质量评估" |
| 🛠️ [code-audit-fix](code-audit-fix/) | 缺陷扫描与分批修复 | "审计并修复代码问题"、"分批扫描缺陷并修复" |
| 🐛 [debug_code](debug_code/) | 系统化代码调试 | "帮我调试"、"修复这个错误" |
| 🔧 [refactor_code](refactor_code/) | 系统化代码重构 | "重构代码"、"架构改进" |
| 📁 [file_organize](file_organize/) | 系统化文件整理 | "整理文件"、"清理目录" |
| 📊 [version_compare](version_compare/) | 系统化版本对比 | "版本对比"、"变更分析" |
| 💰 [invest_analysis](invest_analysis/) | A股投资分析 | "分析这个板块"、"财报验证" |
| 🖥️ [html-presentation-generator](html-presentation-generator/) | HTML 演示文稿生成流水线 | "根据讲稿生成HTML演示"、"分镜合并并校验页序" |
| 🏗️ [skill_builder](skill_builder/) | **元技能** - 创建新技能 | "创建技能"、"设计技能" |

## 🚀 快速开始

### 1）安装

方式1：克隆整个仓库

```bash
git clone https://github.com/Linearl/linearleaf_skill_repo.git
```

方式2：作为 Git 子模块

```bash
git submodule add https://github.com/Linearl/linearleaf_skill_repo.git .skills
```

方式3：直接复制技能目录

将所需的技能目录（如 `analysis_code/`、`debug_code/`）复制到你的项目中。

### 2）启用 Agent Skills

```json
{
  "chat.useAgentSkills": true
}
```

### 3）使用

技能会根据你的请求上下文动态加载，直接向 Copilot 描述需求即可。

## 📚 技能亮点

### 🔍 analysis_code

- 代码质量评估
- 性能分析
- 架构审查
- 技术债务识别
- ask_questions 引导式检查点（阶段范围与优先级确认）
- 首轮分析后支持 sub-agent 并行加速

### 🛠️ code-audit-fix

- 全项目缺陷扫描与优先级归类
- 按优先级分批修复流程
- 修复前后多轮交叉复核
- 支持 CI 非交互执行与结果契约输出

### 🐛 debug_code

- 6步调试循环
- 结构化根因定位
- 验证与收尾记录

### 🔧 refactor_code

- 三层级计划的渐进式重构
- P0–P3 优先级控制
- 分阶段安全执行

### 📁 file_organize

- 优先级导向整理
- 类型导向整理
- 时间线导向整理

### 📊 version_compare

- 版本差异分析
- 变更影响评估
- 更新日志生成
- ask_questions 引导式模块优先级确认
- sub-agent 并行模块分析

### 🖥️ html-presentation-generator

- 长文档拆分与分镜并行产出
- 分片 HTML 生成与合并构建
- 页序一致性与质量门禁校验
- 预览迭代与改进闭环

### 🏗️ skill_builder

- IPD 驱动技能设计流程
- 技能设计模式库
- 质量保证检查清单

### 💰 invest_analysis

- 赛道筛选与趋势识别
- 产业链深度分析
- 财报验证
- 节奏与风险评估
- 跨模型验证

## 🔗 相关链接

- [English Documentation (README.md)](README.md)
- [作者说明 / 方法哲学](AUTHOR_NOTE.md)
- [Agent Skills 开放标准](https://agentskills.io/)
- [VS Code Agent Skills 文档](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [原工作流项目（已停止维护）](https://github.com/Linearl/copilot_workflows)

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE)。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request。

---

Made with ❤️ by Linearleaf
