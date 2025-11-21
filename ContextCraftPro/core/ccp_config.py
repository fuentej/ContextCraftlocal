"""
Configuration management for ContextCraftPro

Handles loading, validation, and management of configuration files.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


class ConfigError(Exception):
    """Configuration-related errors"""

    pass


@dataclass
class FoundryLocalConfig:
    """Foundry Local LLM configuration"""

    endpoint: str = "http://localhost:11434/v1/chat/completions"
    model: str = "gpt-4o-mini"
    timeout: int = 30
    max_retries: int = 3


@dataclass
class PathsConfig:
    """Path configuration"""

    project_root: str = ".."
    context_root: str = "context"
    claude_rules: str = "context/claude.md"
    initial_spec: str = "context/INITIAL.md"
    examples_dir: str = "context/examples"
    docs_dir: str = "context/docs-context"
    prps_dir: str = "context/prps"
    validation_dir: str = "context/validation"


@dataclass
class BehaviorConfig:
    """Behavior configuration"""

    auto_open_browser: bool = False
    confirm_exports: bool = True
    max_repo_scan_depth: int = 5
    enable_refinement: bool = True  # Use LLM to refine feature specs
    require_confirmation: bool = True  # Always confirm before writing


@dataclass
class CCPConfig:
    """Main ContextCraftPro configuration"""

    foundry_local: FoundryLocalConfig
    paths: PathsConfig
    behavior: BehaviorConfig

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "foundry_local": asdict(self.foundry_local),
            "paths": asdict(self.paths),
            "behavior": asdict(self.behavior),
        }


def load_config(config_path: Path) -> CCPConfig:
    """
    Load configuration from YAML file with environment variable overrides.

    Args:
        config_path: Path to config YAML file

    Returns:
        CCPConfig instance

    Raises:
        ConfigError: If config file is invalid or missing required fields
    """
    if not config_path.exists():
        raise ConfigError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigError(f"Invalid YAML in configuration file: {e}")

    if not config_data:
        raise ConfigError("Configuration file is empty")

    # Apply environment variable overrides
    config_data = _apply_env_overrides(config_data)

    # Validate and create config objects
    try:
        foundry_config = FoundryLocalConfig(**config_data.get("foundry_local", {}))
        paths_config = PathsConfig(**config_data.get("paths", {}))
        behavior_config = BehaviorConfig(**config_data.get("behavior", {}))

        return CCPConfig(
            foundry_local=foundry_config, paths=paths_config, behavior=behavior_config
        )
    except TypeError as e:
        raise ConfigError(f"Invalid configuration structure: {e}")


def save_config(config: CCPConfig, config_path: Path) -> None:
    """
    Save configuration to YAML file.

    Args:
        config: CCPConfig instance to save
        config_path: Path where to save the config

    Raises:
        ConfigError: If unable to write config file
    """
    config_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_path, "w") as f:
            yaml.safe_dump(
                config.to_dict(), f, default_flow_style=False, sort_keys=False
            )
    except Exception as e:
        raise ConfigError(f"Failed to save configuration: {e}")


def create_default_config(ccp_root: Path) -> CCPConfig:
    """
    Create a default configuration.

    Args:
        ccp_root: Root directory of ContextCraftPro

    Returns:
        CCPConfig with default values
    """
    return CCPConfig(
        foundry_local=FoundryLocalConfig(),
        paths=PathsConfig(),
        behavior=BehaviorConfig(),
    )


def ensure_config_exists(config_path: Path, ccp_root: Path) -> CCPConfig:
    """
    Ensure configuration file exists, creating default if needed.

    Args:
        config_path: Path to config file
        ccp_root: Root directory of ContextCraftPro

    Returns:
        CCPConfig instance
    """
    if config_path.exists():
        return load_config(config_path)
    else:
        # Create default config and save it
        config = create_default_config(ccp_root)
        save_config(config, config_path)
        return config


def _apply_env_overrides(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply environment variable overrides to configuration.

    Environment variables follow the pattern: CCP_SECTION_KEY
    Example: CCP_FOUNDRY_LOCAL_ENDPOINT, CCP_BEHAVIOR_CONFIRM_EXPORTS

    Args:
        config_data: Configuration dictionary

    Returns:
        Updated configuration dictionary
    """
    # Foundry Local overrides
    if "CCP_FOUNDRY_LOCAL_ENDPOINT" in os.environ:
        if "foundry_local" not in config_data:
            config_data["foundry_local"] = {}
        config_data["foundry_local"]["endpoint"] = os.environ[
            "CCP_FOUNDRY_LOCAL_ENDPOINT"
        ]

    if "CCP_FOUNDRY_LOCAL_MODEL" in os.environ:
        if "foundry_local" not in config_data:
            config_data["foundry_local"] = {}
        config_data["foundry_local"]["model"] = os.environ["CCP_FOUNDRY_LOCAL_MODEL"]

    if "CCP_FOUNDRY_LOCAL_TIMEOUT" in os.environ:
        if "foundry_local" not in config_data:
            config_data["foundry_local"] = {}
        try:
            config_data["foundry_local"]["timeout"] = int(
                os.environ["CCP_FOUNDRY_LOCAL_TIMEOUT"]
            )
        except ValueError:
            pass  # Ignore invalid timeout values

    # Behavior overrides
    if "CCP_CONFIRM_EXPORTS" in os.environ:
        if "behavior" not in config_data:
            config_data["behavior"] = {}
        config_data["behavior"]["confirm_exports"] = os.environ[
            "CCP_CONFIRM_EXPORTS"
        ].lower() in ("true", "1", "yes")

    if "CCP_VERBOSE" in os.environ:
        # Store verbose flag for logger (not in config structure but can be checked)
        pass

    return config_data


def get_config_path(ccp_root: Path, custom_path: Optional[str] = None) -> Path:
    """
    Get the configuration file path.

    Args:
        ccp_root: Root directory of ContextCraftPro
        custom_path: Optional custom config path (overrides default)

    Returns:
        Path to configuration file
    """
    if custom_path:
        return Path(custom_path).resolve()
    else:
        return ccp_root / "config" / "contextcraft.yaml"


def resolve_path(base_path: Path, relative_path: str) -> Path:
    """
    Resolve a relative path from configuration relative to base path.

    Args:
        base_path: Base path (usually ContextCraftPro root)
        relative_path: Relative path from config

    Returns:
        Resolved absolute path
    """
    if Path(relative_path).is_absolute():
        return Path(relative_path)
    else:
        return (base_path / relative_path).resolve()
