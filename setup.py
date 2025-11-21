#!/usr/bin/env python3
"""
Setup script for ContextCraft
Provides backward compatibility with older pip/setuptools versions
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Core dependencies
INSTALL_REQUIRES = [
    "click>=8.1.7",
    "typer>=0.9.0",
    "rich>=13.7.0",
    "PyYAML>=6.0.1",
]

# Optional dependencies
EXTRAS_REQUIRE = {
    "dev": [
        "pytest>=7.4.3",
        "pytest-cov>=4.1.0",
        "black>=23.12.1",
        "flake8>=6.1.0",
        "mypy>=1.7.1",
        "types-PyYAML>=6.0.12",
    ],
    "web": [
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
    ],
    "ai": [
        "openai>=1.3.9",
        "anthropic>=0.7.1",
    ],
    "docs": [
        "mkdocs>=1.5.3",
        "mkdocs-material>=9.4.14",
    ],
}

# Add 'all' extra that includes everything
EXTRAS_REQUIRE["all"] = [
    dep for extra in ["dev", "web", "ai", "docs"] for dep in EXTRAS_REQUIRE[extra]
]

setup(
    name="contextcraft",
    version="1.0.0",
    description="Enhanced AI Project Structure Generator - Rapidly scaffold professional software projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ContextCraft Contributors",
    author_email="",
    url="https://github.com/fuentej/ContextCraftlocal",
    project_urls={
        "Homepage": "https://github.com/fuentej/ContextCraftlocal",
        "Documentation": "https://github.com/fuentej/ContextCraftlocal/blob/main/README.md",
        "Repository": "https://github.com/fuentej/ContextCraftlocal",
        "Bug Tracker": "https://github.com/fuentej/ContextCraftlocal/issues",
        "Changelog": "https://github.com/fuentej/ContextCraftlocal/blob/main/CHANGELOG.md",
    },
    packages=find_packages(include=["src", "src.*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points={
        "console_scripts": [
            "contextcraft=src.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Environment :: Console",
        "Typing :: Typed",
    ],
    keywords=[
        "project-generator",
        "scaffolding",
        "cli",
        "boilerplate",
        "templates",
        "ai",
        "fastapi",
        "react",
        "flask",
        "django",
        "nextjs",
        "typescript",
    ],
    license="MIT",
    zip_safe=False,
)
