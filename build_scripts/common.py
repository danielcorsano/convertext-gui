"""Common build configuration and utilities."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def get_common_args():
    """PyInstaller arguments shared across all platforms."""
    return [
        # Backend package - comprehensive imports
        "--hidden-import=convertext",
        "--hidden-import=convertext.core",
        "--hidden-import=convertext.config",
        "--hidden-import=convertext.registry",
        "--hidden-import=convertext.cli",

        # Converter infrastructure
        "--hidden-import=convertext.converters",
        "--hidden-import=convertext.converters.base",
        "--hidden-import=convertext.converters.loader",

        # Document converters
        "--hidden-import=convertext.converters.documents.txt",
        "--hidden-import=convertext.converters.documents.pdf",
        "--hidden-import=convertext.converters.documents.markdown",
        "--hidden-import=convertext.converters.documents.html",
        "--hidden-import=convertext.converters.documents.docx",
        "--hidden-import=convertext.converters.documents.rtf",
        "--hidden-import=convertext.converters.documents.odt",

        # Ebook converters
        "--hidden-import=convertext.converters.ebooks.epub",
        "--hidden-import=convertext.converters.ebooks.mobi",
        "--hidden-import=convertext.converters.ebooks.fb2",

        # GUI dependencies
        "--hidden-import=tkinter",
        "--hidden-import=ttkbootstrap",
        "--hidden-import=tkinterdnd2",
        "--hidden-import=queue",

        # Collect all package data
        "--collect-all=convertext",
        "--collect-all=pypdf",
        "--collect-all=python-docx",
        "--collect-all=lxml",
        "--collect-all=beautifulsoup4",
        "--collect-all=striprtf",
        "--collect-all=ttkbootstrap",
        "--collect-all=tkinterdnd2",

        # Exclusions
        "--exclude-module=test",
        "--exclude-module=unittest",
        "--exclude-module=http.server",
        "--exclude-module=pydoc",
        "--exclude-module=lib2to3",
        "--exclude-module=pytest",
        "--exclude-module=black",
        "--exclude-module=ruff",
        "--exclude-module=mypy",

        # Build options
        "--noconfirm",
        "--clean",
    ]
