"""
File system utilities for ContextCraftPro

Provides safe file operations with boundary checking, repository scanning,
and template management.
"""

import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import re


class BoundaryViolationError(Exception):
    """Raised when attempting to access files outside allowed boundaries"""

    pass


class FileSystemError(Exception):
    """General file system operation errors"""

    pass


@dataclass
class ProjectProfile:
    """Profile of a project repository"""

    name: str
    languages: List[str]
    frameworks: List[str]
    test_framework: Optional[str] = None
    test_command: Optional[str] = None
    notes: str = "Derived automatically. User can edit."


class SafeFileSystem:
    """
    File system operations with boundary enforcement.

    Ensures all operations stay within the ContextCraftPro folder boundary.
    """

    def __init__(self, ccp_root: Path, allow_host_read: bool = True):
        """
        Initialize safe file system.

        Args:
            ccp_root: Root of ContextCraftPro folder (boundary for writes)
            allow_host_read: Allow reading from host repo (outside CCP folder)
        """
        self.ccp_root = Path(ccp_root).resolve()
        self.allow_host_read = allow_host_read
        self.host_root = self.ccp_root.parent

    def validate_write_path(self, path: Path) -> Path:
        """
        Validate that a path is within the CCP boundary for writing.

        Args:
            path: Path to validate

        Returns:
            Resolved absolute path

        Raises:
            BoundaryViolationError: If path is outside CCP folder
        """
        resolved = Path(path).resolve()

        # Check if path is within CCP root
        try:
            resolved.relative_to(self.ccp_root)
        except ValueError:
            raise BoundaryViolationError(
                f"Write operation outside ContextCraftPro folder: {resolved}"
            )

        return resolved

    def validate_read_path(self, path: Path) -> Path:
        """
        Validate that a path is allowed for reading.

        Args:
            path: Path to validate

        Returns:
            Resolved absolute path

        Raises:
            BoundaryViolationError: If path is outside allowed boundaries
        """
        resolved = Path(path).resolve()

        # Check if within CCP root (always allowed)
        try:
            resolved.relative_to(self.ccp_root)
            return resolved
        except ValueError:
            pass

        # Check if within host root (allowed if allow_host_read is True)
        if self.allow_host_read:
            try:
                resolved.relative_to(self.host_root)
                return resolved
            except ValueError:
                raise BoundaryViolationError(
                    f"Read operation outside allowed boundaries: {resolved}"
                )
        else:
            raise BoundaryViolationError(
                f"Read operation outside ContextCraftPro folder: {resolved}"
            )

    def read_file(self, path: Path) -> str:
        """
        Safely read a file.

        Args:
            path: Path to file

        Returns:
            File contents as string

        Raises:
            BoundaryViolationError: If path is outside boundaries
            FileSystemError: If file cannot be read
        """
        validated_path = self.validate_read_path(path)

        try:
            return validated_path.read_text(encoding="utf-8")
        except Exception as e:
            raise FileSystemError(f"Failed to read file {path}: {e}")

    def write_file(self, path: Path, content: str) -> None:
        """
        Safely write a file using atomic write (temp file + rename).

        Args:
            path: Path to file
            content: Content to write

        Raises:
            BoundaryViolationError: If path is outside CCP folder
            FileSystemError: If file cannot be written
        """
        validated_path = self.validate_write_path(path)

        # Ensure parent directory exists
        validated_path.parent.mkdir(parents=True, exist_ok=True)

        # Atomic write: write to temp file, then rename
        try:
            fd, temp_path = tempfile.mkstemp(
                dir=validated_path.parent, prefix=f".{validated_path.name}.", text=True
            )

            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(content)

                # Rename temp file to target (atomic on POSIX, nearly atomic on Windows)
                Path(temp_path).replace(validated_path)
            except Exception:
                # Clean up temp file on error
                try:
                    Path(temp_path).unlink()
                except Exception:
                    pass
                raise

        except Exception as e:
            raise FileSystemError(f"Failed to write file {path}: {e}")

    def ensure_directory(self, path: Path) -> None:
        """
        Ensure a directory exists within CCP boundary.

        Args:
            path: Directory path

        Raises:
            BoundaryViolationError: If path is outside CCP folder
            FileSystemError: If directory cannot be created
        """
        validated_path = self.validate_write_path(path)

        try:
            validated_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise FileSystemError(f"Failed to create directory {path}: {e}")


class RepositoryScanner:
    """
    Scans a repository to detect languages, frameworks, and project structure.
    """

    # File extensions for language detection
    LANGUAGE_EXTENSIONS = {
        "python": [".py"],
        "javascript": [".js", ".jsx", ".mjs"],
        "typescript": [".ts", ".tsx"],
        "java": [".java"],
        "csharp": [".cs"],
        "go": [".go"],
        "rust": [".rs"],
        "ruby": [".rb"],
        "php": [".php"],
        "cpp": [".cpp", ".cc", ".cxx", ".h", ".hpp"],
        "c": [".c", ".h"],
    }

    # Config files for framework detection
    FRAMEWORK_INDICATORS = {
        "django": ["manage.py", "django"],
        "flask": ["app.py", "flask"],
        "fastapi": ["fastapi"],
        "react": ["package.json:react"],
        "vue": ["package.json:vue"],
        "angular": ["angular.json"],
        "nextjs": ["next.config.js", "next.config.ts"],
        "express": ["package.json:express"],
        "spring": ["pom.xml:spring", "build.gradle:spring"],
        "dotnet": [".csproj", ".sln"],
    }

    # Test framework indicators
    TEST_FRAMEWORKS = {
        "pytest": {
            "indicators": ["pytest.ini", "pyproject.toml:pytest"],
            "command": "pytest",
        },
        "unittest": {
            "indicators": ["test_*.py", "*_test.py"],
            "command": "python -m unittest",
        },
        "jest": {
            "indicators": ["jest.config.js", "package.json:jest"],
            "command": "npm test",
        },
        "mocha": {"indicators": ["mocha"], "command": "npm test"},
        "junit": {"indicators": ["pom.xml:junit"], "command": "mvn test"},
        "go test": {"indicators": ["*_test.go"], "command": "go test ./..."},
    }

    # Directories to exclude from scanning
    EXCLUDE_DIRS = {
        ".git",
        ".hg",
        ".svn",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        "venv",
        "env",
        ".venv",
        ".env",
        "dist",
        "build",
        "target",
        "out",
        ".idea",
        ".vscode",
        ".vs",
        "ContextCraftPro",  # Don't scan ourselves
    }

    def __init__(self, project_root: Path, max_depth: int = 5):
        """
        Initialize repository scanner.

        Args:
            project_root: Root directory of the project to scan
            max_depth: Maximum directory depth to scan
        """
        self.project_root = Path(project_root).resolve()
        self.max_depth = max_depth

    def scan(self) -> ProjectProfile:
        """
        Scan the repository and generate a project profile.

        Returns:
            ProjectProfile with detected information
        """
        languages = self._detect_languages()
        frameworks = self._detect_frameworks()
        test_framework, test_command = self._detect_test_framework()

        project_name = self.project_root.name

        return ProjectProfile(
            name=project_name,
            languages=sorted(languages),
            frameworks=sorted(frameworks),
            test_framework=test_framework,
            test_command=test_command,
        )

    def _detect_languages(self) -> Set[str]:
        """Detect programming languages used in the project"""
        languages = set()
        extension_counts = {}

        for file_path in self._walk_files():
            ext = file_path.suffix.lower()

            for lang, extensions in self.LANGUAGE_EXTENSIONS.items():
                if ext in extensions:
                    extension_counts[lang] = extension_counts.get(lang, 0) + 1

        # Consider a language present if it has at least 2 files
        languages = {lang for lang, count in extension_counts.items() if count >= 2}

        return languages

    def _detect_frameworks(self) -> Set[str]:
        """Detect frameworks used in the project"""
        frameworks = set()

        for framework, indicators in self.FRAMEWORK_INDICATORS.items():
            if self._check_indicators(indicators):
                frameworks.add(framework)

        return frameworks

    def _detect_test_framework(self) -> tuple[Optional[str], Optional[str]]:
        """Detect test framework and command"""
        for framework, info in self.TEST_FRAMEWORKS.items():
            if self._check_indicators(info["indicators"]):
                return framework, info["command"]

        return None, None

    def _check_indicators(self, indicators: List[str]) -> bool:
        """Check if any indicator is present in the project"""
        for indicator in indicators:
            # Handle file:content indicators (e.g., "package.json:react")
            if ":" in indicator:
                file_pattern, content_pattern = indicator.split(":", 1)
                if self._check_file_content(file_pattern, content_pattern):
                    return True
            else:
                # Simple file existence check
                if self._file_exists_pattern(indicator):
                    return True

        return False

    def _check_file_content(self, file_pattern: str, content_pattern: str) -> bool:
        """Check if a file matching pattern contains content pattern"""
        for file_path in self._walk_files():
            if file_path.name == file_pattern or file_path.match(file_pattern):
                try:
                    content = file_path.read_text(encoding="utf-8")
                    if content_pattern.lower() in content.lower():
                        return True
                except Exception:
                    pass

        return False

    def _file_exists_pattern(self, pattern: str) -> bool:
        """Check if any file matches the pattern"""
        for file_path in self._walk_files():
            if file_path.match(pattern) or file_path.name == pattern:
                return True

        return False

    def _walk_files(self, current_depth: int = 0):
        """Walk through files in the project, respecting max_depth and exclusions"""
        if current_depth > self.max_depth:
            return

        try:
            for item in self.project_root.iterdir():
                # Skip excluded directories
                if item.is_dir() and item.name in self.EXCLUDE_DIRS:
                    continue

                if item.is_file():
                    yield item
                elif item.is_dir():
                    scanner = RepositoryScanner(
                        item, self.max_depth - current_depth - 1
                    )
                    scanner.max_depth = self.max_depth - current_depth - 1
                    yield from scanner._walk_files(current_depth + 1)
        except PermissionError:
            pass


class GitIgnoreManager:
    """Manages .gitignore file operations"""

    def __init__(self, repo_root: Path):
        """
        Initialize .gitignore manager.

        Args:
            repo_root: Root of the git repository
        """
        self.repo_root = Path(repo_root).resolve()
        self.gitignore_path = self.repo_root / ".gitignore"

    def exists(self) -> bool:
        """Check if .gitignore file exists"""
        return self.gitignore_path.exists()

    def contains_entry(self, entry: str) -> bool:
        """
        Check if .gitignore contains a specific entry.

        Args:
            entry: Entry to check for

        Returns:
            True if entry exists
        """
        if not self.exists():
            return False

        try:
            content = self.gitignore_path.read_text(encoding="utf-8")
            # Check for exact line match (ignoring whitespace)
            for line in content.splitlines():
                if line.strip() == entry.strip():
                    return True
            return False
        except Exception:
            return False

    def add_entry(self, entry: str, comment: Optional[str] = None) -> None:
        """
        Add an entry to .gitignore.

        Args:
            entry: Entry to add
            comment: Optional comment to add before the entry

        Raises:
            FileSystemError: If unable to update .gitignore
        """
        try:
            # Read existing content
            if self.exists():
                content = self.gitignore_path.read_text(encoding="utf-8")
                # Ensure file ends with newline
                if content and not content.endswith("\n"):
                    content += "\n"
            else:
                content = ""

            # Add new entry
            if comment:
                content += f"\n# {comment}\n"
            else:
                content += "\n"
            content += f"{entry}\n"

            # Write back
            self.gitignore_path.write_text(content, encoding="utf-8")

        except Exception as e:
            raise FileSystemError(f"Failed to update .gitignore: {e}")
