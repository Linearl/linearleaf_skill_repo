# Refactor Code Skill | 代码重构技能

> 🌍 **Language**: English / 中文

## Overview | 概述

The Refactor Code skill provides systematic code refactoring and architecture improvement capabilities using a three-level planning system and dual-loop execution mechanism.

代码重构技能使用三层级计划体系和双循环执行机制，提供系统化的代码重构和架构改进能力。

## Features | 功能特点

- 🎯 **Three-Level Planning** | 三层级计划: Overall → Phase → Implementation
- 🔄 **Dual-Loop Execution** | 双循环执行: Outer (phase) + Inner (modification point)
- 📊 **Priority Management** | 优先级管理: P0/P1/P2/P3 classification
- ✅ **User Checkpoints** | 用户检查点: Mandatory confirmation before execution
- 📈 **Progress Tracking** | 进度跟踪: Visual progress with Mermaid diagrams
- 💾 **Backup Strategy** | 备份策略: Git-based and file-based backup options

## Trigger Keywords | 触发关键词

`code refactoring`, `system refactoring`, `architecture improvement`, `refactor plan`, `technical debt`, `代码重构`, `系统重构`, `架构改进`, `重构计划`, `技术债务`

## Directory Structure | 目录结构

```
refactor_code/
├── SKILL.md              # Main skill definition
├── README.md             # This file
├── templates/            # Workflow templates
│   ├── level1-overall-plan.md
│   ├── level2-phase-plan.md
│   ├── level3-implementation-plan.md
│   ├── progress-tracking.md
│   ├── quality-checklist.md
│   └── lessons-learned.md
└── examples/             # Usage examples
    └── README.md
```

## Quick Start | 快速开始

```markdown
我需要对 [模块名] 进行重构，请启动重构工作流。

目标：
1. 优化代码结构和可维护性
2. 清理技术债务
3. 提升性能

约束：
- 保持API兼容性
- 不能影响现有功能
```

## Workflow Phases | 工作流阶段

1. **Phase 1: Planning** | 规划阶段
   - User input collection
   - Environment initialization
   - Overall plan development
   - User feedback and confirmation

2. **Phase 2: Implementation** | 实施阶段
   - Outer loop: Phase-level execution
   - Inner loop: Modification point execution
   - Continuous verification

3. **Phase 3: Verification** | 验证阶段
   - Comprehensive testing
   - Results analysis
   - Documentation and archiving

## Best Practices | 最佳实践

1. Always base refactoring on analysis results
2. Execute small batches progressively
3. Verify immediately after each modification
4. Keep documentation synchronized
5. Use Git commits for version control

## Related Skills | 相关技能

- `analysis-code`: Provides code quality analysis as refactoring input
- `debug-code`: For fixing issues discovered during refactoring

## Reference | 参考资料

- Original workflow: `refactor_system/refactor_workflow_template.md`
- Full documentation: `refactor_system/README.md`
