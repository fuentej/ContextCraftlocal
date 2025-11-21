"""
Python stack generators (Flask, FastAPI, Streamlit, Django, Pydantic AI)
"""

from pathlib import Path
from typing import Dict

from src.stack_generators.base import BaseStackGenerator
from src.utils import write_file, process_template


class PythonFlaskGenerator(BaseStackGenerator):
    """Generator for Python/Flask projects."""

    def generate_main_file(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> bool:
        """Generate Flask app.py file."""
        template_path = Path("templates/python_flask_template.py")
        output_path = project_path / "app.py"

        try:
            process_template(template_path, output_path, variables)
            return True
        except Exception as e:
            print(f"Error generating Flask main file: {e}")
            return False

    def generate_dependencies(self, project_path: Path) -> bool:
        """Generate requirements.txt for Flask."""
        deps = self.get_dependencies()
        content = "\n".join(deps) + "\n"
        return write_file(project_path / "requirements.txt", content)


class PythonFastAPIGenerator(BaseStackGenerator):
    """Generator for Python/FastAPI projects."""

    def generate_main_file(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> bool:
        """Generate FastAPI main.py file."""
        template_path = Path("templates/python_fastapi_template.py")
        output_path = project_path / "main.py"

        try:
            process_template(template_path, output_path, variables)
            return True
        except Exception as e:
            print(f"Error generating FastAPI main file: {e}")
            return False

    def generate_dependencies(self, project_path: Path) -> bool:
        """Generate requirements.txt for FastAPI."""
        deps = self.get_dependencies()
        content = "\n".join(deps) + "\n"
        return write_file(project_path / "requirements.txt", content)


class PythonStreamlitGenerator(BaseStackGenerator):
    """Generator for Python/Streamlit projects."""

    def generate_main_file(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> bool:
        """Generate Streamlit app.py file."""
        template_path = Path("templates/python_streamlit_template.py")
        output_path = project_path / "app.py"

        try:
            process_template(template_path, output_path, variables)
            return True
        except Exception as e:
            print(f"Error generating Streamlit main file: {e}")
            return False

    def generate_dependencies(self, project_path: Path) -> bool:
        """Generate requirements.txt for Streamlit."""
        deps = self.get_dependencies()
        content = "\n".join(deps) + "\n"
        return write_file(project_path / "requirements.txt", content)

    def get_run_command(self) -> str:
        """Override to return Streamlit-specific run command."""
        return "streamlit run app.py"


class PythonDjangoGenerator(BaseStackGenerator):
    """Generator for Python/Django projects."""

    def generate_main_file(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> bool:
        """Generate Django project structure."""
        # Django has complex structure, simplified here
        manage_py = f'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''
        return write_file(project_path / "manage.py", manage_py)

    def generate_dependencies(self, project_path: Path) -> bool:
        """Generate requirements.txt for Django."""
        deps = self.get_dependencies()
        content = "\n".join(deps) + "\n"
        return write_file(project_path / "requirements.txt", content)

    def generate_config_files(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> bool:
        """Generate Django settings."""
        settings_content = f'''"""
Django settings for {variables['project_name']}
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

STATIC_URL = 'static/'
'''
        config_dir = project_path / "config"
        config_dir.mkdir(exist_ok=True)
        return write_file(config_dir / "settings.py", settings_content)


class PydanticAIGenerator(BaseStackGenerator):
    """Generator for Pydantic AI agent projects."""

    def generate_main_file(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> bool:
        """Generate Pydantic AI main file and agent structure."""
        main_content = f'''"""
{variables['project_name']} - Pydantic AI Agent
Created: {variables['date']}
"""

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UserQuery(BaseModel):
    question: str
    context: str = ""

# Initialize the AI model
model = OpenAIModel("gpt-4o-mini")

# Create the agent
agent = Agent(
    model,
    system_prompt="""You are a helpful AI assistant for {variables['project_name']}.

    Your role is to:
    - Answer questions accurately and helpfully
    - Provide clear and concise responses
    - Be friendly and professional

    Always aim to be helpful while staying within your capabilities."""
)

async def run_agent(query: str, context: str = "") -> str:
    """Run the agent with a user query."""
    try:
        user_input = UserQuery(question=query, context=context)
        result = await agent.run(user_input.question)
        return result.data
    except Exception as e:
        return f"Error: {{str(e)}}"

if __name__ == "__main__":
    import asyncio

    async def main():
        print("🤖 {variables['project_name']} Agent")
        print("=" * 50)

        while True:
            query = input("\\nYou: ")
            if query.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break

            print("Agent: ", end="")
            response = await run_agent(query)
            print(response)

    asyncio.run(main())
'''
        return write_file(project_path / "main.py", main_content)

    def generate_dependencies(self, project_path: Path) -> bool:
        """Generate requirements.txt for Pydantic AI."""
        deps = self.get_dependencies()
        content = "\n".join(deps) + "\n"
        return write_file(project_path / "requirements.txt", content)

    def generate_config_files(
        self,
        project_path: Path,
        variables: Dict[str, str]
    ) -> bool:
        """Generate additional Pydantic AI files (agents, tools, prompts)."""
        # Create agent file
        agent_content = '''"""Main agent definition."""

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
        system_prompt="You are a helpful AI assistant.",
        result_type=AgentResponse
    )
'''
        write_file(project_path / "agents" / "agent.py", agent_content)
        write_file(project_path / "agents" / "__init__.py", "")

        # Create tools file
        tools_content = '''"""Tools for the AI agent."""

from pydantic_ai.tools import Tool
from datetime import datetime

@Tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
'''
        write_file(project_path / "tools" / "tools.py", tools_content)
        write_file(project_path / "tools" / "__init__.py", "")

        # Create prompts file
        prompts_content = '''"""System prompts and templates."""

SYSTEM_PROMPTS = {
    "default": "You are a helpful AI assistant.",
    "analytical": "You are an analytical AI assistant.",
}
'''
        write_file(project_path / "prompts" / "prompts.py", prompts_content)
        write_file(project_path / "prompts" / "__init__.py", "")

        return True


# Factory function to create appropriate generator
def get_python_generator(stack_name: str, config: Dict) -> BaseStackGenerator:
    """
    Factory function to create the appropriate Python stack generator.

    Args:
        stack_name: Name of the stack
        config: Stack configuration

    Returns:
        Appropriate generator instance
    """
    generators = {
        'python_flask': PythonFlaskGenerator,
        'python_fastapi': PythonFastAPIGenerator,
        'python_streamlit': PythonStreamlitGenerator,
        'python_django': PythonDjangoGenerator,
        'pydantic_ai': PydanticAIGenerator,
    }

    generator_class = generators.get(stack_name, PythonFlaskGenerator)
    return generator_class(config)
