# CLAUDE.md

## Repository Purpose

This is a **Claude Code Skills Repository** containing custom skills that extend Claude's capabilities for systematic software development workflows. Skills are specialized prompts with supporting documentation that guide Claude to perform expert-level tasks in code analysis, debugging, refactoring, file organization, version comparison, and skill creation.

## Repository Structure

```
linearleaf_skill_repo/
├── analysis_code/                     # Code Analysis Skill
│   ├── SKILL.md                       # Main skill definition with YAML frontmatter (REQUIRED)
│   ├── README.md                      # User-facing documentation (REQUIRED)
│   ├── examples/                      # Example usage and sample tasks
│   ├── templates/                     # Analysis report templates
│   └── tools/                         # Helper scripts and utilities
├── debug_code/                        # Debugging Skill
│   ├── SKILL.md                       # Main skill definition
│   ├── README.md                      # User-facing documentation
│   ├── examples/                      # Debugging examples
│   └── templates/                     # Debug report templates
├── refactor_code/                     # Code Refactoring Skill
│   ├── SKILL.md                       # Main skill definition
│   ├── README.md                      # User-facing documentation
│   ├── examples/                      # Refactoring examples
│   └── templates/                     # Planning and tracking templates
├── file_organize/                     # File Organization Skill
│   ├── SKILL.md                       # Main skill definition
│   ├── README.md                      # User-facing documentation
│   ├── examples/                      # Organization examples
│   └── templates/                     # Organization templates
├── version_compare/                   # Version Comparison Skill
│   ├── SKILL.md                       # Main skill definition
│   ├── README.md                      # User-facing documentation
│   ├── examples/                      # Comparison examples
│   └── templates/                     # Comparison report templates
├── skill_builder/                     # Skill Builder Meta-Skill
│   ├── SKILL.md                       # Main skill definition
│   ├── README.md                      # User-facing documentation
│   ├── examples/                      # Example skill designs
│   └── templates/                     # Skill creation templates
├── CLAUDE.md                          # This file - Claude Code guidance
├── README.md                          # Project overview and documentation
├── LICENSE                            # MIT License
├── CHANGELOG.md                       # Version history
└── .gitignore                         # Git exclusions
```

## Skills Overview

### 1. analysis_code - Code Analysis Skill
**Purpose**: Systematic code analysis with overview-detail-summary structure
**When to use**: Code quality assessment, performance analysis, architecture review, technical debt identification

### 2. debug_code - Debugging Skill
**Purpose**: 6-step debugging cycle methodology
**When to use**: Problem definition, hypothesis testing, root cause analysis, fix implementation

### 3. refactor_code - Code Refactoring Skill
**Purpose**: Three-tier planning system for systematic refactoring
**When to use**: Overall refactoring planning, stage-level execution, priority-based task management

### 4. file_organize - File Organization Skill
**Purpose**: Systematic file and directory organization
**When to use**: Priority-oriented, type-oriented, or timeline-oriented file organization

### 5. version_compare - Version Comparison Skill
**Purpose**: Systematic version comparison and change analysis
**When to use**: Version difference analysis, change impact assessment, update log generation

### 6. skill_builder - Skill Builder Meta-Skill
**Purpose**: IPD-driven skill design and creation
**When to use**: Creating new Agent Skills, skill design pattern application, quality assurance

## Working with This Repository

### For Claude Code Users

When working with this repository, Claude Code will automatically:
- Detect available skills based on directory structure
- Load skill definitions from SKILL.md files
- Use templates and examples to guide task execution
- Follow systematic workflows defined in each skill

### For Skill Developers

When creating or modifying skills:
1. Each skill MUST have a SKILL.md file with YAML frontmatter
2. Each skill MUST have a README.md for user documentation
3. Supporting files (examples, templates, tools) should be organized in subdirectories
4. Follow the existing skill structure for consistency

### Git Workflow

- **Branch**: main
- **Commit Standards**: Use conventional commits (feat:, fix:, docs:, etc.)
- **NEVER mention Claude in commit messages**

Good commit messages:
- "feat: add new analysis template for performance metrics"
- "fix: correct debug workflow step ordering"
- "docs: update README with installation instructions"

Bad commit messages:
- "Claude added new template" ❌
- "Asked Claude to update docs" ❌

### Standard Compliance

This repository follows the [Agent Skills open standard](https://agentskills.io/) for VS Code and GitHub Copilot integration.

## Integration Points

### VS Code Agent Skills
- Skills are automatically discovered in the repository
- Enable with `"chat.useAgentSkills": true` in VS Code settings
- Skills trigger based on user requests matching skill descriptions

### GitHub Copilot
- Skills enhance Copilot's capabilities with specialized workflows
- Provide systematic approaches to complex development tasks
- Can be used in chat or inline suggestions

## Development Principles

1. **Systematic Workflows**: Each skill provides structured, repeatable processes
2. **Documentation First**: Comprehensive documentation for users and developers
3. **Template-Driven**: Reusable templates for consistent outputs
4. **Example-Rich**: Real-world examples demonstrate skill usage
5. **Tool Support**: Helper scripts and utilities enhance skill capabilities

## Validation Requirements

Before committing:
- [ ] All skills have SKILL.md and README.md
- [ ] YAML frontmatter is valid in all SKILL.md files
- [ ] No broken links in documentation
- [ ] All templates are properly formatted
- [ ] Examples are clear and accurate
- [ ] CHANGELOG.md is updated for version changes

## Resources

- [Agent Skills Standard](https://agentskills.io/)
- [VS Code Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

**Repository Maintainer**: Linearleaf  
**Project Type**: Agent Skills Collection  
**Standard Compliance**: Agent Skills v1.0  
**License**: MIT
