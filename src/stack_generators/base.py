"""
Base generator class for tech stack-specific generators
Defines the interface that all stack generators must implement
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any


class BaseStackGenerator(ABC):
    """
    Abstract base class for technology stack generators.

    Each tech stack should have its own generator class that inherits
    from this base class and implements the required methods.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the stack generator.

        Args:
            config: Stack configuration from stacks.yaml
        """
        self.config = config
        self.name = config.get('name', 'Unknown')
        self.folder = config.get('folder', '')
        self.type = config.get('type', 'custom')

    @abstractmethod
    def generate_main_file(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> bool:
        """
        Generate the main application file for this stack.

        Args:
            project_path: Path to the project root
            variables: Template variables dictionary

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def generate_dependencies(self, project_path: Path) -> bool:
        """
        Generate dependency files (requirements.txt, package.json, etc.).

        Args:
            project_path: Path to the project root

        Returns:
            True if successful, False otherwise
        """
        pass

    def generate_config_files(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> bool:
        """
        Generate configuration files specific to this stack.

        Args:
            project_path: Path to the project root
            variables: Template variables dictionary

        Returns:
            True if successful, False otherwise
        """
        # Default implementation - can be overridden by subclasses
        return True

    def generate_tests(self, project_path: Path) -> bool:
        """
        Generate test files and test configuration.

        Args:
            project_path: Path to the project root

        Returns:
            True if successful, False otherwise
        """
        # Default implementation - can be overridden by subclasses
        return True

    def get_required_folders(self) -> List[str]:
        """
        Get list of folders required for this stack.

        Returns:
            List of folder names
        """
        return self.config.get('folders', [])

    def get_port(self) -> int:
        """
        Get default port for this stack.

        Returns:
            Port number
        """
        return self.config.get('port', 8000)

    def get_dependencies(self) -> List[str]:
        """
        Get list of dependencies for this stack.

        Returns:
            List of dependencies
        """
        return self.config.get('dependencies', [])

    def supports_hot_reload(self) -> bool:
        """
        Check if this stack supports hot reloading during development.

        Returns:
            True if hot reload is supported
        """
        # Default: assume yes for modern stacks
        return True

    def get_docker_base_image(self) -> str:
        """
        Get Docker base image for this stack.

        Returns:
            Docker image name
        """
        if self.is_python_stack():
            return "python:3.11-slim"
        elif self.is_node_stack():
            return "node:18-alpine"
        else:
            return "ubuntu:latest"

    def is_python_stack(self) -> bool:
        """Check if this is a Python-based stack."""
        return 'python' in self.folder.lower()

    def is_node_stack(self) -> bool:
        """Check if this is a Node.js-based stack."""
        return any(x in self.folder.lower() for x in ['node', 'react', 'vue', 'svelte', 'next'])

    def get_run_command(self) -> str:
        """
        Get the command to run the application.

        Returns:
            Run command string
        """
        if 'streamlit' in self.folder:
            return 'streamlit run app.py'
        elif 'fastapi' in self.folder:
            return 'uvicorn main:app --reload'
        elif self.is_python_stack():
            return 'python main.py'
        else:
            return 'npm run dev'

    def __str__(self) -> str:
        """String representation of the generator."""
        return f"{self.name} Generator ({self.type})"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"<{self.__class__.__name__}: {self.name}>"
