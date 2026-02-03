# Version Compare Skill Examples | 版本对比技能示例

## Overview | 概述

This directory contains examples demonstrating how to use the version-compare skill.

此目录包含展示如何使用版本对比技能的示例。

---

## Example 1: Basic Version Comparison | 基本版本对比

```markdown
分析V1.86到V1.87的变更，目标是补充更新日志。
```

**Expected AI Actions | 预期AI操作**:
1. Parse version range: V1.86 → V1.87
2. Create task folder and initialize environment
3. Create dual worktrees for both versions
4. Execute 3-stage analysis process
5. Generate version comparison report
6. Create update log draft

---

## Example 2: Focused Module Analysis | 聚焦模块分析

```markdown
分析V2.0到V3.0的变更，重点关注algorithm模块和config管理，
目标是生成升级指导文档。
```

**Analysis Focus | 分析重点**:
- Stage 1: Overall change analysis with module filtering
- Stage 2: Deep dive into algorithm and config modules only
- Stage 3: Skip or brief documentation analysis
- Output: Upgrade guidance document

---

## Example 3: Upgrade Impact Assessment | 升级影响评估

```markdown
评估从项目V1.5升级到V2.0的影响，
重点识别破坏性变更和API变化，
生成兼容性分析报告和迁移指南。
```

**Key Outputs | 关键输出**:
- Breaking changes list
- API compatibility analysis
- Migration guide
- Risk assessment

---

## Example 4: Update Log Supplement | 更新日志补充

```markdown
分析最近三个版本(V1.5 → V1.6 → V1.7)的变更，
重点补充更新日志中缺失的技术细节。
```

**Note | 注意**: This requires running analysis for each version pair:
1. V1.5 → V1.6 analysis
2. V1.6 → V1.7 analysis
3. Consolidate into comprehensive update log

---

## Example 5: Release Note Generation | 发布说明生成

```markdown
为即将发布的V2.1版本准备发布说明。
对比V2.0到当前开发分支(develop)的所有变更。
```

**Special Considerations | 特殊考虑**:
- Target may be a branch instead of tag
- Need to identify completed vs in-progress features
- Generate user-facing release notes

---

## Workflow Integration | 工作流集成

### Complete Analysis Session | 完整分析会话

```markdown
# Session 1: Initialize
分析V1.0到V2.0的变更，目标是全面评估升级影响。

# AI creates environment, dual worktrees...
# AI executes Stage 1 analysis...

# Session 2: Confirm module plan
[AI presents module impact analysis]
确认需要深度分析的模块：core, api, utils
跳过模块：tests, docs, scripts

# Session 3: Deep analysis
继续执行模块深度分析。

# AI executes Stage 2 for confirmed modules...

# Session 4: Generate outputs
生成最终报告和更新日志。

# AI generates version_comparison_report.md and update_log_draft.md
```

---

## Tips for Effective Analysis | 高效分析技巧

1. **Clear Version Specification | 明确版本指定**
   - Use exact tag names: V1.86, v2.0, release-1.0
   - Or commit hashes: abc1234
   - Or branch names: main, develop

2. **Define Analysis Scope | 定义分析范围**
   - Specify modules to focus on
   - Indicate modules to skip
   - Set clear output goals

3. **Leverage Scripts | 利用脚本**
   - Use `setup_worktree.ps1` for environment setup
   - Use `generate-summary-metrics.ps1` for quick stats
   - Use `extract-breaking-api.ps1` for compatibility analysis

4. **Periodic Summaries | 定期总结**
   - Request summary every 2-5 minutes
   - Or after analyzing 5-10 files
   - Keep findings recorded

5. **Confirm Before Acting | 行动前确认**
   - Review module analysis plan
   - Confirm update log content before applying
   - Decide on worktree cleanup

---

## Common Scenarios | 常见场景

### Scenario A: Small Release | 小版本发布
- Few changes, quick analysis
- Focus on bug fixes and minor features
- Brief update log

### Scenario B: Major Release | 大版本发布
- Many changes, thorough analysis
- Multiple modules affected
- Detailed compatibility analysis
- Comprehensive migration guide

### Scenario C: Hotfix Analysis | 热修复分析
- Focused on specific bug fix
- Minimal scope
- Quick turnaround

### Scenario D: Quarterly Review | 季度回顾
- Multiple version spans
- Trend analysis
- Summary statistics
