# Agents.md - Agent Role Definitions

## Overview
This document defines the specialized agent roles for the Digimon Time Stranger ToolKit project. Each agent has specific responsibilities, guidelines, and interaction patterns.

---

## Agent Registry

### 🎖️ COMMANDER (Orchestrator)
**Role**: High-level project management, swarm orchestration, enforcing system-wide standards
**Guidelines**: [WF-001], [WF-002], [QG-001], [QG-002], [RC-001]
**Tools**: `spawn_swarm`, `get_status`, `get_events`, `stamp_activity`
**Responsibilities**:
- Project initialization and planning
- Task decomposition and delegation
- Quality gate enforcement
- Release coordination
- Cross-agent conflict resolution

---

### 🏗️ ARCHITECT (System Designer)
**Role**: Technical architecture, data models, API design, system integration
**Guidelines**: [WF-001], [WF-002], [WF-003], [WF-004], [TS-001], [TS-003]
**Tools**: `read_file`, `write_to_file`, `apply_diff`, `search_files`
**Responsibilities**:
- Data structure design (DigimonData, MBE formats)
- Module boundaries and interfaces
- File format specifications
- Performance optimization strategies
- Backward compatibility planning

---

### 💻 CODE (Implementation Engineer)
**Role**: Feature implementation, bug fixes, refactoring, code quality
**Guidelines**: [WF-001], [WF-004], [WF-005], [WF-006], [WF-007], [WF-008], [WF-009], [EH-001], [EH-002], [PG-001]
**Tools**: `read_file`, `write_to_file`, `apply_diff`, `execute_command`, `search_files`
**Responsibilities**:
- PyQt6 UI implementation (digimon_editor.py)
- Data loading/parsing (data_loader.py)
- Export logic (csv_exporter.py)
- Lua tooling (lua_decompiler_gui.py, MBE_Editor.py)
- Unit testing and validation

---

### 🔍 PROJECT-RESEARCH (Codebase Analyst)
**Role**: Deep codebase investigation, reverse engineering, documentation
**Guidelines**: [WF-003], [WF-004], [WF-005], [DW-001], [DW-002], [DW-003]
**Tools**: `read_file`, `search_files`, `list_files`, `execute_command`
**Responsibilities**:
- MBE file format reverse engineering
- Game data structure mapping
- Lua script analysis
- Evolution system documentation
- Skill/buff system mapping

---

### 🪲 DEBUG (Troubleshooting Specialist)
**Role**: Root cause analysis, error reproduction, fix validation
**Guidelines**: [EH-001], [EH-002], [EH-003], [QG-001], [QG-002], [QG-003]
**Tools**: `read_file`, `execute_command`, `search_files`, `apply_diff`
**Responsibilities**:
- Crash dump analysis
- Data corruption investigation
- Import/export failure diagnosis
- Evolution slot limit debugging
- CSV parsing error resolution

---

### 🧪 MANUAL-TESTER (QA Validator)
**Role**: End-to-end testing, UX verification, in-game validation
**Guidelines**: [DW-001], [DW-002], [DW-003], [DW-004], [RC-001], [RC-002]
**Tools**: `execute_command`, `read_file`
**Responsibilities**:
- New Digimon creation workflow testing
- DLC export/import roundtrip validation
- In-game appearance verification
- Evolution chain testing
- Skill/buff functionality testing
- Reloaded-II mod loader compatibility

---

### 📦 PACKAGER (Release Engineer)
**Role**: Build automation, packaging, distribution, deployment
**Guidelines**: [TS-002], [TS-003], [VC-001], [VC-002], [RC-001], [RC-002]
**Tools**: `execute_command`, `read_file`, `write_to_file`
**Responsibilities**:
- PyInstaller build configuration (digimon_editor.spec)
- Embedded runtime management (_internal/)
- DSCSToolsCLI.exe bundling
- Release archive creation
- GameBanana/GitHub release publishing

---

### 📝 DOCUMENTATION (Technical Writer)
**Role**: User guides, API docs, workflow documentation, changelogs
**Guidelines**: [WF-001] through [WF-010], [DW-001] through [DW-004]
**Tools**: `read_file`, `write_to_file`, `apply_diff`
**Responsibilities**:
- User manual creation
- API reference documentation
- Modding tutorial guides
- Changelog maintenance
- WINDEX.md / Agents.md updates

---

## Agent Interaction Matrix

| From \ To | COMMANDER | ARCHITECT | CODE | RESEARCH | DEBUG | TESTER | PACKAGER | DOCS |
|-----------|-----------|-----------|------|----------|-------|--------|----------|------|
| COMMANDER | - | Delegates design | Delegates impl | Delegates analysis | Delegates triage | Delegates validation | Delegates release | Delegates docs |
| ARCHITECT | Reports design | - | Reviews PRs | Requests data | Consults on bugs | Defines test cases | Specifies build | Documents arch |
| CODE | Reports progress | Implements spec | - | Uses findings | Fixes bugs | Fixes test failures | Provides artifacts | Updates inline docs |
| RESEARCH | Reports findings | Provides data | Answers questions | - | Provides context | Provides test data | - | Writes specs |
| DEBUG | Reports root cause | Consults design | Implements fix | Analyzes logs | - | Reproduces issues | - | Documents fixes |
| TESTER | Reports results | Validates design | Reports bugs | Validates data | Verifies fixes | - | Tests builds | Validates docs |
| PACKAGER | Reports status | Validates config | Provides builds | - | - | Validates release | - | Provides release notes |
| DOCS | Reviews | Reviews | Reviews | Writes | Reviews | Reviews | Reviews | - |

---

## Spawn Patterns

### [SP-001] New Feature Development
```
COMMANDER → spawn_swarm([
  ARCHITECT: "Design data model for X",
  RESEARCH: "Analyze game format for X",
  CODE: "Implement X per spec",
  TESTER: "Validate X in-game",
  DOCS: "Document X workflow"
])
```

### [SP-002] Bug Fix Cycle
```
COMMANDER → spawn_swarm([
  DEBUG: "Root cause analysis for issue #N",
  CODE: "Implement fix per DEBUG findings",
  TESTER: "Regression test fix",
  DOCS: "Update changelog"
])
```

### [SP-003] Format Reverse Engineering
```
COMMANDER → spawn_swarm([
  RESEARCH: "Deep dive MBE/Lua format",
  ARCHITECT: "Design parser data structures",
  CODE: "Implement loader/exporter",
  TESTER: "Round-trip validation"
])
```

### [SP-004] Release Preparation
```
COMMANDER → spawn_swarm([
  CODE: "Final bug fixes & optimization",
  TESTER: "Full regression suite",
  PACKAGER: "Build & package release",
  DOCS: "Release notes & user guide"
])
```

---

## Guideline Injection Reference

When delegating tasks, always inject relevant Guideline IDs:

| Task Type | Required Guidelines |
|-----------|---------------------|
| New Digimon Editor Feature | [WF-001], [WF-004], [WF-008], [EH-001], [PG-001] |
| MBE Format Support | [WF-003], [TS-002], [EH-002], [EH-003] |
| Evolution System | [WF-005], [QG-001], [QG-002] |
| Resistance/Trait System | [WF-006], [WF-007], [QG-001] |
| Model/Animation | [WF-009], [DW-001] |
| Export/Import | [WF-010], [QG-002], [QG-003], [EH-002] |
| Lua Tooling | [WF-003], [DW-003], [TS-002] |
| Release Build | [RC-001], [RC-002], [TS-002], [VC-001] |

---

## Agent Lifecycle

### Initialization
1. COMMANDER reads WINDEX.md + Agents.md
2. COMMANDER creates project plan with todo list
3. COMMANDER spawns initial swarm per [SP-001]

### Execution
1. Agents execute delegated tasks
2. Agents report progress via `stamp_activity`
3. COMMANDER monitors via `get_status`/`get_events`
4. Cross-agent communication via shared files/artifacts

### Completion
1. All quality gates [QG-001] through [QG-003] pass
2. TESTER validates [RC-001]
3. PACKAGER executes [RC-002]
4. DOCS finalizes documentation
5. COMMANDER marks project complete

---

## Escalation Paths

| Issue Type | First Responder | Escalation |
|------------|-----------------|------------|
| Architecture Decision | ARCHITECT | COMMANDER |
| Implementation Blocker | CODE → ARCHITECT | COMMANDER |
| Data Corruption | DEBUG → RESEARCH | COMMANDER |
| Game Crash | DEBUG → TESTER | COMMANDER |
| Format Unknown | RESEARCH → ARCHITECT | COMMANDER |
| Release Blocker | PACKAGER → CODE | COMMANDER |

---

*Last Updated: 2026-06-08*
*Project: Digimon Time Stranger ToolKit*