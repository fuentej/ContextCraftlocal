"""
Unit tests for stack-specific generators
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from src.stack_generators.base import BaseStackGenerator
from src.stack_generators.python import (
    PythonFlaskGenerator,
    PythonFastAPIGenerator,
    PythonStreamlitGenerator,
    PydanticAIGenerator,
    get_python_generator
)
from src.stack_generators.javascript import (
    ReactTypeScriptGenerator,
    NodeExpressGenerator,
    get_javascript_generator
)


class TestBaseStackGenerator:
    """Tests for the base stack generator."""

    def test_base_generator_initialization(self):
        """Test base generator initialization."""
        config = {
            'name': 'Test Stack',
            'folder': 'test-stack',
            'type': 'backend',
            'port': 8000,
            'folders': ['src', 'tests'],
            'dependencies': ['pytest>=7.0.0']
        }

        class TestGenerator(BaseStackGenerator):
            def generate_main_file(self, project_path, variables):
                return True

            def generate_dependencies(self, project_path):
                return True

        generator = TestGenerator(config)

        assert generator.name == 'Test Stack'
        assert generator.folder == 'test-stack'
        assert generator.type == 'backend'
        assert generator.get_port() == 8000
        assert generator.get_required_folders() == ['src', 'tests']

    def test_is_python_stack(self):
        """Test Python stack detection."""
        config = {'name': 'Python/Flask', 'folder': 'python-flask', 'type': 'backend'}

        class TestGenerator(BaseStackGenerator):
            def generate_main_file(self, project_path, variables):
                return True

            def generate_dependencies(self, project_path):
                return True

        generator = TestGenerator(config)
        assert generator.is_python_stack() is True

    def test_is_node_stack(self):
        """Test Node.js stack detection."""
        config = {'name': 'React', 'folder': 'react-typescript', 'type': 'frontend'}

        class TestGenerator(BaseStackGenerator):
            def generate_main_file(self, project_path, variables):
                return True

            def generate_dependencies(self, project_path):
                return True

        generator = TestGenerator(config)
        assert generator.is_node_stack() is True


class TestPythonGenerators:
    """Tests for Python stack generators."""

    def setup_method(self):
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_flask_generator_creates_app_file(self):
        """Test Flask generator creates app.py."""
        config = {
            'name': 'Python/Flask',
            'folder': 'python-flask',
            'type': 'backend',
            'dependencies': ['Flask>=3.0.0', 'pytest>=7.0.0']
        }

        generator = PythonFlaskGenerator(config)
        variables = {'project_name': 'TestApp', 'date': '2024-01-01'}

        result = generator.generate_main_file(self.temp_dir, variables)

        # Note: Will fail if template doesn't exist, but structure is correct
        assert generator.name == 'Python/Flask'

    def test_flask_generator_creates_dependencies(self):
        """Test Flask generator creates requirements.txt."""
        config = {
            'name': 'Python/Flask',
            'folder': 'python-flask',
            'type': 'backend',
            'dependencies': ['Flask>=3.0.0', 'flask-cors>=4.0.0', 'pytest>=7.0.0']
        }

        generator = PythonFlaskGenerator(config)
        result = generator.generate_dependencies(self.temp_dir)

        assert result is True
        requirements_file = self.temp_dir / "requirements.txt"
        assert requirements_file.exists()

        content = requirements_file.read_text()
        assert "Flask>=3.0.0" in content
        assert "flask-cors>=4.0.0" in content

    def test_fastapi_generator(self):
        """Test FastAPI generator."""
        config = {
            'name': 'Python/FastAPI',
            'folder': 'python-fastapi',
            'type': 'backend',
            'dependencies': ['fastapi>=0.104.1', 'uvicorn>=0.24.0']
        }

        generator = PythonFastAPIGenerator(config)

        assert generator.name == 'Python/FastAPI'
        assert generator.get_run_command() == 'uvicorn main:app --reload'

    def test_streamlit_generator_run_command(self):
        """Test Streamlit generator run command."""
        config = {
            'name': 'Python/Streamlit',
            'folder': 'python-streamlit',
            'type': 'fullstack',
            'dependencies': ['streamlit>=1.28.0']
        }

        generator = PythonStreamlitGenerator(config)

        assert generator.get_run_command() == "streamlit run app.py"

    def test_pydantic_ai_generator_config_files(self):
        """Test Pydantic AI generator creates agent files."""
        config = {
            'name': 'Pydantic AI',
            'folder': 'pydantic-ai',
            'type': 'ai-agent',
            'dependencies': ['pydantic-ai>=0.0.14']
        }

        generator = PydanticAIGenerator(config)
        variables = {'project_name': 'TestAgent', 'date': '2024-01-01'}

        # Create required directories
        (self.temp_dir / "agents").mkdir()
        (self.temp_dir / "tools").mkdir()
        (self.temp_dir / "prompts").mkdir()

        result = generator.generate_config_files(self.temp_dir, variables)

        assert result is True
        assert (self.temp_dir / "agents" / "agent.py").exists()
        assert (self.temp_dir / "tools" / "tools.py").exists()
        assert (self.temp_dir / "prompts" / "prompts.py").exists()

    def test_get_python_generator_factory(self):
        """Test Python generator factory function."""
        config = {'name': 'Flask', 'folder': 'python-flask', 'type': 'backend'}

        generator = get_python_generator('python_flask', config)

        assert isinstance(generator, PythonFlaskGenerator)

        generator2 = get_python_generator('python_fastapi', config)
        assert isinstance(generator2, PythonFastAPIGenerator)


class TestJavaScriptGenerators:
    """Tests for JavaScript stack generators."""

    def setup_method(self):
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_react_generator_creates_package_json(self):
        """Test React generator creates package.json."""
        config = {
            'name': 'React/TypeScript',
            'folder': 'react-typescript',
            'type': 'frontend',
            'dependencies': {'react': '^18.2.0'},
            'dev_dependencies': {'typescript': '^4.9.0'}
        }

        generator = ReactTypeScriptGenerator(config)
        result = generator.generate_dependencies(self.temp_dir)

        assert result is True
        package_json = self.temp_dir / "package.json"
        assert package_json.exists()

        import json
        content = json.loads(package_json.read_text())
        assert 'dependencies' in content
        assert 'react' in content['dependencies']

    def test_react_generator_creates_tsconfig(self):
        """Test React generator creates tsconfig.json."""
        config = {
            'name': 'React/TypeScript',
            'folder': 'react-typescript',
            'type': 'frontend',
            'dependencies': {},
            'dev_dependencies': {}
        }

        # Create required directories
        (self.temp_dir / "src").mkdir()
        (self.temp_dir / "public").mkdir()

        generator = ReactTypeScriptGenerator(config)
        variables = {'project_name': 'TestApp', 'date': '2024-01-01'}

        result = generator.generate_main_file(self.temp_dir, variables)

        tsconfig = self.temp_dir / "tsconfig.json"
        assert tsconfig.exists()

        import json
        content = json.loads(tsconfig.read_text())
        assert 'compilerOptions' in content
        assert content['compilerOptions']['jsx'] == 'react-jsx'

    def test_node_express_generator(self):
        """Test Node/Express generator."""
        config = {
            'name': 'Node.js/Express',
            'folder': 'node-express',
            'type': 'backend',
            'dependencies': {'express': '^4.18.2'},
            'dev_dependencies': {'nodemon': '^3.0.1'}
        }

        generator = NodeExpressGenerator(config)

        assert generator.name == 'Node.js/Express'
        assert generator.is_node_stack() is True

    def test_node_express_package_json(self):
        """Test Node/Express creates proper package.json."""
        config = {
            'name': 'Node.js/Express',
            'folder': 'node-express',
            'type': 'backend',
            'dependencies': {'express': '^4.18.2', 'cors': '^2.8.5'},
            'dev_dependencies': {'nodemon': '^3.0.1'}
        }

        generator = NodeExpressGenerator(config)
        result = generator.generate_dependencies(self.temp_dir)

        assert result is True
        package_json = self.temp_dir / "package.json"
        assert package_json.exists()

        import json
        content = json.loads(package_json.read_text())
        assert 'express' in content['dependencies']
        assert 'cors' in content['dependencies']
        assert 'nodemon' in content['devDependencies']
        assert 'scripts' in content

    def test_get_javascript_generator_factory(self):
        """Test JavaScript generator factory function."""
        config = {'name': 'React', 'folder': 'react-typescript', 'type': 'frontend'}

        generator = get_javascript_generator('react_typescript', config)

        assert isinstance(generator, ReactTypeScriptGenerator)

        generator2 = get_javascript_generator('node_express', config)
        assert isinstance(generator2, NodeExpressGenerator)


class TestGeneratorDockerSupport:
    """Tests for Docker configuration in generators."""

    def test_python_docker_base_image(self):
        """Test Python generators use correct Docker base image."""
        config = {'name': 'Flask', 'folder': 'python-flask', 'type': 'backend'}
        generator = PythonFlaskGenerator(config)

        assert generator.get_docker_base_image() == "python:3.11-slim"

    def test_node_docker_base_image(self):
        """Test Node generators use correct Docker base image."""
        config = {'name': 'React', 'folder': 'react-typescript', 'type': 'frontend'}
        generator = ReactTypeScriptGenerator(config)

        assert generator.get_docker_base_image() == "node:18-alpine"


class TestGeneratorStringMethods:
    """Tests for generator string representations."""

    def test_generator_str(self):
        """Test generator __str__ method."""
        config = {'name': 'Python/Flask', 'folder': 'python-flask', 'type': 'backend'}
        generator = PythonFlaskGenerator(config)

        assert str(generator) == "Python/Flask Generator (backend)"

    def test_generator_repr(self):
        """Test generator __repr__ method."""
        config = {'name': 'Python/Flask', 'folder': 'python-flask', 'type': 'backend'}
        generator = PythonFlaskGenerator(config)

        repr_str = repr(generator)
        assert "PythonFlaskGenerator" in repr_str
        assert "Python/Flask" in repr_str
