"""
CLI interface for ContextCraft
Handles user interaction and orchestrates project generation
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from src.generator import ProjectGenerator


app = typer.Typer(
    name="contextcraft",
    help="Enhanced AI Project Structure Generator",
    add_completion=False
)

console = Console()


def display_welcome():
    """Display welcome banner."""
    welcome_text = """
[bold cyan]ContextCraft[/bold cyan] 🚀
[dim]Enhanced AI Project Structure Generator[/dim]

Rapidly scaffold professional software projects
with modern tech stacks and best practices built-in.
"""
    console.print(Panel(welcome_text, border_style="cyan"))


def display_options(
    title: str,
    options: Dict[str, Dict[str, Any]],
    show_description: bool = True
) -> Table:
    """
    Display options in a formatted table.

    Args:
        title: Table title
        options: Dictionary of options
        show_description: Whether to show descriptions

    Returns:
        Rich Table object
    """
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=6)
    table.add_column("Name", style="cyan")

    if show_description:
        table.add_column("Description", style="dim")

    for idx, (key, value) in enumerate(options.items(), 1):
        name = value.get('name', key)
        if show_description:
            description = value.get('description', '')
            table.add_row(str(idx), name, description)
        else:
            table.add_row(str(idx), name)

    return table


def get_project_name() -> str:
    """
    Prompt user for project name with validation.

    Returns:
        Validated project name
    """
    while True:
        name = Prompt.ask("[cyan]Project name[/cyan]")

        if not name or not name.strip():
            console.print("[red]❌ Project name cannot be empty[/red]")
            continue

        if Path(name).exists():
            console.print(f"[red]❌ Directory '{name}' already exists[/red]")
            continue

        return name.strip()


def get_choice(
    prompt_text: str,
    options: Dict[str, Any],
    default: str = "1"
) -> str:
    """
    Get user choice from options.

    Args:
        prompt_text: Prompt message
        options: Dictionary of available options
        default: Default choice

    Returns:
        Selected option key
    """
    while True:
        choice = Prompt.ask(
            f"[cyan]{prompt_text}[/cyan]",
            default=default
        )

        # Convert choice number to key
        try:
            idx = int(choice) - 1
            keys = list(options.keys())
            if 0 <= idx < len(keys):
                return keys[idx]
        except (ValueError, IndexError):
            pass

        # Check if choice is a valid key
        if choice in options:
            return choice

        console.print("[red]❌ Invalid choice. Please try again.[/red]")


def display_next_steps(
    project_name: str,
    tech_stack: str,
    project_path: Path
):
    """
    Display next steps after project creation.

    Args:
        project_name: Name of created project
        tech_stack: Technology stack used
        project_path: Path to created project
    """
    console.print("\n[bold green]✅ Project created successfully![/bold green]")
    console.print(f"[dim]📁 Location: {project_path.absolute()}[/dim]\n")

    # Determine commands based on tech stack
    is_python = 'python' in tech_stack
    is_streamlit = 'streamlit' in tech_stack

    next_steps = []

    next_steps.append(f"cd {project_name}")

    if is_python:
        next_steps.extend([
            "python -m venv venv",
            "source venv/bin/activate  # Mac/Linux, or venv\\Scripts\\activate on Windows",
            "pip install -r requirements.txt",
        ])

        if is_streamlit:
            next_steps.append("streamlit run app.py")
        else:
            next_steps.append("python main.py")
    else:
        next_steps.extend([
            "npm install",
            "npm run dev  # or npm start"
        ])

    # Create table for next steps
    table = Table(title="🚀 Next Steps", show_header=False, border_style="green")
    table.add_column("Step", style="cyan")

    for idx, step in enumerate(next_steps, 1):
        table.add_row(f"{idx}. {step}")

    console.print(table)

    # Additional tips
    console.print("\n[bold]💡 Additional Tips:[/bold]")
    tips = [
        "📝 Edit template files in the 'templates/' folder",
        "🐳 Use Docker: [dim]docker-compose -f docker/docker-compose.yml up[/dim]",
        "☁️  Deploy with IaC templates in 'iac/' folder",
        "📚 Check docs/ for planning and task templates"
    ]

    for tip in tips:
        console.print(f"  • {tip}")


@app.command()
def create(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Project name"),
    project_type: Optional[str] = typer.Option(None, "--type", "-t", help="Project type"),
    stack: Optional[str] = typer.Option(None, "--stack", "-s", help="Tech stack"),
    non_interactive: bool = typer.Option(False, "--yes", "-y", help="Skip prompts"),
):
    """
    Create a new project with guided prompts.

    You can provide all options via flags for non-interactive mode,
    or run without flags for an interactive experience.
    """
    try:
        generator = ProjectGenerator()

        # Interactive mode
        if not non_interactive:
            display_welcome()

        # Get project name
        if not name:
            project_name = get_project_name()
        else:
            project_name = name

        # Get project type
        project_types = generator.get_available_project_types()
        if not project_type:
            console.print()
            console.print(display_options("Select Project Type", project_types))
            project_type_key = get_choice(
                "Choose project type",
                project_types,
                default="1"
            )
        else:
            project_type_key = project_type

        # Get tech stack
        tech_stacks = generator.get_available_stacks()
        if not stack:
            console.print()
            console.print(display_options("Select Technology Stack", tech_stacks))
            tech_stack_key = get_choice(
                "Choose tech stack",
                tech_stacks,
                default="1"
            )
        else:
            tech_stack_key = stack

        # Confirm before creating
        if not non_interactive:
            console.print()
            selected_type = project_types[project_type_key]['name']
            selected_stack = tech_stacks[tech_stack_key]['name']

            console.print(f"[cyan]Project:[/cyan] {project_name}")
            console.print(f"[cyan]Type:[/cyan] {selected_type}")
            console.print(f"[cyan]Stack:[/cyan] {selected_stack}")
            console.print()

            if not Confirm.ask("Create project?", default=True):
                console.print("[yellow]Cancelled.[/yellow]")
                return

        # Create the project
        console.print()
        success = generator.create_project(
            project_name,
            project_type_key,
            tech_stack_key
        )

        if success:
            display_next_steps(
                project_name,
                tech_stack_key,
                Path(project_name)
            )
        else:
            console.print("[red]❌ Failed to create project[/red]")
            sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


@app.command()
def list_stacks():
    """List all available technology stacks."""
    try:
        generator = ProjectGenerator()
        stacks = generator.get_available_stacks()

        console.print(display_options("Available Technology Stacks", stacks))

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


@app.command()
def list_types():
    """List all available project types."""
    try:
        generator = ProjectGenerator()
        types = generator.get_available_project_types()

        console.print(display_options("Available Project Types", types))

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


@app.command()
def version():
    """Show ContextCraft version."""
    console.print("[cyan]ContextCraft[/cyan] v1.0.0")
    console.print("[dim]Enhanced AI Project Structure Generator[/dim]")


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
