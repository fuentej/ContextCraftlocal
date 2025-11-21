"""
Shared pytest fixtures for ContextCraftPro tests
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_project_dir(tmp_path):
    """
    Create a temporary project directory structure for testing.

    Returns a Path object pointing to a fake host project root with
    a ContextCraftPro/ subdirectory.
    """
    # Create fake host project structure
    host_root = tmp_path / "test_project"
    host_root.mkdir()

    # Create some fake source files
    src_dir = host_root / "src"
    src_dir.mkdir()
    (src_dir / "main.py").write_text("# Main module\n")

    # Create ContextCraftPro folder
    ccp_dir = host_root / "ContextCraftPro"
    ccp_dir.mkdir()

    yield host_root

    # Cleanup is automatic with tmp_path


@pytest.fixture
def ccp_dir(temp_project_dir):
    """
    Return the ContextCraftPro directory within a temp project.
    """
    return temp_project_dir / "ContextCraftPro"


@pytest.fixture
def sample_config():
    """
    Return a sample configuration dictionary for testing.
    """
    return {
        "foundry_local": {
            "endpoint": "http://localhost:11434/v1/chat/completions",
            "model": "gpt-4o-mini",
        },
        "paths": {
            "project_root": "..",
            "context_root": "context",
            "claude_rules": "context/claude.md",
            "initial_spec": "context/INITIAL.md",
            "examples_dir": "context/examples",
            "docs_dir": "context/docs-context",
            "prps_dir": "context/prps",
            "validation_dir": "context/validation",
        },
        "behavior": {"auto_open_browser": False, "confirm_exports": True},
    }


@pytest.fixture
def mock_llm_client(monkeypatch):
    """
    Mock the Foundry Local LLM client for testing without a real LLM.

    Returns a mock client that returns predefined responses.
    """

    class MockLLMClient:
        def __init__(self, config):
            self.config = config
            self.call_count = 0

        def complete(self, prompt, **kwargs):
            """Mock completion that returns a simple response"""
            self.call_count += 1
            return {
                "choices": [
                    {
                        "message": {
                            "content": "# Mock Response\n\nThis is a mock LLM response for testing."
                        }
                    }
                ]
            }

    return MockLLMClient


@pytest.fixture
def sample_initial_content():
    """
    Return sample INITIAL.md content for testing.
    """
    return """# INITIAL Specification

## Feature: User Authentication

### Problem / Goal
Implement secure user authentication for the application.

### Why It Matters
Users need to securely access their accounts.

### Scope & Constraints

#### In Scope
- Login with email/password
- Session management

#### Out of Scope
- OAuth integration
- Two-factor authentication

### Acceptance Criteria
- [ ] Users can log in with valid credentials
- [ ] Invalid credentials are rejected
- [ ] Sessions persist across page reloads
"""
