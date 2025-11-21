"""
Prompt templates and builders for ContextCraftPro LLM operations.

Provides structured prompt construction for each command, with proper
context layering and variable safety.
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
import json

from core.ccp_fs import ProjectProfile
from core.ccp_logger import CCPLogger


class PromptBuilder:
    """
    Constructs prompts from templates and context.

    Handles variable interpolation, context layering, and prompt structuring
    for different CCP commands.
    """

    def __init__(self, logger: CCPLogger):
        self.logger = logger

    def build_new_feature_prompt(
        self,
        user_answers: Dict[str, str],
        project_profile: ProjectProfile,
        existing_features: List[str],
    ) -> List[Dict[str, str]]:
        """
        Build prompt for new-feature command to refine user's answers.

        Args:
            user_answers: Q&A responses from user
            project_profile: Project metadata
            existing_features: List of existing feature names

        Returns:
            Messages for chat completion
        """
        system_prompt = """You are a senior software architect helping to create a clear feature specification.

Your role is to:
1. Take the user's answers about a feature they want to build
2. Structure them into a clear, actionable feature specification
3. Identify any gaps or ambiguities that need clarification
4. Ensure the specification is concrete and implementable

Do NOT add requirements the user didn't mention.
Do NOT suggest technology choices they didn't specify.
DO preserve their exact terminology and constraints."""

        user_prompt = f"""Please convert these feature planning answers into a structured specification.

Project: {project_profile.name}
Languages: {', '.join(project_profile.languages) if project_profile.languages else 'Not specified'}
Frameworks: {', '.join(project_profile.frameworks) if project_profile.frameworks else 'Not specified'}

User's Answers:
{self._format_user_answers(user_answers)}

Existing Features in Project:
{self._format_list(existing_features) if existing_features else 'None'}

Please create a feature specification with these sections:
1. **Feature Name**: A concise, descriptive name
2. **Description**: What this feature does (2-3 sentences)
3. **User Value**: Why this matters to users
4. **Scope**: What's included and what's explicitly excluded
5. **Key Requirements**: Bullet points of must-have functionality
6. **Technical Considerations**: Any technical constraints or notes
7. **Open Questions**: Any ambiguities that need clarification

Format as clean Markdown suitable for saving in INITIAL.md."""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def build_generate_prp_prompt(
        self,
        feature_spec: str,
        project_profile: ProjectProfile,
        claude_rules: str,
        examples: List[str],
        docs_context: str,
    ) -> List[Dict[str, str]]:
        """
        Build comprehensive PRP generation prompt.

        Args:
            feature_spec: Feature specification from INITIAL.md
            project_profile: Project metadata
            claude_rules: Contents of claude.md
            examples: Relevant code examples
            docs_context: Documentation references

        Returns:
            Messages for chat completion
        """
        system_prompt = """You are a senior software architect creating a Product Requirements Prompt (PRP).

A PRP is a comprehensive document that enables an AI coding assistant to implement a feature correctly on the first attempt. It must be self-contained, precise, and actionable.

Your PRP must include ALL of these sections:
1. Context & Assumptions
2. Goals and Non-Goals
3. Ordered Implementation Steps
4. Implementation Checklist
5. Validation Plan

Be specific about file paths, function names, and technical details when the project structure makes them clear."""

        # Build context sections
        context_parts = []

        # Project context
        context_parts.append(
            f"""## Project Context

**Name**: {project_profile.name}
**Languages**: {', '.join(project_profile.languages) if project_profile.languages else 'Not specified'}
**Frameworks**: {', '.join(project_profile.frameworks) if project_profile.frameworks else 'Not specified'}
**Test Command**: {project_profile.test_command or 'Not specified'}"""
        )

        # Coding rules (truncated if too long)
        if claude_rules:
            rules_preview = (
                claude_rules[:2000] if len(claude_rules) > 2000 else claude_rules
            )
            context_parts.append(
                f"""## Coding Rules

{rules_preview}"""
            )

        # Feature specification
        context_parts.append(
            f"""## Feature Specification

{feature_spec}"""
        )

        # Examples (if provided)
        if examples:
            examples_text = "\n\n".join(examples[:3])  # Limit to 3 examples
            context_parts.append(
                f"""## Code Examples

{examples_text}"""
            )

        # Documentation context (if provided)
        if docs_context:
            docs_preview = (
                docs_context[:1000] if len(docs_context) > 1000 else docs_context
            )
            context_parts.append(
                f"""## Documentation Context

{docs_preview}"""
            )

        full_context = "\n\n".join(context_parts)

        user_prompt = f"""{full_context}

## Your Task

Create a comprehensive Product Requirements Prompt (PRP) for implementing this feature.

The PRP must have these exact sections:

### Context & Assumptions
- Current state of the codebase
- What already exists that we'll build on
- Key assumptions about the implementation

### Goals and Non-Goals
- **Goals**: What this implementation MUST achieve
- **Non-Goals**: What this implementation should NOT attempt

### Ordered Implementation Steps
1. First concrete step (e.g., "Create new file `src/feature.py`")
2. Second concrete step (e.g., "Add function `process_data()` that...")
3. Continue with specific, actionable steps...

### Implementation Checklist
A checklist an implementer can use to verify completeness:
- [ ] Component X is created and exported
- [ ] Function Y handles edge case Z
- [ ] Tests cover scenarios A, B, C
- [ ] Documentation updated in file D

### Validation Plan
How to verify the implementation works:
1. Run these specific commands...
2. Expected outcomes should be...
3. Manual testing steps include...

Remember:
- Be specific about file paths and function names
- Include error handling requirements
- Specify test coverage expectations
- Make each step concrete and actionable"""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def build_validate_prompt(
        self,
        feature_name: str,
        prp_content: str,
        test_output: Optional[str],
        implementation_notes: str,
    ) -> List[Dict[str, str]]:
        """
        Build prompt for validation analysis.

        Args:
            feature_name: Name of the feature
            prp_content: Original PRP content
            test_output: Output from test execution (if any)
            implementation_notes: Developer's notes on implementation

        Returns:
            Messages for chat completion
        """
        system_prompt = """You are a QA engineer analyzing whether an implementation matches its requirements.

Your role is to:
1. Compare the PRP requirements against actual implementation results
2. Identify what was successfully implemented
3. Note any deviations or missing pieces
4. Suggest improvements for future iterations

Be objective and specific in your analysis."""

        test_section = ""
        if test_output:
            test_section = f"""## Test Results

```
{test_output[:2000]}  # Truncated if long
```
"""

        user_prompt = f"""Please analyze the implementation of "{feature_name}".

## Original PRP

{prp_content}

{test_section}

## Implementation Notes

{implementation_notes}

Please provide:

### Implementation Assessment
- What requirements were met?
- What requirements were missed or changed?
- Quality observations

### Patterns to Promote
- What worked well that should become standard practice?
- Any elegant solutions worth documenting?

### Issues Found
- Bugs or problems discovered
- Edge cases not handled
- Performance concerns

### Recommendations
- Specific improvements for this feature
- Updates needed for project's claude.md
- Suggestions for future PRPs"""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def build_health_check_prompt(
        self,
        features_status: Dict[str, Dict[str, Any]],
        project_profile: ProjectProfile,
        days_since_init: int,
    ) -> List[Dict[str, str]]:
        """
        Build prompt for context health analysis.

        Args:
            features_status: Status of each feature (has_prp, has_validation, etc.)
            project_profile: Project metadata
            days_since_init: Days since CCP was initialized

        Returns:
            Messages for chat completion
        """
        system_prompt = """You are a project manager analyzing the health of a context engineering workspace.

Your role is to:
1. Identify stale or incomplete artifacts
2. Suggest next actions for the team
3. Highlight any concerning patterns
4. Recommend cleanup or updates needed

Be constructive and action-oriented."""

        # Format features status
        status_lines = []
        for feature, status in features_status.items():
            prp_check = "✓" if status.get("has_prp") else "✗"
            val_check = "✓" if status.get("has_validation") else "✗"
            age = status.get("age_days", 0)
            status_lines.append(
                f"- {feature}: PRP {prp_check}, Validation {val_check}, Age: {age} days"
            )

        user_prompt = f"""Please analyze the health of this ContextCraftPro workspace.

## Project Information
- **Name**: {project_profile.name}
- **Days Since Setup**: {days_since_init}
- **Active Features**: {len(features_status)}

## Feature Status
{chr(10).join(status_lines) if status_lines else 'No features found'}

## Analysis Requested

### Overall Health Score
Give a score (1-10) with explanation.

### Stale Artifacts
Which features or files appear abandoned?

### Missing Documentation
What context is incomplete?

### Recommended Actions
1. Immediate priorities
2. Cleanup tasks
3. Documentation updates

### Process Improvements
Suggestions for better context engineering workflow."""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def _format_user_answers(self, answers: Dict[str, str]) -> str:
        """Format user Q&A answers for inclusion in prompt."""
        lines = []
        for question, answer in answers.items():
            lines.append(f"**{question}**")
            lines.append(f"{answer}")
            lines.append("")
        return "\n".join(lines)

    def _format_list(self, items: List[str]) -> str:
        """Format a list for inclusion in prompt."""
        if not items:
            return "None"
        return "\n".join(f"- {item}" for item in items)


class ResponseProcessor:
    """
    Processes and validates LLM responses.

    Extracts structured information from LLM responses and validates
    against expected formats.
    """

    def __init__(self, logger: CCPLogger):
        self.logger = logger

    def extract_markdown_sections(
        self, response: str, expected_sections: List[str]
    ) -> Dict[str, str]:
        """
        Extract expected sections from markdown response.

        Args:
            response: Raw markdown response
            expected_sections: List of section headers to extract

        Returns:
            Dictionary mapping section names to content
        """
        sections = {}
        current_section = None
        current_content = []

        lines = response.split("\n")

        for line in lines:
            # Check if this is a section header
            if line.startswith("#"):
                # Extract header text
                header = line.lstrip("#").strip()

                # Check if it matches an expected section
                for expected in expected_sections:
                    if expected.lower() in header.lower():
                        # Save previous section
                        if current_section:
                            sections[current_section] = "\n".join(
                                current_content
                            ).strip()

                        current_section = expected
                        current_content = []
                        break
            elif current_section:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        # Log missing sections
        missing = [s for s in expected_sections if s not in sections]
        if missing:
            self.logger.warning(
                "Missing expected sections in response",
                missing=missing,
                found=list(sections.keys()),
            )

        return sections

    def validate_prp_structure(self, prp_content: str) -> Dict[str, Any]:
        """
        Validate that PRP has required structure.

        Args:
            prp_content: PRP markdown content

        Returns:
            Validation result with status and details
        """
        required_sections = [
            "Context & Assumptions",
            "Goals and Non-Goals",
            "Ordered Implementation Steps",
            "Implementation Checklist",
            "Validation Plan",
        ]

        sections = self.extract_markdown_sections(prp_content, required_sections)

        # Check each required section
        missing = []
        empty = []

        for section in required_sections:
            if section not in sections:
                missing.append(section)
            elif not sections[section].strip():
                empty.append(section)

        is_valid = len(missing) == 0 and len(empty) == 0

        return {
            "valid": is_valid,
            "missing_sections": missing,
            "empty_sections": empty,
            "sections_found": list(sections.keys()),
            "content": sections,
        }

    def format_feature_spec(self, raw_response: str) -> str:
        """
        Convert LLM response into INITIAL.md format.

        Args:
            raw_response: Raw LLM response

        Returns:
            Formatted feature specification
        """
        # Expected sections for a feature spec
        expected_sections = [
            "Feature Name",
            "Description",
            "User Value",
            "Scope",
            "Key Requirements",
            "Technical Considerations",
            "Open Questions",
        ]

        sections = self.extract_markdown_sections(raw_response, expected_sections)

        # Build formatted specification
        lines = []

        # Add feature name as header
        feature_name = sections.get("Feature Name", "New Feature").strip()
        lines.append(f"## {feature_name}")
        lines.append("")

        # Add each section
        for section in expected_sections[1:]:  # Skip Feature Name as it's the header
            if section in sections and sections[section]:
                lines.append(f"### {section}")
                lines.append("")
                lines.append(sections[section])
                lines.append("")

        # Add metadata
        lines.append("---")
        lines.append(f"*Generated by ContextCraftPro*")
        lines.append("")

        return "\n".join(lines)

    def extract_validation_insights(self, response: str) -> Dict[str, str]:
        """
        Extract insights from validation analysis.

        Args:
            response: Validation analysis from LLM

        Returns:
            Dictionary of insights
        """
        sections_to_extract = [
            "Implementation Assessment",
            "Patterns to Promote",
            "Issues Found",
            "Recommendations",
        ]

        return self.extract_markdown_sections(response, sections_to_extract)

    def extract_health_report(self, response: str) -> Dict[str, Any]:
        """
        Extract health check report details.

        Args:
            response: Health analysis from LLM

        Returns:
            Structured health report
        """
        sections = self.extract_markdown_sections(
            response,
            [
                "Overall Health Score",
                "Stale Artifacts",
                "Missing Documentation",
                "Recommended Actions",
                "Process Improvements",
            ],
        )

        # Try to extract score
        score = None
        score_text = sections.get("Overall Health Score", "")
        if score_text:
            # Look for a number between 1-10
            import re

            match = re.search(r"\b([1-9]|10)\b", score_text)
            if match:
                score = int(match.group(1))

        return {
            "score": score,
            "score_explanation": score_text,
            "stale_artifacts": sections.get("Stale Artifacts", ""),
            "missing_docs": sections.get("Missing Documentation", ""),
            "recommended_actions": sections.get("Recommended Actions", ""),
            "process_improvements": sections.get("Process Improvements", ""),
        }
