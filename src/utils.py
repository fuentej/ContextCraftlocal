"""
Utility functions for ContextCraft
Handles common operations like file I/O, path validation, template processing
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import yaml


def load_stack_config(config_path: str = "config/stacks.yaml") -> Dict[str, Any]:
    """
    Load technology stack configuration from YAML file.

    Args:
        config_path: Path to the stacks configuration file

    Returns:
        Dictionary containing stack configurations

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


def validate_project_name(name: str) -> bool:
    """
    Validate project name for filesystem compatibility.

    Args:
        name: Proposed project name

    Returns:
        True if name is valid, False otherwise
    """
    if not name or not name.strip():
        return False

    # Check for invalid characters
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    if any(char in name for char in invalid_chars):
        return False

    # Check if path already exists
    if Path(name).exists():
        return False

    return True


def create_directory_structure(base_path: Path, folders: List[str]) -> None:
    """
    Create a directory structure from a list of folder names.

    Args:
        base_path: Base directory path
        folders: List of folder names to create
    """
    base_path.mkdir(parents=True, exist_ok=True)

    for folder in folders:
        folder_path = base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)


def process_template(
    template_path: Path,
    output_path: Path,
    variables: Dict[str, str]
) -> None:
    """
    Process a template file by replacing variables and writing to output.

    Args:
        template_path: Path to template file
        output_path: Path where processed file should be written
        variables: Dictionary of variable name -> value mappings

    Raises:
        FileNotFoundError: If template file doesn't exist
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, 'r') as f:
        content = f.read()

    # Replace all variables in the template
    for key, value in variables.items():
        placeholder = "{" + key + "}"
        content = content.replace(placeholder, str(value))

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(content)


def copy_template_file(src: Path, dest: Path) -> bool:
    """
    Copy a template file from source to destination.

    Args:
        src: Source file path
        dest: Destination file path

    Returns:
        True if successful, False otherwise
    """
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        return True
    except Exception as e:
        print(f"Error copying {src} to {dest}: {e}")
        return False


def get_current_date() -> str:
    """
    Get current date in YYYY-MM-DD format.

    Returns:
        Formatted date string
    """
    return datetime.now().strftime("%Y-%m-%d")


def get_template_variables(
    project_name: str,
    project_type: str,
    tech_stack: str,
    config: Dict[str, Any]
) -> Dict[str, str]:
    """
    Generate template variables dictionary for a project.

    Args:
        project_name: Name of the project
        project_type: Type of project (from config)
        tech_stack: Technology stack (from config)
        config: Full configuration dictionary

    Returns:
        Dictionary of template variables
    """
    stack_info = config['tech_stacks'].get(tech_stack, {})

    variables = {
        'project_name': project_name,
        'date': get_current_date(),
        'project_type': project_type,
        'tech_stack': stack_info.get('name', tech_stack),
        'tech_stack_details': stack_info.get('description', ''),
        'port': str(stack_info.get('port', '8000')),
    }

    # Generate install commands based on tech stack
    if 'python' in tech_stack:
        variables['prerequisites'] = 'Python 3.8 or higher'
        variables['install_commands'] = '''# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Mac/Linux
# or
venv\\Scripts\\activate  # On Windows

# Install dependencies
pip install -r requirements.txt'''
        variables['run_commands'] = get_python_run_command(stack_info)
        variables['test_commands'] = 'pytest tests/'

    else:  # JavaScript/TypeScript
        variables['prerequisites'] = 'Node.js 16 or higher'
        variables['install_commands'] = 'npm install'
        variables['run_commands'] = get_node_run_command(stack_info)
        variables['test_commands'] = 'npm test'

    return variables


def get_python_run_command(stack_info: Dict[str, Any]) -> str:
    """Get the appropriate run command for a Python stack."""
    main_file = stack_info.get('main_file', 'main.py')

    if 'streamlit' in stack_info.get('folder', ''):
        return f'streamlit run {main_file}'
    elif 'fastapi' in stack_info.get('folder', ''):
        return f'uvicorn {main_file.replace(".py", "")}:app --reload'
    else:
        return f'python {main_file}'


def get_node_run_command(stack_info: Dict[str, Any]) -> str:
    """Get the appropriate run command for a Node.js stack."""
    if stack_info.get('type') == 'frontend':
        return 'npm start'
    else:
        return 'npm run dev'


def create_init_file(directory: Path, content: str = "") -> None:
    """
    Create a __init__.py file in a directory.

    Args:
        directory: Directory to create __init__.py in
        content: Optional content for the file
    """
    init_file = directory / "__init__.py"
    with open(init_file, 'w') as f:
        f.write(content)


def ensure_directory_exists(path: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists
    """
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str) -> bool:
    """
    Write content to a file, creating parent directories if needed.

    Args:
        path: File path to write to
        content: Content to write

    Returns:
        True if successful, False otherwise
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to {path}: {e}")
        return False


def read_file(path: Path) -> Optional[str]:
    """
    Read content from a file.

    Args:
        path: File path to read from

    Returns:
        File content as string, or None if error
    """
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None


def get_project_folders(
    project_type: str,
    tech_stack: str,
    config: Dict[str, Any]
) -> List[str]:
    """
    Get the list of folders to create for a project.

    Args:
        project_type: Type of project
        tech_stack: Technology stack
        config: Configuration dictionary

    Returns:
        List of folder names to create
    """
    folders = config['common']['standard_folders'].copy()

    # Add project type specific folders
    project_config = config['project_types'].get(project_type, {})
    folders.extend(project_config.get('folders', []))

    # Add tech stack specific folders
    stack_config = config['tech_stacks'].get(tech_stack, {})
    folders.extend(stack_config.get('folders', []))

    # Remove duplicates while preserving order
    seen = set()
    unique_folders = []
    for folder in folders:
        if folder not in seen:
            seen.add(folder)
            unique_folders.append(folder)

    return unique_folders


def format_list_for_display(items: List[str], numbered: bool = True) -> str:
    """
    Format a list of items for console display.

    Args:
        items: List of items to format
        numbered: Whether to number the items

    Returns:
        Formatted string
    """
    if numbered:
        return "\n".join(f"  {i+1}. {item}" for i, item in enumerate(items))
    else:
        return "\n".join(f"  - {item}" for item in items)
