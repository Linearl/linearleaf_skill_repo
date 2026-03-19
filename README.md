# Linearleaf Agent Skills

![VS Code Agent Skills](https://img.shields.io/badge/VS%20Code-Agent%20Skills-blue?logo=visualstudiocode)
![Agent Skills Standard](https://img.shields.io/badge/Standard-agentskills.io-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

🚀 Professional VS Code Agent Skills Collection

Language: **English** | [中文（README_CN.md）](README_CN.md)

---

## 📖 Overview

Linearleaf Agent Skills is a collection of skill packages compliant with the [Agent Skills open standard](https://agentskills.io/), providing GitHub Copilot and Claude Code with systematic capabilities for code analysis, debugging, refactoring, file organization, version comparison, HTML presentation generation, and skill building.

> 🔄 **Project Evolution**: This repository is the standardized Agent Skills evolution of [copilot_workflows](https://github.com/Linearl/copilot_workflows).

## 🧭 Method Philosophy (from AUTHOR_NOTE)

We are not inventing an entirely new collaboration logic. We are translating proven human organizational practices into AI collaboration engineering:

- **Workflow is the methodological core**: it keeps complex tasks controllable, reviewable, and reusable.
- **Skill is the standardized shell**: dynamic loading improves adoption and reduces manual wake-up overhead.
- **Multi-agent collaboration requires workspace structure**: team-level workspace + per-agent subspace enables “docs as communication,” lowering coordination bandwidth.

👉 See: [`AUTHOR_NOTE.md`](AUTHOR_NOTE.md)

## 🎯 Available Skills

| Skill | Description | Trigger Examples |
| --- | --- | --- |
| 🔍 [analysis_code](analysis_code/) | Systematic code analysis | "analyze this code", "code quality assessment" |
| 🛠️ [code-audit-fix](code-audit-fix/) | Defect scanning and staged batch remediation | "audit and fix code issues", "scan defects and repair in batches" |
| 🐛 [debug_code](debug_code/) | Systematic debugging | "help me debug", "fix this error" |
| 🔧 [refactor_code](refactor_code/) | Systematic refactoring | "refactor code", "improve architecture" |
| 📁 [file_organize](file_organize/) | Systematic file organization | "organize files", "clean up directory" |
| 📊 [version_compare](version_compare/) | Systematic version comparison | "compare versions", "change analysis" |
| 💰 [invest_analysis](invest_analysis/) | A-share investment analysis | "analyze this sector", "verify financial report" |
| 🖥️ [html-presentation-generator](html-presentation-generator/) | HTML presentation generation pipeline | "generate HTML slides from script", "merge parts and validate page order" |
| 🎬 [html-deck-pipeline-skill](html-deck-pipeline-skill/) | Advanced HTML deck pipeline with fine-grained stage control | "context too long for one-shot deck", "split storyboard and generate parts in parallel" |
| 🏗️ [skill_builder](skill_builder/) | **Meta-skill** - Create new skills | "create skill", "design skill" |

## 🚀 Quick Start

### 1) Installation

Option 1: Clone the entire repository

```bash
git clone https://github.com/Linearl/linearleaf_skill_repo.git
```

Option 2: Add as a Git submodule

```bash
git submodule add https://github.com/Linearl/linearleaf_skill_repo.git .skills
```

Option 3: Copy specific skill folders

Copy only what you need (for example, `analysis_code/`, `debug_code/`).

### 2) Enable Agent Skills

```json
{
  "chat.useAgentSkills": true
}
```

### 3) Use

Skills are dynamically loaded based on your request context.

## 📚 Skill Highlights

### 🔍 analysis_code

- Code quality assessment
- Performance analysis
- Architecture review
- Technical debt identification
- ask_questions-guided checkpoints for stage scope and priority confirmation
- Sub-agent parallel acceleration after the first round

### 🛠️ code-audit-fix

- Project-wide defect scanning and prioritization
- Batch-by-priority remediation workflow
- Multi-round cross-review before and after fixes
- CI-ready non-interactive execution and result contract

### 🐛 debug_code

- 6-step debugging cycle methodology
- Structured root-cause investigation
- Validation and closure records

### 🔧 refactor_code

- Three-tier planning for progressive refactoring
- P0–P3 priority control
- Safe staged execution

### 📁 file_organize

- Priority-oriented organization
- Type-oriented organization
- Timeline-oriented organization

### 📊 version_compare

- Version difference analysis
- Change impact assessment
- Update log generation
- ask_questions-guided module prioritization
- Sub-agent parallel module analysis

### 🖥️ html-presentation-generator

- Split long source content and generate storyboards in parallel
- Generate partial HTML files and merge into final deck
- Validate page order and quality gates
- Iterative preview and controlled improvements

### 🎬 html-deck-pipeline-skill

- End-to-end HTML script pipeline for long-context deck generation
- Storyboard-first workflow with optional parallel part generation and merge validation
- Fine-grained stage control with style contract/showcase pairing and versioned outputs

### 🏗️ skill_builder

- IPD-driven skill design process
- Skill design pattern library
- Quality assurance checklist

### 💰 invest_analysis

- Sector selection and trend identification
- Supply chain deep analysis
- Financial report verification
- Timing analysis and risk assessment
- Cross-model validation

## 🔗 Related Links

- [中文文档（README_CN.md）](README_CN.md)
- [Author Note / Philosophy](AUTHOR_NOTE.md)
- [Agent Skills Open Standard](https://agentskills.io/)
- [VS Code Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Original Workflow Project (Deprecated)](https://github.com/Linearl/copilot_workflows)

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome. Feel free to open issues and pull requests.

---

Made with ❤️ by Linearleaf
