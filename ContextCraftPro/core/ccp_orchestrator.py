"""
Core orchestration logic for ContextCraftPro commands

This module contains the business logic for all CCP commands.
"""

import click
import yaml
import re
from pathlib import Path
from typing import Optional
from core.ccp_logger import CCPLogger
from core import ccp_config, ccp_fs, ccp_templates


def init_project(
    ccp_root: Path,
    config_path: Optional[str],
    dry_run: bool,
    auto_yes: bool,
    logger: CCPLogger,
):
    """
    Initialize ContextCraftPro for a project.

    Steps:
    1. Verify layout and determine host root
    2. Check and update .gitignore
    3. Profile the host repository
    4. Seed context files from templates
    5. Initialize configuration
    """
    logger.info("Starting init-project")

    # Step 1: Verify layout
    host_root = ccp_root.parent
    logger.debug(f"CCP root: {ccp_root}")
    logger.debug(f"Host root: {host_root}")

    if not ccp_root.exists():
        raise click.ClickException(f"ContextCraftPro folder not found: {ccp_root}")

    click.echo(f"Initializing ContextCraftPro in: {host_root.name}/")

    # Step 2: Check .gitignore
    gitignore = ccp_fs.GitIgnoreManager(host_root)

    if gitignore.exists():
        if not gitignore.contains_entry("ContextCraftPro/"):
            if auto_yes or click.confirm(
                "\nRecommend adding 'ContextCraftPro/' to .gitignore. Add now?",
                default=True,
            ):
                if not dry_run:
                    gitignore.add_entry(
                        "ContextCraftPro/",
                        comment="ContextCraftPro - disposable context engineering workspace",
                    )
                    logger.info("Added ContextCraftPro/ to .gitignore")
                    click.echo("✓ Added to .gitignore")
                else:
                    click.echo("[DRY RUN] Would add ContextCraftPro/ to .gitignore")
            else:
                click.echo("⚠ Skipped .gitignore update")
        else:
            logger.debug("ContextCraftPro/ already in .gitignore")
            click.echo("✓ Already in .gitignore")
    else:
        click.echo("⚠ No .gitignore found - consider creating one")
        logger.warning("No .gitignore file found in host root")

    # Step 3: Profile the repository
    click.echo("\nProfiling project...")
    scanner = ccp_fs.RepositoryScanner(host_root, max_depth=5)
    profile = scanner.scan()

    logger.info(
        "Project profiled",
        name=profile.name,
        languages=profile.languages,
        frameworks=profile.frameworks,
    )

    click.echo(f"  Name: {profile.name}")
    click.echo(
        f"  Languages: {', '.join(profile.languages) if profile.languages else 'none detected'}"
    )
    click.echo(
        f"  Frameworks: {', '.join(profile.frameworks) if profile.frameworks else 'none detected'}"
    )
    if profile.test_framework:
        click.echo(f"  Tests: {profile.test_framework} ({profile.test_command})")

    # Step 4: Seed context files
    click.echo("\nSetting up context files...")
    fs = ccp_fs.SafeFileSystem(ccp_root, allow_host_read=True)
    template_mgr = ccp_templates.TemplateManager(ccp_root / "templates")

    # Create directories
    dirs_to_create = [
        ccp_root / "context",
        ccp_root / "context" / "examples",
        ccp_root / "context" / "docs-context",
        ccp_root / "context" / "prps",
        ccp_root / "context" / "validation",
        ccp_root / "runtime" / "logs",
        ccp_root / "runtime" / "sessions",
        ccp_root / "config",
    ]

    for directory in dirs_to_create:
        if not dry_run:
            fs.ensure_directory(directory)
            logger.debug(f"Created directory: {directory.relative_to(ccp_root)}")

    # Create project profile YAML
    profile_path = ccp_root / "context" / "project-profile.yaml"
    if (
        not profile_path.exists()
        or auto_yes
        or click.confirm(
            f"\n{profile_path.name} already exists. Overwrite?", default=False
        )
        if profile_path.exists()
        else True
    ):
        profile_data = {
            "name": profile.name,
            "languages": profile.languages,
            "frameworks": profile.frameworks,
            "tests": (
                {"framework": profile.test_framework, "command": profile.test_command}
                if profile.test_framework
                else None
            ),
            "notes": profile.notes,
        }

        if not dry_run:
            with open(profile_path, "w") as f:
                yaml.safe_dump(
                    profile_data, f, default_flow_style=False, sort_keys=False
                )
            logger.info("Created project-profile.yaml")
            click.echo(f"✓ Created {profile_path.relative_to(ccp_root)}")
        else:
            click.echo(f"[DRY RUN] Would create {profile_path.relative_to(ccp_root)}")

    # Create claude.md from template
    claude_path = ccp_root / "context" / "claude.md"
    if not claude_path.exists():
        template_vars = {
            "project_name": profile.name,
            "languages": profile.languages,
            "frameworks": profile.frameworks,
            "test_framework": profile.test_framework or "none",
            "test_command": profile.test_command or "none",
            "architecture_notes": "Add your architecture notes here",
            "common_patterns": "Add common code patterns here",
            "known_issues": "Add known issues here",
        }

        rendered = template_mgr.render_template_file(
            "claude-rules-template", template_vars
        )

        if not dry_run:
            fs.write_file(claude_path, rendered)
            logger.info("Created claude.md")
            click.echo(f"✓ Created {claude_path.relative_to(ccp_root)}")
        else:
            click.echo(f"[DRY RUN] Would create {claude_path.relative_to(ccp_root)}")
    else:
        click.echo(f"⚠ {claude_path.relative_to(ccp_root)} already exists (keeping)")

    # Create INITIAL.md stub
    initial_path = ccp_root / "context" / "INITIAL.md"
    if not initial_path.exists():
        initial_content = "# INITIAL Specifications\n\n<!-- Add feature specifications here using 'ccp new-feature' -->\n"

        if not dry_run:
            fs.write_file(initial_path, initial_content)
            logger.info("Created INITIAL.md")
            click.echo(f"✓ Created {initial_path.relative_to(ccp_root)}")
        else:
            click.echo(f"[DRY RUN] Would create {initial_path.relative_to(ccp_root)}")
    else:
        click.echo(f"⚠ {initial_path.relative_to(ccp_root)} already exists (keeping)")

    # Create docs-index.md
    docs_index_path = ccp_root / "context" / "docs-context" / "docs-index.md"
    if not docs_index_path.exists():
        docs_content = """# Documentation Index

Add links to relevant documentation here to help the LLM find context.

## External Documentation
- [Framework docs](https://example.com)
- [API reference](https://example.com)

## Local Documentation
- `../docs/` - Project documentation
- `../README.md` - Project overview
"""
        if not dry_run:
            fs.write_file(docs_index_path, docs_content)
            logger.info("Created docs-index.md")
            click.echo(f"✓ Created {docs_index_path.relative_to(ccp_root)}")
        else:
            click.echo(
                f"[DRY RUN] Would create {docs_index_path.relative_to(ccp_root)}"
            )

    # Create prp-template.md reference
    prp_template_path = ccp_root / "context" / "prps" / "prp-template.md"
    if not prp_template_path.exists():
        # Copy from templates
        source_template = template_mgr.load_template("prp-template")
        if not dry_run:
            fs.write_file(prp_template_path, source_template)
            logger.info("Created prp-template.md")
            click.echo(f"✓ Created {prp_template_path.relative_to(ccp_root)}")
        else:
            click.echo(
                f"[DRY RUN] Would create {prp_template_path.relative_to(ccp_root)}"
            )

    # Create README.md for the ContextCraftPro folder
    readme_path = ccp_root / "README.md"
    if not readme_path.exists():
        readme_vars = {
            "project_name": profile.name,
            "languages": profile.languages,
            "frameworks": profile.frameworks,
            "test_command": profile.test_command or "pytest",
        }
        rendered_readme = template_mgr.render_template_file(
            "readme-template", readme_vars
        )

        if not dry_run:
            fs.write_file(readme_path, rendered_readme)
            logger.info("Created README.md")
            click.echo(f"✓ Created {readme_path.relative_to(ccp_root)}")
        else:
            click.echo(f"[DRY RUN] Would create {readme_path.relative_to(ccp_root)}")

    # Step 5: Initialize configuration
    click.echo("\nInitializing configuration...")
    config_file_path = ccp_config.get_config_path(ccp_root, custom_path=config_path)

    if not config_file_path.exists():
        default_config = ccp_config.create_default_config(ccp_root)
        if not dry_run:
            ccp_config.save_config(default_config, config_file_path)
            logger.info("Created contextcraft.yaml")
            click.echo(f"✓ Created {config_file_path.relative_to(ccp_root)}")
        else:
            click.echo(
                f"[DRY RUN] Would create {config_file_path.relative_to(ccp_root)}"
            )
    else:
        click.echo(
            f"⚠ {config_file_path.relative_to(ccp_root)} already exists (keeping)"
        )
        logger.info("Configuration already exists")

    # Success!
    click.echo("\n" + "=" * 60)
    click.echo("✓ ContextCraftPro initialized successfully!")
    click.echo("=" * 60)
    click.echo("\nNext steps:")
    click.echo("  1. Review and edit context/claude.md with project-specific rules")
    click.echo("  2. Run 'python ccp.py new-feature' to define your first feature")
    click.echo("  3. Run 'python ccp.py generate-prp --feature <name>' to create a PRP")
    click.echo("\nFor help: python ccp.py --help")

    logger.info("init-project completed successfully")


def new_feature(
    ccp_root: Path,
    config_path: Optional[str],
    feature_slug: Optional[str],
    dry_run: bool,
    logger: CCPLogger,
):
    """
    Create a new feature specification through interactive Q&A.

    Steps:
    1. Interactive questions about the feature
    2. Optional LLM refinement of answers
    3. Write to INITIAL.md or feature-specific file
    """
    logger.info("Starting new-feature command", feature_slug=feature_slug)

    click.echo("✨ Creating New Feature Specification")
    click.echo("=" * 60)

    # Load configuration
    config = ccp_config.load_config(ccp_config.get_config_path(ccp_root, config_path))

    # Interactive Q&A
    questions = [
        (
            "What feature are you building?",
            "Describe the feature in 1-2 sentences. Be specific about what it does.",
        ),
        (
            "Why does this feature matter?",
            "What user problem does it solve? What value does it provide?",
        ),
        ("What's the scope?", "What's included? What's explicitly NOT included?"),
        (
            "Any technical constraints?",
            "Specific technologies, performance requirements, compatibility needs?",
        ),
        (
            "Related components?",
            "What existing code will this interact with or modify?",
        ),
        (
            "Known challenges?",
            "Any tricky parts, edge cases, or potential issues to watch for?",
        ),
    ]

    answers = {}
    click.echo("\nPlease answer these questions about your feature:\n")

    for question, hint in questions:
        click.echo(f"📝 {question}")
        click.echo(f"   {click.style(hint, fg='bright_black')}")
        answer = click.prompt("   ", type=str, default="", show_default=False)
        if answer.strip():
            answers[question] = answer.strip()
        click.echo()

    # Check if we have enough information
    if len(answers) < 3:
        click.echo(
            "⚠️  Not enough information provided. Please answer at least 3 questions."
        )
        return

    # Load project profile
    profile_path = ccp_root / "context" / "project-profile.yaml"
    if profile_path.exists():
        with open(profile_path) as f:
            profile_data = yaml.safe_load(f)
            profile = ccp_fs.ProjectProfile(
                name=profile_data.get("name", "Unknown"),
                languages=profile_data.get("languages", []),
                frameworks=profile_data.get("frameworks", []),
                test_framework=(
                    profile_data.get("tests", {}).get("framework")
                    if isinstance(profile_data.get("tests"), dict)
                    else None
                ),
                test_command=(
                    profile_data.get("tests", {}).get("command")
                    if isinstance(profile_data.get("tests"), dict)
                    else None
                ),
                notes=profile_data.get("notes", ""),
            )
    else:
        profile = ccp_fs.ProjectProfile(name="Project", languages=[], frameworks=[])

    # Get existing features
    initial_path = ccp_root / "context" / "INITIAL.md"
    existing_features = []
    if initial_path.exists():
        content = initial_path.read_text()
        # Extract feature names (look for ## headers)
        import re

        features = re.findall(r"^## (.+)$", content, re.MULTILINE)
        existing_features = [f for f in features if f != "INITIAL Specifications"]

    # Ask if user wants LLM refinement
    use_llm = False
    if config.behavior.get("enable_refinement", True):
        use_llm = click.confirm(
            "\nWould you like to use LLM to refine and structure your answers?",
            default=True,
        )

    feature_content = ""

    if use_llm:
        click.echo("\n🤖 Refining feature specification with LLM...")

        try:
            # Import LLM modules
            from core.ccp_llm import FoundryLocalClient
            from core.ccp_prompts import PromptBuilder, ResponseProcessor

            # Initialize LLM client
            llm_client = FoundryLocalClient(config.foundry_local, logger)
            prompt_builder = PromptBuilder(logger)
            response_processor = ResponseProcessor(logger)

            # Build prompt
            messages = prompt_builder.build_new_feature_prompt(
                user_answers=answers,
                project_profile=profile,
                existing_features=existing_features,
            )

            # Call LLM
            response = llm_client.chat_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                feature_context="new-feature",
            )

            if response.success:
                # Process response
                feature_content = response_processor.format_feature_spec(
                    response.content
                )
                click.echo("✓ Feature specification refined successfully")
            else:
                click.echo(f"⚠️  LLM refinement failed: {response.error_message}")
                click.echo("Falling back to template format...")

        except Exception as e:
            logger.error("Failed to use LLM for refinement", error=str(e))
            click.echo(f"⚠️  LLM error: {e}")
            click.echo("Falling back to template format...")

    # If no LLM or LLM failed, use template format
    if not feature_content:
        # Build feature spec from template
        feature_name = answers.get("What feature are you building?", "New Feature")[:50]

        lines = [
            f"## {feature_name}",
            "",
            "### Description",
            "",
            answers.get("What feature are you building?", ""),
            "",
            "### User Value",
            "",
            answers.get("Why does this feature matter?", "Not specified"),
            "",
            "### Scope",
            "",
            answers.get("What's the scope?", "Not specified"),
            "",
            "### Key Requirements",
            "",
        ]

        # Add requirements as bullet points
        if "What feature are you building?" in answers:
            lines.append(f"- {answers['What feature are you building?']}")
        if "Any technical constraints?" in answers:
            lines.append(f"- {answers['Any technical constraints?']}")

        lines.extend(
            [
                "",
                "### Technical Considerations",
                "",
                answers.get("Any technical constraints?", "None specified"),
                "",
                f"**Related Components:** {answers.get('Related components?', 'None specified')}",
                "",
                f"**Known Challenges:** {answers.get('Known challenges?', 'None specified')}",
                "",
                "### Open Questions",
                "",
                "- [Add any questions that need answers]",
                "",
                "---",
                "*Generated by ContextCraftPro*",
                "",
            ]
        )

        feature_content = "\n".join(lines)

    # Display the specification
    click.echo("\n" + "=" * 60)
    click.echo("📋 Generated Feature Specification:")
    click.echo("=" * 60)
    click.echo(feature_content)
    click.echo("=" * 60)

    # Ask for confirmation
    if not dry_run:
        save = click.confirm("\nSave this specification to INITIAL.md?", default=True)

        if save:
            # Append to INITIAL.md
            initial_path = ccp_root / "context" / "INITIAL.md"

            if initial_path.exists():
                existing_content = initial_path.read_text()
                if not existing_content.endswith("\n\n"):
                    existing_content += "\n\n"
                new_content = existing_content + feature_content
            else:
                new_content = "# INITIAL Specifications\n\n" + feature_content

            fs = ccp_fs.SafeFileSystem(ccp_root)
            fs.write_file(initial_path, new_content)

            click.echo(
                f"✓ Feature specification saved to {initial_path.relative_to(ccp_root)}"
            )
            logger.info("Feature specification saved", path=str(initial_path))

            # Suggest next steps
            click.echo("\n" + "=" * 60)
            click.echo("✨ Feature specification created successfully!")
            click.echo("=" * 60)
            click.echo("\nNext steps:")
            click.echo("  1. Review and refine the specification in context/INITIAL.md")
            click.echo("  2. Run 'python ccp.py generate-prp' to create a PRP")
            click.echo("  3. Use the PRP with Claude Code to implement the feature")
        else:
            click.echo("Feature specification not saved.")
    else:
        click.echo("\n[DRY RUN] Would save to context/INITIAL.md")

    logger.info("new-feature command completed")


def generate_prp(
    ccp_root: Path,
    config_path: Optional[str],
    feature_slug: str,
    dry_run: bool,
    logger: CCPLogger,
):
    """
    Generate a Product Requirements Prompt for a feature.

    Steps:
    1. Load context (project profile, claude.md, feature spec, examples, docs)
    2. Build comprehensive prompt
    3. Call LLM to generate PRP
    4. Validate PRP structure
    5. Display for human review
    6. Save to context/prps/<feature-slug>.md
    """
    logger.info("Starting generate-prp", feature=feature_slug)

    click.echo("🎯 Generating Product Requirements Prompt")
    click.echo("=" * 60)
    click.echo(f"Feature: {feature_slug}\n")

    # Load configuration
    config = ccp_config.load_config(ccp_config.get_config_path(ccp_root, config_path))

    # Step 1: Gather context
    click.echo("📚 Gathering context...")

    # Load project profile
    profile_path = ccp_root / "context" / "project-profile.yaml"
    if not profile_path.exists():
        click.echo("⚠️  No project profile found. Run 'init-project' first.")
        logger.error("Project profile not found")
        return

    with open(profile_path) as f:
        profile_data = yaml.safe_load(f)
        profile = ccp_fs.ProjectProfile(
            name=profile_data.get("name", "Unknown"),
            languages=profile_data.get("languages", []),
            frameworks=profile_data.get("frameworks", []),
            test_framework=(
                profile_data.get("tests", {}).get("framework")
                if isinstance(profile_data.get("tests"), dict)
                else None
            ),
            test_command=(
                profile_data.get("tests", {}).get("command")
                if isinstance(profile_data.get("tests"), dict)
                else None
            ),
            notes=profile_data.get("notes", ""),
        )

    click.echo(f"  ✓ Project: {profile.name}")

    # Load claude.md rules
    claude_rules_path = ccp_root / "context" / "claude.md"
    claude_rules = ""
    if claude_rules_path.exists():
        claude_rules = claude_rules_path.read_text()
        click.echo(f"  ✓ Coding rules: {len(claude_rules)} chars")
    else:
        click.echo("  ⚠️  No claude.md found")

    # Load feature spec from INITIAL.md
    initial_path = ccp_root / "context" / "INITIAL.md"
    feature_spec = ""

    if not initial_path.exists():
        click.echo(
            "⚠️  No INITIAL.md found. Create a feature spec with 'new-feature' first."
        )
        logger.error("INITIAL.md not found")
        return

    initial_content = initial_path.read_text()

    # Extract the specific feature section
    # Look for ## {feature_slug} or similar
    feature_pattern = rf"^## .*{re.escape(feature_slug)}.*$"
    match = re.search(feature_pattern, initial_content, re.MULTILINE | re.IGNORECASE)

    if match:
        # Extract from this header to the next ## or end of file
        start_pos = match.start()
        next_header = re.search(
            r"^## ", initial_content[start_pos + len(match.group()) :], re.MULTILINE
        )

        if next_header:
            end_pos = start_pos + len(match.group()) + next_header.start()
            feature_spec = initial_content[start_pos:end_pos].strip()
        else:
            feature_spec = initial_content[start_pos:].strip()

        click.echo(f"  ✓ Feature spec: {len(feature_spec)} chars")
    else:
        # Feature not found, use entire INITIAL.md content
        click.echo(
            f"  ⚠️  Specific feature '{feature_slug}' not found, using entire INITIAL.md"
        )
        feature_spec = initial_content

    if not feature_spec:
        click.echo("⚠️  Feature specification is empty")
        logger.error("Empty feature specification")
        return

    # Load examples
    examples_dir = ccp_root / "context" / "examples"
    examples = []
    if examples_dir.exists():
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            examples.append(f"## {example_file.stem}\n\n{content}")

        if examples:
            click.echo(f"  ✓ Examples: {len(examples)} files")
        else:
            click.echo("  ⚠️  No examples found")
    else:
        click.echo("  ⚠️  No examples directory")

    # Load docs context
    docs_dir = ccp_root / "context" / "docs-context"
    docs_context = ""
    if docs_dir.exists():
        docs_index = docs_dir / "docs-index.md"
        if docs_index.exists():
            docs_context = docs_index.read_text()
            click.echo(f"  ✓ Documentation index: {len(docs_context)} chars")
        else:
            click.echo("  ⚠️  No docs-index.md found")
    else:
        click.echo("  ⚠️  No docs-context directory")

    # Step 2: Build prompt and call LLM
    click.echo("\n🤖 Generating PRP with LLM...")

    try:
        from core.ccp_llm import FoundryLocalClient
        from core.ccp_prompts import PromptBuilder, ResponseProcessor

        llm_client = FoundryLocalClient(config.foundry_local, logger)
        prompt_builder = PromptBuilder(logger)
        response_processor = ResponseProcessor(logger)

        # Test connection first
        click.echo("  Testing Foundry Local connection...")
        if not llm_client.test_connection():
            click.echo(
                "⚠️  Cannot connect to Foundry Local. Please ensure it's running."
            )
            click.echo(f"   Endpoint: {config.foundry_local.endpoint}")
            logger.error("LLM connection test failed")
            return

        click.echo("  ✓ Connected to Foundry Local")

        # Build prompt
        messages = prompt_builder.build_generate_prp_prompt(
            feature_spec=feature_spec,
            project_profile=profile,
            claude_rules=claude_rules,
            examples=examples[:3],  # Limit to 3 examples to save tokens
            docs_context=docs_context,
        )

        click.echo(f"  Sending request (temperature=0.7)...")

        # Call LLM
        response = llm_client.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=4000,
            feature_context=f"generate-prp:{feature_slug}",
        )

        if not response.success:
            click.echo(f"\n⚠️  LLM generation failed: {response.error_message}")
            logger.error("LLM generation failed", error=response.error_message)
            return

        click.echo(f"  ✓ Generated in {response.latency_ms}ms")
        if response.usage:
            click.echo(f"  Tokens: {response.usage.get('total_tokens', 'unknown')}")

        prp_content = response.content

        # Step 3: Validate PRP structure
        click.echo("\n🔍 Validating PRP structure...")
        validation = response_processor.validate_prp_structure(prp_content)

        if validation["valid"]:
            click.echo("  ✓ All required sections present")
        else:
            click.echo("  ⚠️  PRP structure issues:")
            if validation["missing_sections"]:
                click.echo(f"     Missing: {', '.join(validation['missing_sections'])}")
            if validation["empty_sections"]:
                click.echo(f"     Empty: {', '.join(validation['empty_sections'])}")

            # Continue anyway but warn
            proceed = click.confirm("\n  Continue with incomplete PRP?", default=True)
            if not proceed:
                click.echo("PRP generation cancelled.")
                return

        # Step 4: Display for review
        click.echo("\n" + "=" * 60)
        click.echo("📋 Generated PRP:")
        click.echo("=" * 60)
        click.echo(prp_content)
        click.echo("=" * 60)

        # Step 5: Save if approved
        if not dry_run:
            save = click.confirm("\nSave this PRP?", default=True)

            if save:
                # Ensure prps directory exists
                prps_dir = ccp_root / "context" / "prps"
                fs = ccp_fs.SafeFileSystem(ccp_root)
                fs.ensure_directory(prps_dir)

                # Sanitize feature slug for filename
                safe_slug = re.sub(r"[^a-zA-Z0-9_-]", "-", feature_slug.lower())
                prp_path = prps_dir / f"{safe_slug}.md"

                # Check if file exists
                if prp_path.exists():
                    overwrite = click.confirm(
                        f"\n⚠️  PRP already exists: {prp_path.name}. Overwrite?",
                        default=False,
                    )
                    if not overwrite:
                        click.echo("PRP not saved.")
                        return

                # Write PRP with metadata header
                prp_with_header = f"""# Product Requirements Prompt: {feature_slug}

**Generated:** {click.get_current_context().obj.get('timestamp', 'Unknown') if hasattr(click, 'get_current_context') else 'N/A'}
**Project:** {profile.name}

---

{prp_content}
"""

                fs.write_file(prp_path, prp_with_header)

                click.echo(f"\n✓ PRP saved to {prp_path.relative_to(ccp_root)}")
                logger.info("PRP saved", path=str(prp_path), feature=feature_slug)

                # Next steps
                click.echo("\n" + "=" * 60)
                click.echo("✨ PRP generated successfully!")
                click.echo("=" * 60)
                click.echo("\nNext steps:")
                click.echo(f"  1. Review the PRP in {prp_path.relative_to(ccp_root)}")
                click.echo("  2. Use the PRP with Claude Code to implement the feature")
                click.echo(
                    "  3. Run 'python ccp.py validate <feature>' after implementation"
                )
            else:
                click.echo("PRP not saved.")
        else:
            click.echo(f"\n[DRY RUN] Would save to context/prps/{safe_slug}.md")

    except ImportError as e:
        logger.error("Failed to import LLM modules", error=str(e))
        click.echo(f"⚠️  Import error: {e}")
    except Exception as e:
        logger.error(
            "Unexpected error during PRP generation", error=str(e), exc_info=True
        )
        click.echo(f"⚠️  Unexpected error: {e}")
        raise

    logger.info("generate-prp completed", feature=feature_slug)


def validate(
    ccp_root: Path,
    config_path: Optional[str],
    feature_slug: str,
    tests_command: Optional[str],
    skip_tests: bool,
    dry_run: bool,
    logger: CCPLogger,
):
    """
    Validate implementation against PRP.

    Steps:
    1. Load the PRP for the feature
    2. Optionally run tests in host repo
    3. Collect user feedback on implementation
    4. Use LLM to analyze validation
    5. Save validation report
    """
    logger.info("Starting validate", feature=feature_slug)

    click.echo("✅ Validating Feature Implementation")
    click.echo("=" * 60)
    click.echo(f"Feature: {feature_slug}\n")

    # Load configuration
    config = ccp_config.load_config(ccp_config.get_config_path(ccp_root, config_path))

    # Step 1: Load PRP
    click.echo("📚 Loading PRP...")
    safe_slug = re.sub(r"[^a-zA-Z0-9_-]", "-", feature_slug.lower())
    prp_path = ccp_root / "context" / "prps" / f"{safe_slug}.md"

    if not prp_path.exists():
        click.echo(f"⚠️  No PRP found for '{feature_slug}'")
        click.echo(f"   Expected: {prp_path.relative_to(ccp_root)}")
        click.echo(
            "\n   Generate a PRP first with: python ccp.py generate-prp <feature>"
        )
        logger.error("PRP not found", feature=feature_slug)
        return

    prp_content = prp_path.read_text()
    click.echo(f"  ✓ Loaded PRP: {prp_path.name}")

    # Step 2: Run tests (optional)
    test_output = None
    test_passed = None

    if not skip_tests:
        click.echo("\n🧪 Running tests...")

        # Determine test command
        if tests_command:
            cmd = tests_command
        else:
            # Try to get from project profile
            profile_path = ccp_root / "context" / "project-profile.yaml"
            if profile_path.exists():
                with open(profile_path) as f:
                    profile_data = yaml.safe_load(f)
                    tests_data = profile_data.get("tests")
                    if isinstance(tests_data, dict):
                        cmd = tests_data.get("command")
                    else:
                        cmd = None
            else:
                cmd = None

        if cmd:
            click.echo(f"  Running: {cmd}")
            host_root = ccp_root.parent

            try:
                import subprocess

                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=host_root,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minute timeout
                )

                test_output = f"Exit code: {result.returncode}\n\n"
                test_output += f"STDOUT:\n{result.stdout}\n\n"
                test_output += f"STDERR:\n{result.stderr}"

                test_passed = result.returncode == 0

                if test_passed:
                    click.echo("  ✓ Tests passed")
                else:
                    click.echo(f"  ✗ Tests failed (exit code {result.returncode})")

            except subprocess.TimeoutExpired:
                click.echo("  ⚠️  Tests timed out (5 minute limit)")
                test_output = "Tests timed out after 5 minutes"
                test_passed = False
            except Exception as e:
                click.echo(f"  ⚠️  Error running tests: {e}")
                test_output = f"Error running tests: {e}"
                test_passed = False
        else:
            click.echo("  ⚠️  No test command configured, skipping tests")
    else:
        click.echo("\n⏭️  Skipping tests (--skip-tests)")

    # Step 3: Collect user feedback
    click.echo("\n📝 Implementation Feedback")
    click.echo("-" * 60)

    questions = [
        ("Did the implementation satisfy the PRP requirements?", "yes/no/partial"),
        ("What worked well?", "Patterns, approaches, or solutions worth repeating"),
        ("What broke or didn't work?", "Bugs, issues, or unexpected problems"),
        (
            "What would you change for next time?",
            "Improvements to the PRP or implementation approach",
        ),
    ]

    feedback = {}
    for question, hint in questions:
        click.echo(f"\n{question}")
        click.echo(click.style(f"  ({hint})", fg="bright_black"))
        answer = click.prompt("  ", type=str, default="", show_default=False)
        if answer.strip():
            feedback[question] = answer.strip()

    if not feedback:
        click.echo("\n⚠️  No feedback provided. Validation report will be minimal.")

    # Step 4: Generate validation analysis with LLM
    validation_content = ""

    use_llm = click.confirm("\nUse LLM to analyze validation?", default=True)

    if use_llm:
        click.echo("\n🤖 Analyzing validation with LLM...")

        try:
            from core.ccp_llm import FoundryLocalClient
            from core.ccp_prompts import PromptBuilder, ResponseProcessor

            llm_client = FoundryLocalClient(config.foundry_local, logger)
            prompt_builder = PromptBuilder(logger)
            response_processor = ResponseProcessor(logger)

            # Build implementation notes from feedback
            implementation_notes = "\n\n".join(
                [f"**{q}**\n{a}" for q, a in feedback.items()]
            )

            # Build prompt
            messages = prompt_builder.build_validate_prompt(
                feature_name=feature_slug,
                prp_content=prp_content,
                test_output=test_output,
                implementation_notes=implementation_notes,
            )

            # Call LLM
            response = llm_client.chat_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=3000,
                feature_context=f"validate:{feature_slug}",
            )

            if response.success:
                validation_content = response.content
                click.echo(f"  ✓ Analysis complete ({response.latency_ms}ms)")
            else:
                click.echo(f"  ⚠️  LLM analysis failed: {response.error_message}")
                validation_content = None

        except Exception as e:
            logger.error("LLM validation analysis failed", error=str(e))
            click.echo(f"  ⚠️  Error: {e}")
            validation_content = None

    # If no LLM analysis, create basic report
    if not validation_content:
        sections = []

        sections.append("## Implementation Assessment\n")
        if feedback:
            for question, answer in feedback.items():
                sections.append(f"**{question}**\n{answer}\n")
        else:
            sections.append("No feedback provided.\n")

        if test_output:
            sections.append("\n## Test Results\n")
            sections.append(
                f"**Status:** {'✓ Passed' if test_passed else '✗ Failed'}\n"
            )
            sections.append(f"\n```\n{test_output[:1000]}\n```\n")

        validation_content = "\n".join(sections)

    # Step 5: Display and save validation report
    click.echo("\n" + "=" * 60)
    click.echo("📋 Validation Report:")
    click.echo("=" * 60)
    click.echo(validation_content)
    click.echo("=" * 60)

    if not dry_run:
        save = click.confirm("\nSave validation report?", default=True)

        if save:
            # Ensure validation directory exists
            validation_dir = ccp_root / "context" / "validation"
            fs = ccp_fs.SafeFileSystem(ccp_root)
            fs.ensure_directory(validation_dir)

            # Generate timestamp
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            validation_path = validation_dir / f"{safe_slug}.md"

            # Build full report with metadata
            full_report = f"""# Validation Report: {feature_slug}

**Date:** {timestamp}
**Tests:** {'✓ Passed' if test_passed else '✗ Failed' if test_passed is False else 'Not run'}

---

{validation_content}

---

## Original PRP

See: `{prp_path.relative_to(ccp_root)}`
"""

            fs.write_file(validation_path, full_report)

            click.echo(
                f"\n✓ Validation report saved to {validation_path.relative_to(ccp_root)}"
            )
            logger.info(
                "Validation report saved",
                path=str(validation_path),
                feature=feature_slug,
            )

            # Suggest next steps
            click.echo("\n" + "=" * 60)
            click.echo("✨ Validation complete!")
            click.echo("=" * 60)
            click.echo("\nNext steps:")
            click.echo("  1. Review insights in the validation report")
            click.echo("  2. Update context/claude.md with any new patterns")
            click.echo("  3. Consider creating examples for successful approaches")
            click.echo(
                "  4. Run 'python ccp.py health' to check overall context health"
            )
        else:
            click.echo("Validation report not saved.")
    else:
        click.echo(f"\n[DRY RUN] Would save to context/validation/{safe_slug}.md")

    logger.info("validate completed", feature=feature_slug)


def health(
    ccp_root: Path,
    config_path: Optional[str],
    generate_report: bool,
    dry_run: bool,
    logger: CCPLogger,
):
    """
    Check context health.

    Steps:
    1. Scan features, PRPs, and validation reports
    2. Calculate health metrics
    3. Optionally use LLM for insights
    4. Display and save health report
    """
    logger.info("Starting health check")

    click.echo("🏥 Context Health Check")
    click.echo("=" * 60)

    # Load configuration
    config = ccp_config.load_config(ccp_config.get_config_path(ccp_root, config_path))

    # Calculate initialization date
    from datetime import datetime

    init_marker = ccp_root / "context" / "project-profile.yaml"
    if init_marker.exists():
        init_time = datetime.fromtimestamp(init_marker.stat().st_mtime)
        days_since_init = (datetime.now() - init_time).days
        click.echo(f"Workspace age: {days_since_init} days\n")
    else:
        days_since_init = 0
        click.echo("⚠️  Project not initialized\n")

    # Scan features
    click.echo("📊 Scanning context artifacts...\n")

    features_status = {}

    # Extract features from INITIAL.md
    initial_path = ccp_root / "context" / "INITIAL.md"
    if initial_path.exists():
        content = initial_path.read_text()
        feature_headers = re.findall(r"^## (.+)$", content, re.MULTILINE)
        features = [f for f in feature_headers if f != "INITIAL Specifications"]

        for feature in features:
            safe_slug = re.sub(r"[^a-zA-Z0-9_-]", "-", feature.lower())
            features_status[feature] = {
                "slug": safe_slug,
                "has_spec": True,
                "has_prp": False,
                "has_validation": False,
                "age_days": 0,
            }

        click.echo(f"  Features in INITIAL.md: {len(features)}")
    else:
        click.echo("  ⚠️  No INITIAL.md found")

    # Check for PRPs
    prps_dir = ccp_root / "context" / "prps"
    prp_count = 0
    if prps_dir.exists():
        for prp_file in prps_dir.glob("*.md"):
            if prp_file.name == "prp-template.md":
                continue

            prp_count += 1
            slug = prp_file.stem

            # Find matching feature
            matched = False
            for feature, status in features_status.items():
                if status["slug"] == slug:
                    status["has_prp"] = True
                    status["age_days"] = (
                        datetime.now()
                        - datetime.fromtimestamp(prp_file.stat().st_mtime)
                    ).days
                    matched = True
                    break

            if not matched:
                # PRP without feature spec
                features_status[f"[{slug}]"] = {
                    "slug": slug,
                    "has_spec": False,
                    "has_prp": True,
                    "has_validation": False,
                    "age_days": (
                        datetime.now()
                        - datetime.fromtimestamp(prp_file.stat().st_mtime)
                    ).days,
                }

        click.echo(f"  PRPs found: {prp_count}")
    else:
        click.echo("  ⚠️  No PRPs directory")

    # Check for validation reports
    validation_dir = ccp_root / "context" / "validation"
    validation_count = 0
    if validation_dir.exists():
        for val_file in validation_dir.glob("*.md"):
            validation_count += 1
            slug = val_file.stem

            # Find matching feature
            for feature, status in features_status.items():
                if status["slug"] == slug:
                    status["has_validation"] = True
                    break

        click.echo(f"  Validation reports: {validation_count}")
    else:
        click.echo("  ⚠️  No validation directory")

    # Display feature status
    click.echo("\n📋 Feature Status:\n")

    if not features_status:
        click.echo("  No features found")
    else:
        for feature, status in features_status.items():
            spec_icon = "📄" if status["has_spec"] else "  "
            prp_icon = "📝" if status["has_prp"] else "  "
            val_icon = "✅" if status["has_validation"] else "  "

            click.echo(f"  {spec_icon} {prp_icon} {val_icon}  {feature}")
            if status["age_days"] > 0:
                click.echo(f"      (Last updated: {status['age_days']} days ago)")

        click.echo("\nLegend: 📄 Spec  📝 PRP  ✅ Validated")

    # Calculate health score
    total_features = len(features_status)
    features_with_prp = sum(1 for s in features_status.values() if s["has_prp"])
    features_validated = sum(1 for s in features_status.values() if s["has_validation"])

    if total_features > 0:
        completeness = (
            (features_with_prp + features_validated) / (total_features * 2)
        ) * 100
    else:
        completeness = 0

    click.echo(f"\n📊 Health Metrics:")
    click.echo(f"  Total features: {total_features}")
    click.echo(f"  With PRPs: {features_with_prp}/{total_features}")
    click.echo(f"  Validated: {features_validated}/{total_features}")
    click.echo(f"  Completeness: {completeness:.0f}%")

    # Identify issues
    issues = []
    if total_features == 0:
        issues.append("No features defined - start with 'new-feature'")

    incomplete_features = [
        f for f, s in features_status.items() if s["has_spec"] and not s["has_prp"]
    ]
    if incomplete_features:
        issues.append(f"{len(incomplete_features)} feature(s) need PRPs")

    unvalidated = [
        f
        for f, s in features_status.items()
        if s["has_prp"] and not s["has_validation"]
    ]
    if unvalidated:
        issues.append(f"{len(unvalidated)} feature(s) need validation")

    stale_features = [f for f, s in features_status.items() if s["age_days"] > 30]
    if stale_features:
        issues.append(
            f"{len(stale_features)} feature(s) haven't been updated in 30+ days"
        )

    if issues:
        click.echo("\n⚠️  Issues:")
        for issue in issues:
            click.echo(f"  • {issue}")
    else:
        click.echo("\n✨ No issues found!")

    # Optional LLM analysis
    health_report = None

    if generate_report:
        use_llm = click.confirm(
            "\nGenerate detailed health report with LLM?", default=True
        )

        if use_llm:
            click.echo("\n🤖 Generating health analysis...")

            try:
                from core.ccp_llm import FoundryLocalClient
                from core.ccp_prompts import PromptBuilder, ResponseProcessor

                # Load project profile
                profile_path = ccp_root / "context" / "project-profile.yaml"
                if profile_path.exists():
                    with open(profile_path) as f:
                        profile_data = yaml.safe_load(f)
                        profile = ccp_fs.ProjectProfile(
                            name=profile_data.get("name", "Unknown"),
                            languages=profile_data.get("languages", []),
                            frameworks=profile_data.get("frameworks", []),
                            test_framework=(
                                profile_data.get("tests", {}).get("framework")
                                if isinstance(profile_data.get("tests"), dict)
                                else None
                            ),
                            test_command=(
                                profile_data.get("tests", {}).get("command")
                                if isinstance(profile_data.get("tests"), dict)
                                else None
                            ),
                            notes=profile_data.get("notes", ""),
                        )
                else:
                    profile = ccp_fs.ProjectProfile(
                        name="Unknown", languages=[], frameworks=[]
                    )

                llm_client = FoundryLocalClient(config.foundry_local, logger)
                prompt_builder = PromptBuilder(logger)
                response_processor = ResponseProcessor(logger)

                # Build prompt
                messages = prompt_builder.build_health_check_prompt(
                    features_status=features_status,
                    project_profile=profile,
                    days_since_init=days_since_init,
                )

                # Call LLM
                response = llm_client.chat_completion(
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000,
                    feature_context="health-check",
                )

                if response.success:
                    health_report = response.content
                    click.echo(f"  ✓ Analysis complete ({response.latency_ms}ms)")

                    # Display report
                    click.echo("\n" + "=" * 60)
                    click.echo("📋 Health Analysis:")
                    click.echo("=" * 60)
                    click.echo(health_report)
                    click.echo("=" * 60)
                else:
                    click.echo(f"  ⚠️  LLM analysis failed: {response.error_message}")

            except Exception as e:
                logger.error("Health check LLM analysis failed", error=str(e))
                click.echo(f"  ⚠️  Error: {e}")

        # Save health report
        if health_report and not dry_run:
            save = click.confirm("\nSave health report?", default=True)

            if save:
                reports_dir = ccp_root / "context"
                fs = ccp_fs.SafeFileSystem(ccp_root)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                report_content = f"""# Context Health Report

**Generated:** {timestamp}
**Workspace Age:** {days_since_init} days
**Completeness:** {completeness:.0f}%

## Summary

- Total features: {total_features}
- With PRPs: {features_with_prp}/{total_features}
- Validated: {features_validated}/{total_features}

## Feature Status

"""
                for feature, status in features_status.items():
                    report_content += f"- **{feature}**: "
                    report_content += f"Spec {'✓' if status['has_spec'] else '✗'}, "
                    report_content += f"PRP {'✓' if status['has_prp'] else '✗'}, "
                    report_content += (
                        f"Validated {'✓' if status['has_validation'] else '✗'}"
                    )
                    if status["age_days"] > 0:
                        report_content += f" ({status['age_days']} days old)"
                    report_content += "\n"

                if issues:
                    report_content += "\n## Issues\n\n"
                    for issue in issues:
                        report_content += f"- {issue}\n"

                if health_report:
                    report_content += f"\n## Detailed Analysis\n\n{health_report}\n"

                report_path = reports_dir / "health-report.md"
                fs.write_file(report_path, report_content)

                click.echo(
                    f"\n✓ Health report saved to {report_path.relative_to(ccp_root)}"
                )
                logger.info("Health report saved", path=str(report_path))

    # Summary
    click.echo("\n" + "=" * 60)
    click.echo("✨ Health check complete!")
    click.echo("=" * 60)

    if incomplete_features:
        click.echo("\n💡 Next steps:")
        click.echo("  Generate PRPs for incomplete features:")
        for feature in incomplete_features[:3]:  # Show first 3
            safe_slug = features_status[feature]["slug"]
            click.echo(f"    python ccp.py generate-prp {safe_slug}")

    logger.info("health check completed")


def export(
    ccp_root: Path,
    config_path: Optional[str],
    target: str,
    auto_yes: bool,
    dry_run: bool,
    logger: CCPLogger,
):
    """
    Export artifacts to host repository.

    Steps:
    1. Determine what to export based on target
    2. Check safety (confirm overwrites, check paths)
    3. Copy files to host repository
    4. Log exports
    """
    logger.info("Starting export", target=target)

    click.echo("📤 Exporting Context Artifacts")
    click.echo("=" * 60)

    # Load configuration
    config = ccp_config.load_config(ccp_config.get_config_path(ccp_root, config_path))

    host_root = ccp_root.parent

    # Determine export target
    valid_targets = ["docs", "readme", "all"]
    if target not in valid_targets:
        click.echo(f"⚠️  Invalid target: '{target}'")
        click.echo(f"   Valid targets: {', '.join(valid_targets)}")
        return

    click.echo(f"Target: {target}")
    click.echo(f"Host repository: {host_root.name}/\n")

    # Safety check - ensure we're not overwriting critical files
    if config.behavior.confirm_exports and not auto_yes:
        click.echo("⚠️  This will write files outside ContextCraftPro/")
        proceed = click.confirm("Continue?", default=False)
        if not proceed:
            click.echo("Export cancelled.")
            return

    # Collect files to export
    exports = []

    if target == "docs" or target == "all":
        # Export documentation
        click.echo("📚 Preparing documentation export...\n")

        docs_to_export = [
            ("context/claude.md", "docs/CLAUDE_RULES.md", "AI coding rules"),
            ("context/INITIAL.md", "docs/FEATURES.md", "Feature specifications"),
        ]

        # Add PRPs if they exist
        prps_dir = ccp_root / "context" / "prps"
        if prps_dir.exists():
            for prp_file in prps_dir.glob("*.md"):
                if prp_file.name != "prp-template.md":
                    dest = f"docs/prps/{prp_file.name}"
                    exports.append(
                        (
                            str(prp_file.relative_to(ccp_root)),
                            dest,
                            f"PRP: {prp_file.stem}",
                        )
                    )

        # Add validation reports if they exist
        val_dir = ccp_root / "context" / "validation"
        if val_dir.exists():
            for val_file in val_dir.glob("*.md"):
                dest = f"docs/validation/{val_file.name}"
                exports.append(
                    (
                        str(val_file.relative_to(ccp_root)),
                        dest,
                        f"Validation: {val_file.stem}",
                    )
                )

        for source, dest, description in docs_to_export:
            source_path = ccp_root / source
            if source_path.exists():
                exports.append((source, dest, description))
            else:
                click.echo(f"  ⚠️  Skipping {source} (not found)")

    if target == "readme" or target == "all":
        # Export context README
        click.echo("📄 Preparing README export...\n")

        readme_content = f"""# Context Engineering Documentation

This documentation was generated by ContextCraftPro.

## What is ContextCraftPro?

ContextCraftPro is an ephemeral context engineering workspace that helps teams:
- Define features with structured specifications
- Generate comprehensive Product Requirements Prompts (PRPs)
- Validate implementations against requirements
- Track context health over time

## Generated Artifacts

"""

        # Add links to exported docs
        if (ccp_root / "context" / "claude.md").exists():
            readme_content += "- [AI Coding Rules](docs/CLAUDE_RULES.md)\n"

        if (ccp_root / "context" / "INITIAL.md").exists():
            readme_content += "- [Feature Specifications](docs/FEATURES.md)\n"

        prps_dir = ccp_root / "context" / "prps"
        if prps_dir.exists() and list(prps_dir.glob("*.md")):
            readme_content += "- [Product Requirements Prompts](docs/prps/)\n"

        val_dir = ccp_root / "context" / "validation"
        if val_dir.exists() and list(val_dir.glob("*.md")):
            readme_content += "- [Validation Reports](docs/validation/)\n"

        readme_content += f"""

## About This Workspace

ContextCraftPro is a disposable tool. The `ContextCraftPro/` folder can be deleted at any time
without affecting your project. These exported artifacts capture the key insights and specifications.

For more information, see: https://github.com/your-org/contextcraft-pro
"""

        exports.append(
            ("README.context.md", "README.context.md", "Context README", readme_content)
        )

    if target == "all":
        # Export everything to _context_exports/
        click.echo("📦 Preparing full export bundle...\n")

        # Create timestamp for export bundle
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        bundle_dir = f"_context_exports/{timestamp}"

        # Add all context files to bundle
        context_files = [
            "context/project-profile.yaml",
            "context/claude.md",
            "context/INITIAL.md",
        ]

        for rel_path in context_files:
            source_path = ccp_root / rel_path
            if source_path.exists():
                dest = f"{bundle_dir}/{rel_path}"
                exports.append((rel_path, dest, f"Bundle: {rel_path}"))

    # Display export plan
    click.echo("📋 Export Plan:\n")
    for item in exports:
        if len(item) == 4:
            source, dest, desc, _ = item
        else:
            source, dest, desc = item
        click.echo(f"  {source}")
        click.echo(f"    → {dest}")
        click.echo(f"       ({desc})\n")

    if not exports:
        click.echo("⚠️  Nothing to export")
        return

    # Final confirmation
    if not auto_yes and not dry_run:
        confirm = click.confirm(
            f"\nExport {len(exports)} file(s) to host repository?", default=True
        )
        if not confirm:
            click.echo("Export cancelled.")
            return

    # Perform exports
    if not dry_run:
        click.echo("\n🚀 Exporting...\n")
        exported_count = 0
        errors = []

        for item in exports:
            if len(item) == 4:
                source, dest, desc, custom_content = item
            else:
                source, dest, desc = item
                custom_content = None

            try:
                source_path = ccp_root / source if not custom_content else None
                dest_path = host_root / dest

                # Ensure destination directory exists
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Check if destination exists
                if dest_path.exists():
                    if config.behavior.confirm_exports and not auto_yes:
                        overwrite = click.confirm(f"  Overwrite {dest}?", default=False)
                        if not overwrite:
                            click.echo(f"  ⏭️  Skipped {dest}")
                            continue

                # Copy file or write custom content
                if custom_content:
                    dest_path.write_text(custom_content)
                else:
                    import shutil

                    shutil.copy2(source_path, dest_path)

                click.echo(f"  ✓ Exported {dest}")
                logger.info("Exported file", source=source, destination=dest)
                exported_count += 1

            except Exception as e:
                error_msg = f"Failed to export {dest}: {e}"
                errors.append(error_msg)
                click.echo(f"  ✗ {error_msg}")
                logger.error(
                    "Export failed", source=source, destination=dest, error=str(e)
                )

        # Summary
        click.echo("\n" + "=" * 60)
        if exported_count > 0:
            click.echo(f"✨ Exported {exported_count} file(s) successfully!")
        if errors:
            click.echo(f"⚠️  {len(errors)} error(s) occurred:")
            for error in errors:
                click.echo(f"  • {error}")
        click.echo("=" * 60)

        if exported_count > 0:
            click.echo("\n💡 Next steps:")
            click.echo("  1. Review exported files in your host repository")
            click.echo("  2. Commit the files you want to keep")
            click.echo("  3. Update your project documentation as needed")

    else:
        click.echo(f"\n[DRY RUN] Would export {len(exports)} file(s)")
        for item in exports:
            if len(item) == 4:
                _, dest, _, _ = item
            else:
                _, dest, _ = item
            click.echo(f"  Would create: {dest}")

    logger.info(
        "export completed", target=target, exported=exported_count if not dry_run else 0
    )
