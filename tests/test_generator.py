"""
Unit tests for ProjectGenerator
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from src.generator import ProjectGenerator


class TestProjectGenerator:
    """Tests for the ProjectGenerator class."""

    def setup_method(self):
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.generator = ProjectGenerator()

    def teardown_method(self):
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_generator_initialization(self):
        """Test that generator initializes with config."""
        assert self.generator.config is not None
        assert 'tech_stacks' in self.generator.config
        assert 'project_types' in self.generator.config

    def test_get_available_stacks(self):
        """Test getting available technology stacks."""
        stacks = self.generator.get_available_stacks()

        assert isinstance(stacks, dict)
        assert len(stacks) > 0
        assert 'python_fastapi' in stacks
        assert 'react_typescript' in stacks

    def test_get_available_project_types(self):
        """Test getting available project types."""
        types = self.generator.get_available_project_types()

        assert isinstance(types, dict)
        assert len(types) > 0
        assert 'ai_agent' in types
        assert 'web_app' in types

    def test_create_project_invalid_name(self):
        """Test that invalid project names are rejected."""
        result = self.generator.create_project(
            "",  # Invalid empty name
            "web_app",
            "python_flask",
            self.temp_dir
        )

        assert result is False

    def test_create_project_basic_python(self):
        """Test creating a basic Python/Flask project."""
        project_name = "test-flask-app"

        result = self.generator.create_project(
            project_name,
            "web_app",
            "python_flask",
            self.temp_dir
        )

        assert result is True

        project_path = self.temp_dir / project_name
        assert project_path.exists()

        # Check for key files
        assert (project_path / "app.py").exists()
        assert (project_path / "requirements.txt").exists()
        assert (project_path / "README.md").exists()
        assert (project_path / ".gitignore").exists()
        assert (project_path / ".env.example").exists()

        # Check for directories
        assert (project_path / "docs").exists()
        assert (project_path / "tests").exists()
        assert (project_path / "src").exists()
        assert (project_path / "docker").exists()
        assert (project_path / "iac").exists()

    def test_create_project_basic_javascript(self):
        """Test creating a basic React/TypeScript project."""
        project_name = "test-react-app"

        result = self.generator.create_project(
            project_name,
            "web_app",
            "react_typescript",
            self.temp_dir
        )

        assert result is True

        project_path = self.temp_dir / project_name
        assert project_path.exists()

        # Check for key React files
        assert (project_path / "src" / "App.tsx").exists()
        assert (project_path / "src" / "index.tsx").exists()
        assert (project_path / "public" / "index.html").exists()
        assert (project_path / "package.json").exists()
        assert (project_path / "tsconfig.json").exists()

    def test_create_project_ai_agent(self):
        """Test creating a Pydantic AI agent project."""
        project_name = "test-ai-agent"

        result = self.generator.create_project(
            project_name,
            "ai_agent",
            "pydantic_ai",
            self.temp_dir
        )

        assert result is True

        project_path = self.temp_dir / project_name
        assert project_path.exists()

        # Check for AI-specific directories
        assert (project_path / "agents").exists()
        assert (project_path / "tools").exists()
        assert (project_path / "prompts").exists()

        # Check for AI-specific files
        assert (project_path / "main.py").exists()
        assert (project_path / "agents" / "agent.py").exists()
        assert (project_path / "tools" / "tools.py").exists()

    def test_create_project_documentation_files(self):
        """Test that documentation files are created."""
        project_name = "test-docs-app"

        result = self.generator.create_project(
            project_name,
            "web_app",
            "python_fastapi",
            self.temp_dir
        )

        assert result is True

        project_path = self.temp_dir / project_name

        # Check documentation files
        assert (project_path / "README.md").exists()
        assert (project_path / "docs" / "PLANNING.md").exists()
        assert (project_path / "docs" / "TASKS.md").exists()

        # Verify README has content
        readme_content = (project_path / "README.md").read_text()
        assert project_name in readme_content
        assert "Overview" in readme_content

    def test_create_project_docker_files(self):
        """Test that Docker files are created."""
        project_name = "test-docker-app"

        result = self.generator.create_project(
            project_name,
            "api_service",
            "python_fastapi",
            self.temp_dir
        )

        assert result is True

        project_path = self.temp_dir / project_name

        # Check Docker files
        assert (project_path / "docker" / "Dockerfile").exists()
        assert (project_path / "docker" / "docker-compose.yml").exists()

        # Verify Dockerfile has content
        dockerfile_content = (project_path / "docker" / "Dockerfile").read_text()
        assert "FROM python" in dockerfile_content
        assert "WORKDIR /app" in dockerfile_content

    def test_create_project_iac_files(self):
        """Test that Infrastructure as Code files are created."""
        project_name = "test-iac-app"

        result = self.generator.create_project(
            project_name,
            "web_app",
            "python_flask",
            self.temp_dir
        )

        assert result is True

        project_path = self.temp_dir / project_name

        # Check IaC files
        assert (project_path / "iac" / "main.tf").exists()
        assert (project_path / "iac" / "variables.tf").exists()
        assert (project_path / "iac" / "README.md").exists()

    def test_create_project_dependencies_python(self):
        """Test that Python dependencies are correctly generated."""
        project_name = "test-deps-python"

        result = self.generator.create_project(
            project_name,
            "web_app",
            "python_fastapi",
            self.temp_dir
        )

        assert result is True

        project_path = self.temp_dir / project_name
        requirements = (project_path / "requirements.txt").read_text()

        # Check for expected dependencies
        assert "fastapi" in requirements.lower()
        assert "uvicorn" in requirements.lower()
        assert "pytest" in requirements.lower()

    def test_create_project_dependencies_javascript(self):
        """Test that JavaScript dependencies are correctly generated."""
        project_name = "test-deps-js"

        result = self.generator.create_project(
            project_name,
            "web_app",
            "node_express",
            self.temp_dir
        )

        assert result is True

        project_path = self.temp_dir / project_name
        package_json_content = (project_path / "package.json").read_text()

        # Check for expected dependencies
        assert "express" in package_json_content
        assert "cors" in package_json_content
        assert '"scripts"' in package_json_content

    def test_create_duplicate_project_fails(self):
        """Test that creating duplicate project fails."""
        project_name = "test-duplicate"

        # Create first project
        result1 = self.generator.create_project(
            project_name,
            "web_app",
            "python_flask",
            self.temp_dir
        )
        assert result1 is True

        # Try to create duplicate
        result2 = self.generator.create_project(
            project_name,
            "web_app",
            "python_flask",
            self.temp_dir
        )
        assert result2 is False

    def test_create_project_config_files(self):
        """Test that config files (.env, .gitignore) are created."""
        project_name = "test-config-app"

        result = self.generator.create_project(
            project_name,
            "web_app",
            "python_fastapi",
            self.temp_dir
        )

        assert result is True

        project_path = self.temp_dir / project_name

        # Check config files
        assert (project_path / ".env.example").exists()
        assert (project_path / ".gitignore").exists()

        # Verify .gitignore has content
        gitignore_content = (project_path / ".gitignore").read_text()
        assert "__pycache__" in gitignore_content
        assert "node_modules" in gitignore_content
        assert ".env" in gitignore_content
