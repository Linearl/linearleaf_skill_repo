# Version Compare Skill | 版本对比技能

> 🌍 **Language**: English / 中文

## Overview | 概述

The Version Compare skill provides systematic version comparison and change analysis capabilities using a three-stage analysis process and Git worktree integration.

版本对比技能使用三阶段分析流程和Git worktree集成，提供系统化的版本对比和变更分析能力。

## Features | 功能特点

- 🔄 **Three-Stage Analysis** | 三阶段分析: Overview → Modules → Documentation
- 📊 **Git Worktree Integration** | Git工作区集成: Safe dual-version comparison
- 🎯 **Dynamic Module Discovery** | 动态模块发现: Auto-detect changed modules
- 📝 **Multiple Outputs** | 多种输出: Reports, update logs, upgrade guides
- ⚠️ **Breaking Change Detection** | 破坏性变更检测: API and config changes
- 📈 **Code Metrics** | 代码指标: Automated statistics collection
- ⚡ **Sub-agent Parallel Acceleration** | 子代理并行加速: ask_questions确认优先级后并行深挖，分目录隔离输出

## Trigger Keywords | 触发关键词

`version comparison`, `change analysis`, `update log`, `version diff`, `upgrade assessment`, `changelog`, `版本对比`, `变更分析`, `更新日志`, `版本差异`, `升级评估`

## Directory Structure | 目录结构

```
version_compare/
├── SKILL.md              # Main skill definition
├── README.md             # This file
├── templates/            # Workflow templates
│   ├── analysis-index.md     # Analysis navigation index
│   ├── stage-record.md       # Stage analysis record
│   ├── module-analysis.md    # Module analysis report
│   ├── version-summary.md    # Version comparison summary
│   └── update-log.md         # Update log template
└── examples/             # Usage examples
    └── README.md
```

## Three-Stage Analysis | 三阶段分析

1. **Stage 1 - Overall Analysis | 总体变更分析**
   - Commit classification (feat/fix/refactor)
   - File change statistics
   - Module impact assessment

2. **Stage 2 - Module Deep Dive | 核心模块深度对比**
   - Bottom-up: tools → logic → algorithm
   - ask_questions-guided module selection and priority confirmation
   - Parallel sub-agent execution with isolated output directories (e.g., `subagent_01_xxx/`)
   - Periodic summaries and merged findings

3. **Stage 3 - Documentation | 文档变更分析**
   - Brief documentation review
   - Structure changes
   - No deep analysis

## Quick Start | 快速开始

### Basic Comparison | 基本对比
```markdown
分析V1.86到V1.87的变更，目标是补充更新日志。
```

### Focused Analysis | 聚焦分析
```markdown
分析V2.0到V3.0的变更，重点关注算法模块，目标是生成升级指导文档。
```

### Impact Assessment | 影响评估
```markdown
评估从V1.5升级到V2.0的影响，识别破坏性变更，生成兼容性分析报告。
```

## Output Deliverables | 输出交付物

| Output | Description |
|--------|-------------|
| version_comparison_report.md | Complete comparison report |
| update_log_draft.md | Update log draft |
| module_impact.md | Module impact analysis |
| INDEX.md | Analysis navigation |

## Script Tools | 脚本工具

| Script | Purpose |
|--------|---------|
| setup_worktree.ps1 | Create worktree + diff data |
| cleanup_worktree.ps1 | Clean worktree |
| generate-summary-metrics.ps1 | Summary metrics |
| extract-breaking-api.ps1 | Breaking API detection |
| generate-module-impact.ps1 | Module impact analysis |

## Tech Stack Support | 技术栈支持

> ⚠️ Current version primarily supports **Python, C/C++** for deep code analysis. Other languages can use the framework and templates.

## Related Skills | 相关技能

- `analysis-code`: Code quality metrics input
- `refactor-code`: Post-analysis refactoring

## Reference | 参考资料

- Original workflow: `version-comparison-system/version-comparison-workflow-template.md`
- Full documentation: `version-comparison-system/README.md`
