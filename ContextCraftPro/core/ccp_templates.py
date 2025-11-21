"""
Template management for ContextCraftPro

Handles loading, rendering, and managing Markdown templates.
"""

import re
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class TemplateError(Exception):
    """Template-related errors"""

    pass


class TemplateManager:
    """
    Manages Markdown templates with variable interpolation.

    Uses simple {{variable}} syntax for template variables.
    """

    def __init__(self, templates_dir: Path):
        """
        Initialize template manager.

        Args:
            templates_dir: Directory containing template files
        """
        self.templates_dir = Path(templates_dir)
        if not self.templates_dir.exists():
            raise TemplateError(f"Templates directory not found: {templates_dir}")

    def load_template(self, template_name: str) -> str:
        """
        Load a template file.

        Args:
            template_name: Name of template file (with or without .md extension)

        Returns:
            Template content as string

        Raises:
            TemplateError: If template file not found
        """
        # Add .md extension if not present
        if not template_name.endswith(".md"):
            template_name += ".md"

        template_path = self.templates_dir / template_name

        if not template_path.exists():
            raise TemplateError(f"Template not found: {template_name}")

        try:
            return template_path.read_text(encoding="utf-8")
        except Exception as e:
            raise TemplateError(f"Failed to read template {template_name}: {e}")

    def render_template(self, template_content: str, variables: Dict[str, Any]) -> str:
        """
        Render a template with variable substitution.

        Variables use {{variable_name}} syntax.
        Missing variables are left as-is (not replaced).

        Args:
            template_content: Template string
            variables: Dictionary of variable name -> value

        Returns:
            Rendered template
        """
        # Add common variables
        variables = self._add_common_variables(variables)

        # Simple regex-based substitution
        def replace_var(match):
            var_name = match.group(1).strip()
            value = variables.get(
                var_name, match.group(0)
            )  # Keep original if not found

            # Convert lists to formatted strings
            if isinstance(value, list):
                if len(value) == 0:
                    return "(none)"
                elif len(value) == 1:
                    return str(value[0])
                else:
                    return ", ".join(str(v) for v in value)

            return str(value) if value is not None else match.group(0)

        pattern = re.compile(r"\{\{([^}]+)\}\}")
        return pattern.sub(replace_var, template_content)

    def render_template_file(
        self, template_name: str, variables: Dict[str, Any]
    ) -> str:
        """
        Load and render a template file.

        Args:
            template_name: Name of template file
            variables: Dictionary of variables

        Returns:
            Rendered template
        """
        template_content = self.load_template(template_name)
        return self.render_template(template_content, variables)

    def _add_common_variables(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Add common variables that are always available"""
        variables = variables.copy()

        # Add date if not present
        if "date" not in variables:
            variables["date"] = datetime.now().strftime("%Y-%m-%d")

        # Add timestamp if not present
        if "timestamp" not in variables:
            variables["timestamp"] = datetime.now().isoformat()

        return variables


def slugify(text: str) -> str:
    """
    Convert text to a URL-friendly slug.

    Args:
        text: Text to slugify

    Returns:
        Slugified text (lowercase, hyphens, alphanumeric)
    """
    # Convert to lowercase
    text = text.lower()

    # Replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)

    # Remove non-alphanumeric characters except hyphens
    text = re.sub(r"[^a-z0-9-]", "", text)

    # Remove multiple consecutive hyphens
    text = re.sub(r"-+", "-", text)

    # Remove leading/trailing hyphens
    text = text.strip("-")

    return text


def extract_section(markdown: str, section_title: str) -> str:
    """
    Extract a section from a Markdown document.

    Args:
        markdown: Markdown content
        section_title: Title of section to extract (without #)

    Returns:
        Section content (including the heading), or empty string if not found
    """
    lines = markdown.split("\n")
    section_lines = []
    in_section = False
    section_level = None

    for line in lines:
        # Check if this is a heading
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)

        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()

            # Check if this is the target section
            if title.lower() == section_title.lower():
                in_section = True
                section_level = level
                section_lines.append(line)
            # Check if this is a same-or-higher level heading (end of section)
            elif in_section and level <= section_level:
                break
            # Add line if we're in the section
            elif in_section:
                section_lines.append(line)
        elif in_section:
            section_lines.append(line)

    return "\n".join(section_lines)


def append_section(markdown: str, section_content: str) -> str:
    """
    Append a section to a Markdown document.

    Args:
        markdown: Existing Markdown content
        section_content: New section to append

    Returns:
        Updated Markdown content
    """
    # Ensure existing content ends with newline
    if markdown and not markdown.endswith("\n"):
        markdown += "\n"

    # Ensure section starts with newline separation
    if markdown and not section_content.startswith("\n"):
        markdown += "\n"

    markdown += section_content

    # Ensure final newline
    if not markdown.endswith("\n"):
        markdown += "\n"

    return markdown
