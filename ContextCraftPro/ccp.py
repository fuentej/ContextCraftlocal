#!/usr/bin/env python3
"""
ContextCraftPro (CCP) - Main Entry Point

A self-contained, disposable context engineering workspace for AI-driven development.
"""

import sys
from pathlib import Path

# Add the core module to the Python path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))


def main():
    """Main entry point for ContextCraftPro CLI"""
    try:
        from core.ccp_cli import cli

        cli()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
