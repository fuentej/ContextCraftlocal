# ContextCraftPro

**ContextCraftPro (CCP)** is a self-contained, disposable Python tool that enables structured context engineering for AI-driven development.

## What is it?

ContextCraftPro helps you:

- **Define features** with structured specifications
- **Generate PRPs** (Product Requirements Prompts) that guide AI coding assistants
- **Validate implementations** against requirements
- **Maintain context health** and track completeness

All operations are **local-only** using Foundry Local. The entire tool lives in `ContextCraftPro/` and is **entirely disposable**—delete it anytime without affecting your project.

## Quick Start

```bash
cd ContextCraftPro
pip install -r requirements.txt
python ccp.py init-project
```

### Optional: Create an alias

Instead of typing `python ContextCraftPro/ccp.py` every time, create an alias:

**Bash/Zsh** (add to `~/.bashrc` or `~/.zshrc`):
```bash
alias ccp="python /path/to/repo/ContextCraftPro/ccp.py"
```

Then just run:
```bash
ccp init-project
ccp new-feature
ccp generate-prp --feature my-feature
```

## Documentation

- **[ContextCraftPro README](ContextCraftPro/README.md)** — Full guide and usage
- **[User Guide](ContextCraftPro/USERGUIDE.md)** — Step-by-step workflows
- **[Commands Reference](ContextCraftPro/COMMANDS.md)** — All available commands
- **[Testing Guide](ContextCraftPro/TESTING.md)** — How to test and validate
- **[Claude Rules](CLAUDE.md)** — AI coding guidelines for this project

## Key Features

🏠 **Local-only** — All operations use Foundry Local (no cloud LLM calls)

📦 **Self-contained** — Everything lives inside `ContextCraftPro/`

🗑️ **Disposable** — Delete the folder and your project is unchanged

🤖 **Agentic** — Guides you through structured workflows with optional LLM enhancement

📝 **Transparent** — All artifacts are human-readable text (Markdown, YAML, JSON)

## Requirements

- Python 3.8+
- Foundry Local running locally

## License

See [LICENSE](LICENSE)
