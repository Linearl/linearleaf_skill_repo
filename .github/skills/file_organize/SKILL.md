---
name: file-organize
description: 系统化文件整理和项目清理。当用户需要文件整理、目录清理、文件组织、项目整理、文档归档时激活。Systematic file organization and project cleanup. Activates when user needs file organization, directory cleanup, file management, project organization, or document archiving.
---

# 🗂️ File Organize Skill | 文件整理技能

## Overview | 概述

This skill provides systematic file organization capabilities with three organizing approaches: standard templates, reference folder analysis, and AI-designed custom rules.

此技能提供系统化的文件整理能力，包含三种整理方式：标准模板、参考文件夹分析和AI定制规则。

## Trigger Conditions | 触发条件

**Keywords | 关键词**: file organization, cleanup, directory restructure, file management, project organization, document archiving, 文件整理, 清理, 目录重构, 文件管理, 项目整理, 文档归档

**Auto-suggestion | 自动建议**:
> "我看到您需要文件整理协助。是否需要我启动文件整理工作流？我可以帮助您使用标准模板、参考文件夹分析或AI定制方案系统地整理文件。"

## Three Organizing Approaches | 三大整理方式

### Approach 1: Standard Templates | 方式一：使用已有模板

Quick start with 4 proven standard templates:

| Template | Name | Use Cases | Recommended For |
|----------|------|-----------|-----------------|
| A | 🎓 Academic Research | Academic work, research projects | Teachers, researchers, students |
| B | 💼 Business Office | Enterprise office, project management | Employees, managers |
| C | 🏠 Personal Life | Personal documents, life materials | Personal users, families |
| D | 🔧 Custom | Multi-role, complex needs | Flexible workers |

**Usage Example | 使用示例**:
```
请使用模板B整理我的工作文档，按商务办公型的结构组织文件
```

### Approach 2: Reference Folder Analysis | 方式二：参考文件夹分析

Generate custom template based on an already organized folder:

1. **Specify Reference Folder | 指定参考文件夹**: Provide path to well-organized folder
2. **Smart Analysis | 智能分析**: System analyzes organization logic and naming conventions
3. **Generate Template | 生成模板**: Create directory structure template from analysis
4. **Confirm and Apply | 确认应用**: User confirms before applying to target directory

**Usage Example | 使用示例**:
```
参考D:\已整理的项目A文件夹，分析其结构并生成相似的模板来整理E:\新项目文件
```

### Approach 3: AI-Designed Custom Rules | 方式三：AI定制设计

AI designs complete organizing rules based on detailed requirements:

1. **Describe Requirements | 需求描述**: Detail your personalized needs
2. **AI Design | AI设计**: Generate complete organizing rules document
3. **Multi-round Iteration | 多轮迭代**: Support feedback and adjustments
4. **Final Confirmation | 最终确认**: Confirm rules document and start applying

**Output Contents | 输出内容**:
- 📁 Directory Structure | 目录结构
- 📋 Classification Rules | 分类规则
- 🏷️ Naming Conventions | 命名规范
- ⚙️ Special Handling | 特殊处理
- 🔄 Duplicate Files Strategy | 重复文件策略

**Usage Example | 使用示例**:
```
请整理G:\我的创作资料库，按创作类型和状态分类：
1. 按创作类型：小说、诗歌、剧本、散文
2. 每个类型下按状态：构思中、创作中、已完成、已发表
3. 素材文件单独管理
请生成详细的整理规则文档供我确认。
```

## Workflow Phases | 工作流阶段

### Phase 1: Preparation | 一、准备阶段

1. **User Describes Requirements | 用户描述需求**
   - Describe target directory and organizing goals
   - Choose organizing approach (1/2/3)
   - Specify constraints and special requirements

2. **AI Parses and Formats | AI解析并格式化**
   - Extract key information
   - Identify organizing approach
   - (Approach 2) Analyze reference folder
   - (Approach 3) Generate rules document

3. **User Confirms | 用户确认信息**
   - Confirm target directory path
   - Confirm chosen template or custom rules
   - Multi-round iteration if needed

4. **Create Task Document | 创建专用文档**
   - Copy template as task-specific document
   - Fill in auto-generated sections

5. **Initialize Environment | 初始化环境**
   - Create standardized directory structure
   - Initialize template files

### Phase 2: Execution | 二、执行阶段

1. **📊 Directory Structure Analysis | 目录结构分析**
   - Scan directory structure
   - Count file types and quantities
   - Identify naming patterns
   - Run duplicate file detection

2. **🗂️ Classification Planning | 分类规划设计**
   - Define classification standards
   - Design new directory structure
   - Plan file movement scheme
   - Determine duplicate file handling strategy

3. **🔄 Duplicate File Processing | 重复文件处理**
   - Same directory: Keep one copy (newest)
   - Cross-directory: Allow duplicates (different purposes)
   - Run detection tool

4. **📋 Plan Development | 整理计划制定**
   - Generate detailed execution steps
   - Assess operation risks
   - Prepare rollback plan

5. **⚙️ Execute Operations | 执行操作**
   - Execute organizing operations
   - Create target directory structure
   - Move and rename files
   - Process duplicate files
   - Handle thematic folders
   - Record operation logs

6. **✅ Verify Results | 验证结果**
   - Completeness check
   - Confirm organizing effect
   - Execute task archiving

### Phase 3: Summary | 三、总结阶段

1. **📊 Review and Improvement | 复盘与改进** (Optional)
   - Identify problems encountered
   - Propose improvement suggestions

2. **🔧 Workflow Optimization | 工作流优化** (Optional)
   - Organize process files
   - Evaluate tools effectiveness
   - Create improvement plan

3. **📝 Output Summary Report | 输出总结报告**
   - Task overview and comparison data
   - Results display
   - Experience summary
   - Follow-up suggestions

## Core Principles | 核心原则

1. **Safety First | 安全第一**: Always maintain data safety, backup important files
2. **Progressive Organizing | 渐进整理**: Execute in steps, verify before continuing
3. **Standardization | 标准化**: Establish consistent naming and classification standards
4. **Traceability | 可追溯**: Record all operations, support rollback
5. **Duplicate Handling | 重复文件处理**: Same-directory dedupe, cross-directory allow
6. **Completeness Verification | 完整性验证**: Full check after each operation
7. **Continuous Improvement | 持续改进**: Review and optimize after each task

## Thematic Folder Handling | 主题文件夹处理原则

- **Identification | 识别标准**: Folders named by person, place, event, project
- **Strategy | 处理策略**: Move whole to 99_待确认 directory, keep structure intact
- **Protection | 保护逻辑**: Avoid breaking logical associations between files
- **User Decision | 用户决策**: User decides whether to reorganize

## Templates | 模板

Core templates available in `templates/` directory:

- `analysis-template.md` - File analysis template
- `plan-template.md` - Organizing plan template
- `directory-templates.md` - Directory structure templates (4 standard templates)
- `summary-report-template.md` - Summary report template

## Tools | 工具

Available tools in `tools/` directory:

- `duplicate_detector.py` - Duplicate file detection
- `duplicate_processor.py` - Duplicate file processing
- `integrity_validator.py` - Integrity validation
- `validation.ps1` - PowerShell validation script

## Directory Structure Standard | 目录结构标准

```
organize/
└── [task_name]/                      # Specific organizing task
    ├── file_organize_workflow_[task].md  # Task-specific workflow
    ├── analysis/                     # Analysis folder
    │   └── 分析报告.md               # Analysis report
    ├── plan/                         # Plan folder
    │   └── 整理计划.md               # Organizing plan
    ├── backup/                       # Backup folder
    ├── logs/                         # Logs folder
    └── docs/                         # Documentation folder
```

## Usage Examples | 使用示例

### Quick Start with Template | 快速开始

```markdown
请参考工作流，整理D:\Downloads目录，使用模板A（学术研究型），
目标是将所有PDF论文、PPT课件、研究资料按照学术分类整理，
约束条件是不能删除任何文件，只允许移动和重命名。
```

### Reference Folder Approach | 参考文件夹方式

```markdown
请参考工作流，整理E:\新项目文件，
参考文件夹为D:\已整理的项目A，
分析参考文件夹的结构并生成相似的目录模板，
然后用这个模板整理新项目的文件。
```

### Custom AI Design | AI定制设计

```markdown
请参考工作流，整理G:\我的创作资料库，
我需要个性化的整理方案，按照以下要求：
1. 按创作类型分类：小说、诗歌、剧本、散文
2. 每个类型下按状态分类：构思中、创作中、已完成、已发表
3. 素材文件单独管理：灵感记录、人物设定、背景资料
4. 特殊要求：手稿扫描件要保留原始文件名，参考资料按来源分类
请生成详细的整理规则文档供我确认。
```

## Best Practices | 最佳实践

1. **Backup Before Organizing | 整理前备份**
   - Always backup important files before operations
   - Use backup/ directory for safety copies

2. **Confirm Before Large Operations | 大操作前确认**
   - Get user confirmation before mass file moves
   - Show preview of changes when possible

3. **Log All Operations | 记录所有操作**
   - Keep detailed operation logs
   - Enable rollback if needed

4. **Verify Completeness | 验证完整性**
   - Check that all files are accounted for
   - Ensure no files are lost or misplaced

## References | 参考

- Original workflow: `file-organize-system/file_organize_workflow_template.md`
- Detailed documentation: `file-organize-system/README.md`
