# Refactor Code Skill Examples | 代码重构技能示例

## Overview | 概述

This directory contains examples demonstrating how to use the refactor-code skill.

此目录包含展示如何使用代码重构技能的示例。

---

## Example 1: Basic Refactoring Request | 基本重构请求

```markdown
我需要对 user_service 模块进行重构，请启动重构工作流。

目标：
1. 优化代码结构和可维护性
2. 减少代码重复
3. 提升性能

约束：
- 保持API兼容性
- 不能影响现有功能
```

**Expected AI Response | 预期AI响应**:
AI will start the refactoring workflow by:
1. Creating a task folder structure
2. Developing a Level 1 overall plan
3. Waiting for user confirmation

---

## Example 2: Analysis-Based Refactoring | 基于分析的重构

```markdown
请基于代码分析结果，为 payment_module 制定重构计划。

输入文档：
- analysis_system/tasks/payment_analysis_20250203/reports/final_analysis_report.md
- 技术债务清单已识别

重构优先级：
1. P0: 修复关键性能问题
2. P1: 清理冗余代码
3. P2: 优化架构设计
```

---

## Example 3: Module Comparison Refactoring | 模块对比重构

```markdown
我想参考 module_v2 的实现，重构 module_v1。

参考模块：src/module_v2/
目标模块：src/module_v1/

目标：
- 统一两个模块的设计模式
- 复用 v2 中的最佳实践
- 保持 v1 的业务逻辑不变
```

---

## Example 4: Specific Phase Execution | 指定阶段执行

```markdown
继续执行重构工作流的 P1 阶段。

当前状态：
- P0 阶段已完成
- P1 阶段计划已制定

请开始 P1 阶段的实施。
```

---

## Example 5: Single Modification Point | 单个修改点

```markdown
请执行修改点 P0.2 - 数据库连接池优化。

修改点信息：
- 涉及文件：src/db/connection_pool.py
- 目标：实现连接池复用
- 约束：保持现有接口不变
```

---

## Workflow Integration Example | 工作流集成示例

### Complete Refactoring Session | 完整重构会话

```markdown
# Session 1: Start refactoring
我需要重构订单处理模块，请启动重构工作流。

# AI creates Level 1 plan...
# User reviews and confirms...

# Session 2: Execute P0
请开始执行 P0 阶段。

# AI develops Level 2 plan for P0...
# User confirms modification points...

# Session 3: Continue with P0.1
请执行修改点 P0.1 - 订单验证逻辑重构。

# AI develops Level 3 plan and implements...
# Tests pass, move to P0.2...

# Session N: Complete
P0 阶段已完成，请进行阶段总结并提交代码。
```

---

## Tips for Effective Refactoring | 高效重构技巧

1. **Start with Analysis | 从分析开始**
   - Use analysis-code skill first to identify issues
   - Base refactoring on quantified metrics

2. **Small Steps | 小步前进**
   - Execute one modification point at a time
   - Verify after each change

3. **Checkpoint Discipline | 检查点纪律**
   - Always confirm plans before execution
   - Don't skip user confirmation steps

4. **Backup Strategy | 备份策略**
   - Create backups before major changes
   - Use Git commits for tracking

5. **Documentation | 文档记录**
   - Keep lessons learned updated
   - Document decisions and rationale
