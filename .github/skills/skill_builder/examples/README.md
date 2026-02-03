# Skill Builder 使用示例 | Usage Examples

本文档提供 Skill Builder 技能的实际使用示例。

## 📚 示例目录 | Examples Index

| # | 示例名称 | 难度 | 场景 |
|---|----------|------|------|
| 1 | 创建简单技能 | 入门 | 从零创建一个简单的 Agent Skill |
| 2 | 转换工作流系统 | 进阶 | 将现有工作流系统转换为 Agent Skill |
| 3 | 设计复杂技能 | 高级 | 设计包含多模板和工具的复杂技能 |

---

## Example 1: 创建简单技能 | Create Simple Skill

### 场景描述 | Scenario

用户想要创建一个用于自动生成 Git 提交信息的简单技能。

### 用户请求 | User Request

```markdown
@copilot 请帮我创建一个新的 Agent Skill，用于自动生成 Git 提交信息。

需求：
- 分析 staged changes
- 根据变更类型生成规范的 commit message
- 支持 Conventional Commits 格式
```

### 预期行为 | Expected Behavior

1. **需求概念化**
   - 识别核心功能：分析变更、生成提交信息
   - 确定触发关键词：git commit, commit message, 提交信息

2. **设计结构**
   - 创建 `.github/skills/git_commit/` 目录
   - 设计 SKILL.md 结构

3. **构建实现**
   - 创建 SKILL.md
   - 创建 README.md
   - 创建示例文件

### 预期输出 | Expected Output

```
.github/skills/git_commit/
├── SKILL.md
├── README.md
└── examples/
    └── README.md
```

### 要点说明 | Key Points

- 📌 简单技能不需要复杂的模板
- 📌 触发关键词要覆盖常见用语
- 📌 方法论要清晰简洁

---

## Example 2: 转换工作流系统 | Convert Workflow System

### 场景描述 | Scenario

用户有一个现有的文档生成工作流系统，想要将其转换为 Agent Skill 格式。

### 用户请求 | User Request

```markdown
@copilot 请将 doc-generator-workflow 转换为 Agent Skill 格式。

原工作流目录：workflow-systems/doc-generator/
特点：
- 三步骤流程：需求分析、模板选择、内容生成
- 包含5个文档模板
- 有一个验证工具脚本

请保留核心方法论，适配为 Agent Skills 标准。
```

### 预期行为 | Expected Behavior

1. **分析原工作流**
   - 读取并理解原工作流的 README 和主模板
   - 提取核心方法论和流程
   - 识别可复用的模板

2. **设计技能结构**
   - 设计触发条件和关键词
   - 规划目录结构
   - 决定保留哪些模板

3. **执行转换**
   - 创建 SKILL.md（整合原方法论）
   - 转换模板文件
   - 创建示例

4. **质量验证**
   - 检查 SKILL.md 完整性
   - 验证模板可用性

### 预期输出 | Expected Output

```
.github/skills/doc_generator/
├── SKILL.md              # 整合后的技能定义
├── README.md             # 技能说明
├── templates/
│   ├── template-1.md     # 转换后的模板
│   ├── template-2.md
│   └── ...
├── tools/
│   └── validator.py      # 保留的工具
└── examples/
    └── README.md         # 使用示例
```

### 要点说明 | Key Points

- 📌 转换时保留核心方法论
- 📌 精简冗余内容，适配技能格式
- 📌 确保触发关键词覆盖原使用场景
- 📌 工具脚本可按需保留

---

## Example 3: 设计复杂技能 | Design Complex Skill

### 场景描述 | Scenario

用户想要设计一个完整的代码审查技能，包含多个审查维度、模板和工具。

### 用户请求 | User Request

```markdown
@copilot 请帮我设计一个完整的代码审查 Agent Skill。

要求：
1. 支持多维度审查
   - 代码质量
   - 安全漏洞
   - 性能问题
   - 代码规范
   
2. 需要的模板
   - 审查报告模板
   - 问题清单模板
   - 改进建议模板
   
3. 工具需求
   - 自动检测脚本
   - 报告生成工具

4. 工作流
   - 支持增量审查
   - 支持全量审查
   - 支持用户确认机制

请使用完整的 IPD 设计流程。
```

### 预期行为 | Expected Behavior

1. **需求概念化**
   - 明确技能边界：代码审查，不含自动修复
   - 定义成功标准：覆盖4个维度，生成可执行的改进建议

2. **需求分析**
   - 分析复杂度：中高复杂度，需要多模板多工具
   - 识别模块：审查引擎、报告生成、检测工具

3. **概念设计**
   - 选择设计模式：阶段化流程 + 检查点确认
   - 设计架构：核心方法论 + 维度模块

4. **详细设计**
   - SKILL.md 结构设计
   - 每个模板的详细字段
   - 工具接口定义

5. **构建实现**
   - 按计划创建所有文件

6. **质量验证**
   - 运行检查清单
   - 验证完整性

### 预期输出 | Expected Output

```
.github/skills/code_review/
├── SKILL.md                      # 主技能定义（包含核心方法论）
├── README.md                     # 详细技能说明
├── templates/
│   ├── review-report.md          # 审查报告模板
│   ├── issue-checklist.md        # 问题清单模板
│   ├── improvement-plan.md       # 改进建议模板
│   ├── quality-dimension.md      # 质量维度模板
│   ├── security-dimension.md     # 安全维度模板
│   ├── performance-dimension.md  # 性能维度模板
│   └── standards-dimension.md    # 规范维度模板
├── tools/
│   ├── detector.py               # 自动检测脚本
│   ├── detector-README.md        # 检测工具说明
│   ├── report-generator.py       # 报告生成工具
│   └── report-generator-README.md
└── examples/
    └── README.md                 # 使用示例（包含增量和全量审查示例）
```

### 要点说明 | Key Points

- 📌 复杂技能使用完整的 IPD 六阶段设计流程
- 📌 模块化设计便于维护和扩展
- 📌 每个工具都应有对应的 README
- 📌 示例应覆盖主要使用场景

---

## 💡 使用技巧 | Tips

### 有效触发 Skill Builder | Effective Triggering

- ✅ 使用关键词：`创建技能`、`create skill`、`build skill`、`设计技能`
- ✅ 明确说明技能的用途和需求
- ✅ 提供足够的上下文（如有现有工作流）

### 设计技能的最佳实践 | Best Practices for Designing Skills

1. **从简单开始**: 先设计核心功能，再逐步增强
2. **关注触发条件**: 好的 description 决定技能能否被正确触发
3. **双语支持**: 中英文关键词都要覆盖
4. **测试验证**: 创建后测试技能是否能被正确触发

### 常见问题 | Common Issues

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 技能未被触发 | description 关键词不足 | 增加更多触发关键词 |
| 方法论不清晰 | SKILL.md 结构混乱 | 使用模板重新组织 |
| 模板难以使用 | 缺少示例和说明 | 添加占位符和使用示例 |

---

## 🔗 相关资源 | Related Resources

- [SKILL.md](../SKILL.md) - 完整的 Skill Builder 定义
- [Templates](../templates/) - 可用于创建技能的模板
- [README](../README.md) - Skill Builder 说明
