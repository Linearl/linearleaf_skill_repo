# 并行 HTML 生成作业手册（Playbook）

本文件是阶段 D.1 的详细作业规范。

## 生成前准备

- 已完成并冻结分镜
- 已冻结风格资产（`style-contract` + `style-showcase`）
- 已确认版本号与命名规则

## Sub-agent 指令要点

并行生成前，必须明确告知：

- 先读取已冻结风格资产，不得自创风格来源
- 必须同时读取：`style-contract-<style-id>.md` 与 `style-showcase-<style-id>.html`
- 产出前先回传“已读取文件清单”，未回传视为未满足前置条件
- 示例用于对齐风格语言，不是逐页照抄
- 需满足冻结后的 `ratio_mode`（默认 16:9，可选 4:3 / 16:10 / adaptive）、可访问性基线、统一版本号

## 并行派发最小指令包（必填）

每个 sub-agent 任务至少包含以下字段：

- 分镜文件路径
- 风格描述文件路径（style-contract）
- 风格展示文件路径（style-showcase）
- 目标 HTML 输出路径
- 必做限制（无 `#progress`、无 `prevBtn/nextBtn`、遵守无障碍基线）

## 文件命名

- HTML 分片命名：`{part_no:02d}-{part_name}.html`

## 质量控制

- 页面内容仅保留观众可见信息，讲者提示放备注链路
- 不允许同章节连续复用单一版式骨架
- 分片完成后再做合并与页序校验

## 失败回退

- 如出现风格漂移、页序错乱、同质化严重，回退到分镜阶段修正后再生成
