# VS Code Agent Skills 测试指南

## 目录结构说明

本项目采用双层目录结构：

### 1. 根目录（标准结构）
```
linearleaf_skill_repo/
├── analysis_code/          # 标准 Agent Skills 结构
├── debug_code/
├── file_organize/
├── refactor_code/
├── skill_builder/
├── version_compare/
├── invest_analysis/        # 新增：投资分析技能
├── CLAUDE.md
├── README.md
└── ...
```

这是符合 Agent Skills 标准的项目结构，用于发布和分发。

### 2. .github/skills 目录（测试结构）
```
.github/
└── skills/
    ├── analysis_code/      # 复制的技能，用于 VS Code 测试
    ├── debug_code/
    ├── file_organize/
    ├── refactor_code/
    ├── skill_builder/
    ├── version_compare/
    └── invest_analysis/
```

这是专门为 VS Code Agent Skills 测试创建的目录，所有技能都被复制到这里。

## 如何在 VS Code 中测试

### 启用 Agent Skills

1. 打开 VS Code 设置（File > Preferences > Settings）
2. 搜索 `chat.useAgentSkills`
3. 勾选启用该选项

或者在 `settings.json` 中添加：
```json
{
  "chat.useAgentSkills": true
}
```

### 技能自动发现

当你在本项目目录下工作时，VS Code 会自动发现 `.github/skills/` 目录中的所有技能。

### 触发技能

直接在 GitHub Copilot Chat 中使用自然语言：

- **代码分析**: "分析这段代码的质量"
- **调试**: "帮我调试这个错误"
- **重构**: "重构这个函数"
- **文件整理**: "整理这个目录的文件"
- **版本对比**: "对比这两个版本的差异"
- **投资分析**: "分析人形机器人板块" （新技能！）
- **创建技能**: "创建一个新的 Agent Skill"

## 新增技能：invest_analysis

### 功能特性

本次新增的投资分析技能包含：

1. **赛道筛选**：基于即将发生的事件识别投资机会
2. **产业链挖掘**：深入分析供应链结构
3. **财报验证**：验证公司业务真实性
4. **择时分析**：评估市场情绪和介入时机
5. **跨模型验证**：使用多个 AI 模型交叉验证

### 使用示例

```
用户: "我想了解 2026年2月可能爆发的 A 股板块"
→ 触发 invest_analysis 技能的赛道筛选流程

用户: "帮我分析人形机器人产业链"
→ 触发 invest_analysis 技能的产业链挖掘流程

用户: "这份财报的 AI 业务是真的还是炒作？"
→ 触发 invest_analysis 技能的财报验证流程
```

### 推荐 AI 模型

- **DeepSeek**: 擅长中文市场和 A 股分析
- **Gemini Deep Research**: 综合研究能力强
- **ChatGPT**: 逻辑推理和结构化输出好

## 技能开发流程

如果你想添加新技能或修改现有技能：

1. **修改根目录中的技能**（如 `analysis_code/SKILL.md`）
2. **运行同步命令**（复制到 `.github/skills/`）：
   ```powershell
   $skills = @('analysis_code', 'debug_code', 'file_organize', 'refactor_code', 'skill_builder', 'version_compare', 'invest_analysis')
   foreach ($skill in $skills) {
       Copy-Item -Path $skill -Destination ".github\skills\$skill" -Recurse -Force
   }
   ```
3. **重启 VS Code** 或重新加载窗口以刷新技能

## 注意事项

- `.github/skills/` 目录中的内容是从根目录复制的
- 不要直接修改 `.github/skills/` 中的文件
- 始终在根目录进行修改，然后同步到测试目录
- 测试目录已在 `.gitignore` 中添加说明

## 投资分析技能风险提示

⚠️ **重要**：
- invest_analysis 技能仅供研究辅助，不构成投资建议
- AI 可能产生幻觉或提供过时信息
- 务必通过官方渠道验证所有信息
- 市场有风险，投资需谨慎

---

更新日期：2026-02-03
版本：1.1.0
