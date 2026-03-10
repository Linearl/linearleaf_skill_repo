---
name: html-presentation-generator
description: 端到端 HTML 演示文稿生成技能（主文档拆分→分镜稿→HTML落地→合并校验→预览）。当用户提到“上下文过长导致循环总结”“需要拆分分镜”“并行用 sub-agent 生成内容”“合并 part1/part2/part3 HTML 并检查页序”时启用。支持工作流固化、脚本化校验与改进闭环。
---

# HTML Presentation Generator

把“长文档一次性生成导致上下文失控”的任务，转成可并行、可校验、可回退的稳定流水线。

## 适用场景

- 用户反馈：对话不断总结、任务无法推进、上下文过长。
- 目标是产出讲稿型 HTML（分片 + 合并）并可预览验证。
- 需要先分镜再落地，且要支持中途改版与回归检查。

## 核心工作方式

1. **主文档拆分**：按章节边界拆成基础/进阶/收官（或其它业务分段）。
2. **并行产出分镜稿**：每段独立，优先用 sub-agent 并行生成与校对。
3. **分片落地 HTML**：每段对应一个 part HTML，单段内部先验证页序与文案。
4. **合并构建**：统一用合并脚本生成总稿（重排 `active` / `data-index` / 页码）。
5. **回归检查**：做结构一致性与质量检查（禁用词、附录、行动页口播等）。
6. **预览与迭代**：按页反馈，最小改动修复，重复合并验证。

## 推荐 Agent 组合

- **Plan**：前期边界梳理与切分方案确认。
- **5.4 Beast Mode v3.1**：并行生成分镜稿、HTML 文案细化、质量复审。
- **当前执行 Agent（GitHub Copilot）**：落盘、脚本执行、回归验证与最终整合。

> 原则：分析与执行分离；并行产出后必须由单线程收敛。

## 内置 Agent（便携）

技能目录已内置以下 Agent 文件，放到新工作区或离线环境时可直接随技能一起导入：

- `./agents/plan.agent.md`
- `./agents/gpt-5-beast-mode.agent.md`

适用场景：

- 新环境还没同步 `.github/agents/`，但需要立即复用既有 Agent 组合。
- 技能要打包分享给他人，希望“脚本 + 说明 + Agent”一次带走。
- 离线演示或受限环境下，需要从技能目录直接恢复工作流入口。

## 配套脚本

- [init_topic_folder.py](./scripts/init_topic_folder.py)
  - 初始化专题目录与标准子目录：`00-input / 10-storyboards / 20-html / 90-tests`。
  - 自动创建分镜稿/测试记录/HTML 占位文件，并可复制输入原稿副本。
- [run_merge.py](./scripts/run_merge.py)
  - 调用项目已有 `组内分享/merge_scheme_c_parts.py` 进行合并。
- [run_merge_generic.py](./scripts/run_merge_generic.py)
  - 传入任意 3 个或以上分片 HTML，生成新的合并稿，不覆盖旧产物命名约定。
- [extract_slide_titles.ps1](./scripts/extract_slide_titles.ps1)
  - 从 HTML 提取页标题，快速检查首尾页与关键页序。
- [validate_storyboards.py](./scripts/validate_storyboards.py)
  - 校验三份分镜稿质量（禁用标记、必备章节、附录完整性）。
- [validate_storyboards_generic.py](./scripts/validate_storyboards_generic.py)
  - 用自定义 glob 扫描任意一组分镜稿，复用同一套门禁规则。

## 执行流程（简版）

1. 运行 `init_topic_folder.py` 初始化专题目录和编号骨架。
2. 在 `00-input` 放入输入原稿副本并确定切分边界（建议每段 6-12 页）。
3. 在 `10-storyboards` 生成/更新分镜稿。
4. 在 `20-html` 生成对应 `part1/part2/part3`。
5. 运行 `run_merge_generic.py` 合并（输入为 `20-html` 下分片）。
6. 运行 `extract_slide_titles.ps1` 检查关键页序。
7. 运行 `validate_storyboards_generic.py --root <专题目录> --glob "10-storyboards/*分镜稿.md"` 校验。
8. 修复问题后重复 5~7，直到通过。

## 详细说明

- 详见 [workflow.md](./references/workflow.md)
- 编号规则见 [numbering-rules.md](./references/numbering-rules.md)

## 产物约定（建议）

- 专题目录：`组内分享/docs/{专题目录}/`
- 输入原稿副本：`组内分享/docs/{专题目录}/00-input/{topic_code}-{标题}-组内分享.md`
- 分镜稿：`组内分享/docs/{专题目录}/10-storyboards/{topic_code}-0X-*-分镜稿.md`
- 分片 HTML：`组内分享/docs/{专题目录}/20-html/{topic_code}-{方案}-partN.html`
- 合并 HTML：`组内分享/docs/{专题目录}/20-html/{topic_code}-{方案}-合并.html`
- 测试记录：`组内分享/docs/{专题目录}/90-tests/{topic_code}-90-技能测试记录_YYYYMMDD.md`

## 质量门禁

- 禁止残留：`（轻）`、`（重）`、`这一页不做什么`。
- 必须具备：
  - 每页 `页面目标/页面完整文案/演讲备注`
  - 过渡句
  - 行动页口播三步法
  - 附录A 页码映射
  - 附录B 质量检查清单
