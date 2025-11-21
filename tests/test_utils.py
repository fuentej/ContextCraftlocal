"""
Unit tests for utility functions
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import yaml

from src.utils import (
    validate_project_name,
    create_directory_structure,
    process_template,
    get_current_date,
    get_template_variables,
    get_project_folders,
    write_file,
    read_file,
)


class TestValidateProjectName:
    """Tests for project name validation."""

    def test_valid_project_name(self):
        """Test that valid names are accepted."""
        assert validate_project_name("my-project") is True
        assert validate_project_name("MyProject123") is True
        assert validate_project_name("test_project") is True

    def test_empty_name(self):
        """Test that empty names are rejected."""
        assert validate_project_name("") is False
        assert validate_project_name("   ") is False

    def test_invalid_characters(self):
        """Test that invalid characters are rejected."""
        assert validate_project_name("my/project") is False
        assert validate_project_name("my:project") is False
        assert validate_project_name("my*project") is False
        assert validate_project_name("my<project>") is False


class TestDirectoryOperations:
    """Tests for directory creation and management."""

    def setup_method(self):
        """Create temp directory for tests."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up temp directory."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_create_directory_structure(self):
        """Test directory structure creation."""
        folders = ["src", "tests", "docs", "config"]
        create_directory_structure(self.temp_dir, folders)

        for folder in folders:
            assert (self.temp_dir / folder).exists()
            assert (self.temp_dir / folder).is_dir()

    def test_create_nested_directories(self):
        """Test creating nested directory structures."""
        folders = ["src/components", "tests/unit", "docs/api"]
        create_directory_structure(self.temp_dir, folders)

        for folder in folders:
            assert (self.temp_dir / folder).exists()


class TestTemplateProcessing:
    """Tests for template processing."""

    def setup_method(self):
        """Create temp directory and template files."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.template_file = self.temp_dir / "template.txt"

    def teardown_method(self):
        """Clean up temp directory."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_process_template_basic(self):
        """Test basic template variable replacement."""
        # Create template
        template_content = "Project: {project_name}\nDate: {date}"
        self.template_file.write_text(template_content)

        # Process template
        variables = {"project_name": "TestProject", "date": "2024-01-01"}
        output_file = self.temp_dir / "output.txt"
        process_template(self.template_file, output_file, variables)

        # Verify output
        assert output_file.exists()
        content = output_file.read_text()
        assert "Project: TestProject" in content
        assert "Date: 2024-01-01" in content

    def test_process_template_multiple_variables(self):
        """Test template with multiple variables."""
        template_content = "{greeting} {name}! Welcome to {project}."
        self.template_file.write_text(template_content)

        variables = {
            "greeting": "Hello",
            "name": "World",
            "project": "ContextCraft"
        }
        output_file = self.temp_dir / "output.txt"
        process_template(self.template_file, output_file, variables)

        content = output_file.read_text()
        assert content == "Hello World! Welcome to ContextCraft."

    def test_process_template_nonexistent_file(self):
        """Test that processing nonexistent template raises error."""
        output_file = self.temp_dir / "output.txt"
        variables = {"test": "value"}

        with pytest.raises(FileNotFoundError):
            process_template(
                self.temp_dir / "nonexistent.txt",
                output_file,
                variables
            )


class TestFileOperations:
    """Tests for file reading and writing."""

    def setup_method(self):
        """Create temp directory."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up temp directory."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_write_file(self):
        """Test writing content to file."""
        file_path = self.temp_dir / "test.txt"
        content = "Test content"

        result = write_file(file_path, content)

        assert result is True
        assert file_path.exists()
        assert file_path.read_text() == content

    def test_write_file_creates_parent_dirs(self):
        """Test that write_file creates parent directories."""
        file_path = self.temp_dir / "nested" / "dirs" / "test.txt"
        content = "Test content"

        result = write_file(file_path, content)

        assert result is True
        assert file_path.exists()
        assert file_path.parent.exists()

    def test_read_file(self):
        """Test reading content from file."""
        file_path = self.temp_dir / "test.txt"
        content = "Test content"
        file_path.write_text(content)

        result = read_file(file_path)

        assert result == content

    def test_read_nonexistent_file(self):
        """Test reading nonexistent file returns None."""
        file_path = self.temp_dir / "nonexistent.txt"
        result = read_file(file_path)

        assert result is None


class TestTemplateVariables:
    """Tests for template variable generation."""

    def test_get_current_date(self):
        """Test current date format."""
        date = get_current_date()
        assert len(date) == 10  # YYYY-MM-DD
        assert date.count("-") == 2

    def test_get_template_variables_python(self):
        """Test template variables for Python projects."""
        config = {
            'tech_stacks': {
                'python_fastapi': {
                    'name': 'Python/FastAPI',
                    'description': 'Modern async Python framework',
                    'port': 8000
                }
            }
        }

        variables = get_template_variables(
            "TestProject",
            "web_app",
            "python_fastapi",
            config
        )

        assert variables['project_name'] == "TestProject"
        assert variables['project_type'] == "web_app"
        assert variables['tech_stack'] == "Python/FastAPI"
        assert variables['port'] == "8000"
        assert 'date' in variables
        assert 'install_commands' in variables

    def test_get_template_variables_javascript(self):
        """Test template variables for JavaScript projects."""
        config = {
            'tech_stacks': {
                'react_typescript': {
                    'name': 'React/TypeScript',
                    'description': 'React with TypeScript',
                    'port': 3000,
                    'folder': 'react-typescript'
                }
            }
        }

        variables = get_template_variables(
            "MyApp",
            "web_app",
            "react_typescript",
            config
        )

        assert variables['project_name'] == "MyApp"
        assert variables['prerequisites'] == 'Node.js 16 or higher'
        assert variables['install_commands'] == 'npm install'


class TestProjectFolders:
    """Tests for project folder configuration."""

    def test_get_project_folders(self):
        """Test getting project folders from config."""
        config = {
            'common': {
                'standard_folders': ['docs', 'tests']
            },
            'project_types': {
                'web_app': {
                    'folders': ['static', 'app']
                }
            },
            'tech_stacks': {
                'python_flask': {
                    'folders': ['src', 'config']
                }
            }
        }

        folders = get_project_folders('web_app', 'python_flask', config)

        assert 'docs' in folders
        assert 'tests' in folders
        assert 'static' in folders
        assert 'app' in folders
        assert 'src' in folders
        assert 'config' in folders

    def test_get_project_folders_no_duplicates(self):
        """Test that duplicate folders are removed."""
        config = {
            'common': {
                'standard_folders': ['docs', 'tests']
            },
            'project_types': {
                'web_app': {
                    'folders': ['docs', 'static']  # 'docs' duplicate
                }
            },
            'tech_stacks': {
                'python_flask': {
                    'folders': ['src']
                }
            }
        }

        folders = get_project_folders('web_app', 'python_flask', config)

        # Count occurrences of 'docs'
        assert folders.count('docs') == 1
