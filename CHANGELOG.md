# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added **code-audit-fix** skill documentation entry for defect scanning, staged batch remediation, multi-round review, and CI-oriented execution.
- Added **html-deck-pipeline-skill** documentation entry as an advanced HTML deck pipeline skill with finer stage-level control.

### Changed

- Updated skill indexes and readmes to include `code-audit-fix` (`README.md`, `README_CN.md`, `.github/skills/README.md`, `CLAUDE.md`)
- Updated skill indexes and readmes to include `html-deck-pipeline-skill` (`README.md`, `README_CN.md`, `.github/skills/README.md`, `CLAUDE.md`)
- Renamed skill directory from `html-deck-pipeline-skill` to `html-presentation-generator`
- Updated the renamed skill's metadata and reference descriptions
- Updated project documentation to include `html-presentation-generator`

## [1.2.0] - 2026-02-03

### Added

- **invest_analysis v2.1.0** - Major enhancement with real battle lessons
  - **Step2.5**: Commodity cycle positioning (mandatory for resource stocks)
  - **Step3.6**: Geopolitical risk assessment  
  - **Step6**: Research report cross-validation (mandatory for BUY stocks)
  - **Step7**: Multi-perspective reflection and adversarial thinking
  - **3-3-4 position building method** replacing traditional "wait for perfect entry"
  - **Psychological trap warning system** (4 traps from real cases)
  - **Resource moat rating** and cycle-adjusted PE
  - 11 comprehensive prompt templates
  - Real battle case studies (白银踏空, 铝龙头踏空, 铜金资源)

## [1.1.0] - 2026-02-03

### Added

- **invest_analysis v1.0** - A-share investment analysis skill
  - Sector selection with catalyst identification
  - Supply chain deep analysis
  - Financial report verification
  - Timing and sentiment analysis
  - Cross-model validation framework
  - 7 structured prompt templates

### Changed

- Created `.github/skills/` directory for VS Code Agent Skills testing
- All skills are now available in both root directory (standard structure) and `.github/skills/` (testing)
- Updated `.gitignore` to document testing directory purpose
- Updated `README.md` and `CLAUDE.md` to include invest_analysis skill

## [1.0.0] - 2026-02-03

### Added

- Initial release of Linearleaf Agent Skills
- **analysis_code** - Systematic code analysis skill
  - Overview-detail-summary structure
  - Multi-round analysis support
  - Code quality metrics
  
- **debug_code** - Systematic debugging skill
  - 6-step debugging cycle
  - Human confirmation checkpoints
  - Root cause analysis
  
- **refactor_code** - Systematic refactoring skill
  - Three-tier planning system
  - P0-P3 priority management
  - Dual-loop execution
  
- **file_organize** - Systematic file organization skill
  - Priority-oriented organization
  - Type-oriented organization
  - Timeline-oriented organization
  
- **version_compare** - Systematic version comparison skill
  - Version difference analysis
  - Change impact assessment
  - Update log generation
  
- **skill_builder** - Meta-skill for creating Agent Skills
  - IPD-driven design process
  - Skill design patterns
  - Quality assurance checklist
  - Templates for SKILL.md, README, and examples

### Notes

- This project is the Agent Skills standardized version of [copilot_workflows](https://github.com/Linearl/copilot_workflows)
- Follows the [Agent Skills open standard](https://agentskills.io/)
