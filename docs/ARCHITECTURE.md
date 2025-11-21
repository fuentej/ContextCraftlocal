# ContextCraft Architecture

## Overview

ContextCraft is designed as a modular project generator with clear separation of concerns.

## Project Structure

```
ContextCraftlocal/
├── src/                          # Main source code (Phase 2)
│   ├── __init__.py
│   ├── cli.py                   # CLI interface and user interaction
│   ├── generator.py             # Core generator logic
│   ├── stack_generators/        # Stack-specific generators
│   │   ├── __init__.py
│   │   ├── base.py             # Base generator class
│   │   ├── python.py           # Python stack generators
│   │   ├── javascript.py       # JavaScript stack generators
│   │   └── ai.py               # AI framework generators
│   └── utils.py                # Utility functions
├── tests/                        # Test suite (Phase 3)
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_generator.py
│   └── test_stacks.py
├── templates/                    # Project templates (Phase 1)
│   ├── __init__.py
│   ├── planning_template.md
│   ├── task_template.md
│   └── readme_template.md
├── config/                       # Configuration files
│   └── stacks.yaml             # Stack definitions (Phase 2)
├── docs/                         # Documentation (Phase 5)
│   ├── ARCHITECTURE.md
│   ├── CONTRIBUTING.md
│   └── API.md
├── README.md                     # Main project documentation
├── PRD.md                        # Product Requirements (Phase 3)
├── requirements.txt              # Python dependencies
├── newprojectv3.py              # Current legacy implementation
├── setup.py                      # PyPI package setup (Phase 4)
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD (Phase 4)
└── .gitignore
```

## Core Components

### 1. CLI Interface (`src/cli.py`)
- User input prompts
- Project creation orchestration
- Status reporting and next steps

### 2. Generator (`src/generator.py`)
- Project structure creation
- File generation logic
- Template processing

### 3. Stack Generators (`src/stack_generators/`)
- Technology-specific code generation
- Framework-specific boilerplate
- Dependency management per stack

### 4. Utilities (`src/utils.py`)
- Path handling
- File operations
- Validation functions

## Current Implementation (Legacy)

The current `newprojectv3.py` is a single-file implementation containing:
- Project type definitions
- Tech stack definitions
- Complete generation logic
- Template content and file creation

## Refactoring Roadmap (Phase 2)

**Step 1**: Extract templates to separate files
**Step 2**: Create `GeneratorBase` class
**Step 3**: Extract CLI logic to `cli.py`
**Step 4**: Create stack-specific generator classes
**Step 5**: Move utility functions
**Step 6**: Maintain backward compatibility

## Design Patterns

### Factory Pattern
Each tech stack has a corresponding generator class created via a factory method.

### Template Method Pattern
Base generator class defines the structure generation process; subclasses customize specific tech stacks.

### Strategy Pattern
Different file creation strategies for different project types.

## Data Flow

```
User Input
    ↓
CLI Interface
    ↓
Project Generator
    ↓
Stack Selector
    ↓
Stack Generator
    ↓
Template Processing
    ↓
File Creation
    ↓
Project Output
```

## Extension Points

### Adding a New Tech Stack
1. Create new generator class inheriting from `BaseStackGenerator`
2. Implement `generate_main_file()` method
3. Implement `generate_dependencies()` method
4. Register in stack factory

### Adding a New Project Type
1. Add project type to configuration
2. Create corresponding template files
3. Add handling in `ProjectTypeManager`

### Customizing Templates
1. Modify template files in `templates/` directory
2. Update template processing logic if needed
3. Test with new project generation

## Technology Stack

- **Language**: Python 3.8+
- **Testing**: Pytest
- **CLI**: Typer/Click + Rich
- **Type Hints**: Full Python type annotations (future)
- **Package Management**: Poetry (planned)

## Phase-Based Development

Each development phase adds specific capabilities:

**Phase 1**: Foundation (Templates, documentation)
**Phase 2**: Modularization (Code structure, generators)
**Phase 3**: Quality (Tests, CI/CD, PRD)
**Phase 4**: Distribution (PyPI, setup.py, Packaging)
**Phase 5**: Enhancement (Rich CLI, Advanced features)
**Phase 6**: Web (FastAPI interface, Web UI)
**Phase 7**: Advanced (AI integration, Plugins)

## See Also

- [README.md](../README.md) - User-facing documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [PRD.md](../PRD.md) - Product requirements
