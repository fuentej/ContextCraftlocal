# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ContextCraftPro (CCP)** is a self-contained, disposable Python-based tool that provides an opinionated, agent-driven context engineering workspace powered by Foundry Local. It lives entirely within a `ContextCraftPro/` folder that can be dropped into any codebase and deleted when done.

**Key properties:**
- **Ephemeral:** All files live inside `ContextCraftPro/` at the project root with no hidden state elsewhere
- **Local-only:** Uses Foundry Local's OpenAI-compatible API; no cloud LLM calls
- **Git-ignored:** The host project's `.gitignore` includes `ContextCraftPro/`
- **Deletable:** Removing the folder leaves the host project intact and unchanged
- **Agentic workflow:** Guides users through structured context engineering (specs, plans, validation, health checks)

## Core Architecture

### Directory Structure

```
ContextCraftPro/
├── ccp.py                    # CLI entrypoint
├── config/
│   ├── contextcraft.yaml     # Core configuration & paths
│   └── models.yaml           # (Optional) Foundry Local model mapping
├── context/
│   ├── project-profile.yaml  # Derived project metadata
│   ├── claude.md             # Global rules for AI coding assistants
│   ├── INITIAL.md            # Current feature/change spec
│   ├── examples/             # Examples for LLM consumption
│   ├── docs-context/         # Documentation pointers
│   ├── prps/                 # Product Requirements Prompts per feature
│   └── validation/           # Validation logs per feature
├── runtime/
│   ├── logs/
│   │   └── ccp.log           # Operation logs
│   └── sessions/             # Per-session snapshots (optional)
└── templates/                # Reusable markdown templates
```

**Critical rule:** CCP MUST NOT create or modify files outside `ContextCraftPro/` except:
- During `export` commands (explicit user action)
- When updating `.gitignore` during `init-project` (with user confirmation)

### Main Components

1. **CLI / Command Layer** (`ccp_cli.py`)
   - Parses commands and options
   - Dispatches to orchestrator functions

2. **Orchestrator / Core Logic** (`ccp_orchestrator.py`)
   - Inspects the host repo (one directory up from `ContextCraftPro/`)
   - Reads/writes context files
   - Manages sessions and run history
   - Calls LLM client with structured prompts

3. **LLM Client** (`ccp_llm.py`)
   - Minimal wrapper around Foundry Local's OpenAI-compatible HTTP API
   - Handles retries, timeouts, and safety checks
   - Ensures output is valid Markdown where expected

4. **Filesystem Utilities** (`ccp_fs.py`)
   - Repo scanner (language, structure, config files)
   - Template rendering
   - Markdown parsing/section extraction

### Technology Stack

- **Language:** Python 3.8+
- **Dependencies:**
  - Standard library where possible
  - Optional: `pyyaml` for YAML configs
  - Optional: `rich` for CLI output (non-essential)
- **Storage:** All state as text/Markdown/YAML/JSON (no database)
- **LLM Backend:** Foundry Local via OpenAI-compatible HTTP API

## Commands

All commands execute from the host repo root. The script detects the host root by finding `ContextCraftPro/` as a parent.

### `init-project`
**Purpose:** First-time setup of ContextCraftPro for a repo.

**Behavior:**
1. Verify layout and determine host root
2. Check `.gitignore` and optionally add `ContextCraftPro/` entry
3. Profile host repo: detect languages, frameworks, test setup
4. Seed context files from templates (`claude.md`, `INITIAL.md`, etc.)
5. Initialize `config/contextcraft.yaml` with defaults
6. Log to `runtime/logs/ccp.log`

**Key aspect:** Re-running must be idempotent (no duplicate `.gitignore` entries, preserve user edits).

### `new-feature`
**Purpose:** Convert a loosely specified feature idea into structured `INITIAL.md` spec.

**Behavior:**
1. Interactive Q&A: "What are you building?", "Why does it matter?", "Scope & constraints?", "Related modules?", "Known gotchas?"
2. Write or update `context/INITIAL.md` with a new feature section (or per-feature file in `context/features/`)
3. Optionally call Foundry Local to refine wording
4. Log operation

### `generate-prp`
**Purpose:** Create a Product Requirements Prompt (PRP) for a specific feature to be used with Claude Code.

**Behavior:**
1. Load context: config, project profile, rules, INITIAL spec, examples, docs
2. Build a prompt instructing Foundry Local to propose:
   - Context & assumptions
   - Goals and non-goals
   - Ordered implementation steps
   - Implementation checklist
   - Validation plan
3. Write structured result to `context/prps/<feature-slug>.md`

**Key aspect:** PRP must be self-contained enough that a coding assistant can read only that file plus relevant code and implement the feature.

### `validate`
**Purpose:** Capture validation results for how well the implementation matched the PRP.

**Behavior:**
1. Optionally execute test command in host repo root (capture exit code and output)
2. Prompt user: "Did implementation satisfy PRP?", "What broke?", "Patterns to promote?"
3. Write `context/validation/<feature-slug>.md` with test results, manual assessment, and suggestions
4. Suggest improvements to `claude.md` or examples (displayed, not auto-edited in MVP)

### `health`
**Purpose:** Snapshot of context health and potential stale artifacts.

**Behavior:**
1. Scan INITIAL, PRPs, and validation files
2. Identify features with missing PRPs or validations
3. Track timestamps and heuristics
4. Optional Foundry Local call to summarize and suggest next actions
5. Print report and optionally write `context/health-report.md`

**Key aspect:** Does not modify context files (unless creating health report).

### `export`
**Purpose:** Explicitly copy selected artifacts out of `ContextCraftPro/` into host repo for committing.

**Options:**
- `docs` → export to `../docs/`
- `readme` → export to `../README.context.md`
- `all` → export bundle into `../_context_exports/`

**Behavior:**
1. Require explicit confirmation (unless `--yes`)
2. Gather and render selected files
3. Never overwrite without confirmation
4. Log exports

## Global Options

- `--config <path>` → override default `contextcraft.yaml`
- `--dry-run` → show what would happen without writing
- `--verbose` → extra logs to stdout

## Configuration

**`contextcraft.yaml` (auto-generated on init):**
```yaml
foundry_local:
  endpoint: "http://localhost:11434/v1/chat/completions"
  model: "gpt-4o-mini"  # user can change

paths:
  project_root: ".."
  context_root: "context"
  claude_rules: "context/claude.md"
  initial_spec: "context/INITIAL.md"
  examples_dir: "context/examples"
  docs_dir: "context/docs-context"
  prps_dir: "context/prps"
  validation_dir: "context/validation"

behavior:
  auto_open_browser: false
  confirm_exports: true
```

Configuration can be overridden via environment variables.

## Implementation Notes

1. **Modular design:** Separate concerns into `ccp_cli.py`, `ccp_orchestrator.py`, `ccp_llm.py`, `ccp_fs.py`, `ccp_templates.py`

2. **Testability:**
   - Unit tests use temporary directories as fake host projects
   - Avoid hard-coding paths; derive from `__file__` and config
   - No external dependencies (Foundry Local) required for tests

3. **Prompt templates:** Keep in dedicated module for easy iteration

4. **Host repo access:** All behavior touching the host repo outside `ContextCraftPro/` must be explicit, documented, and confirmed

## Key Constraints & Functional Requirements

- **FR-1:** Must operate only within `ContextCraftPro/` by default (export/gitignore exceptions only)
- **FR-2:** Must support `init-project`, `new-feature`, `generate-prp`, `validate`, `health`, `export`
- **FR-3:** Must maintain config, project-profile, claude.md, INITIAL.md, prp-template, and logs
- **FR-4:** Check for `.gitignore` during init; prompt to add `ContextCraftPro/` entry
- **FR-5:** Support Foundry Local endpoint and model configuration via YAML and environment variables
- **FR-6:** Log all LLM calls with timestamp, feature, command, prompt size, truncated response size
- **FR-7:** Handle LLM errors gracefully with clear error messages
- **FR-8:** Re-running `init-project` must be idempotent
- **FR-9:** Deleting `ContextCraftPro/` folder leaves host project buildable and runnable
- **FR-10:** All config files must be human-editable text (YAML, Markdown, JSON)

## Non-Functional Requirements

- **NFR-1 – Local-Only:** No network access beyond configured Foundry Local endpoint
- **NFR-2 – Performance:** Core commands should complete within seconds (plus LLM latency) for typical repos
- **NFR-3 – Security:** Never read/send secrets (`.env`, keys) to LLM by default; opt-in with clear labeling
- **NFR-4 – Portability:** Must run on Windows, macOS, Linux with Python 3.8+
- **NFR-5 – Observability:** Logs in `runtime/logs/ccp.log` must be sufficient to reconstruct command history
