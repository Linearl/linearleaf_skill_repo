# 分析工具使用说明

> **位置**: `.github/skills/analysis_code/tools/`

## 📋 工具清单

| 工具 | 用途 | 语言 |
|------|------|------|
| code-metrics-collector.py | 代码指标收集 | Python |

---

## 🔧 code-metrics-collector.py

Python 项目代码指标收集工具，用于自动收集和分析代码质量指标。

### 功能特点

- ✅ 自动收集代码行数、函数数、类数等基础指标
- ✅ 计算圈复杂度和复杂度分布
- ✅ 自动识别代码问题（长函数、高复杂度等）
- ✅ 生成质量评分 (0-100)
- ✅ 支持多种输出格式 (JSON/Markdown/Summary)

### 使用方法

#### 基本用法

```powershell
# 显示摘要
python tools/code-metrics-collector.py --project-path "C:/path/to/project"

# 输出 JSON
python tools/code-metrics-collector.py -p "项目路径" -f json -o metrics.json

# 输出 Markdown 报告
python tools/code-metrics-collector.py -p "项目路径" -f markdown -o report.md
```

#### 命令参数

| 参数 | 简写 | 必需 | 说明 |
|------|------|------|------|
| --project-path | -p | ✅ | 项目根目录路径 |
| --output | -o | ❌ | 输出文件路径 |
| --format | -f | ❌ | 输出格式: json/markdown/summary |
| --exclude | -e | ❌ | 排除的目录模式 |
| --verbose | -v | ❌ | 显示详细日志 |

#### 输出示例

**控制台摘要**:
```
==================================================
📊 代码分析摘要
==================================================
项目路径: C:/my_project
分析时间: 2025-01-20T10:30:00
质量评分: 🟢 85/100
==================================================
Python文件: 42
代码行数: 3500
函数数量: 120
类数量: 25
平均文件长度: 83.3 行
==================================================
复杂度分布:
  🟢 低: 95
  🟡 中: 20
  🟠 高: 4
  🔴 极高: 1
==================================================
```

### 收集的指标

| 指标类型 | 具体指标 |
|----------|----------|
| 规模指标 | 文件数、代码行数、空行数、注释行数 |
| 结构指标 | 函数数、类数、导入数 |
| 复杂度 | 圈复杂度、复杂度分布 |
| 质量指标 | 长函数、高复杂度函数、质量评分 |

### 质量评分说明

质量评分基于以下因素计算：

| 因素 | 影响 |
|------|------|
| 注释覆盖率 < 10% | -15 分 |
| 注释覆盖率 10-15% | -5 分 |
| 高复杂度函数 > 20% | -20 分 |
| 高复杂度函数 10-20% | -10 分 |
| 每个高严重度问题 | -5 分 |
| 每个中严重度问题 | -2 分 |

### 识别的问题类型

| 问题类型 | 触发条件 | 严重度 |
|----------|----------|--------|
| syntax_error | Python 语法错误 | 高 |
| high_complexity | 圈复杂度 > 10 | 中/高 |
| long_function | 函数超过 50 行 | 中 |
| long_file | 文件超过 500 行 | 低 |

---

## 🔗 与分析工作流集成

在分析工作流的第3步（收集项目数据）中使用此工具：

```powershell
# 进入 skill 目录
cd .github/skills/analysis_code

# 运行指标收集
python tools/code-metrics-collector.py `
    --project-path "要分析的项目路径" `
    --format json `
    --output "tasks/项目名_分析/1_初始质量评估/metrics/metrics.json"
```

收集的指标将用于：
- 建立代码质量基线
- 识别需要重点分析的模块
- 量化技术债务
- 评估改进效果

---

*工具版本: 1.0 | 基于 analysis_system/tools/code-metrics-collector.py*
