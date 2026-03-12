---
name: html-presentation-generator
description: 端到端 HTML 演示文稿生成技能（主文档拆分→分镜稿→HTML落地→合并校验→预览）。当用户提到“上下文过长导致循环总结”“需要拆分分镜”“并行用 sub-agent 生成内容”“合并 part1/part2/part3 HTML 并检查页序”时启用。支持 ask_questions 决策点、流程固化、脚本化校验与改进闭环。
---

# HTML Presentation Generator

> **版本**: 1.1.0 | **定位**: 长文档拆分与并行生成的 HTML 演示流水线

## 🎯 技能概述

本技能把“长文档一次性生成导致上下文失控”的任务，转成可并行、可校验、可回退的稳定流程。适用于讲稿型 HTML 产出（分片 + 合并 + 预览），强调过程决策可视化与最小改动迭代。

### 核心能力

- **结构化拆分**: 主文档按章节边界切分为可独立处理的分段。
- **并行分镜**: 使用 sub-agent 并行生成与复核分镜稿。
- **分片落地**: 每段独立生成 part HTML，并先做单段校验。
- **自动合并**: 用脚本重排 `active` / `data-index` / 页码生成总稿。
- **质量门禁**: 针对禁用词、附录、行动页口播等进行回归检查。

### 适用场景

- 用户反馈对话反复总结、上下文过长、任务推进缓慢。
- 需要“拆分生成 + 合并校验”的讲稿型演示文档。
- 需要多轮修改，且希望每轮都可验证、可回退。

## 📋 执行流程

### 阶段一：规划与切分

1. 运行 `init_topic_folder.py` 初始化专题目录。
2. 将输入原稿副本放入 `00-input/`。
3. 设计切分边界（建议每段 6-12 页）。

**阶段一决策点（ask_questions）**:
- 问题: `是否批准当前切分方案？`
- 建议选项: `批准（推荐）` / `调整切分规则` / `自定义（由用户填写）`

### 阶段二：分镜与并行产出

1. 在 `10-storyboards/` 生成/更新各段分镜稿。
2. 优先使用 sub-agent 并行产出不同分段。
3. 汇总分镜差异并形成统一约束。

**阶段二决策点（ask_questions）**:
- 问题: `是否进入 HTML 落地阶段？`
- 建议选项: `进入落地（推荐）` / `先修分镜后再落地` / `自定义（由用户填写）`

### 阶段三：HTML 落地、合并与回归

1. 在 `20-html/` 生成 `part1/part2/part3...`。
2. 运行 `run_merge_generic.py` 进行合并。
3. 运行 `extract_slide_titles.ps1` 检查关键页序。
4. 运行 `validate_storyboards_generic.py` 做门禁校验。

**阶段三决策点（ask_questions）**:
- 问题: `当前合并结果是否通过并进入交付？`
- 建议选项: `通过并交付（推荐）` / `再迭代一轮` / `自定义（由用户填写）`

## 🧭 ask_questions 标准决策卡片

建议在关键节点统一使用以下配置：

- `allowFreeformInput=true`（支持用户补充自定义策略）
- 对可并行内容使用 `multiSelect=true`
- 每次提问前先给出默认建议路径，再允许用户覆盖

## 🤝 推荐 Agent 组合

- **Plan**: 前期边界梳理与切分方案确认。
- **5.4 Beast Mode v3.1**: 并行生成分镜稿、HTML 文案细化、质量复审。
- **当前执行 Agent（GitHub Copilot）**: 落盘、脚本执行、回归验证与最终整合。

> 原则：分析与执行分离；并行产出后必须由单线程收敛。

## 🧰 配套脚本

- [init_topic_folder.py](./scripts/init_topic_folder.py)
  - 初始化专题目录与标准子目录：`00-input / 10-storyboards / 20-html / 90-tests`。
  - 自动创建分镜稿/测试记录/HTML 占位文件，并可复制输入原稿副本。
- [run_merge.py](./scripts/run_merge.py)
  - 调用项目已有 `docs/merge_scheme_c_parts.py` 进行合并。
- [run_merge_generic.py](./scripts/run_merge_generic.py)
  - 传入任意 3 个或以上分片 HTML，生成新的合并稿，不覆盖旧产物命名约定。
- [extract_slide_titles.ps1](./scripts/extract_slide_titles.ps1)
  - 从 HTML 提取页标题，快速检查首尾页与关键页序。
- [validate_storyboards.py](./scripts/validate_storyboards.py)
  - 校验三份分镜稿质量（禁用标记、必备章节、附录完整性）。
- [validate_storyboards_generic.py](./scripts/validate_storyboards_generic.py)
  - 用自定义 glob 扫描任意一组分镜稿，复用同一套门禁规则。

## 📁 产物约定（建议）

- 专题目录：`docs/{专题目录}/`
- 输入原稿副本：`docs/{专题目录}/00-input/{topic_code}-{标题}.md`
- 分镜稿：`docs/{专题目录}/10-storyboards/{topic_code}-0X-*-分镜稿.md`
- 分片 HTML：`docs/{专题目录}/20-html/{topic_code}-{方案}-partN.html`
- 合并 HTML：`docs/{专题目录}/20-html/{topic_code}-{方案}-合并.html`
- 测试记录：`docs/{专题目录}/90-tests/{topic_code}-90-技能测试记录_YYYYMMDD.md`

## ✅ 质量门禁

- 禁止残留：`（轻）`、`（重）`、`这一页不做什么`。
- 必须具备：
  - 每页 `页面目标/页面完整文案/演讲备注`
  - 过渡句
  - 行动页口播三步法
  - 附录A 页码映射
  - 附录B 质量检查清单

## 🔗 参考资料

- 详见 [workflow.md](./references/workflow.md)
- 编号规则见 [numbering-rules.md](./references/numbering-rules.md)
