# SKILL.md 模板 | SKILL.md Template

此模板用于创建新 Agent Skill 的 SKILL.md 文件。

---

## 模板内容 | Template Content

```markdown
---
name: [skill-name]
description: [中文描述]。当用户需要[触发场景1]、[触发场景2]时激活。[English description]. Activates when user needs [trigger1], [trigger2].
---

# [技能图标] [技能名称] | [Skill Name]

## Overview | 概述

[技能的简要说明，包括：]
- 解决什么问题
- 目标用户
- 核心价值

This skill provides [核心功能] capabilities for [目标用户/场景].

## Trigger Conditions | 触发条件

**Keywords | 关键词**: [关键词1], [关键词2], [关键词3], [中文关键词1], [中文关键词2]

**Auto-suggestion | 自动建议**:
> "[当检测到相关场景时的自动建议语句]"

## Core Methodology | 核心方法论

### [方法论名称] | [Methodology Name]

[方法论的整体描述]

```mermaid
graph LR
    A[步骤1] --> B[步骤2]
    B --> C[步骤3]
    C --> D[步骤4]
```

### Key Principles | 核心原则

1. **[原则1]**: [说明]
2. **[原则2]**: [说明]
3. **[原则3]**: [说明]

## Workflow Steps | 工作流步骤

### Step 1: [步骤名称] | [Step Name]

**Goals | 目标**:
- [目标1]
- [目标2]

**Process | 流程**:
1. [操作1]
2. [操作2]
3. [操作3]

**Output | 输出**:
- [输出物1]
- [输出物2]

**Checkpoint | 检查点**: [需要用户确认的内容]

### Step 2: [步骤名称] | [Step Name]

[重复上述结构...]

## Templates | 模板

| 模板 | 用途 | 路径 |
|------|------|------|
| [模板1名称] | [用途说明] | `templates/[filename].md` |
| [模板2名称] | [用途说明] | `templates/[filename].md` |

## Tools | 工具

| 工具 | 用途 | 路径 |
|------|------|------|
| [工具1名称] | [用途说明] | `tools/[filename].py` |

## Usage Examples | 使用示例

### Example 1: [场景名称]

```markdown
[用户可能的请求示例]
```

**Expected Process | 预期流程**:
1. [步骤1]
2. [步骤2]
3. [步骤3]

### Example 2: [场景名称]

[重复上述结构...]

## Best Practices | 最佳实践

### Recommended | 推荐做法

- ✅ [推荐做法1]
- ✅ [推荐做法2]

### Avoid | 避免做法

- ❌ [避免做法1]
- ❌ [避免做法2]

## Integration | 集成

### Related Skills | 相关技能

- `[skill_name]` - [如何与此技能协作]

### Prerequisites | 前提条件

- [前提条件1]
- [前提条件2]

## References | 参考

- [参考资源1](链接)
- [参考资源2](链接)
```

---

## 使用说明 | Usage Instructions

### 必填字段 | Required Fields

1. **YAML Frontmatter**
   - `name`: kebab-case 格式的技能标识
   - `description`: 包含关键词的触发描述

2. **Overview**: 技能的核心价值说明

3. **Trigger Conditions**: 明确的触发关键词

4. **Workflow Steps**: 至少一个可执行的步骤

### 推荐字段 | Recommended Fields

1. **Templates**: 如果技能使用模板
2. **Examples**: 至少2-3个使用示例
3. **Best Practices**: 帮助用户正确使用

### 格式要求 | Format Requirements

- 使用中英双语标题格式：`## Title | 标题`
- 使用 Mermaid 图表展示流程
- 使用表格组织结构化信息
- 使用 emoji 增强可读性

### 检查清单 | Checklist

- [ ] YAML frontmatter 完整
- [ ] 触发关键词覆盖中英文
- [ ] 核心方法论清晰
- [ ] 步骤可执行
- [ ] 示例实用
- [ ] 双语支持
