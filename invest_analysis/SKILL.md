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

This skill implements a comprehensive multi-phase workflow for systematic investment research:

### Phase 1: Sector Selection (Step1 - 赛道筛选)

**Objective**: Use AI's information breadth to identify short-term opportunity sectors based on upcoming events (conferences, policies, seasonal factors).

**Process**:
1. Gather context about current market environment
2. Identify upcoming catalysts (1-2 months outlook based on conferences, policies, seasonal events)
3. Rank 3-5 sectors by importance and certainty
4. Extract core investment thesis (催化逻辑) for each sector
5. Identify 1-2 leading stocks as references per sector

**Output**:
- Document: `01_赛道筛选_YYYYQx_A股潜在爆发行情.md`
- Directory: `step1/`

**Checkpoints**:
- ✅ Is the catalyst source明确?
- ✅ Are representative leading stocks provided?
- ✅ Is the ranking logic explained?

**Recommended Models**: DeepSeek, Gemini Deep Research, ChatGPT

### Phase 2: Supply Chain Analysis (Step2 - 产业链挖掘)

**Objective**: After identifying target sector, drill down to specific supply chain segments and high-value components (找铲子).

**Process**:
1. Create separate analysis for each sector from Step1
2. Decompose sector into core supply chain components
3. Identify segments with highest value contribution (价值量最高处)
4. Find A-share leaders in each segment
5. Discover "picks and shovels" stocks (铲子股 - universal suppliers)
6. Map competitive landscape and backup candidates

**Output**:
- Documents: `02A~02E_产业链挖掘_{赛道}_YYYYQx.md` (one per sector)
- Stock list: `step2/02_标的清单.yaml` (fields: name, track, code)
- Directory: `step2/`

**Checkpoints**:
- ✅ Does it include key segments/value contribution/picks-and-shovels analysis?
- ✅ Are A-share leaders and backups provided?
- ✅ Is the YAML stock list generated for downstream steps?

### Phase 3: Fundamental Verification (Step3 - 深度去伪/财报验证)

**Objective**: Validate investment thesis through financial reports and business fundamentals, distinguish real business from speculation. Separated into 3 layers: automated download/extraction and manual analysis.

#### Step3a: Financial Report Download (财报获取 - 自动化)

**Objective**: Automatically download annual and quarterly reports for all stocks from Step2.

**Process**:
1. Read `step2/02_标的清单.yaml` for stock codes
2. Use CNINFO API to download latest annual/quarterly reports
3. Save reports as PDF files by stock code

**Output**:
- Directory: `step3/financials/{代码_名称}/`
- Contents: `{年份}_annual_report.pdf`, `{季度}_quarterly_report.pdf`

**Tools** (automation):
- Download script: `step3/tools/step3a_download_reports.py`
- Config: Input `step2/02_标的清单.yaml`

**Checkpoints**:
- ✅ Are all reports for Step2 stocks downloaded?
- ✅ Are reports organized by stock code and year/quarter?
- ✅ Are missing reports logged for manual intervention?

#### Step3b: Financial Report Content Extraction (财报内容提取 - 自动化)

**Objective**: Extract key sections from downloaded reports using AI or OCR for structured analysis.

**Process**:
1. Read PDF reports from `step3/financials/`
2. Extract key sections: 产品分类、主要客户、订单信息、风险因素、收入和毛利
3. Generate extraction summaries with timestamps
4. Create searchable index for manual review

**Output**:
- Extracts: `step3/extracts/{代码_名称}_annual_extract.txt`, `quarterly_extract.txt`
- Index: `step3/extracts/extraction_index.yaml` (fields: code, name, sections, extraction_date)
- Directory: `step3/extracts/`

**Tools** (automation):
- Extraction script: `step3/tools/step3b_extract_content.py`
- Supports: PDF text extraction, structured data parsing
- Config: Rules for section identification

**Checkpoints**:
- ✅ Are key sections extracted for all reports?
- ✅ Is extracted content organized and searchable?
- ✅ Are extraction timestamps recorded?

#### Step3c: Financial Report Analysis & Verification (财报阅读分析 - AI + 人工)

**Objective**: Deep-read extracted content and manual reports to verify business fundamentals and identify red flags.

**Process** (Human-Driven with AI Assistance):
1. **Manual Reading** ⭐: Open extracted content and original PDF side-by-side
   - Read "产品分类" section: Is new business substantial or just R&D?
   - Read "主要客户" section: Are there real customer names with order volumes?
   - Read "风险因素" section: Are there hidden risks or competitive threats?
2. **AI-Assisted Writing**: Use AI to help structure natural language conclusions
   - Evidence-based writing: Must cite specific report sections and numbers
   - Risk identification: List top 3-5 risks with supporting evidence
   - Business assessment: Determine if business is "real", "trial", or "speculation"
3. **Generate Analysis Report**: Write individual report per stock with findings
4. **Summary Table**: Create consolidated verification table

**Critical Requirements**:
- ⚠️ **Human judgment is essential**: AI extraction is prep work, your reading is the judgment
- ⚠️ Conclusions must use natural language with specific evidence points (e.g., "Customer A ordered 1000 units in Q3 per page 45")
- ⚠️ Identify business landing evidence + risk concentration + disclosure gaps
- ⚠️ No template-like statements; distinguish "announced plans" vs "actual sales"
- ⚠️ No long original text quotations; summarize in your own words with citations

**Output**:
- Individual Reports: `step3/analysis/03_{赛道}_{代码}_{名称}.md`
- Summary Table: `step3/report/03_汇总_结论表.md`
  - Fields: Code, Name, Track, Business Reality, Key Risks, Revenue Proportion, Recommendation
- Directory: `step3/`

**Tools** (AI assistance):
- Analysis helper script: `step3/tools/step3c_analysis_helper.py` (optional formatting tool)
- Config: Use extraction output from Step3b as input

**Checkpoints**:
- ✅ Have you personally read the extracted content and original reports?
- ✅ Are conclusions backed by specific quotes with page numbers?
- ✅ Is the recommendation clear: Bullish/Neutral/Bearish with 2-3 main reasons?
- ✅ Is Step3 summary table complete with all stocks from Step2?
- ✅ Have you identified key risks that would change your thesis if materialized?

### Phase 3.5: Supply Chain Verification (Step3.5 - 产业链验证 - 可选但推荐)

**Objective**: Cross-validate Step2's supply chain assumptions using evidence from financial reports and news events. Identify if assumed relationships actually exist in the market.

**Process**:
1. **Financial Report Cross-Check**: 
   - Review Step3c extracted content for customer/supplier relationships
   - Does Company A (identified as supplier in Step2) mention Company B (identified as customer) in their reports?
   - Are order volumes and cooperation status mentioned?
   - Red flag: Assumed relationship but no mutual mention in reports
2. **News Event Verification**:
   - Check Step4 news for partnership announcements between Step2 companies
   - Validate if supply chain relationships have been publicly announced
   - Identify new partnerships not covered in Step2 analysis
3. **Competitive Threat Assessment**:
   - Are there alternative suppliers or competitors emerging?
   - Has any Step2 company lost market share to new entrants?
   - Identify potential disruption to the assumed supply chain structure
4. **Supply Chain Risk Mapping**:
   - Identify bottleneck positions (single supplier or customer dependency)
   - Assess concentration risk: If key company fails, does entire chain collapse?

**Output**:
- Verification report: `step3.5/report/03.5_供应链验证表.md`
- Fields: Company, Role, Assumed Relationships, Evidence Found, Confidence Level, Risks
- Risk mapping: `step3.5/report/03.5_供应链风险地图.md`
- Directory: `step3.5/`

**Tools** (optional automation):
- Verification script: `step3.5/tools/step3.5_supply_chain_verify.py`
- Input: Step2 supply chain structure + Step3c analysis reports + Step4 news data

**Checkpoints**:
- ✅ Are supply chain relationships verified with evidence from financial reports?
- ✅ Have you identified companies mentioned in Step2 but without actual business relationships?
- ✅ Are bottleneck positions clearly marked?
- ✅ Is the confidence level for each relationship documented?

**Impact on Decision**:
- 🔴 Low confidence supply chain → Reduce investment conviction or wait for clearer validation
- 🟡 Moderate confidence → Proceed but monitor news for relationship confirmation
- 🟢 High confidence → Thesis strengthened, ready for Step4 analysis

### Phase 4: News & Events Analysis (Step4 - 消息与新闻检索)

**Objective**: Discover catalysts and risks through systematic news and event analysis.

#### Step4a: News Search & Collection (新闻搜索 - 自动化)

**Objective**: Automatically search and collect announcements, news, and events from multiple sources.

**Process**:
1. Search CNINFO (巨潮资讯) for official announcements from all Step2 stocks
2. Search news platforms for industry news and company news (past 30-60 days)
3. Search event calendars for conferences, earnings announcements, policy releases
4. Collect metadata: source, date, title, URL
5. De-duplicate and organize by date

**Output**:
- Raw news collection: `step4/raw_data/{代码_名称}_news_raw.yaml`
- Fields: date, source, title, url, category (announcement/news/event)
- News index: `step4/raw_data/news_index.yaml`
- Directory: `step4/raw_data/`

**Tools** (automation):
- Search script: `step4/tools/step4a_search_news.py`
- Supports: CNINFO API, news APIs, web scraping
- Config: Search keywords from Step2 stock names

**Checkpoints**:
- ✅ Are all Step2 stocks covered in news search?
- ✅ Is the time window correct (30-60 days)?
- ✅ Are duplicate news items removed?

#### Step4b: News Classification & Tagging (新闻分类与标注 - AI + 人工)

**Objective**: Classify news into catalysts and risks, and tag relevance and impact.

**Process**:
1. **AI-Assisted Classification**:
   - Use AI to read news titles and summaries
   - Classify: Positive Catalyst / Negative Risk / Neutral News / Irrelevant
   - Extract key entities: Company affected, event type, impact area
2. **Human Validation**:
   - Review AI classifications for accuracy
   - Correct misclassifications
   - Add manual notes for ambiguous cases
3. **Time Window Tagging**:
   - When did the event occur? (event_date)
   - When will impact be realized? (impact_date)
   - Any upcoming milestones mentioned? (milestone_date)
4. **Impact Assessment**:
   - High Impact: Could significantly change investment thesis
   - Medium Impact: Notable but not thesis-changing
   - Low Impact: Routine or minor news

**Output**:
- Classified news: `step4/classified/{代码_名称}_news_classified.yaml`
- Fields: date, source, title, classification, impact_level, event_date, impact_date, notes, reviewed
- Summary table: `step4/report/04_汇总_新闻分类表.md`
- Directory: `step4/classified/`

**Tools** (AI assistance):
- Classification script: `step4/tools/step4b_classify_news.py`
- Input: Raw news from Step4a
- Output format: Structured YAML

**Checkpoints**:
- ✅ Have you reviewed AI classifications for accuracy?
- ✅ Are impact levels assigned based on thesis relevance?
- ✅ Are all dates clearly documented?
- ✅ Are ambiguous news items marked for human review?

#### Step4c: News-Technical Conflict Check (新闻与技术面冲突检查)

**Objective**: Cross-check if news timeline aligns with technical analysis to identify inconsistencies.

**Process**:
1. **Timeline Analysis**:
   - Major positive catalyst → Did stock price rise after announcement? If not, red flag
   - Major negative risk → Did stock price fall after announcement? If not, red flag
   - Upcoming catalyst → Is stock price already pricing in expectation?
2. **Conflict Detection**:
   - Stock already rallied 50% but catalyst still 1 month away → Overheating risk
   - Negative news announced but stock price unchanged → Market disagrees, investigate why
   - Gap between news date and stock reaction → Possible delayed impact
3. **Validation Gaps**:
   - Which news items don't match the technical trend?
   - Are there hidden catalysts not captured in news search?
4. **Final News Summary**:
   - List catalysts with timeline and confidence level
   - Highlight conflicts and their implications
   - Recommend: Watch for upcoming catalyst dates, avoid trading before announcements

**Output**:
- Conflict analysis: `step4/analysis/04_新闻技术面冲突分析.md`
- Final news summary: `step4/report/04_汇总_新闻与事件表.md`
- Fields: Stock, Event Type, Event Date, Expected Impact Date, News Catalyst, Technical Signal, Alignment, Risk Notes
- Directory: `step4/`

**Tools** (AI + manual analysis):
- Helper script: `step4/tools/step4c_conflict_check.py` (optional)
- Input: Step4b classified news + Step5a technical data
- Output: Conflict report and recommendations

**Checkpoints**:
- ✅ Are major catalysts aligned with technical trends?
- ✅ Have you identified conflicts and their implications?
- ✅ Is the timeline clear for upcoming catalysts?
- ✅ Are recommendations based on both news and technical signals?

**Objective**: Search for recent announcements, news, and events to identify catalysts and risks.

### Phase 5: Technical Analysis & Entry Strategy (Step5 - 技术面走势与介入策略)

**Objective**: Combine fundamental and news analysis with technical analysis to formulate final entry strategy.

#### Step5a: Technical Data Collection & Indicator Calculation (技术数据获取与指标计算 - 自动化)

**Objective**: Automatically collect historical price data and calculate technical indicators.

**Process**:
1. Retrieve recent 120 trading days' price data for all stocks
2. Calculate moving averages: MA20, MA60, MA250
3. Calculate high/low points: 20-day/60-day/250-day high and low
4. Calculate volatility metrics: ATR, daily range, amplitude
5. Organize data into time-indexed format

**Output**:
- Technical data: `step5/raw_data/{代码_名称}_technical_data.csv`
- Columns: date, open, close, high, low, volume, ma20, ma60, ma250, h20, l20, h60, l60, h250, l250
- Data index: `step5/raw_data/technical_index.yaml`
- Directory: `step5/raw_data/`

**Tools** (automation):
- Data collection script: `step5/tools/step5a_fetch_technical_data.py`
- Supports: Wind API, Tushare, Yahoo Finance
- Config: Stock codes from Step2 YAML

**Checkpoints**:
- ✅ Are all 120 trading days of data collected?
- ✅ Are all indicators calculated correctly?
- ✅ Are data gaps handled (holidays, missing data)?

#### Step5b: Trend Analysis & Signal Detection (趋势判断与信号检测 - AI + 人工)

**Objective**: Analyze price trends and identify technical signals aligned with fundamental and news analysis.

**Process**:
1. **Trend Assessment** ⭐:
   - Short-term (20-day): Is price above/below MA20? Momentum direction?
   - Medium-term (60-day): Is price above/below MA60? Established trend?
   - Long-term (250-day): Is price above/below MA250? Overall trend?
   - Trend health: Are MAs in proper order (MA20 > MA60 > MA250 for uptrend)?
2. **Support & Resistance**:
   - Recent support: 20-day low, 60-day low
   - Potential resistance: 20-day high, 60-day high, previous highs
   - Breakout zones: If price breaks 60-day high, where's next resistance?
3. **Volatility & Risk**:
   - Average daily range and amplitude
   - Recent volatility vs historical average (high volatility = risk)
   - Gap risk: Overnight gaps that could stop-loss?
4. **Signal Validation with Fundamentals & News**:
   - Does uptrend align with positive catalysts (Step4)?
   - Does downtrend align with negative risks (Step4)?
   - Conflict detection: Stock rallying but negative news → Be cautious
   - Wait for signals: Is price still waiting for announced catalyst?
5. **AI-Generated Signal Report**:
   - Use AI to synthesize: fundamentals + news + technical signals
   - Highlight alignment and conflicts
   - Estimate confidence level for each signal

**Output**:
- Technical analysis: `step5/analysis/05_{赛道}_{代码}_{名称}_technical.md`
- Signal summary: `step5/report/05_汇总_技术信号表.md`
- Fields: Stock, Short-term Trend, Mid-term Trend, Support, Resistance, Signal Strength, Catalyst Alignment, Risk Level
- Directory: `step5/analysis/`

**Tools** (AI assistance):
- Analysis helper: `step5/tools/step5b_trend_analysis.py` (optional)
- Input: Technical data from Step5a + catalyst timeline from Step4c
- Output: Signal report with recommendations

**Checkpoints**:
- ✅ Have you assessed trends at multiple timeframes?
- ✅ Are support/resistance levels clearly identified?
- ✅ Is technical signal aligned with fundamental analysis?
- ✅ Are conflicts with news catalysts documented?

#### Step5c: Entry Decision & Strategy Formulation (入场决策与策略制定)

**Objective**: Make final investment decision based on integrated analysis (fundamentals + news + technical).

**Process**:
1. **Integrated Assessment**:
   - Step3c: Is business fundamentally sound? (Business Reality Score: 1-10)
   - Step4c: Are catalysts positive and upcoming? (Catalyst Timeline)
   - Step5b: Is technical setup favorable for entry? (Trend & Signal Quality)
   - Step3.5: Is supply chain thesis validated? (Confidence Level)

2. **Decision Matrix**:
   | Business | Catalyst | Technical | Supply Chain | **Action** |
   |----------|----------|-----------|--------------|-----------|
   | Bullish | Positive | Strong Up | High Conf | **BUY** |
   | Bullish | Positive | Neutral | High Conf | **WAIT for Setup** |
   | Bullish | Neutral | Strong Up | High Conf | **Consider BUY** |
   | Bullish | Negative | Strong Down | High Conf | **WAIT** |
   | Neutral | Positive | Strong Up | Mod Conf | **Monitor** |
   | Bearish | Any | Any | Low Conf | **AVOID** |

3. **Price Target & Risk Management**:
   - Entry price range: Where is the best risk/reward ratio?
     - Trend continuation entry: Above/near 20-day high (stronger momentum)
     - Pullback entry: Near 20-day or 60-day support (lower risk)
     - Breakout entry: Above resistance level (requires catalyst confirmation)
   - Support level (Stop Loss): Where would thesis break?
   - Profit targets: Conservative/Base/Aggressive targets based on volatility
   - Position sizing: Based on risk (account % to risk = risk per share × position size)

4. **Final Recommendation**:
   - Clear recommendation: Buy / Hold / Avoid
   - Reasoning: 2-3 key reasons from all analysis layers
   - Timeline: When to enter, when to exit, when to monitor
   - Risk triggers: What would invalidate the thesis?

**Output**:
- Final strategy table: `step5/report/05_汇总_介入策略表.md`
- Fields: Stock, Business Score, Catalyst, Technical Signal, Supply Chain Conf, Recommendation, Entry Range, Support, Target1/2/3, Risk Triggers, Timeline
- Executive summary: `step5/report/05_汇总_最终决策摘要.md`
- Directory: `step5/`

**Checklist Before Decision** ⭐:
- ✅ Have you personally reviewed all analysis? (Don't just rely on AI synthesis)
- ✅ Is the recommendation clear and backed by 2-3 key reasons?
- ✅ Are risk triggers defined (what would change your mind)?
- ✅ Are timeline expectations clear (when to buy, when to sell)?
- ✅ Does entry price make sense given current technical setup?
- ✅ Can you explain your thesis to someone else clearly?

**Implementation Notes**:
- 🎯 **High Conviction**: Business + Catalyst + Technical all aligned → Larger position
- 🟡 **Medium Conviction**: 2 of 3 factors aligned → Normal position
- 🔴 **Low Conviction**: Only 1 factor favorable → Small position or wait
- ⛔ **No Setup**: Thesis broken or factors misaligned → Avoid or close position

### Bonus: Cross-Model Validation (跨模型验证)

**Objective**: Use different AI models to cross-validate findings and avoid single-model bias.

**Process**:
1. Run same analysis through multiple models (DeepSeek, Gemini, ChatGPT)
2. Compare recommendations and identify discrepancies
3. Challenge assumptions and reasoning
4. Identify potential blind spots
5. Synthesize final conclusion

**Best Practice**: Apply cross-model validation at any step (especially Step1 and Step2) for critical decisions.

**When to Apply Cross-Validation**:
- Step1 sector selection: Different models may identify different macro trends
- Step2 supply chain analysis: Different models may emphasize different segments
- Step3c business verification: Ask different models to challenge your conclusions
- Step5c final decision: Get second opinion on entry strategy before committing capital

## Complete Workflow Architecture

```
赛道筛选（Step1）
    ↓
产业链挖掘（Step2）
    ↓
┌──────────────────────────────────────┐
│ 财报验证（Step3a/b/c）               │
│ ├─ Step3a：财报获取 [自动]          │
│ ├─ Step3b：内容提取 [自动]          │
│ └─ Step3c：深度分析 [AI+人工] ⭐    │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 产业链验证（Step3.5，可选但推荐）    │
│ └─ 财报+新闻反向验证供应链           │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 新闻事件分析（Step4a/b/c）           │
│ ├─ Step4a：新闻搜索 [自动]          │
│ ├─ Step4b：分类标注 [AI+人工]       │
│ └─ Step4c：冲突检查 [混合]          │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 技术面与入场（Step5a/b/c）           │
│ ├─ Step5a：数据计算 [自动]          │
│ ├─ Step5b：趋势评估 [AI+人工]       │
│ └─ Step5c：决策执行 [人工] ⭐      │
└──────────────────────────────────────┘
    ↓
跨模型验证（Bonus，关键步骤）
```

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

### Template 4: Supply Chain Verification

```
I previously identified [COMPANY_A] as a supplier of [COMPONENT] to [COMPANY_B]. Please review their latest financial reports and find evidence of:

1) Does [COMPANY_A]'s annual report mention [COMPANY_B] as a customer or mention [COMPONENT] sales?
2) What percentage of [COMPANY_A]'s revenue comes from [COMPANY_B] and similar customers?
3) Are there any risks to this supply relationship (e.g., customer concentration, alternative suppliers)?

我之前识别[公司A]是[部件]供应商到[公司B]。请根据最新财报验证：

1) [公司A]的年报中是否提到[公司B]作为客户，或提到[部件]销售？
2) [公司A]来自[公司B]和类似客户的收入占比多少？
3) 这个供应关系有哪些风险（如客户集中度、替代供应商）？
```

### Template 5: News-Technical Conflict Analysis

```
[COMPANY_NAME] announced [POSITIVE/NEGATIVE EVENT] on [DATE], but the stock price [describe movement, e.g., "continued falling instead of rising"]. 

1) What could explain this disconnect between news and price action?
2) Is the market disagreeing with the event's importance, or is there hidden negative news?
3) Should I wait for further price action confirmation before entering?

[公司名]在[日期]宣布了[正面/负面事件]，但股价[描述走势，例如："没有上涨反而继续下跌"]。

1) 这种新闻和股价的脱节可能说明什么？
2) 市场是在否定这个事件的重要性，还是存在隐藏的负面消息？
3) 我应该等待进一步的价格确认再介入吗？
```

### Template 6: Technical Setup Validation

```
Stock [STOCK_CODE] is currently at [PRICE], with:
- 20-day MA: [MA20]
- 60-day MA: [MA60]  
- 20-day high: [H20], low: [L20]
- Recent news: [CATALYST]

Given this technical setup and fundamental thesis, is [PRICE] a good entry point? When should I enter?

股票[代码]目前价格[价格]，技术面：
- 20日均线[MA20]
- 60日均线[MA60]
- 20日高[H20]、低[L20]
- 最近事件[催化]

考虑到技术面和基本面，[价格]是好的入场点吗？我应该什么时候入场？
```

### Template 7: Decision Review (Self-Challenging)

```
I have decided to buy [STOCK_NAME] at [PRICE] based on:
- Catalyst: [CATALYST]
- Business: [THESIS]
- Technical: [SETUP]

Please challenge my thesis:
1) What are the top 3 ways my analysis could be wrong?
2) What would make you avoid this stock?
3) If this stock drops 20%, would you still believe in the thesis?

我决定以[价格]买入[股票]，基于：
- 催化[催化逻辑]
- 基本面[论证]
- 技术面[设置]

请质疑我的逻辑：
1) 我的分析可能出错的前3个方面是什么？
2) 你会因为什么而回避这只股票？
3) 如果股价下跌20%，你还会相信这个论证吗？
```

## Best Practices

### Model Selection Strategy
- **Step1 (Sector Selection)**: DeepSeek (best A-share knowledge) → Gemini Deep Research (validation)
- **Step2 (Supply Chain)**: ChatGPT or Gemini (detailed reasoning) → DeepSeek (A-share specifics)
- **Step3c (Financial Analysis)**: DeepSeek (reports/fundamentals) → ChatGPT (second opinion on risks)
- **Step4b (News Classification)**: Gemini Deep Research (web search + classification)
- **Step5c (Final Decision)**: Use Template 7 with multiple models for self-challenge

### Research Workflow Best Practices
1. **Start Broad, Verify Narrow**: Begin with sector (macro) → supply chain (meso) → companies (micro)
2. **Separate Automation from Judgment**: 
   - Automate: Data collection, extraction, initial classification
   - Human review: Financial interpretation, relationship validation, final decision
3. **Document Everything**: Keep notes on what you found, what changed your mind, what surprised you
4. **Cross-Check Systematically**: 
   - Financial reports vs news (Step3c vs Step4b)
   - News timeline vs technical moves (Step4c)
   - Fundamentals vs technical setup (Step5b vs Step5c)
5. **Question Your Assumptions**:
   - Use Template 7 before every major decision
   - Ask "What would prove me wrong?"
   - Build in a 20% margin of safety

### Risk Management Rules
- **Position Sizing**: Never risk more than 2% of portfolio on single thesis
- **Stop Loss**: Set before entering, not after losing
- **Catalyst Timing**: Know when catalyst should be realized; if not by then, exit
- **Thesis Invalidation**: If any major assumption changes, reconsider position
- **Overheating**: If stock has rallied >30% since your thesis began, reassess entry

### Time Investment Estimates
- **Step1**: 1-2 hours (sector scanning)
- **Step2**: 2-3 hours per sector (supply chain research)
- **Step3a/b**: 30-60 minutes (automatic download & extraction)
- **Step3c**: 3-5 hours per company (manual deep reading)
- **Step3.5**: 1-2 hours per supply chain (validation)
- **Step4a/b**: 1-2 hours per stock (news search & classification)
- **Step4c**: 30 minutes (conflict analysis)
- **Step5a**: 15 minutes (automatic data fetch)
- **Step5b/c**: 1-2 hours (trend analysis + decision)
- **Total for 5-10 stocks**: 20-40 hours (realistic for quality research)
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

- **v2.0.0** (2026-02-03): Comprehensive workflow restructuring
  - **Step3 (Fundamentals)**: Split into 3 layers - Download/Extract/Analysis
    - Step3a: Automated financial report download
    - Step3b: Automated content extraction with OCR/AI
    - Step3c: Manual deep-reading + AI assistance for analysis
  - **Step3.5 (Supply Chain Verification)**: New optional verification step
    - Cross-validate supply chain relationships with financial reports
    - Identify bottleneck positions and concentration risks
  - **Step4 (News & Events)**: Split into 3 layers - Search/Classification/Validation
    - Step4a: Automated news collection from multiple sources
    - Step4b: AI-assisted classification + human validation
    - Step4c: News-technical alignment check to detect conflicts
  - **Step5 (Technical Analysis)**: Split into 3 layers - Data/Trend/Decision
    - Step5a: Automated technical data collection and indicator calculation
    - Step5b: Trend analysis with fundamental & news cross-check
    - Step5c: Integrated decision-making with risk management
  - **New prompt templates**: 4 additional templates for Step3.5-5 validation
  - **New tools development**: Scripts for automation at layers a (data collection)
  - **Architecture diagram**: Complete workflow visualization added

- **v1.0.0** (2026-02-03): Initial release
  - Core 5-phase workflow
  - 5 prompt templates for different research stages
  - Cross-model validation framework
  - Risk disclaimers and best practices
  - Core 5-phase workflow
  - 5 prompt templates for different research stages
  - Cross-model validation framework
  - Risk disclaimers and best practices

---

**Note**: Markets carry inherent risks. This skill provides a systematic research framework but does not guarantee investment success. Always make decisions based on your own analysis and risk tolerance.

**注**：市场有风险，入市需谨慎。本技能提供系统化的研究框架，但不保证投资成功。请基于自身分析和风险承受能力做出决策。
