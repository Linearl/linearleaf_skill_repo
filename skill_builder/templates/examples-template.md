# Examples 模板 | Examples Template

此模板用于创建 Agent Skill 的 examples/README.md 文件。

---

## 模板内容 | Template Content

```markdown
# [技能名称] 使用示例 | Usage Examples

本文档提供 [技能名称] 技能的实际使用示例和场景说明。

## 📚 示例目录 | Examples Index

| # | 示例名称 | 难度 | 场景 |
|---|----------|------|------|
| 1 | [示例1名称] | 入门 | [场景描述] |
| 2 | [示例2名称] | 进阶 | [场景描述] |
| 3 | [示例3名称] | 高级 | [场景描述] |

---

## Example 1: [示例1名称] | [Example Name]

### 场景描述 | Scenario

[描述这个示例的使用场景和背景]

### 用户请求 | User Request

\`\`\`markdown
@copilot [用户的实际请求内容]

[额外的上下文或要求]
\`\`\`

### 预期行为 | Expected Behavior

1. **[阶段1名称]**
   - [预期操作1]
   - [预期操作2]

2. **[阶段2名称]**
   - [预期操作1]
   - [预期操作2]

### 预期输出 | Expected Output

[描述或展示预期的输出内容]

\`\`\`
[输出示例]
\`\`\`

### 要点说明 | Key Points

- 📌 [要点1]
- 📌 [要点2]

---

## Example 2: [示例2名称] | [Example Name]

### 场景描述 | Scenario

[描述...]

### 用户请求 | User Request

\`\`\`markdown
@copilot [请求内容...]
\`\`\`

### 预期行为 | Expected Behavior

[行为描述...]

### 预期输出 | Expected Output

[输出描述...]

### 要点说明 | Key Points

- 📌 [要点...]

---

## Example 3: [示例3名称] | [Example Name]

[重复上述结构...]

---

## 💡 使用技巧 | Tips

### 有效触发技能 | Effective Triggering

- ✅ 使用明确的关键词：[关键词列表]
- ✅ 提供足够的上下文
- ✅ 明确说明期望的输出

### 常见问题 | Common Issues

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| [问题1] | [原因] | [解决方案] |
| [问题2] | [原因] | [解决方案] |

### 最佳实践 | Best Practices

1. **[实践1标题]**: [说明]
2. **[实践2标题]**: [说明]
3. **[实践3标题]**: [说明]

---

## 🔗 相关资源 | Related Resources

- [SKILL.md](../SKILL.md) - 完整技能定义
- [Templates](../templates/) - 可用模板
- [README](../README.md) - 技能说明
```

---

## 使用说明 | Usage Instructions

### 示例设计原则 | Example Design Principles

1. **渐进式难度** - 从简单到复杂
2. **覆盖主要场景** - 体现技能的核心价值
3. **实际可执行** - 用户可以直接复制使用
4. **清晰的预期** - 让用户知道会发生什么

### 每个示例应包含 | Each Example Should Include

- **场景描述**: 为什么需要这样做
- **用户请求**: 实际的请求内容
- **预期行为**: 技能会做什么
- **预期输出**: 最终结果是什么
- **要点说明**: 关键注意事项

### 示例数量建议 | Suggested Number of Examples

| 技能复杂度 | 建议示例数量 |
|------------|--------------|
| 简单 | 2-3 |
| 中等 | 3-5 |
| 复杂 | 5-7 |

### 检查清单 | Checklist

- [ ] 包含入门级示例
- [ ] 包含进阶级示例
- [ ] 场景描述清晰
- [ ] 请求内容可复制
- [ ] 预期行为明确
- [ ] 包含使用技巧
