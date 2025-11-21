# ContextCraftPro — AI-Driven Context Engineering

## Overview

**ContextCraftPro (CCP)** is a self-contained, disposable Python tool that enables structured **context engineering** for AI-driven development. It helps you:

- **Define features** with structured specifications
- **Generate PRPs** (Product Requirements Prompts) that guide AI coding assistants
- **Validate implementations** against requirements
- **Maintain context health** and track completeness

This folder is **git-ignored** and **entirely disposable**—delete it anytime without affecting your project.

### Key Principles

- 🏠 **Local-only**: All operations use Foundry Local (no cloud LLM calls)
- 📦 **Self-contained**: Everything lives inside `ContextCraftPro/`
- 🗑️ **Disposable**: Delete the folder and your project is unchanged
- 🤖 **Agentic**: Guides you through structured workflows with optional LLM enhancement
- 📝 **Transparent**: All artifacts are human-readable text (Markdown, YAML, JSON)

---

## Installation & Setup

### Requirements

- **Python 3.8+**
- **Foundry Local** running locally with OpenAI-compatible API

See root [README.md](../README.md#requirements) for Foundry Local installation and setup instructions.

### Step 1: Install Dependencies

```bash
cd ContextCraftPro
pip install -r requirements.txt
```

### Step 2: Initialize the Project (First Time)

```bash
python ccp.py init-project
```

This one-time command:
- ✓ Profiles your repo (detects languages, frameworks, test setup)
- ✓ Creates context directory structure
- ✓ Seeds `claude.md` with coding guidelines
- ✓ Initializes `config/contextcraft.yaml`
- ✓ Asks to add `ContextCraftPro/` to `.gitignore`

**Re-running is safe** — it's idempotent and preserves your existing work.

### Step 3: Verify Foundry Local Connection

```bash
python ccp.py health
```

This checks if Foundry Local is reachable and ready. You should see:
```
✓ Foundry Local is accessible
  Endpoint: http://127.0.0.1:PORT/v1/chat/completions
  Model: qwen2.5-0.5b
```

---

## Quick Start: Feature to PRP Workflow

### 1. Define a New Feature

```bash
python ccp.py new-feature
```

Interactive prompts ask you:
- What are you building? (feature name & description)
- Why does it matter? (user value)
- What's in scope? (scope & constraints)
- Related code areas? (modules/components)
- Any gotchas? (known issues or technical challenges)

Your answers are structured into `context/INITIAL.md` as a feature spec.

### 2. Generate a Product Requirements Prompt (PRP)

```bash
python ccp.py generate-prp --feature my-feature
```

This uses Foundry Local to:
1. Read your feature spec from `INITIAL.md`
2. Gather context (coding rules, examples, docs)
3. Generate a comprehensive PRP with:
   - **Context & Assumptions** — what the code currently does
   - **Goals and Non-Goals** — what to build and what to avoid
   - **Ordered Implementation Steps** — precise, actionable steps
   - **Implementation Checklist** — verification points
   - **Validation Plan** — how to test it

Result: `context/prps/my-feature.md` — use this file with Claude Code or other AI assistants.

### 3. Implement the Feature

Use the PRP with your coding assistant:

```bash
# Example with Claude Code CLI
claude-code --instructions "context/prps/my-feature.md"
```

Or copy/paste the PRP into Claude Code web interface.

### 4. Validate Against Requirements

```bash
python ccp.py validate --feature my-feature
```

This:
- Runs your project tests (if configured)
- Asks you: Did it work? What broke? What's good?
- Uses LLM to analyze and record validation results
- Saves insights to `context/validation/my-feature.md`

### 5. Check Overall Health

```bash
python ccp.py health
```

Shows a snapshot:
- Features with/without PRPs
- Features with/without validation
- Age of artifacts (flags stale work)
- Completeness percentage

---

## Command Reference

### `init-project`

**Purpose:** First-time setup of ContextCraftPro for your repo.

```bash
python ccp.py init-project [OPTIONS]
```

**What it does:**
1. Scans your repo for languages, frameworks, test commands
2. Creates `config/contextcraft.yaml` with defaults
3. Seeds `context/claude.md` with coding guidelines
4. Initializes `context/INITIAL.md` with template
5. Asks to add `ContextCraftPro/` to `.gitignore`

**Options:**
- `--dry-run` — Show what would be created without writing
- `--verbose` — Extra logging to stdout

**Idempotent?** Yes. Safe to re-run.

---

### `new-feature`

**Purpose:** Create a structured feature specification.

```bash
python ccp.py new-feature [OPTIONS]
```

**What it does:**
1. Interactive Q&A about the feature (name, description, scope, etc.)
2. Optional LLM refinement of your answers (configurable)
3. Writes feature section to `context/INITIAL.md`

**Options:**
- `--feature-name TEXT` — Pre-fill feature name (skips first prompt)
- `--no-llm` — Skip LLM refinement, use template format
- `--dry-run` — Show output without writing
- `--verbose` — Extra logging

**Example:**
```bash
python ccp.py new-feature --feature-name "user-authentication"
```

**Output:** Feature section appended to `context/INITIAL.md`

---

### `generate-prp`

**Purpose:** Generate a Product Requirements Prompt for implementation.

```bash
python ccp.py generate-prp --feature FEATURE_SLUG [OPTIONS]
```

**What it does:**
1. Loads feature spec from `context/INITIAL.md`
2. Gathers context: coding rules, examples, docs
3. Calls Foundry Local to generate comprehensive PRP
4. Validates PRP structure (ensures all sections present)
5. Shows for review, asks to confirm
6. Saves to `context/prps/<feature-slug>.md`

**Options:**
- `--feature FEATURE_SLUG` — Required. Feature to generate PRP for
- `--temperature FLOAT` — LLM sampling (0.0–1.0, default 0.7)
- `--max-tokens INT` — Max response length (default auto)
- `--dry-run` — Show what would be written
- `--verbose` — Extra logging

**Example:**
```bash
python ccp.py generate-prp --feature user-auth
```

**Output:** Markdown file at `context/prps/user-auth.md`

---

### `validate`

**Purpose:** Record how well implementation matched the PRP.

```bash
python ccp.py validate --feature FEATURE_SLUG [OPTIONS]
```

**What it does:**
1. Loads original PRP for the feature
2. Optionally runs tests in your repo (captures output)
3. Asks you: Did it work? What broke? What's good?
4. Uses LLM to analyze and produce validation report
5. Saves to `context/validation/<feature-slug>.md`

**Options:**
- `--feature FEATURE_SLUG` — Required. Feature to validate
- `--tests-command TEXT` — Override test command (instead of config)
- `--skip-tests` — Skip test execution entirely
- `--dry-run` — Show report without saving
- `--verbose` — Extra logging

**Example:**
```bash
python ccp.py validate --feature user-auth --tests-command "pytest -v tests/"
```

**Output:** Markdown file at `context/validation/user-auth.md`

---

### `health`

**Purpose:** Assess overall context health and completeness.

```bash
python ccp.py health [OPTIONS]
```

**What it does:**
1. Scans all features, PRPs, and validation files
2. Calculates health metrics:
   - Total features defined
   - Features with PRPs (% complete)
   - Features with validation (% complete)
   - Age of artifacts (flags >30 days old)
3. Optional LLM analysis of stale artifacts and next actions
4. Displays summary and optional health report

**Options:**
- `--generate-report` — Save health report to `context/health-report.md`
- `--verbose` — Extra logging

**Output:** Colored status display + optional health report

**Example output:**
```
📊 Context Health Report
========================
✓ 3 features defined
  ✓ 2 with PRPs (67%)
  ✓ 1 validated (33%)
  ⚠ 1 stale (>30 days)

Issues Found:
  • feature-x: No PRP generated yet
  • feature-y: Not validated
```

---

### `export`

**Purpose:** Export context artifacts to your main repo.

```bash
python ccp.py export --target TARGET [OPTIONS]
```

**What it does:**
1. Gathers selected context artifacts (PRPs, validation, docs)
2. Renders them into readable format
3. Copies to specified location in your repo
4. Confirms before overwriting

**Export targets:**
- `docs` — Export to `../docs/context/` directory
- `readme` — Export to `../README.context.md` (single file)
- `all` — Export everything to `../_context_exports/<timestamp>/` (full bundle)

**Options:**
- `--target TARGET` — Required. One of: docs, readme, all
- `--yes` — Skip confirmation prompts (auto-confirm)
- `--dry-run` — Show what would be exported
- `--verbose` — Extra logging

**Examples:**
```bash
# Export all PRPs and validation to docs/
python ccp.py export --target docs

# Export single README to main repo
python ccp.py export --target readme --yes

# Full bundle with timestamp
python ccp.py export --target all
```

**Caution:** Always review exports before committing—they touch your main repo!

---

## Configuration

### `config/contextcraft.yaml`

Generated by `init-project`. Edit to customize:

```yaml
foundry_local:
  endpoint: "http://127.0.0.1:PORT/v1/chat/completions"  # Replace PORT with your Foundry Local port
  model: "qwen2.5-0.5b"
  timeout: 30
  max_retries: 3

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
  enable_refinement: true
  require_confirmation: true
```

### Environment Variable Overrides

All config values can be overridden with `CCP_*` environment variables:

```bash
# Override endpoint (check Foundry Local output for PORT)
export CCP_FOUNDRY_LOCAL_ENDPOINT="http://127.0.0.1:PORT/v1/chat/completions"

# Override model
export CCP_FOUNDRY_LOCAL_MODEL="qwen2.5-0.5b"

# Override timeout (seconds)
export CCP_FOUNDRY_LOCAL_TIMEOUT=60

# Skip confirmation on exports
export CCP_CONFIRM_EXPORTS=false

# Run commands
python ccp.py generate-prp --feature my-feature
```

---

## Directory Structure

```
ContextCraftPro/
├── ccp.py                     Main CLI entry point
├── README.md                  This file
├── requirements.txt           Python dependencies
│
├── config/
│   └── contextcraft.yaml      Configuration (auto-generated)
│
├── context/                   All context artifacts
│   ├── project-profile.yaml   Auto-detected repo info
│   ├── claude.md              Global coding rules for AI assistants
│   ├── INITIAL.md             Feature specifications (you edit this)
│   ├── examples/              Code examples for LLM context
│   ├── docs-context/          Documentation references
│   ├── prps/                  Product Requirements Prompts
│   │   ├── feature-1.md
│   │   └── feature-2.md
│   └── validation/            Validation reports
│       ├── feature-1.md
│       └── feature-2.md
│
├── runtime/
│   └── logs/
│       └── ccp.log            Operation logs (JSON format)
│
├── templates/                 Markdown templates (internal)
│   ├── claude-rules-template.md
│   ├── initial-template.md
│   ├── prp-template.md
│   └── ...
│
├── core/                      Python implementation
│   ├── ccp_cli.py             CLI command routing
│   ├── ccp_orchestrator.py    Core logic & workflows
│   ├── ccp_llm.py             Foundry Local client
│   ├── ccp_prompts.py         Prompt templates
│   ├── ccp_config.py          Configuration management
│   ├── ccp_fs.py              Filesystem utilities
│   └── ccp_logger.py          Structured logging
│
└── docs/                      Architecture docs
    └── llm-architecture.md    LLM integration design
```

---

## Workflows & Use Cases

### Use Case 1: New Feature from Scratch

```bash
# 1. Define the feature
$ python ccp.py new-feature
  → Prompts: name, description, scope, modules, gotchas
  → Writes to context/INITIAL.md

# 2. Generate PRP
$ python ccp.py generate-prp --feature my-new-feature
  → Reads spec from INITIAL.md
  → Calls LLM with full context
  → Saves PRP to context/prps/my-new-feature.md

# 3. Use PRP with Claude Code
$ cat context/prps/my-new-feature.md  # Copy contents
  → Paste into Claude Code
  → Let AI implement based on PRP

# 4. Validate
$ python ccp.py validate --feature my-new-feature
  → Runs tests
  → Asks if implementation matched PRP
  → Records insights to context/validation/my-new-feature.md
```

### Use Case 2: Context Health Check

```bash
# Check overall status
$ python ccp.py health
  Shows:
  - Features without PRPs
  - PRPs without validation
  - Stale artifacts (30+ days)

# Generate report
$ python ccp.py health --generate-report
  → Saves to context/health-report.md
  → Good for planning next steps
```

### Use Case 3: Export for Stakeholders

```bash
# Export all PRPs to docs/
$ python ccp.py export --target docs
  → Copies prps/ and validation/ to ../docs/context/
  → Creates summary README

# Single file export
$ python ccp.py export --target readme
  → Exports to ../README.context.md
  → Good for including in main README
```

---

## Best Practices

### 1. Keep `claude.md` Updated

Your `context/claude.md` contains coding rules and patterns. As you discover:
- Common mistakes in implementations
- Patterns that work well
- Project-specific conventions

Add them to `claude.md` so LLM uses this knowledge for future PRPs.

### 2. Review PRPs Before Use

Always review the generated PRP before using it:
- Check that it matches your intent
- Look for any misunderstandings
- Edit if needed (it's just Markdown)

Use `--dry-run` to preview:
```bash
python ccp.py generate-prp --feature x --dry-run
```

### 3. Validate Regularly

Don't skip validation:
- Captures what worked and what didn't
- Feeds back into context (improves future PRPs)
- Creates a record of decisions

### 4. Use Dry-Run Before Write

Most commands support `--dry-run` to preview changes:

```bash
python ccp.py export --target docs --dry-run
python ccp.py new-feature --dry-run
```

### 5. Check Health Weekly

Monitor context freshness:

```bash
python ccp.py health --generate-report
# Review context/health-report.md
# Address stale or incomplete items
```

---

## Troubleshooting

### First: Check Your Configuration

Before troubleshooting, verify your current configuration:

```bash
python ccp.py config
```

This shows:
- Active Foundry Local endpoint and model
- All configured file paths
- Behavior settings

If the model or endpoint is wrong, this is usually the problem.

### Problem: "Cannot connect to Foundry Local"

**Error:** `Cannot connect to Foundry Local`

**Solution:**
1. Check if Foundry Local is running:
   ```bash
   foundry service status
   ```
2. If not, start a model:
   ```bash
   foundry model run qwen2.5-0.5b
   ```
3. Verify endpoint in `config/contextcraft.yaml`

### Problem: "Model not found"

**Error:** `Model 'gpt-4o-mini' not found. Check available models: foundry-local list`

**Solution:**
1. List available models:
   ```bash
   foundry-local list
   ```
2. Update `config/contextcraft.yaml`:
   ```yaml
   foundry_local:
     model: "llama2"  # or other available model
   ```

### Problem: "Feature not found in INITIAL.md"

**Error:** `Could not extract feature 'my-feature' from INITIAL.md`

**Solution:**
1. Check that feature exists in `context/INITIAL.md`
2. Ensure section header matches (case-sensitive):
   ```markdown
   ## my-feature
   ```
3. Use `new-feature` to create it first

### Problem: "Request timed out"

**Error:** `Request timed out. Try a simpler prompt or increase timeout in config.`

**Solution:**
- Increase timeout in `config/contextcraft.yaml`:
  ```yaml
  foundry_local:
    timeout: 60  # Was 30
  ```
- Use simpler prompts (fewer examples in context)
- Try a faster model

### Problem: Tests won't run during validation

**Error:** `Failed to run tests: [error details]`

**Solution:**
1. Verify test command works manually:
   ```bash
   cd ..
   pytest  # or your test command
   ```
2. Update `config/contextcraft.yaml` with correct command
3. Use `--skip-tests` flag to skip validation tests:
   ```bash
   python ccp.py validate --feature x --skip-tests
   ```

---

## Advanced Configuration

### Custom Foundry Local Endpoint

For remote Foundry Local or custom setup:

```yaml
foundry_local:
  endpoint: "http://192.168.1.100:8000/v1/chat/completions"
  model: "custom-model"
```

### Different Models for Different Tasks

Create wrapper script:

```bash
#!/bin/bash
export CCP_FOUNDRY_LOCAL_MODEL="gpt-4-turbo"
python ccp.py generate-prp --feature "$1"
```

### Disable LLM Refinement

For offline mode or to save LLM calls:

```yaml
behavior:
  enable_refinement: false  # Skip LLM in new-feature
```

---

## Logging & Debugging

All operations are logged to `runtime/logs/ccp.log` in JSON format:

```bash
# View logs
tail -f runtime/logs/ccp.log

# Pretty-print logs
cat runtime/logs/ccp.log | jq .
```

Enable verbose output:

```bash
python ccp.py generate-prp --feature x --verbose
```

---

## Deleting ContextCraftPro

When you're done:

```bash
rm -rf ContextCraftPro/
```

Your project is unchanged. All files live only inside the `ContextCraftPro/` folder.

---

## Project: ContextCraftlocal

**Languages:** (none)
**Frameworks:** (none)
**Test Command:** `pytest`

---

*ContextCraftPro v1.0 — Initialized on 2025-11-21*
*For architecture details, see [docs/llm-architecture.md](docs/llm-architecture.md)*
