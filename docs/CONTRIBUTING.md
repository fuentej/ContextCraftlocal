# Contributing to ContextCraft

Thank you for your interest in contributing to ContextCraft! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Adding New Tech Stacks](#adding-new-tech-stacks)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip and virtualenv

### Finding Issues to Work On

- Check the [GitHub Issues](https://github.com/fuentej/ContextCraftlocal/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to let others know you're working on it

## Development Setup

1. **Fork and Clone**

```bash
git clone https://github.com/YOUR_USERNAME/ContextCraftlocal.git
cd ContextCraftlocal
```

2. **Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```

4. **Verify Installation**

```bash
# Run tests
pytest

# Check code quality
black --check src/ tests/
flake8 src/ tests/
mypy src/
```

## Contributing Process

### 1. Create a Branch

Create a descriptive branch name:

```bash
git checkout -b feature/add-golang-support
git checkout -b fix/template-variable-bug
git checkout -b docs/improve-readme
```

### Branch Naming Convention

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications

### 2. Make Your Changes

- Write clear, concise code
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Test specific module
pytest tests/test_generator.py

# Run linters
black src/ tests/
flake8 src/ tests/
mypy src/
```

### 4. Commit Your Changes

Write clear commit messages:

```bash
git add .
git commit -m "feat: Add Go/Gin stack generator

- Implemented GoGinGenerator class
- Added Go template files
- Updated stacks.yaml configuration
- Added tests for Go generator
"
```

**Commit Message Format:**

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `chore`: Maintenance tasks

## Coding Standards

### Python Style Guide

We follow PEP 8 with these specifics:

- Line length: 100 characters (enforced by black)
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Use meaningful variable names

**Example:**

```python
def create_project(
    project_name: str,
    project_type: str,
    tech_stack: str
) -> bool:
    """
    Create a new project with the specified configuration.

    Args:
        project_name: Name of the project
        project_type: Type of project (from config)
        tech_stack: Technology stack (from config)

    Returns:
        True if successful, False otherwise
    """
    # Implementation here
    pass
```

### Code Formatting

We use these tools:

- **black**: Code formatting (automatically formats code)
- **flake8**: Linting (checks for errors and style issues)
- **mypy**: Type checking (verifies type hints)

Run before committing:

```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

### Import Organization

Use `isort` for organizing imports:

```python
# Standard library imports
import os
from pathlib import Path
from typing import Dict, List

# Third-party imports
import yaml
from rich.console import Console

# Local imports
from src.utils import validate_project_name
from src.generator import ProjectGenerator
```

## Testing Guidelines

### Test Structure

```python
"""
Unit tests for <module name>
"""

import pytest
from pathlib import Path

from src.module import function


class TestFunctionName:
    """Tests for function_name."""

    def setup_method(self):
        """Setup for each test."""
        # Initialize test fixtures
        pass

    def teardown_method(self):
        """Cleanup after each test."""
        # Clean up test artifacts
        pass

    def test_basic_functionality(self):
        """Test basic functionality."""
        result = function("test")
        assert result is True

    def test_edge_case(self):
        """Test edge case."""
        result = function("")
        assert result is False
```

### Test Coverage

- Aim for 90%+ code coverage
- Write tests for:
  - Happy paths
  - Edge cases
  - Error conditions
  - Boundary conditions

### Running Specific Tests

```bash
# Run specific test file
pytest tests/test_utils.py

# Run specific test class
pytest tests/test_utils.py::TestValidateProjectName

# Run specific test
pytest tests/test_utils.py::TestValidateProjectName::test_valid_project_name

# Run with verbose output
pytest -v

# Run with print statements
pytest -s
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def generate_project(name: str, stack: str) -> bool:
    """
    Generate a new project with the specified stack.

    This function creates a complete project structure including
    source files, configuration, and documentation.

    Args:
        name: Name of the project to create
        stack: Technology stack identifier

    Returns:
        True if generation succeeded, False otherwise

    Raises:
        ValueError: If project name is invalid
        FileExistsError: If project already exists

    Examples:
        >>> generate_project("my-app", "python_fastapi")
        True
    """
    pass
```

### README Updates

When adding new features, update:

- README.md - User-facing documentation
- ARCHITECTURE.md - Technical documentation
- PRD.md - Product requirements (if applicable)

## Adding New Tech Stacks

To add a new technology stack:

### 1. Update Configuration

Edit `config/stacks.yaml`:

```yaml
go_gin:
  name: "Go/Gin"
  folder: "go-gin"
  type: "backend"
  description: "Go web framework"
  template: "go_gin_template.go"
  main_file: "main.go"
  dependencies: {}  # Go uses go.mod
  folders:
    - cmd
    - pkg
    - internal
  port: 8080
```

### 2. Create Template

Create `templates/go_gin_template.go`:

```go
package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()
    r.GET("/", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "Hello from {project_name}",
        })
    })
    r.Run(":8080")
}
```

### 3. Create Generator Class

Create generator in `src/stack_generators/go.py`:

```python
from src.stack_generators.base import BaseStackGenerator

class GoGinGenerator(BaseStackGenerator):
    def generate_main_file(self, project_path, variables):
        # Implementation
        pass

    def generate_dependencies(self, project_path):
        # Implementation
        pass
```

### 4. Write Tests

Add tests in `tests/test_stack_generators.py`:

```python
def test_go_gin_generator():
    config = {'name': 'Go/Gin', 'folder': 'go-gin', 'type': 'backend'}
    generator = GoGinGenerator(config)
    assert generator.name == 'Go/Gin'
```

### 5. Update Documentation

- Add to README.md tech stack table
- Update PRD.md if needed
- Add example to documentation

## Submitting Changes

### Pull Request Process

1. **Push Your Branch**

```bash
git push origin feature/your-feature-name
```

2. **Create Pull Request**

- Go to GitHub and create a PR
- Fill out the PR template
- Link related issues

3. **PR Title Format**

```
feat: Add Go/Gin stack support
fix: Correct template variable substitution
docs: Improve installation instructions
```

4. **PR Description Template**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests
- [ ] All tests pass
```

### Code Review Process

- Maintainers will review your PR
- Address feedback and make requested changes
- Once approved, your PR will be merged
- Your contribution will be credited

### After Your PR is Merged

- Delete your branch locally:
  ```bash
  git branch -d feature/your-feature-name
  ```

- Update your fork:
  ```bash
  git checkout main
  git pull upstream main
  git push origin main
  ```

## Development Tips

### Debugging

```python
# Use pytest for debugging
pytest --pdb  # Drop into debugger on failure

# Use print debugging with -s flag
pytest -s

# Use logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Virtual Environment Management

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv/

# Recreate clean environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Keeping Your Fork Updated

```bash
# Add upstream remote (once)
git remote add upstream https://github.com/fuentej/ContextCraftlocal.git

# Fetch and merge updates
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Getting Help

- **Documentation**: Check [README.md](../README.md) and [ARCHITECTURE.md](ARCHITECTURE.md)
- **Issues**: Search [GitHub Issues](https://github.com/fuentej/ContextCraftlocal/issues)
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers (see README)

## Recognition

Contributors will be recognized in:

- README.md Contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to ContextCraft! 🚀
