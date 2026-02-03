---
name: "Investment Analysis (A股投资分析)"
description: "Systematic investment research workflow for A-share market using AI-powered analysis. Use when conducting sector selection, supply chain analysis, financial report verification, or market sentiment evaluation. 系统化的 A 股投资研究工作流程，适用于赛道筛选、产业链分析、财报验证和市场情绪评估。"
---

# Investment Analysis Skill (A股投资分析技能)

## Overview

This skill provides a systematic AI-powered investment research framework specifically designed for A-share market analysis. It helps investors identify promising sectors, analyze supply chains, verify business fundamentals, and evaluate market timing through structured prompts and cross-model validation.

本技能为 A 股市场分析提供系统化的 AI 投研框架，帮助投资者通过结构化的提示词和跨模型验证，识别潜力赛道、分析产业链、验证业务真实性并评估市场时机。

## When to Use

Use this skill when you need to:
- Identify emerging sectors based on upcoming events and policies (赛道筛选)
- Analyze supply chain structure and identify key players (产业链挖掘)
- Verify company fundamentals through financial reports (深度去伪)
- Evaluate market sentiment and timing (择时分析)
- Cross-validate investment thesis across different AI models (交叉验证)

适用场景：
- 基于即将到来的事件和政策识别新兴赛道
- 分析供应链结构并识别关键参与者
- 通过财报验证公司基本面
- 评估市场情绪和介入时机
- 跨 AI 模型交叉验证投资逻辑

## Core Workflow

### Phase 1: Sector Selection (赛道筛选)

**Objective**: Use AI's information breadth to identify short-term opportunity sectors based on upcoming events (conferences, policies, seasonal factors).

**Process**:
1. Gather context about current market environment
2. Identify upcoming catalysts (1-2 months outlook)
3. Rank sectors by importance and certainty
4. Extract core investment thesis for each sector
5. Identify 1-2 leading stocks as references

**Recommended Models**: DeepSeek, Gemini Deep Research, ChatGPT

### Phase 2: Supply Chain Analysis (产业链挖掘)

**Objective**: After identifying target sector, drill down to specific supply chain segments and high-value components.

**Process**:
1. Decompose sector into core supply chain components
2. Identify segments with highest value contribution
3. Find A-share leaders in each segment
4. Discover "picks and shovels" stocks (universal suppliers)
5. Map competitive landscape

### Phase 3: Fundamental Verification (深度去伪)

**Objective**: Validate investment thesis through financial reports and business fundamentals, distinguish real business from speculation.

**Process**:
1. Collect and upload financial reports/research reports
2. Verify revenue contribution from target business
3. Identify specific customers or production timeline
4. Assess major risk factors
5. Calculate valuation metrics

### Phase 4: Sentiment & Timing Analysis (情绪与择时)

**Objective**: Evaluate market sentiment and determine optimal entry points.

**Process**:
1. Analyze recent price action and trend
2. Assess current market sentiment
3. Evaluate if current price reflects future expectations
4. Identify potential catalysts or risks
5. Determine entry/exit strategy

### Phase 5: Cross-Model Validation (跨模型验证)

**Objective**: Use different AI models to cross-validate findings and avoid single-model bias.

**Process**:
1. Run same analysis through multiple models
2. Compare recommendations and identify discrepancies
3. Challenge assumptions and reasoning
4. Identify potential blind spots
5. Synthesize final conclusion

## Prompt Templates

### Template 1: Sector Selection

```
I am conducting A-share short-term opportunity research. Based on the market environment in [CURRENT_YEAR + MONTH], and major events occurring in [NEXT_1-2_MONTHS] (such as industry conferences, policy releases, seasonal factors), please list 3-5 sectors most likely to experience active trading.

Requirements:
1) Rank by importance and certainty
2) Provide core catalyst for each sector
3) List 1-2 representative leading stocks for reference

我正在进行 A 股短期热点研究。请结合[当前年份+月份]的市场环境，以及[未来 1-2 个月]即将发生的重大事件（如行业大会、政策发布、季节性因素），列出最有可能进行热门炒作的 3-5 个板块。

要求：
1) 按重要度和确定性排序
2) 给出每个板块的核心炒作逻辑（Catalyst）
3) 列出该板块对应的 1-2 个代表性龙头股作为参考
```

### Template 2: Supply Chain Analysis

```
Assuming we are bullish on [SECTOR: humanoid robots/low-altitude economy/solid-state batteries/commercial space], please act as a professional industry analyst and help me dissect this industry's core supply chain:

1) Which segments have the highest value contribution? (e.g., ball screws, sensors, battery materials)
2) For each core segment, who are the absolute leaders in A-shares?
3) Are there any "picks and shovels" stocks (companies needed regardless of who wins)?

假设我们看好[人形机器人/低空经济/固态电池/商业航天]板块。请像一个专业的行业分析师一样，帮我拆解这个产业的核心供应链：

1) 哪些环节价值量最高？（例如：丝杠、传感器、电池材料）
2) 针对每个核心环节，A 股目前的绝对龙头分别是谁？
3) 有没有那种"铲子股"（不管谁赢，都需要用它的产品）？
```

### Template 3: Financial Report Verification

```
Please carefully review this financial/research report from [COMPANY_NAME]:

1) Is this company's [robots/AI/commercial space] business pure speculation, or does it have substantial revenue? What's the revenue proportion?
2) Does the report mention specific customers (such as Tesla, Huawei) or clear mass production timeline?
3) As an investor, what do you think is the biggest risk in this report?

请仔细阅读这份[公司名]的财报/研报：

1) 这家公司的[机器人/AI/商业航天]业务是纯概念炒作，还是已经有实质性收入？收入占比多少？
2) 报告中是否提到了具体客户（如特斯拉、华为）或明确的量产时间表？
3) 作为投资者，你认为这份报告中最大的风险点是什么？
```

### Template 4: Sentiment & Timing Check

```
[STOCK_A], [STOCK_B] have experienced [describe trend, e.g., "a sharp rally followed by correction"] in the past two months. Given current market sentiment, would entering now be chasing highs?

[公司名1]、[公司名2]在过去两个月已经经历了[描述走势，如：一波大涨后的回调]。结合当前的市场情绪，现在介入是否属于追高？
```

### Template 5: Cross-Model Validation

```
Someone suggested I focus on [STOCK_A] and [STOCK_B] as sector leaders.

1) Do you agree? If not, please explain why.
2) Why weren't these two in your recommendation list?
3) Are there any companies that were overlooked but are indispensable in the supply chain?

有人建议我关注[股票A]和[股票B]作为该板块的龙头。

1) 你是否认同？如果不认同，请给出理由
2) 你的推荐列表中为什么没有这两只？
3) 还有没有被它忽略的、但在供应链中不可或缺的公司？
```

## Best Practices

### Model Selection
- **DeepSeek**: Excellent for Chinese market analysis and A-share specific knowledge
- **Gemini Deep Research**: Best for comprehensive research with extensive web search
- **ChatGPT**: Good for general analysis and structured reasoning

### Research Workflow
1. **Start Broad**: Begin with sector selection to identify macro trends
2. **Drill Down**: Move to supply chain analysis for specific opportunities
3. **Verify**: Always validate with financial reports and business fundamentals
4. **Cross-Check**: Use multiple AI models to avoid bias
5. **Document**: Keep track of your analysis and reasoning

### Risk Management
- Never rely solely on AI recommendations
- Always verify information with official sources
- Use AI as a research assistant, not a decision maker
- Understand that past performance doesn't guarantee future results
- Consider your own risk tolerance and investment horizon

## Important Disclaimers

⚠️ **Critical Reminders**:
- This skill is for **research assistance only**, not investment advice
- AI models can hallucinate or provide outdated information
- Always verify information through official channels
- Market conditions change rapidly; recent AI training data may be outdated
- Conduct your own due diligence before making investment decisions
- Past performance is not indicative of future results

**风险提示**：
- 本技能仅供研究辅助，不构成投资建议
- AI 模型可能产生幻觉或提供过时信息
- 务必通过官方渠道验证信息
- 市场瞬息万变，AI 训练数据可能滞后
- 投资前请进行独立尽职调查
- 过往表现不代表未来收益

## Integration Points

This skill works best when combined with:
- Financial data platforms (东方财富, 同花顺, Wind)
- Official company disclosures (巨潮资讯网)
- Industry research reports
- Real-time market data

## Examples

See [examples/](examples/) directory for:
- Sample sector analysis workflow
- Supply chain mapping example
- Financial report verification case study
- Cross-model validation demonstration

## Version History

- **v1.0.0** (2026-02-03): Initial release
  - Core 5-phase workflow
  - 5 prompt templates for different research stages
  - Cross-model validation framework
  - Risk disclaimers and best practices

---

**Note**: Markets carry inherent risks. This skill provides a systematic research framework but does not guarantee investment success. Always make decisions based on your own analysis and risk tolerance.

**注**：市场有风险，入市需谨慎。本技能提供系统化的研究框架，但不保证投资成功。请基于自身分析和风险承受能力做出决策。
