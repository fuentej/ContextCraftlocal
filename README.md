# ContextCraftPro

**ContextCraftPro (CCP)** is a self-contained, disposable Python tool that enables structured context engineering for AI-driven development.

## What is it?

ContextCraftPro helps you:

- **Define features** with structured specifications
- **Generate PRPs** (Product Requirements Prompts) that guide AI coding assistants
- **Validate implementations** against requirements
- **Maintain context health** and track completeness

All operations are **local-only** using Foundry Local. The entire tool lives in `ContextCraftPro/` and is **entirely disposable**—delete it anytime without affecting your project.

## Installation

### For Existing Projects

Add ContextCraftPro to your project:

**Option 1: Clone and extract**
```bash
cd /path/to/your/project

# Clone repo into temp folder
git clone https://github.com/fuentej/ContextCraftlocal.git temp-ccp

# Copy just ContextCraftPro
cp -r temp-ccp/ContextCraftPro .

# Clean up
rm -rf temp-ccp

# Install and initialize
cd ContextCraftPro
pip install -r requirements.txt
python ccp.py init-project
```

**Option 2: Download manually**
1. Go to https://github.com/fuentej/ContextCraftlocal/
2. Download the repo as ZIP
3. Extract `ContextCraftPro/` folder into your project root
4. Run `pip install -r requirements.txt` and `python ccp.py init-project`

### Reusing the Template

Save `ContextCraftPro/` as a template for future projects:

```bash
# After using CCP, save the initialized folder
cp -r /path/to/project/ContextCraftPro ~/templates/contextcraft-pro-template

# Next project: just copy the template
cp -r ~/templates/contextcraft-pro-template /path/to/new/project/ContextCraftPro
```

### Optional: Create an Alias

Instead of typing `python ContextCraftPro/ccp.py` every time, create an alias:

**Bash/Zsh** (add to `~/.bashrc` or `~/.zshrc`):
```bash
alias ccp="python /path/to/your/project/ContextCraftPro/ccp.py"
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

- **Python 3.8+**
- **Foundry Local** (Microsoft's local AI runtime)

### Installing Foundry Local

Foundry Local runs generative AI models on your device with no cloud calls or Azure account required.

**Windows:**
```bash
winget install Microsoft.FoundryLocal
```

**macOS:**
```bash
brew tap microsoft/foundrylocal
brew install foundrylocal
```

**Linux:** Download from [microsoft/Foundry-Local](https://github.com/microsoft/Foundry-Local)

### Starting Foundry Local

After installation, start a model:

```bash
foundry model run qwen2.5-0.5b
```

This downloads and starts the model. Note the output for the **API endpoint** (typically `http://127.0.0.1:PORT/v1/chat/completions` where PORT is dynamically assigned).

Update `ContextCraftPro/config/contextcraft.yaml` with your endpoint:

```yaml
foundry_local:
  endpoint: "http://127.0.0.1:PORT/v1/chat/completions"
  model: "qwen2.5-0.5b"
```

See [Foundry Local docs](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-local/get-started) for more details.

## License

See [LICENSE](LICENSE)
