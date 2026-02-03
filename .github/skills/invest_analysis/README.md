# Investment Analysis Skill (A股投资分析技能)

<p align="center">
  <strong>🎯 系统化 AI 投研框架 | Systematic AI-Powered Investment Research</strong>
</p>

---

## 📖 概述 | Overview

Investment Analysis Skill 是专为 A 股市场设计的系统化投资研究技能，提供从赛道筛选到择时分析的完整工作流程。通过结构化的提示词模板和跨模型验证机制，帮助投资者更高效地进行投资研究。

The Investment Analysis Skill is a systematic investment research framework specifically designed for the A-share market, providing a complete workflow from sector selection to timing analysis. Through structured prompt templates and cross-model validation mechanisms, it helps investors conduct investment research more efficiently.

---

## ✨ 核心功能 | Key Features

### 🔍 1. 赛道筛选 (Sector Selection)
利用 AI 的信息广度，结合即将发生的重大事件（会议、政策、季节性因素），识别短期可能爆发的投资方向。

Leverage AI's information breadth to identify short-term opportunity sectors based on upcoming events (conferences, policies, seasonal factors).

### ⛓️ 2. 产业链挖掘 (Supply Chain Analysis)
深入拆解产业链条，找到价值量最高的环节和"铲子股"（通用供应商），避免只关注概念炒作。

Dissect supply chains to identify high-value segments and "picks and shovels" stocks, avoiding pure speculation.

### 📊 3. 深度去伪 (Fundamental Verification)
通过财报和研报验证业务真实性，区分纯概念炒作与实质性业务，评估关键风险因素。

Verify business fundamentals through financial reports, distinguish speculation from real business, and assess key risks.

### 📈 4. 择时分析 (Timing Analysis)
评估市场情绪和当前价格，判断介入时机是否合理，避免追高。

Evaluate market sentiment and current pricing to determine optimal entry points and avoid chasing highs.

### 🔄 5. 跨模型验证 (Cross-Model Validation)
利用不同 AI 模型的优势互补，交叉验证投资逻辑，减少单一模型的偏差和幻觉。

Cross-validate investment thesis using different AI models to reduce bias and hallucinations.

---

## 🚀 快速开始 | Quick Start

### 使用场景 | Use Cases

使用本技能当你需要：
- ✅ 寻找下一个可能爆发的投资主题
- ✅ 深入了解某个行业的供应链结构
- ✅ 验证一家公司的业务是否真实
- ✅ 评估当前介入某只股票是否合适
- ✅ 对比不同 AI 给出的投资建议

Use this skill when you need to:
- ✅ Identify the next potential investment theme
- ✅ Understand supply chain structure of an industry
- ✅ Verify if a company's business is real
- ✅ Evaluate if current timing is right for entry
- ✅ Compare investment recommendations from different AIs

### 推荐模型 | Recommended Models

| 模型 | 适用场景 | 优势 |
|------|---------|-----|
| **DeepSeek** | A 股专项分析 | 中文市场理解深入，A 股知识丰富 |
| **Gemini Deep Research** | 综合研究 | 网络搜索能力强，信息覆盖广 |
| **ChatGPT** | 通用分析 | 逻辑推理能力强，结构化输出好 |

---

## 📋 提示词模板 | Prompt Templates

### 模板 1：赛道筛选

**目的**：找到短期可能爆发的投资方向

**替换规则**：
- `[当前年份+月份]` → 如 "2026年2月"
- `[未来1-2个月]` → 如 "2026年3-4月"

```text
我正在进行 A 股短期热点研究。请结合[当前年份+月份]的市场环境，以及[未来 1-2 个月]即将发生的重大事件（如行业大会、政策发布、季节性因素），列出最有可能进行热门炒作的 3-5 个板块。

要求：
1) 按重要度和确定性排序
2) 给出每个板块的核心炒作逻辑（Catalyst）
3) 列出该板块对应的 1-2 个代表性龙头股作为参考
```

### 模板 2：产业链挖掘

**目的**：找到产业链中价值量最高的环节和"铲子股"

**替换规则**：
- `[板块名称]` → 如 "人形机器人" / "低空经济" / "固态电池" / "商业航天"

```text
假设我们看好[人形机器人/低空经济/固态电池/商业航天]板块。请像一个专业的行业分析师一样，帮我拆解这个产业的核心供应链：

1) 哪些环节价值量最高？（例如：丝杠、传感器、电池材料）
2) 针对每个核心环节，A 股目前的绝对龙头分别是谁？
3) 有没有那种"铲子股"（不管谁赢，都需要用它的产品）？
```

### 模板 3：财报验证

**目的**：验证公司业务真实性，区分概念炒作与实质业务

**替换规则**：
- `[公司名]` → 如 "优必选" / "小鹏汽车"
- `[业务类型]` → 如 "机器人" / "AI" / "商业航天"

**使用方式**：配合上传财报或研报文件

```text
请仔细阅读这份[公司名]的财报/研报：

1) 这家公司的[机器人/AI/商业航天]业务是纯概念炒作，还是已经有实质性收入？收入占比多少？
2) 报告中是否提到了具体客户（如特斯拉、华为）或明确的量产时间表？
3) 作为投资者，你认为这份报告中最大的风险点是什么？
```

### 模板 4：择时分析

**目的**：评估当前介入时机是否合理

**替换规则**：
- `[公司名1]`、`[公司名2]` → 如 "三六零" / "科大讯飞"
- `[描述走势]` → 如 "一波大涨后的回调" / "连续三个月横盘整理"

```text
[公司名1]、[公司名2]在过去两个月已经经历了[描述走势，如：一波大涨后的回调]。结合当前的市场情绪，现在介入是否属于追高？
```

### 模板 5：跨模型验证

**目的**：用不同 AI 模型交叉验证，避免单一模型偏差

**替换规则**：
- `[股票A]`、`[股票B]` → 如 "宁德时代" / "比亚迪"

```text
有人建议我关注[股票A]和[股票B]作为该板块的龙头。

1) 你是否认同？如果不认同，请给出理由
2) 你的推荐列表中为什么没有这两只？
3) 还有没有被它忽略的、但在供应链中不可或缺的公司？
```

---

## 🔄 标准工作流程 | Standard Workflow

```
第一步：赛道筛选
    ↓
第二步：产业链挖掘
    ↓
第三步：财报验证
    ↓
第四步：择时分析
    ↓
第五步：跨模型验证
    ↓
最终决策
```

### 详细流程说明

1. **赛道筛选**：使用模板1，在 DeepSeek/Gemini 中运行，获得 3-5 个候选板块
2. **产业链挖掘**：选定 1-2 个板块，使用模板2 深入分析供应链
3. **财报验证**：下载候选公司的财报/研报，使用模板3 验证业务真实性
4. **择时分析**：使用模板4 评估当前价格和介入时机
5. **跨模型验证**：将同样的问题在不同模型中运行，使用模板5 交叉验证

---

## ⚠️ 重要提示 | Important Disclaimers

### 风险警示

- ❌ **本技能不构成投资建议**
- ❌ **AI 可能产生幻觉或提供过时信息**
- ❌ **务必通过官方渠道验证所有信息**
- ❌ **市场有风险，入市需谨慎**

### 最佳实践

- ✅ 将 AI 作为研究助手，而非决策者
- ✅ 始终进行独立尽职调查
- ✅ 使用多个模型交叉验证
- ✅ 验证所有关键信息的来源
- ✅ 了解自己的风险承受能力

---

## 📚 学习资源 | Resources

### 推荐数据源

- **东方财富网** (eastmoney.com): A 股行情、财报数据
- **巨潮资讯网** (cninfo.com.cn): 官方信息披露平台
- **同花顺** (10jqka.com.cn): 财经资讯、研报
- **Wind 终端**: 专业金融数据库

### 补充阅读

- 《证券分析》(Benjamin Graham)
- 《聪明的投资者》(Benjamin Graham)
- 《投资最重要的事》(Howard Marks)

---

## 🤝 贡献 | Contributing

欢迎提交改进建议和使用案例！

Contributions and use cases are welcome!

---

## 📜 许可证 | License

MIT License - 详见 [LICENSE](../LICENSE)

---

<p align="center">
  <strong>⚠️ 市场有风险，投资需谨慎 | Markets Carry Risks - Invest Wisely</strong>
</p>

<p align="center">
  <em>本技能仅供学习研究使用，不构成任何投资建议</em><br>
  <em>This skill is for educational and research purposes only, not investment advice</em>
</p>
