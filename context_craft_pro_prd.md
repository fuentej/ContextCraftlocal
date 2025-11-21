# ContextCraftPro – Detailed Product Requirements Document (PRD)

**Version:** 0.2  
**Owner:** Josh / AgentFactory  
**Target Implementer:** Claude Code (or similar AI coding assistant)  
**Runtime:** Local-only, Python-based tooling + Azure AI Foundry Local ("Foundry Local")

---

## 1. Product Overview

### 1.1 One‑Sentence Summary

ContextCraftPro is a **self‑contained, disposable folder** that you drop into any codebase to get an opinionated, agent‑driven **context engineering workspace** powered by Foundry Local, then safely delete when the project is done.

### 1.2 Key Properties

- **Ephemeral:** All of ContextCraftPro lives inside `ContextCraftPro/` at the project root. It leaves no hidden state outside that folder unless the user explicitly asks for exports.
- **Git‑ignored:** The host project’s `.gitignore` must contain `ContextCraftPro/`. The tool should optionally help add this entry on first run.
- **Local‑only:** The LLM runs via **Foundry Local** on the developer’s machine. No cloud LLM calls.
- **Agentic workflow:** It guides the user through a structured context engineering process (project rules, INITIAL specs, PRPs, validation, and health checks) to be consumed by external AI coders like Claude Code.
- **Deletable:** When the user is done with planning / context work, they can simply delete the `ContextCraftPro/` folder with no impact on application runtime code.

### 1.3 Primary Goal

> Replace ad‑hoc “vibe prompting” for coding with a **repeatable, file‑backed context engineering workflow** that can be used in any repo with near‑zero friction and then thrown away.

The output of ContextCraftPro is:

- Better **specs** (`INITIAL`) and **plans** (PRPs) for features.
- A consistent set of **rules** for AI coders (e.g., `claude.md`).
- **Validation logs** and **context health insights** that can be referenced during development.

All of that lives under `ContextCraftPro/` and is intentionally **not** part of the host repo’s tracked source unless the user chooses to export copies.

---

## 2. Personas & Usage Scenarios

### 2.1 Personas

1. **Solo Dev / Consultant (primary)**  
   - Wants to spin up context engineering on any client repo quickly.  
   - Does not want to permanently “infect” the repo with tooling files.

2. **Team Lead / Architect**  
   - Wants repeatable AI‑coding practices across multiple projects.  
   - Needs a common workflow that can travel from repo to repo.

3. **AI Tooling Engineer**  
   - Owns dev‑experience tools.  
   - Needs a modular, self‑contained context workspace for experiments and pilots.

### 2.2 Example Scenario

1. Developer clones a repo `my-app`.
2. Copies `ContextCraftPro/` folder into the root of `my-app/` (or `git clone` a CCP template into that folder).
3. Ensures `.gitignore` contains `ContextCraftPro/`.
4. Runs `python ContextCraftPro/ccp.py init-project`.  
   - CCP asks questions, scans the repo, and sets up a local context workspace.
5. Runs `ccp new-feature`, `ccp generate-prp`, etc., and uses the generated PRPs + rules in Claude Code.
6. After feature work and validation is done, **optionally export** any final docs to `/docs` or elsewhere.  
7. Deletes the `ContextCraftPro/` folder. The app still builds and runs; the repo remains clean.

---

## 3. High-Level Architecture

### 3.1 Directory Layout (Within Host Project)

At the host project root:

```text
my-app/
  src/               # existing app code (unchanged by CCP)
  tests/
  ...
  ContextCraftPro/   # self-contained CCP workspace (git-ignored)
```

Inside `ContextCraftPro/`:

```text
ContextCraftPro/
  README.md                 # how to use CCP in this project

  ccp.py                    # CLI entrypoint (python script / package main)

  config/
    contextcraft.yaml       # core configuration & paths
    models.yaml             # (optional) Foundry Local model mapping

  context/
    project-profile.yaml    # derived project metadata (language, layout, etc.)
    claude.md               # global rules for AI coding assistants
    INITIAL.md              # current feature / change spec

    examples/               # examples for LLM
      README.md             # how to use examples

    docs-context/           # doc pointers for LLM
      docs-index.md

    prps/                   # Product Requirements Prompts
      prp-template.md
      <feature-slug>.md

    validation/             # validation logs per feature
      <feature-slug>.md

  runtime/
    logs/
      ccp.log               # run logs
    sessions/
      <session-id>.json     # optional per-session snapshots

  templates/                # reusable templates
    claude-rules-template.md
    initial-template.md
    prp-template.md
    planning-template.md
    task-template.md
    readme-template.md
```

> **Rule:** CCP MUST NOT create or modify files outside `ContextCraftPro/` unless the user explicitly triggers an **export** command.

### 3.2 Main Components

1. **CLI / Command Layer (`ccp.py`)**
   - Parses commands and options.
   - Dispatches to orchestrator functions.

2. **Orchestrator / Core Logic**
   - Knows how to:
     - Inspect the host repo (one directory up from `ContextCraftPro/`).
     - Read/write context files under `ContextCraftPro/context/`.
     - Manage sessions and run history.
   - Calls LLM client with well-structured prompts.

3. **LLM Client**
   - Minimal wrapper around Foundry Local’s OpenAI-compatible HTTP API.
   - Handles retries, timeouts, and simple safety checks (e.g., ensure output is valid Markdown where expected).

4. **Tooling Utilities**
   - Repo scanner (language, structure, `pyproject.toml`/`package.json`, etc.).
   - Template renderer.
   - Basic markdown parsing/section extraction where needed.

### 3.3 Technology Choices

- **Language:** Python 3.11+.
- **Dependencies:**
  - Standard library where possible.
  - Optional: `pyyaml` for YAML configs.
  - Optional: `rich` or similar for nicer CLI output (non‑essential).
- **No database:** All state stored as text/Markdown/YAML/JSON inside `ContextCraftPro/`.

---

## 4. Commands & Workflows

### 4.1 CLI Conventions

- All commands are executed from the **host repo root** for convenience, but target the `ContextCraftPro/` folder.

Examples:

```bash
# From my-app/
python ContextCraftPro/ccp.py init-project
python ContextCraftPro/ccp.py new-feature
python ContextCraftPro/ccp.py generate-prp --feature login-flow
python ContextCraftPro/ccp.py validate --feature login-flow
python ContextCraftPro/ccp.py health
python ContextCraftPro/ccp.py export --target docs
```

The script should also work when run from within `ContextCraftPro/` if it can successfully locate the host root by walking `..`.

#### 4.1.1 Global Options

- `--config <path>`: override default `ContextCraftPro/config/contextcraft.yaml`.
- `--dry-run`: do not write any files, just show what would happen.
- `--verbose`: extra logs to stdout.

---

### 4.2 `init-project`

**Intent:** First‑time setup of ContextCraftPro for the current host repo.

#### 4.2.1 Behavior

1. **Verify Layout**
   - Confirm script is inside `ContextCraftPro/`.
   - Determine host root as `..` (one folder up).

2. **Ensure Git Ignore**
   - Look for `.gitignore` in the host root.
   - If found and `ContextCraftPro/` is **not** present:
     - Prompt: `"Recommend adding 'ContextCraftPro/' to .gitignore. Add now? [Y/n]"`.
     - If `Y` (default), append `ContextCraftPro/` with a comment.
   - If `.gitignore` missing, show non‑blocking warning.

3. **Project Profiling**
   - Inspect host repo:
     - Languages (`.py`, `.ts/.js`, `.cs`, etc.).
     - Presence of common configs (`pyproject.toml`, `package.json`, `dockerfile`, etc.).
   - Write a `context/project-profile.yaml` containing:

     ```yaml
     name: <folder-name>
     languages:
       - python
       - typescript
     frameworks:
       - fastapi
       - react
     tests:
       framework: pytest
       command: "pytest"
     notes: "Derived automatically. User can edit."
     ```

4. **Seed Context Files**

   - If `context/claude.md` does not exist:
     - Copy from `templates/claude-rules-template.md` and interpolate project name.
   - If `context/INITIAL.md` does not exist:
     - Copy from `templates/initial-template.md`.
   - Ensure `examples/`, `docs-context/`, `prps/`, `validation/` exist.
   - Ensure `docs-context/docs-index.md` exists with stub content.
   - Ensure `prps/prp-template.md` exists (copy from `templates/prp-template.md`).

5. **Initialize Config**

   - If `config/contextcraft.yaml` does not exist, create with defaults:

     ```yaml
     foundry_local:
       endpoint: "http://localhost:11434/v1/chat/completions"
       model: "gpt-4o-mini"  # example, user can change

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

6. **Log** operation to `runtime/logs/ccp.log`.

#### 4.2.2 Acceptance Criteria

- Running `init-project` on a new repo creates the expected folder structure and files entirely under `ContextCraftPro/`.
- `.gitignore` is updated or the user is clearly warned.
- Re‑running `init-project` is **idempotent** (no duplicate edits to `.gitignore`, no overwriting of edited context files without confirmation).

---

### 4.3 `new-feature`

**Intent:** Convert a loosely specified feature idea into a structured `INITIAL.md` feature section and optional per-feature file.

#### 4.3.1 Inputs

- Flags:
  - `--feature <slug>` (optional). If omitted, CCP prompts for a feature name.

#### 4.3.2 Behavior

1. Interactive Q&A in terminal:
   - "What are you trying to build?" (short description)
   - "Why does this feature matter?" (business / user value)
   - "Scope & constraints?" (in/out of scope, performance, security)
   - "Any related modules or files to reuse?" (paths or names)
   - "Any known gotchas for AI tools here?" (things that often go wrong)

2. Assemble a data structure in memory representing the feature.

3. Write or update **`context/INITIAL.md`**:
   - Either append a new section per feature (e.g., `## Feature: <name>`) or create `context/features/<feature>.md` and link from `INITIAL.md` (implementation choice; define in code comments).
   - Use the `templates/initial-template.md` formatting with the captured answers filled in.

4. Optionally run a **short LLM pass** via Foundry Local:
   - To refine wording and acceptance criteria (but not required for MVP).

5. Log operation.

#### 4.3.3 Acceptance Criteria

- After running `new-feature`, `context/INITIAL.md` contains a clearly labeled section describing the feature with:
  - Problem / goal
  - Why it matters
  - Scope & constraints
  - Inputs and outputs
  - Acceptance criteria checklist
- No changes are made outside `ContextCraftPro/`.

---

### 4.4 `generate-prp`

**Intent:** Create a **Product Requirements Prompt (PRP)** for a specific feature, to be used with Claude Code or similar.

#### 4.4.1 Inputs

- `--feature <slug>` (required). Must match a feature defined in `INITIAL`.

#### 4.4.2 Behavior

1. Load context:
   - `config/contextcraft.yaml`.
   - `context/project-profile.yaml`.
   - `context/claude.md`.
   - `context/INITIAL.md` (or per-feature file).
   - Any existing example files under `context/examples/`.
   - `docs-context/docs-index.md` and linked local docs (if any).

2. Build a **prompt** for Foundry Local instructing it to:
   - Read the feature definition.
   - Consider global rules (`claude.md`).
   - Propose a structured implementation plan and validation strategy.

3. Call Foundry Local via LLM client.

4. Parse result as Markdown and write to `context/prps/<feature-slug>.md`, based on `prp-template.md` structure:
   - Context & assumptions.
   - Goals and non-goals.
   - Plan with ordered steps.
   - Implementation checklist.
   - Validation plan.

5. Log operation and reference to PRP path.

#### 4.4.3 Acceptance Criteria

- The generated PRP file exists and is syntactically valid Markdown.
- The PRP references the feature and project by correct name.
- The PRP is **self-contained** enough that a coding assistant can read only that file plus relevant code and implement the feature.

---

### 4.5 `validate`

**Intent:** Capture validation results and feedback about how well the AI‑driven implementation matched the PRP.

#### 4.5.1 Inputs

- `--feature <slug>` (required).
- Optional `--tests-command "<cmd>"` to override default test command from `project-profile.yaml`.
- Optional `--no-tests` to skip running tests.

#### 4.5.2 Behavior

1. If `--no-tests` not set, execute the test command in the **host repo root** (e.g., `pytest`, `npm test`).
   - Capture exit code and minimal stdout/stderr summary.

2. Prompt the user for manual feedback:
   - "Did the implementation satisfy the PRP?" (Y/N)
   - "What broke or felt wrong?" (free text)
   - "Any patterns we should promote to examples?" (file paths or descriptions)

3. Write/update `context/validation/<feature-slug>.md` with:
   - PRP reference.
   - Test command & result.
   - Manual assessment.
   - Suggested improvements to rules or examples.

4. Optionally suggest updates to `claude.md` or `examples/` (printed suggestions; actual edits can be manual in MVP).

#### 4.5.3 Acceptance Criteria

- Validation file created with:
  - Timestamp.
  - Test outcome.
  - Manual notes.
- No destructive changes to host repo.

---

### 4.6 `health`

**Intent:** Provide a snapshot of context health and potential rot.

#### 4.6.1 Behavior

1. Scan `context/INITIAL.md`, `context/prps/`, and `context/validation/` to identify:
   - Features with INITIAL but no PRP.
   - Features with PRP but no validation.
   - Old PRPs (e.g., older than X days) that have changed code around them.

2. Simple heuristics (no LLM needed in MVP):
   - Compare timestamps of PRP vs latest validation file.
   - Track counts of features in each state.

3. Optional LLM call to summarize and suggest next actions.

4. Print a report to stdout and optionally write a `context/health-report.md` file.

#### 4.6.2 Acceptance Criteria

- Running `health` does not modify any context files (unless creating/updating `health-report.md`).
- Report clearly shows per-feature status and any obvious follow-up actions.

---

### 4.7 `export`

**Intent:** Allow the user to explicitly copy selected artifacts **out of** `ContextCraftPro/` into host repo locations that will be committed.

#### 4.7.1 Inputs

- `--target <preset>` where `<preset>` might be:
  - `docs` → export high-level docs to `../docs/`.
  - `readme` → export a README draft to `../README.context.md`.
  - `all` → export a bundle into `../_context_exports/`.

#### 4.7.2 Behavior

1. Must confirm operation (unless `--yes` used):
   - `"This will create/update files outside ContextCraftPro/. Continue? [y/N]"`

2. For `docs` preset, for example:
   - Gather key context files (`project-profile.yaml`, selected PRPs, latest health report).
   - Render or copy them into `../docs/context/` or similar.

3. Never overwrite host repo files without **explicit confirmation**.

4. Log exports.

#### 4.7.3 Acceptance Criteria

- No accidental overwrites of host repo files.
- All exported content remains readable and clearly labeled as generated by ContextCraftPro.

---

## 5. Functional Requirements (FR)

**FR-1**: CCP MUST operate only within the `ContextCraftPro/` folder by default and MUST NOT modify any files outside that folder except when running a validated `export` command or a user-approved `.gitignore` update.

**FR-2**: CCP MUST support at least the commands: `init-project`, `new-feature`, `generate-prp`, `validate`, `health`, `export`.

**FR-3**: CCP MUST create and maintain:
- `config/contextcraft.yaml`
- `context/project-profile.yaml`
- `context/claude.md`
- `context/INITIAL.md`
- `context/prps/prp-template.md`
- `runtime/logs/ccp.log`

**FR-4**: CCP MUST check for `.gitignore` in host root during `init-project` and:
- If present and missing `ContextCraftPro/`, prompt to add an entry and append on consent.
- If absent, print a clear suggestion but continue.

**FR-5**: CCP MUST support configuration of Foundry Local endpoint and model via `contextcraft.yaml` and override via environment variables.

**FR-6**: CCP MUST log all LLM calls with at least timestamp, feature, command, prompt size, and truncated response size.

**FR-7**: CCP MUST handle LLM errors gracefully (e.g., connection failure, malformed output) and present clear error messages.

**FR-8**: Re-running `init-project` MUST be idempotent, preserving user edits to context files.

**FR-9**: CCP MUST allow easy deletion: if `ContextCraftPro/` is removed, the host project remains buildable and runnable.

**FR-10**: All configuration files MUST be human-editable text (YAML, Markdown, JSON).

---

## 6. Non-Functional Requirements (NFR)

**NFR-1 – Local-Only:** No network access beyond the configured Foundry Local endpoint.

**NFR-2 – Performance:** For typical repos (<10k files), core commands (`init-project`, `health`) should complete within a few seconds plus any LLM latency.

**NFR-3 – Security:**
- CCP MUST NOT read or send secrets (e.g., `.env`, Azure keys) to LLM by default.
- Any inclusion of secrets in prompts MUST be opt-in and clearly labeled.

**NFR-4 – Portability:**
- CCP MUST run on Windows, macOS, and Linux if Python 3.11+ is available.

**NFR-5 – Observability:**
- Logs in `runtime/logs/ccp.log` MUST be sufficient to reconstruct what commands were run and on which features.

---

## 7. Implementation Notes for Claude Code

1. Treat `ContextCraftPro/` as a **single, self-contained Python package** with modules like:
   - `ccp_cli.py` – argument parsing & command routing
   - `ccp_orchestrator.py` – core workflow logic
   - `ccp_llm.py` – Foundry Local client
   - `ccp_fs.py` – file system utilities
   - `ccp_templates.py` – template loading and rendering

2. Emphasize **testability**:
   - Write unit tests for each command using a temporary directory as a fake host project.
   - Avoid hard-coding paths; derive from `__file__` and config.

3. Keep **prompt templates** (for LLM) in a dedicated module or file so they are easy to iterate on later.

4. All behavior that touches the host repo outside `ContextCraftPro/` must be behind an explicit function with clear docstrings and confirmations.

---

## 8. Out of Scope (for v1)

- UI beyond CLI (no web dashboard in v1).
- Multi-repo / global project views.
- Automatic refactoring of existing code based on context health.
- Deep git integration (no auto-commits or branch creation).

---

## 9. Definition of Done (v1)

ContextCraftPro v1 is considered **Done** when:

1. A developer can:
   - Copy `ContextCraftPro/` into any repo.
   - Run `init-project`, `new-feature`, `generate-prp`, `validate`, and `health` without errors.
2. All generated artifacts live under `ContextCraftPro/` and can be deleted by removing that folder.
3. `.gitignore` support works as described.
4. At least one real project has successfully used ContextCraftPro to:
   - Define a feature with `new-feature`.
   - Generate a PRP with `generate-prp`.
   - Implement the feature using that PRP in Claude Code.
   - Record validation outcomes with `validate`.
5. The codebase is readable, documented, and covered by basic tests.

