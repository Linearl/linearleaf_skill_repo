# 编号与命名规则

适用范围：`html-deck-pipeline-skill` 全流程。

## 目标

- 文件可稳定排序、可并行生成、可自动合并
- 版本迭代清晰（`v-01`、`v-02`...）
- 沟通记录可追溯（真实日期）

## 一、目录结构（固定）

- `{work_dir}/00-input/`
- `{work_dir}/10-storyboards/v-XX/`
- `{work_dir}/20-html/v-XX/`
- `{work_dir}/90-tests/`

其中 `v-XX` 为两位版本目录（如 `v-01`、`v-02`）。

## 二、核心编号规则

### 1) 版本号

- 格式：`v-XX`
- 规则：分镜、HTML、合并稿必须同版本。

### 2) 分片号

- 格式：`{part_no:02d}`，从 `01` 递增。
- 推荐分片名：`开头/基础篇/进阶篇/收官篇/结尾`（可按需调整）。

### 3) 分镜命名（强制）

- 格式：`{part_no:02d}-{part_name}-分镜稿.md`
- 示例：`01-开头-分镜稿.md`

### 4) HTML 分片命名（强制）

- 格式：`{part_no:02d}-{part_name}.html`
- 示例：`01-开头.html`

### 4.1) 页内右上角编号规则（新增）

- 分片 HTML 允许使用章节内局部编号（如 `01 / 04`）。
- 合并稿必须重写为全局编号（如 `01 / 37` ... `37 / 37`）。
- 合并后若仍存在局部编号，视为门禁失败并回退修正。

### 5) 沟通记录命名（强制真实日期）

- 原始记录：`A-raw-round{round_no:02d}-{yyyymmdd}.md`
- 总结记录：`A-summary-round{round_no:02d}-{yyyymmdd}.md`
- 冻结快照：`A-freeze-input-snapshot-{yyyymmdd}.md`

示例：

- `A-raw-round01-20260316.md`
- `A-summary-round01-20260316.md`
- `A-freeze-input-snapshot-20260316.md`

> 禁止保留 `YYYYMMDD` 占位名。

## 三、合并稿命名（推荐）

- 格式：`{topic_code}-{scheme_name}-合并.html`
- 说明：合并稿可保留 `topic_code / scheme_name`，便于多方案并存。

## 四、测试记录命名（推荐）

- 格式：`{topic_code}-90-技能测试记录_{yyyymmdd}.md`

## 五、执行注意

1. 阶段 A 结束后立即完成真实日期重命名/落盘。
2. 阶段 C/D 生成文件时必须检查编号连续性（01,02,03...）。
3. 文件名必须保留数字前缀，避免中文排序错位。
4. 进入 `v-(n+1)` 时，先升级分镜，再生成同版本 HTML。
