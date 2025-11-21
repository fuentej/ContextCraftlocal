# Testing Guide for ContextCraftPro

Complete guide to testing ContextCraftPro, including unit tests, integration tests, and functional testing.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Running Tests](#running-tests)
3. [Functional Testing](#functional-testing)
4. [Integration Tests](#integration-tests)
5. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Run All Tests (1 command)
```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

**Expected output:**
```
27 passed in 0.13s
```

### Run and Test ContextCraftPro Live (5 steps)
```bash
cd /tmp
rm -rf test-ccp-demo
mkdir test-ccp-demo
cd test-ccp-demo

# Copy ContextCraftPro
cp -r /path/to/ContextCraftPro ./
cd ContextCraftPro

# 1. Initialize
python ccp.py init-project --yes

# 2. Create a feature
python ccp.py new-feature

# 3. Generate a PRP
python ccp.py generate-prp --feature dark-mode-toggle

# 4. Check health
python ccp.py health

# 5. Export
python ccp.py export --target all --yes
```

---

## Running Tests

### All Tests
```bash
python -m pytest tests/ -v
```

**Output shows:**
- ✅ 27 tests passing
- ✅ 0 warnings
- ✅ Execution time: ~0.13s

### Test Categories

#### Integration Tests Only
Tests complete workflows (init → feature → generate-prp → health → export)
```bash
python -m pytest tests/test_integration.py -v -m integration
```

**Tests:**
- `test_full_init_workflow` — Complete project initialization
- `test_full_feature_workflow` — Feature spec to PRP generation
- `test_health_check_workflow` — Context health analysis
- `test_export_workflow` — Artifact export
- `test_dry_run_mode` — --dry-run flag
- `test_verbose_mode` — --verbose flag

#### Unit Tests Only
Tests individual components
```bash
python -m pytest tests/test_cli.py tests/test_config.py tests/test_fs.py tests/test_llm.py -v
```

**Test Coverage:**
- **test_cli.py** (7 tests) — CLI command parsing and routing
- **test_config.py** (4 tests) — Configuration loading and validation
- **test_fs.py** (5 tests) — File system operations and boundaries
- **test_llm.py** (5 tests) — LLM client functionality

#### Single Test
```bash
python -m pytest tests/test_integration.py::TestIntegration::test_full_init_workflow -v
```

### Verbose Output
```bash
python -m pytest tests/ -vv --tb=long
```

Shows:
- Detailed test names
- Full error tracebacks
- Variable values on failure

### With Coverage Report
```bash
python -m pytest tests/ --cov=core --cov-report=html
# Open htmlcov/index.html in browser
```

---

## Functional Testing

### Full Workflow Test (End-to-End)

This tests all major commands working together in a real scenario.

#### Setup
```bash
# Create a test directory
mkdir ~/my-test-ccp
cd ~/my-test-ccp

# Copy ContextCraftPro
cp -r /path/to/ContextCraftPro ./
cd ContextCraftPro
```

#### Step 1: Initialize Project
```bash
python ccp.py init-project --yes
```

**Verify it worked:**
```bash
ls -la context/
# Should show: claude.md, INITIAL.md, project-profile.yaml

cat context/project-profile.yaml
# Should show: project name, detected languages/frameworks
```

#### Step 2: Create a Feature Spec
```bash
python ccp.py new-feature
```

**Answer the interactive prompts:**
```
Feature name: dark-mode-toggle
Problem/Goal: Users want light/dark theme switching
Why it matters: Improves user experience and accessibility
In scope: Toggle button, persist theme preference, apply to all pages
Out of scope: Sync across devices, themes marketplace
Acceptance criteria: Button toggles theme, preference persists on reload
```

**Verify it worked:**
```bash
cat context/INITIAL.md
# Should show your feature spec
```

#### Step 3: Generate PRP
```bash
python ccp.py generate-prp --feature dark-mode-toggle
```

**Verify it worked:**
```bash
cat context/prps/dark-mode-toggle.md
# Should show comprehensive implementation plan with:
# - Context & Assumptions
# - Goals and Non-Goals
# - Implementation Steps
# - Checklist
# - Validation Plan
```

#### Step 4: Check Health
```bash
python ccp.py health
```

**Expected output:**
```
Context Health Check
  Features defined: 1
  PRPs generated: 1
  Validations recorded: 0
```

#### Step 5: Record Validation
```bash
python ccp.py validate --feature dark-mode-toggle
```

**Answer the prompts:**
```
Did implementation satisfy PRP? [yes/no]: yes
What worked well? Clean implementation, no issues
What broke or needs work? Nothing
Lessons learned for future features? Good separation of concerns
```

**Verify it worked:**
```bash
cat context/validation/dark-mode-toggle.md
# Should show validation report with:
# - Implementation status
# - Test results
# - Patterns learned
```

#### Step 6: Export Artifacts
```bash
python ccp.py export --target all --yes
```

**Verify it worked:**
```bash
ls -la _context_exports/
# Should contain all exported artifacts
```

### Quick Checklist
After running all 6 steps above, you should have:

```
ContextCraftPro/
├── context/
│   ├── claude.md                           ✓
│   ├── INITIAL.md (with your feature)      ✓
│   ├── project-profile.yaml                ✓
│   ├── prps/
│   │   └── dark-mode-toggle.md             ✓
│   └── validation/
│       └── dark-mode-toggle.md             ✓
├── _context_exports/                       ✓
└── runtime/logs/ccp.log                    ✓
```

If all these exist, ContextCraftPro works! ✅

---

## Integration Tests

### What Are Integration Tests?

Integration tests verify that all components work together. They test complete workflows without hitting external dependencies.

### How They Work

```python
# Example integration test structure
def test_full_init_workflow(temp_project_dir, ccp_dir):
    # 1. Setup: Create temporary project
    self._copy_templates(ccp_dir)

    # 2. Execute: Run actual CLI command
    result = runner.invoke(cli, ['init-project', '--yes'])

    # 3. Verify: Check results
    assert result.exit_code == 0
    assert (ccp_dir / "context").exists()
```

### Key Features

- **Isolation**: Each test runs in its own temporary directory
- **No side effects**: Tests don't affect each other
- **Fast**: All 6 integration tests run in < 0.2s
- **Realistic**: Tests use real templates and commands

### Test Coverage

| Test | Workflow | Validates |
|------|----------|-----------|
| `test_full_init_workflow` | init-project | Directory creation, config, file seeding |
| `test_full_feature_workflow` | feature → PRP | Spec loading, LLM integration, output |
| `test_health_check_workflow` | health analysis | Feature scanning, missing detection |
| `test_export_workflow` | export artifacts | Export with confirmation |
| `test_dry_run_mode` | --dry-run flag | No changes made, output format |
| `test_verbose_mode` | --verbose flag | Extra logging output |

---

## Testing Command Flags

### --dry-run (Preview Changes)
```bash
python ccp.py --dry-run init-project --yes
```

**What it does:**
- Shows what WOULD happen
- Makes NO actual changes
- Useful for previewing

**Expected output:**
```
[DRY RUN] Would create context/claude.md
[DRY RUN] Would create context/INITIAL.md
...
```

### --verbose (Extra Output)
```bash
python ccp.py --verbose health
```

**What it does:**
- Shows detailed debug information
- Logs all operations
- Useful for troubleshooting

**Expected output:**
```
Starting: health
  Loading config...
  Scanning features...
  Analyzing PRPs...
  Generating report...
Completed: health
```

### --yes (Auto-Confirm)
```bash
python ccp.py init-project --yes
```

**What it does:**
- Answers "yes" to all prompts
- Good for scripting
- Useful for batch operations

---

## Troubleshooting

### Tests Fail with "Template not found"
**Problem:** Integration tests can't find templates

**Solution:**
```bash
# Make sure you're in ContextCraftPro directory
cd ContextCraftPro
python -m pytest tests/test_integration.py -v
```

### Tests Fail with "Permission denied"
**Problem:** Can't write to temporary directories

**Solution:**
```bash
# Check temp directory permissions
ls -la /tmp
# Or use custom tmp location
export TMPDIR=/tmp/my-test-tmp
python -m pytest tests/ -v
```

### Tests Pass but Functional Testing Fails
**Problem:** `init-project` says "Foundry Local not found"

**Solution:**
This is expected if Foundry Local isn't running. The command should gracefully fall back to template mode. If not:
```bash
# Check Foundry Local is accessible
curl http://127.0.0.1:PORT/v1/models
# If not running, start it (requires separate Foundry Local installation)
```

### "pytest: command not found"
**Problem:** Pytest not installed

**Solution:**
```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

### Tests Slow or Timeout
**Problem:** Tests taking too long

**Solution:**
```bash
# Run with timeout
pytest tests/ --timeout=10

# Or run specific test
pytest tests/test_cli.py -v --tb=short
```

---

## Testing Best Practices

### When to Write Tests

1. **New features** — Add test before implementing
2. **Bug fixes** — Add regression test
3. **Refactoring** — Run tests to verify nothing breaks

### Running Tests During Development

```bash
# Watch for changes and rerun tests
pytest-watch tests/

# Or run on save
python -m pytest tests/ -v --tb=short
```

### Before Committing

```bash
# Run full suite
python -m pytest tests/ -v

# Check coverage
python -m pytest tests/ --cov=core

# Format code
python -m black core/ tests/
```

### CI/CD Integration

For automated testing (GitHub Actions, etc.):

```bash
# Quick test
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=core --cov-report=xml

# With output report
python -m pytest tests/ --junitxml=test-report.xml
```

---

## Test Statistics

**Current Test Suite:**

```
Total Tests:        27
├─ Unit Tests:      21
│  ├─ CLI Tests:           7
│  ├─ Config Tests:        4
│  ├─ FileSystem Tests:    5
│  └─ LLM Tests:           5
└─ Integration Tests: 6
   ├─ Init Workflow:       1
   ├─ Feature Workflow:    1
   ├─ Health Check:        1
   ├─ Export:              1
   ├─ Dry-run Mode:        1
   └─ Verbose Mode:        1

Pass Rate:          100%
Execution Time:     0.13s
Deprecation Warnings: 0
Code Coverage:      ~90% (core modules)
```

---

## Adding New Tests

### Structure
```python
# tests/test_myfeature.py

import pytest
from pathlib import Path

class TestMyFeature:
    """Tests for my new feature"""

    def test_something(self, temp_project_dir):
        """Test description"""
        # Setup
        # Execute
        # Verify
        assert True
```

### Running Your New Test
```bash
python -m pytest tests/test_myfeature.py::TestMyFeature::test_something -v
```

### Test Fixtures Available
```python
# temp_project_dir    - Temporary project directory
# ccp_dir             - ContextCraftPro directory within temp project
# sample_config       - Sample configuration dict
# mock_llm_client     - Mocked LLM client
# sample_initial_content - Sample INITIAL.md content
```

---

## Resources

- **pytest docs:** https://docs.pytest.org/
- **pytest fixtures:** https://docs.pytest.org/en/stable/reference.html#fixtures
- **Click testing:** https://click.palletsprojects.com/testing/
- **Unit vs Integration:** https://en.wikipedia.org/wiki/Integration_testing

---

## Questions?

If tests fail:

1. Check error message carefully
2. Run with `-vv` for more details
3. Check `/runtime/logs/ccp.log` for execution logs
4. Try single test: `pytest tests/test_cli.py::TestCLI::test_cli_help -v`

---

*Testing Guide for ContextCraftPro — Updated 2025-11-21*
