"""
Logging utilities for ContextCraftPro

Provides structured logging to file and formatted output to CLI.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import json


class CCPLogger:
    """
    Logger for ContextCraftPro with both file and console output.

    File logs are structured (JSON lines) for machine parsing.
    Console logs are human-friendly formatted output.
    """

    def __init__(self, log_dir: Path, verbose: bool = False):
        """
        Initialize the CCP logger.

        Args:
            log_dir: Directory for log files
            verbose: Enable verbose console output
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "ccp.log"
        self.verbose = verbose

        # Set up file logger (structured JSON)
        self.file_logger = logging.getLogger("ccp.file")
        self.file_logger.setLevel(logging.DEBUG)
        self.file_logger.handlers.clear()

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(JsonFormatter())
        self.file_logger.addHandler(file_handler)

        # Set up console logger (human-friendly)
        self.console_logger = logging.getLogger("ccp.console")
        self.console_logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        self.console_logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
        console_handler.setFormatter(ConsoleFormatter())
        self.console_logger.addHandler(console_handler)

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error message"""
        self._log(logging.ERROR, message, **kwargs)

    def success(self, message: str, **kwargs):
        """Log success message (info level with special formatting)"""
        kwargs["_success"] = True
        self._log(logging.INFO, message, **kwargs)

    def _log(self, level: int, message: str, **kwargs):
        """
        Internal logging method.

        Args:
            level: Log level
            message: Log message
            **kwargs: Additional structured data for JSON log
        """
        # Add timestamp
        kwargs["timestamp"] = datetime.now(timezone.utc).isoformat()

        # File log (structured JSON)
        extra = {"structured_data": kwargs}
        self.file_logger.log(level, message, extra=extra)

        # Console log (human-friendly)
        self.console_logger.log(level, message, extra={"structured_data": kwargs})

    def operation_start(self, operation: str, **kwargs):
        """Log the start of an operation"""
        self.info(
            f"Starting: {operation}", operation=operation, phase="start", **kwargs
        )

    def operation_end(self, operation: str, success: bool = True, **kwargs):
        """Log the end of an operation"""
        if success:
            self.success(
                f"Completed: {operation}", operation=operation, phase="end", **kwargs
            )
        else:
            self.error(
                f"Failed: {operation}", operation=operation, phase="end", **kwargs
            )

    def llm_call(self, feature: str, prompt_size: int, response_size: int, **kwargs):
        """Log an LLM API call"""
        self.info(
            f"LLM call for feature '{feature}'",
            event_type="llm_call",
            feature=feature,
            prompt_size=prompt_size,
            response_size=response_size,
            **kwargs,
        )


class JsonFormatter(logging.Formatter):
    """Formatter that outputs JSON lines for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Add structured data if present
        if hasattr(record, "structured_data"):
            log_data.update(record.structured_data)

        return json.dumps(log_data)


class ConsoleFormatter(logging.Formatter):
    """Formatter for human-friendly console output"""

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[37m",  # White
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "SUCCESS": "\033[32m",  # Green
        "RESET": "\033[0m",  # Reset
    }

    SYMBOLS = {
        "DEBUG": "⚙",
        "INFO": "ℹ",
        "WARNING": "⚠",
        "ERROR": "✗",
        "SUCCESS": "✓",
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record for console"""
        level = record.levelname

        # Check for success flag
        is_success = False
        if hasattr(record, "structured_data"):
            is_success = record.structured_data.get("_success", False)

        if is_success:
            level = "SUCCESS"

        color = self.COLORS.get(level, self.COLORS["RESET"])
        symbol = self.SYMBOLS.get(level, "•")
        reset = self.COLORS["RESET"]

        message = record.getMessage()

        # Format: [symbol] message
        return f"{color}{symbol}{reset} {message}"


def get_logger(ccp_root: Optional[Path] = None, verbose: bool = False) -> CCPLogger:
    """
    Get or create a CCP logger instance.

    Args:
        ccp_root: Root of ContextCraftPro folder (defaults to script's parent)
        verbose: Enable verbose output

    Returns:
        CCPLogger instance
    """
    if ccp_root is None:
        # Default to ContextCraftPro folder
        ccp_root = Path(__file__).parent.parent

    log_dir = ccp_root / "runtime" / "logs"
    return CCPLogger(log_dir, verbose=verbose)
