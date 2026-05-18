# HTML Deck Pipeline Skill

端到端 HTML 讲稿生产流水线 —— 从需求问询到定版归档，输出可独立部署的网站骨架，内置 WYSIWYG 样式编辑器。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 核心能力

| 维度 | 说明 |
| ---- | ---- |
| **六阶段流水线** | A（问询）→ B（架构）→ C（分镜）→ D（生成）→ E（验收）→ F（归档），门禁停顿，不可越级 |
| **网站骨架输出** | CSS 三层架构 + Hash 路由 + 自适应缩放 + 一键导出 HTML/PPTX |
| **四主题 × 三字号** | 暗色 / 暗色2 / 亮色 / 青律 × 标准 / 高对比 / 大字号，独立切换 |
| **WYSIWYG 编辑器** | 样式编辑、文本编辑、拖拽重排、多选对齐/分布、撤销/重做、持久化保存 |
| **配置驱动** | 主题/字号从 `config.yaml` 读取，新增选项无需改代码 |

## 快速开始

### 启动预览服务器

```bash
# 安装依赖
pip install pyyaml

# 启动服务
python container/serve.py <target_dir> --theme dark-theme-2 --port 8080
```

浏览器打开 `http://localhost:8080` 即可预览幻灯片。

### 启动热重载模式

```bash
python container/serve.py <target_dir> --theme dark-theme-2 --watch
```

文件修改后浏览器自动刷新。

### 导出

- **导出 HTML**：点击页面底部「导出 HTML」按钮，生成单文件静态 HTML
- **导出 PPTX**：点击「导出 PPTX」按钮；若浏览器端失败，自动回落 Playwright 截图方案

## 目录结构

```text
html-deck-pipeline-skill/
├─ SKILL.md                         # 主流程文档（完整流程说明）
├─ README.md                        # 项目说明（本文件）
├─ LICENSE                          # MIT 许可证
├─ CHANGELOG.md                     # 更新日志
├─ examples/<style-id>/             # 风格资产（style-contract + style-showcase）
├─ references/                      # 规范与门禁参考文档（20 篇）
├─ templates/                       # 初始化模板（init_topic、stage-b）
├─ internal-skill/                  # 内置辅助技能
│  ├─ scrapling-web-fetch/          # 网页抓取
│  ├─ web-style-extraction/         # 风格提取
│  ├─ html-deck-to-pptx/            # PPTX 导出保底方案
│  └─ measure-utilization/          # 页面利用率检测
├─ container/                       # 网站骨架容器
│  ├─ index.html                    # 预览外壳
│  ├─ serve.py                      # 本地开发服务器（含 --watch 热重载）
│  ├─ config.json                   # 全局配置（日志/编辑器/组件）
│  ├─ js/
│  │  ├─ deck.js                    # 幻灯片引擎（路由/导航/缩放/导出）
│  │  ├─ editor-state.js            # 编辑器共享状态
│  │  ├─ editor-undo.js             # 撤销/重做管理器
│  │  ├─ editor.js                  # WYSIWYG 样式编辑器
│  │  └─ logger.js                  # 调试日志系统
│  ├─ css/
│  │  ├─ config.yaml                # 主题与字号配置
│  │  ├─ common/                    # base.css + components.css + editor.css
│  │  ├─ fontsize/                  # 字号方案（standard / high-contrast / large）
│  │  └─ theme/                     # 主题 tokens（dark-theme / dark-theme-2 / light-theme / qclaw-theme）
│  └─ tests/                        # 自动化测试
└─ scripts/                         # 工具脚本
   ├─ init_topic_folder.py          # 初始化工作目录
   ├─ validate_storyboards_generic.py  # 分镜质量校验
   ├─ validate_tokens.py            # 主题 Token 完整性 + 对比度校验
   └─ measure_utilization.py        # 页面利用率检测
```

## CSS 架构

```
加载顺序：tokens.css → fontsize.css → base.css → components.css
              ↑              ↑            ↑             ↑
         css/theme/     css/fontsize/  css/common/  css/common/
        (主题配色)      (字号变量)     (舞台布局)   (组件样式)
```

- **tokens.css** — 每个主题一套 CSS 自定义属性（`--bg`、`--text`、`--accent`…），30+ token
- **fontsize.css** — 五级字号变量（`--text-xs` ~ `--text-xl`），3 套方案
- **base.css** — 舞台几何、导航、控件样式
- **components.css** — 面板、卡片、表格、标签等 20+ 共享组件

切换主题仅交换 1 个文件（tokens.css）；切换字号仅交换 1 个文件（fontsize.css）。

## 如何新增主题/字号

编辑 `container/css/config.yaml`：

```yaml
themes:
  - id: new-theme
    label: 新主题
  - id: dark-theme-2
    label: 暗色2
    default: true

fontsizes:
  - id: standard
    label: 标准
    default: true
  - id: xlarge
    label: 超大
```

然后在对应目录下创建 CSS 文件即可，无需修改 JS/HTML。

## WYSIWYG 编辑器功能

| 功能 | 操作 | 快捷键 |
| ---- | ---- | ------ |
| 样式编辑 | 点击选中 → 面板修改 CSS | — |
| 文本编辑 | 双击文字 → contentEditable + 富文本工具栏 | Esc 取消, Enter 确认 |
| 拖拽重排 | 拖动卡片/面板交换位置 | — |
| 添加组件 | 面板底部组件调色板（8 种组件） | — |
| 多选对齐 | Shift+点击 → 对齐工具栏 | — |
| 水平/垂直分布 | 多选后点击分布按钮 | — |
| 容器布局切换 | 选中容器 → 切换列数/排列方向 | — |
| 删除元素 | 选中 → 删除按钮 | — |
| 复制元素 | 选中 → 复制按钮 | — |
| 撤销/重做 | 按钮或快捷键 | Ctrl+Z / Ctrl+Y |
| 保存 | 保存按钮 / 退出时确认 | POST /save |

## 六阶段流水线

| 阶段 | 名称 | 核心产出 | 门禁 |
| ---- | ---- | -------- | ---- |
| A | 问询与对齐 | 需求冻结快照、风格决策、工作目录 | 用户确认 |
| B | 结构规划 | 总分总结构、版本号、框架文档 | 用户确认 |
| C | 分镜编写 | 全量分镜稿（文案/备注/样式标注） | 质量门禁 + 样式多样性 |
| D | 页面生成 | HTML 页面 + 网站骨架 + 本地预览 | 自查回路 |
| E | 验收发布 | 单文件 HTML + PPTX 定版 | 双向验证 |
| F | 归档总结 | 版本归档、经验沉淀 | 用户确认 |

关键约束：阶段顺序强制、分镜先行、版本同步、一页一文件、定版双输出。

## 开发

### 运行测试

```bash
# 单元测试
node container/tests/test-editor-unit.js

# E2E 测试（需 Playwright）
pip install playwright && playwright install chromium
python container/tests/test-editor-e2e.py --target-dir <target_dir>
```

### 验证主题 Token

```bash
python scripts/validate_tokens.py [--theme dark-theme-2] [--json]
```

检查所有主题是否定义了完整的 30+ 设计令牌，并验证 WCAG 对比度。

## 许可

[MIT License](LICENSE)
