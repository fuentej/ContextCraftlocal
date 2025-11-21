"""
CLI interface for ContextCraftPro

Defines all commands and their options using Click.
"""

import click
import sys
from pathlib import Path
from typing import Optional

# Import core modules
from core import ccp_logger, ccp_config


# Determine CCP root (where this script lives)
CCP_ROOT = Path(__file__).parent.parent.resolve()


@click.group()
@click.option(
    "--config", type=click.Path(), help="Path to config file (overrides default)"
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would happen without making changes"
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx, config: Optional[str], dry_run: bool, verbose: bool):
    """
    ContextCraftPro - Context Engineering Workspace for AI-Driven Development

    A self-contained, disposable tool for creating structured specs, plans,
    and validation for your projects.
    """
    # Store global options in context
    ctx.ensure_object(dict)
    ctx.obj["CCP_ROOT"] = CCP_ROOT
    ctx.obj["CONFIG_PATH"] = config
    ctx.obj["DRY_RUN"] = dry_run
    ctx.obj["VERBOSE"] = verbose

    # Initialize logger
    logger = ccp_logger.get_logger(CCP_ROOT, verbose=verbose)
    ctx.obj["LOGGER"] = logger


@cli.command(name="init-project")
@click.option("--yes", "-y", is_flag=True, help="Answer yes to all prompts")
@click.pass_context
def init_project(ctx, yes: bool):
    """
    First-time setup of ContextCraftPro for this repository.

    Profiles the host repository, sets up context files, and initializes configuration.
    """
    logger = ctx.obj["LOGGER"]
    logger.operation_start("init-project", command="init-project")

    try:
        from core import ccp_orchestrator

        ccp_orchestrator.init_project(
            ccp_root=ctx.obj["CCP_ROOT"],
            config_path=ctx.obj.get("CONFIG_PATH"),
            dry_run=ctx.obj["DRY_RUN"],
            auto_yes=yes,
            logger=logger,
        )

        logger.operation_end("init-project", success=True)

    except Exception as e:
        logger.operation_end("init-project", success=False, error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command(name="new-feature")
@click.option("--feature", "-f", type=str, help="Feature name/slug")
@click.pass_context
def new_feature(ctx, feature: Optional[str]):
    """
    Create a new feature specification interactively.

    Guides you through defining a feature with structured questions,
    then adds it to INITIAL.md.
    """
    logger = ctx.obj["LOGGER"]
    logger.operation_start("new-feature", command="new-feature", feature=feature)

    try:
        from core import ccp_orchestrator

        ccp_orchestrator.new_feature(
            ccp_root=ctx.obj["CCP_ROOT"],
            config_path=ctx.obj.get("CONFIG_PATH"),
            feature_slug=feature,
            dry_run=ctx.obj["DRY_RUN"],
            logger=logger,
        )

        logger.operation_end("new-feature", success=True, feature=feature)

    except Exception as e:
        logger.operation_end(
            "new-feature", success=False, feature=feature, error=str(e)
        )
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command(name="generate-prp")
@click.option(
    "--feature", "-f", required=True, type=str, help="Feature name/slug (required)"
)
@click.pass_context
def generate_prp(ctx, feature: str):
    """
    Generate a Product Requirements Prompt (PRP) for a feature.

    Uses Foundry Local to create a detailed, AI-ready implementation plan
    based on the feature spec in INITIAL.md and global rules.
    """
    logger = ctx.obj["LOGGER"]
    logger.operation_start("generate-prp", command="generate-prp", feature=feature)

    try:
        from core import ccp_orchestrator

        ccp_orchestrator.generate_prp(
            ccp_root=ctx.obj["CCP_ROOT"],
            config_path=ctx.obj.get("CONFIG_PATH"),
            feature_slug=feature,
            dry_run=ctx.obj["DRY_RUN"],
            logger=logger,
        )

        logger.operation_end("generate-prp", success=True, feature=feature)

    except Exception as e:
        logger.operation_end(
            "generate-prp", success=False, feature=feature, error=str(e)
        )
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command(name="validate")
@click.option(
    "--feature", "-f", required=True, type=str, help="Feature name/slug (required)"
)
@click.option("--tests-command", type=str, help="Override default test command")
@click.option("--no-tests", is_flag=True, help="Skip running tests")
@click.pass_context
def validate(ctx, feature: str, tests_command: Optional[str], no_tests: bool):
    """
    Capture validation results for a feature implementation.

    Runs tests and collects manual feedback about how well the
    implementation matched the PRP.
    """
    logger = ctx.obj["LOGGER"]
    logger.operation_start("validate", command="validate", feature=feature)

    try:
        from core import ccp_orchestrator

        ccp_orchestrator.validate(
            ccp_root=ctx.obj["CCP_ROOT"],
            config_path=ctx.obj.get("CONFIG_PATH"),
            feature_slug=feature,
            tests_command=tests_command,
            skip_tests=no_tests,
            dry_run=ctx.obj["DRY_RUN"],
            logger=logger,
        )

        logger.operation_end("validate", success=True, feature=feature)

    except Exception as e:
        logger.operation_end("validate", success=False, feature=feature, error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command(name="health")
@click.option("--report", is_flag=True, help="Generate written health report")
@click.pass_context
def health(ctx, report: bool):
    """
    Check the health of your context artifacts.

    Identifies features missing PRPs or validations, and detects
    potentially stale context files.
    """
    logger = ctx.obj["LOGGER"]
    logger.operation_start("health", command="health")

    try:
        from core import ccp_orchestrator

        ccp_orchestrator.health(
            ccp_root=ctx.obj["CCP_ROOT"],
            config_path=ctx.obj.get("CONFIG_PATH"),
            generate_report=report,
            dry_run=ctx.obj["DRY_RUN"],
            logger=logger,
        )

        logger.operation_end("health", success=True)

    except Exception as e:
        logger.operation_end("health", success=False, error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command(name="export")
@click.option(
    "--target",
    type=click.Choice(["docs", "readme", "all"], case_sensitive=False),
    required=True,
    help="Export target preset",
)
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompts")
@click.pass_context
def export(ctx, target: str, yes: bool):
    """
    Export context artifacts to the host repository.

    CAUTION: This modifies files outside ContextCraftPro/.
    Confirmation required unless --yes is used.

    Presets:
      - docs: Export to ../docs/
      - readme: Export README draft to ../README.context.md
      - all: Export bundle to ../_context_exports/
    """
    logger = ctx.obj["LOGGER"]
    logger.operation_start("export", command="export", target=target)

    try:
        from core import ccp_orchestrator

        ccp_orchestrator.export(
            ccp_root=ctx.obj["CCP_ROOT"],
            config_path=ctx.obj.get("CONFIG_PATH"),
            target=target,
            auto_yes=yes,
            dry_run=ctx.obj["DRY_RUN"],
            logger=logger,
        )

        logger.operation_end("export", success=True, target=target)

    except Exception as e:
        logger.operation_end("export", success=False, target=target, error=str(e))
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
