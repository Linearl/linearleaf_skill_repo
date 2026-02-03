---
name: skill-builder
description: 系统化 Agent Skill 设计和构建。当用户需要创建新的 Agent Skill、设计技能包、转换工作流为技能格式时激活。Systematic Agent Skill design and building. Activates when user needs to create new Agent Skills, design skill packages, or convert workflows to skill format.
---

# 🏗️ Skill Builder | 技能构建器

## Overview | 概述

This meta-skill provides systematic capabilities for designing and building VS Code Agent Skills. It helps users create professional, well-structured skill packages that follow the Agent Skills open standard (agentskills.io).

此元技能提供系统化的 VS Code Agent Skills 设计和构建能力。帮助用户创建专业、结构良好的技能包，符合 Agent Skills 开放标准 (agentskills.io)。

## Trigger Conditions | 触发条件

**Keywords | 关键词**: create skill, design skill, build skill, new skill, skill package, convert to skill, skill template, 创建技能, 设计技能, 构建技能, 新技能, 技能包, 转换为技能

**Auto-suggestion | 自动建议**:
> "我看到您需要创建新的 Agent Skill。是否需要我启动技能构建器？我可以帮助您设计技能结构、编写 SKILL.md、创建模板和示例。"

## Core Concepts | 核心概念

### What is an Agent Skill? | 什么是 Agent Skill？

Agent Skills 是一种开放标准，允许创建可被 AI 代理（如 GitHub Copilot）按需加载的专业能力包：

```
.github/skills/[skill_name]/
├── SKILL.md              # 主技能定义（必需）
├── README.md             # 技能说明文档
├── templates/            # 模板文件目录
├── tools/                # 工具脚本目录
└── examples/             # 使用示例目录
```

### SKILL.md Structure | SKILL.md 结构

SKILL.md 是技能的核心定义文件，必须包含 YAML frontmatter：

```yaml
---
name: skill-name           # 技能标识名（kebab-case）
description: 技能描述...    # 触发条件描述（中英文双语推荐）
---

# 技能内容
[详细的技能指令和方法论]
```

### Three-Level Loading | 三级加载机制

1. **Level 1 - Discovery**: Copilot 始终知道有哪些技能可用（基于 name 和 description）
2. **Level 2 - Instructions**: 匹配请求时加载 SKILL.md 的完整内容
3. **Level 3 - Resources**: 按需访问 templates/, tools/, examples/ 中的文件

## Skill Design Methodology | 技能设计方法论

### IPD-Inspired Design Process | 基于IPD的设计流程

```mermaid
graph LR
    A[需求概念化] --> B[需求分析]
    B --> C[概念设计]
    C --> D[详细设计]
    D --> E[构建实现]
    E --> F[质量验证]
```

### Phase 1: Concept | 需求概念化

**Goals | 目标**:
- 明确技能要解决的核心问题
- 定义技能的价值主张
- 确定技能的边界范围

**Questions to Answer | 需要回答的问题**:
1. 这个技能要解决什么问题？
2. 目标用户是谁？
3. 成功的标准是什么？
4. 技能的触发场景有哪些？

### Phase 2: Analysis | 需求分析

**Goals | 目标**:
- 分析技能的复杂度
- 识别核心功能模块
- 评估技术可行性

**Analysis Dimensions | 分析维度**:
- **功能复杂度**: 技能需要多少核心能力？
- **模板需求**: 需要哪些标准化模板？
- **工具需求**: 需要哪些自动化工具？
- **集成需求**: 需要与哪些其他技能协作？

### Phase 3: Conceptual Design | 概念设计

**Goals | 目标**:
- 设计技能的整体架构
- 选择合适的设计模式
- 规划目录结构

**Design Patterns for Skills | 技能设计模式**:

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| 阶段化流程 | 分阶段执行的工作流 | 复杂多步骤任务 |
| 循环控制 | 迭代执行直到满足条件 | 调试、优化任务 |
| 模板驱动 | 基于模板生成内容 | 文档、报告生成 |
| 检查点确认 | 用户确认后继续 | 风险操作、重要决策 |
| 渐进式加载 | 按需加载更多资源 | 资源密集型技能 |

### Phase 4: Detailed Design | 详细设计

**Goals | 目标**:
- 设计 SKILL.md 的详细内容
- 规划每个模板的结构
- 定义工具的接口

**SKILL.md Content Design | SKILL.md 内容设计**:

```markdown
---
name: [skill-name]
description: [触发描述，包含关键词]
---

# 技能标题

## Overview | 概述
[技能的简要说明]

## Trigger Conditions | 触发条件
[关键词列表和自动建议语句]

## Core Methodology | 核心方法论
[技能的核心工作方法]

## Workflow Steps | 工作流步骤
[详细的执行步骤]

## Templates | 模板
[可用模板列表和说明]

## Usage Examples | 使用示例
[典型使用场景]

## Best Practices | 最佳实践
[使用建议和注意事项]

## References | 参考
[相关资源链接]
```

### Phase 5: Build | 构建实现

**Goals | 目标**:
- 创建目录结构
- 编写 SKILL.md
- 创建模板文件
- 编写示例

**Standard Directory Structure | 标准目录结构**:

```
.github/skills/[skill_name]/
├── SKILL.md                    # 主技能定义
├── README.md                   # 技能说明（可选但推荐）
├── templates/                  # 模板目录
│   ├── [template-1].md
│   ├── [template-2].md
│   └── ...
├── tools/                      # 工具目录（可选）
│   ├── [tool-1].py
│   └── [tool-1]-README.md
└── examples/                   # 示例目录
    └── README.md               # 使用示例
```

### Phase 6: Quality Assurance | 质量验证

**Quality Checklist | 质量检查清单**:

- [ ] **SKILL.md 完整性**
  - [ ] YAML frontmatter 正确（name, description）
  - [ ] 触发关键词覆盖主要使用场景
  - [ ] 方法论清晰可执行
  - [ ] 步骤描述详细

- [ ] **模板质量**
  - [ ] 模板结构清晰
  - [ ] 占位符易于理解
  - [ ] 示例内容有帮助

- [ ] **文档质量**
  - [ ] README 说明完整
  - [ ] 示例覆盖典型场景
  - [ ] 双语支持（推荐）

- [ ] **可用性验证**
  - [ ] 技能可被正确触发
  - [ ] 流程可顺利执行
  - [ ] 输出符合预期

## Skill Conversion Guide | 技能转换指南

### Converting Workflow to Skill | 将工作流转换为技能

When converting an existing workflow system to an Agent Skill:

1. **分析原工作流**
   - 识别核心方法论和流程
   - 提取关键模板
   - 理解触发场景

2. **设计触发条件**
   - 提取关键词（中英文）
   - 编写 description 以覆盖触发场景
   - 设计自动建议语句

3. **重构内容结构**
   - 将工作流模板转换为 SKILL.md 格式
   - 精简冗余内容
   - 保留核心方法论

4. **创建支持文件**
   - 转换原模板为技能模板
   - 编写使用示例
   - 创建 README

### Conversion Checklist | 转换检查清单

- [ ] 核心方法论已提取
- [ ] 触发关键词已覆盖原工作流的使用场景
- [ ] 模板已适配技能格式
- [ ] 示例已创建
- [ ] README 已编写

## Templates | 模板

### SKILL.md Template | SKILL.md 模板

参见 `templates/skill-md-template.md`

### README Template | README 模板

参见 `templates/readme-template.md`

### Example Template | 示例模板

参见 `templates/examples-template.md`

## Usage Examples | 使用示例

### Example 1: Create New Skill | 创建新技能

```markdown
请帮我创建一个新的 Agent Skill，用于自动化代码审查。

需求：
- 检查代码规范
- 识别潜在问题
- 生成审查报告
```

### Example 2: Convert Workflow | 转换工作流

```markdown
请将 my-workflow-system 转换为 Agent Skill 格式。

原工作流位于：workflow-system/
特点：三阶段流程、模板驱动、用户确认
```

### Example 3: Enhance Existing Skill | 增强现有技能

```markdown
请为 analysis_code 技能添加新的模板和工具。

新增需求：
- 安全漏洞检测模板
- 性能分析工具
```

## Best Practices | 最佳实践

### Naming Conventions | 命名约定

- **skill_name**: 使用 snake_case（如 `code_review`）
- **YAML name**: 使用 kebab-case（如 `code-review`）
- **Templates**: 使用 kebab-case（如 `review-report.md`）

### Description Writing | 描述编写

好的 description 应该：
1. 包含主要触发关键词
2. 中英文双语
3. 简洁但覆盖核心场景

```yaml
# ✅ 好的例子
description: 系统化代码审查和质量检测。当用户需要代码审查、质量检查、代码规范验证时激活。Systematic code review and quality detection. Activates when user needs code review, quality check, or code standard validation.

# ❌ 不好的例子
description: A skill for code review.  # 太简单，缺少关键词
```

### Content Organization | 内容组织

1. **Overview 放在最前面** - 让用户快速理解技能用途
2. **Trigger Conditions 要明确** - 确保技能被正确触发
3. **Core Methodology 是核心** - 这是技能的主要价值
4. **Examples 要实用** - 真实可用的示例

### Bilingual Support | 双语支持

推荐模式：
```markdown
## Section Title | 章节标题

English content...

中文内容...
```

## Integration with Other Skills | 与其他技能集成

skill_builder 可以与以下技能协作：

- **analysis_code**: 分析现有工作流，提取可复用模式
- **refactor_code**: 重构和优化技能代码
- **file_organize**: 组织技能的目录结构

## References | 参考

- [Agent Skills Open Standard](https://agentskills.io/)
- [VS Code Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- Original workflow: `workflow-builder-system/`
