"""
Core project generator module for ContextCraft
Handles the main logic for creating and scaffolding projects
"""

from pathlib import Path
from typing import Dict, Optional, Any, List
import shutil

from src.utils import (
    load_stack_config,
    validate_project_name,
    create_directory_structure,
    process_template,
    get_template_variables,
    get_project_folders,
    write_file,
    ensure_directory_exists
)


class ProjectGenerator:
    """
    Main project generator class.
    Orchestrates the creation of project structures based on templates.
    """

    def __init__(self, config_path: str = "config/stacks.yaml"):
        """
        Initialize the project generator.

        Args:
            config_path: Path to the stack configuration file
        """
        self.config = load_stack_config(config_path)
        self.template_dir = Path("templates")

    def create_project(
        self,
        project_name: str,
        project_type: str,
        tech_stack: str,
        output_dir: Optional[Path] = None
    ) -> bool:
        """
        Create a new project with the specified configuration.

        Args:
            project_name: Name of the project
            project_type: Type of project (from config)
            tech_stack: Technology stack (from config)
            output_dir: Optional custom output directory

        Returns:
            True if successful, False otherwise
        """
        # Validate project name
        if not validate_project_name(project_name):
            print(f"❌ Invalid project name or project already exists: {project_name}")
            return False

        # Determine project path
        if output_dir:
            project_path = output_dir / project_name
        else:
            project_path = Path(project_name)

        try:
            # Create folder structure
            print("📁 Creating folder structure...")
            self._create_folders(project_path, project_type, tech_stack)

            # Generate template variables
            variables = get_template_variables(
                project_name,
                project_type,
                tech_stack,
                self.config
            )

            # Create main application file
            print("📝 Creating main application file...")
            self._create_main_file(project_path, tech_stack, variables)

            # Create documentation files
            print("📄 Creating documentation files...")
            self._create_documentation(project_path, variables)

            # Create dependency files
            print("📦 Creating dependency files...")
            self._create_dependencies(project_path, tech_stack)

            # Create configuration files
            print("⚙️  Creating configuration files...")
            self._create_config_files(project_path, tech_stack, variables)

            # Create Docker files
            print("🐳 Creating Docker configuration...")
            self._create_docker_files(project_path, tech_stack)

            # Create IaC files
            print("☁️  Creating Infrastructure as Code templates...")
            self._create_iac_files(project_path, project_name)

            print(f"\n✅ Project '{project_name}' created successfully!")
            print(f"📁 Location: {project_path.absolute()}")

            return True

        except Exception as e:
            print(f"❌ Error creating project: {e}")
            # Cleanup partial project on failure
            if project_path.exists():
                shutil.rmtree(project_path)
            return False

    def _create_folders(
        self,
        project_path: Path,
        project_type: str,
        tech_stack: str
    ) -> None:
        """Create the project folder structure."""
        folders = get_project_folders(project_type, tech_stack, self.config)
        create_directory_structure(project_path, folders)

        # Create __init__.py for Python projects
        if 'python' in tech_stack:
            src_dir = project_path / "src"
            if src_dir.exists():
                write_file(src_dir / "__init__.py", '"""Main package."""\n')

    def _create_main_file(
        self,
        project_path: Path,
        tech_stack: str,
        variables: Dict[str, str]
    ) -> None:
        """Create the main application file based on tech stack."""
        stack_config = self.config['tech_stacks'].get(tech_stack, {})
        template_name = stack_config.get('template')

        if not template_name:
            print(f"⚠️  No template defined for {tech_stack}")
            return

        template_path = self.template_dir / template_name
        main_file = stack_config.get('main_file', 'main.py')
        output_path = project_path / main_file

        if template_path.exists():
            process_template(template_path, output_path, variables)
        else:
            print(f"⚠️  Template not found: {template_path}")

        # Handle special cases with additional files
        if tech_stack == 'pydantic_ai':
            self._create_pydantic_ai_files(project_path, variables)
        elif tech_stack == 'react_typescript':
            self._create_react_files(project_path, variables)

    def _create_pydantic_ai_files(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> None:
        """Create additional files for Pydantic AI projects."""
        # Agent file
        agent_content = f'''"""
Main agent definition for {variables['project_name']}
"""

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from typing import List

class AgentResponse(BaseModel):
    """Structured response from the agent."""
    answer: str
    confidence: float = 1.0
    sources: List[str] = []

def create_agent() -> Agent:
    """Create and configure the main agent."""
    model = OpenAIModel("gpt-4o-mini")

    return Agent(
        model,
        system_prompt="""You are an AI assistant.
        Provide helpful, accurate responses.""",
        result_type=AgentResponse
    )
'''
        write_file(project_path / "agents" / "agent.py", agent_content)
        write_file(project_path / "agents" / "__init__.py", "")

        # Tools file
        tools_content = '''"""Tools and functions for the AI agent."""

from pydantic_ai.tools import Tool
from datetime import datetime

@Tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
'''
        write_file(project_path / "tools" / "tools.py", tools_content)
        write_file(project_path / "tools" / "__init__.py", "")

        # Prompts file
        prompts_content = '''"""System prompts and prompt templates."""

SYSTEM_PROMPTS = {
    "default": "You are a helpful AI assistant.",
    "analytical": "You are an analytical AI assistant.",
}
'''
        write_file(project_path / "prompts" / "prompts.py", prompts_content)
        write_file(project_path / "prompts" / "__init__.py", "")

    def _create_react_files(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> None:
        """Create additional React project files."""
        # index.tsx
        index_content = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
        write_file(project_path / "src" / "index.tsx", index_content)

        # index.html
        html_content = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{variables['project_name']}</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
'''
        write_file(project_path / "public" / "index.html", html_content)

        # CSS files
        write_file(project_path / "src" / "index.css", "body { margin: 0; }")
        write_file(project_path / "src" / "App.css", ".App { text-align: center; }")

        # tsconfig.json
        tsconfig = '''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
'''
        write_file(project_path / "tsconfig.json", tsconfig)

    def _create_documentation(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> None:
        """Create documentation files from templates."""
        doc_templates = [
            ('readme_template.md', 'README.md'),
            ('planning_template.md', 'docs/PLANNING.md'),
            ('task_template.md', 'docs/TASKS.md'),
        ]

        for template_name, output_name in doc_templates:
            template_path = self.template_dir / template_name
            output_path = project_path / output_name

            if template_path.exists():
                process_template(template_path, output_path, variables)

    def _create_dependencies(
        self,
        project_path: Path,
        tech_stack: str
    ) -> None:
        """Create dependency files (requirements.txt or package.json)."""
        stack_config = self.config['tech_stacks'].get(tech_stack, {})

        if 'python' in tech_stack:
            # Create requirements.txt
            deps = stack_config.get('dependencies', [])
            content = "\n".join(deps) + "\n"
            write_file(project_path / "requirements.txt", content)

        else:
            # Create package.json
            project_name = project_path.name.lower().replace(' ', '-')
            deps = stack_config.get('dependencies', {})
            dev_deps = stack_config.get('dev_dependencies', {})

            package_json = {
                "name": project_name,
                "version": "0.1.0",
                "private": True,
                "dependencies": deps,
                "devDependencies": dev_deps
            }

            # Add scripts based on stack type
            if stack_config.get('type') == 'frontend':
                package_json["scripts"] = {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test"
                }
            else:
                package_json["scripts"] = {
                    "start": "node index.js",
                    "dev": "nodemon index.js",
                    "test": "jest"
                }

            import json
            content = json.dumps(package_json, indent=2)
            write_file(project_path / "package.json", content)

    def _create_config_files(
        self,
        project_path: Path,
        tech_stack: str,
        variables: Dict[str, str]
    ) -> None:
        """Create configuration files (.env, .gitignore)."""
        # .env.example
        env_template = self.template_dir / "env_template"
        if env_template.exists():
            process_template(
                env_template,
                project_path / ".env.example",
                variables
            )

        # .gitignore
        gitignore_template = self.template_dir / "gitignore_template"
        if gitignore_template.exists():
            shutil.copy2(gitignore_template, project_path / ".gitignore")

    def _create_docker_files(self, project_path: Path, tech_stack: str) -> None:
        """Create Docker configuration files."""
        docker_dir = project_path / "docker"
        ensure_directory_exists(docker_dir)

        stack_config = self.config['tech_stacks'].get(tech_stack, {})
        port = stack_config.get('port', 8000)

        if 'python' in tech_stack:
            dockerfile = f'''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE {port}

CMD ["python", "main.py"]
'''
        else:
            dockerfile = f'''FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

EXPOSE {port}

CMD ["npm", "start"]
'''
        write_file(docker_dir / "Dockerfile", dockerfile)

        # Docker Compose
        compose = f'''version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "{port}:{port}"
    environment:
      - DEBUG=True
    volumes:
      - ..:/app
'''
        write_file(docker_dir / "docker-compose.yml", compose)

    def _create_iac_files(self, project_path: Path, project_name: str) -> None:
        """Create Infrastructure as Code templates."""
        iac_dir = project_path / "iac"
        ensure_directory_exists(iac_dir)

        # Terraform main.tf
        terraform = f'''# Terraform configuration for {project_name}

terraform {{
  required_version = ">= 1.0"
}}

# Add your infrastructure resources here
'''
        write_file(iac_dir / "main.tf", terraform)

        # variables.tf
        variables_tf = f'''variable "project_name" {{
  description = "Name of the project"
  type        = string
  default     = "{project_name}"
}}

variable "environment" {{
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}}
'''
        write_file(iac_dir / "variables.tf", variables_tf)

        # README
        iac_readme = f'''# Infrastructure as Code

This directory contains IaC templates for deploying {project_name}.

## Terraform

```bash
terraform init
terraform plan
terraform apply
```

## Azure ARM

See `azure-template.json` for Azure Resource Manager template.
'''
        write_file(iac_dir / "README.md", iac_readme)

    def get_available_stacks(self) -> Dict[str, Dict[str, Any]]:
        """Get all available technology stacks."""
        return self.config.get('tech_stacks', {})

    def get_available_project_types(self) -> Dict[str, Dict[str, Any]]:
        """Get all available project types."""
        return self.config.get('project_types', {})
