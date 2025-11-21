# ContextCraftPro Workspace

## What is This?

This `ContextCraftPro/` folder is a **self-contained context engineering workspace** for this project. It helps you:

- Create structured feature specifications (INITIAL.md)
- Generate Product Requirements Prompts (PRPs) for AI coding assistants
- Validate implementation against requirements
- Maintain context health over time

**Important:** This folder is **git-ignored** and **disposable**. When you're done with planning and context work, you can safely delete it.

## Quick Start

### 1. Install Dependencies

```bash
cd ContextCraftPro
pip install -r requirements.txt
```

### 2. Initialize (First Time Only)

```bash
python ccp.py init-project
```

This will:
- Profile your project (languages, frameworks, tests)
- Set up context files (claude.md, INITIAL.md)
- Add ContextCraftPro/ to .gitignore (with confirmation)

### 3. Define a New Feature

```bash
python ccp.py new-feature
```

Interactive prompts will guide you through creating a structured feature spec.

### 4. Generate a PRP

```bash
python ccp.py generate-prp --feature login-flow
```

Creates a Product Requirements Prompt using Foundry Local that you can use with Claude Code or other AI coding assistants.

### 5. Validate Implementation

```bash
python ccp.py validate --feature login-flow
```

Runs tests and collects feedback about how well the implementation matched the PRP.

### 6. Check Context Health

```bash
python ccp.py health
```

Shows which features have specs, PRPs, and validation; flags stale artifacts.

### 7. Export Artifacts (Optional)

```bash
python ccp.py export --target docs
```

Copies selected context artifacts to your main repo (with confirmation).

## Configuration

Edit `config/contextcraft.yaml` to configure:
- Foundry Local endpoint and model
- File paths
- Behavior options

## Commands Reference

| Command | Purpose |
|---------|---------|
| `init-project` | First-time setup of ContextCraftPro |
| `new-feature` | Create a new feature specification |
| `generate-prp` | Generate a PRP for a feature |
| `validate` | Record validation results |
| `health` | Check context freshness |
| `export` | Export artifacts to main repo |

## Directory Structure

```
ContextCraftPro/
├── config/            Configuration files
├── context/           All context artifacts
│   ├── claude.md      AI coding rules
│   ├── INITIAL.md     Feature specifications
│   ├── prps/          Product Requirements Prompts
│   └── validation/    Validation results
├── runtime/           Logs and session data
└── templates/         Markdown templates
```

## Project: {{project_name}}

**Languages:** {{languages}}
**Frameworks:** {{frameworks}}
**Test Command:** `{{test_command}}`

---

*Initialized on {{date}}*
