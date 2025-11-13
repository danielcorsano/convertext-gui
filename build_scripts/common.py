"""Common build configuration and utilities."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def get_common_args():
    """PyInstaller arguments shared across all platforms."""
    return [
        "--hidden-import=convertext",
        "--hidden-import=convertext.converters",
        "--hidden-import=convertext.core",
        "--hidden-import=convertext.config",
        "--hidden-import=convertext.registry",
        "--hidden-import=tkinter",
        "--hidden-import=ttkbootstrap",
        "--hidden-import=queue",
        "--exclude-module=test",
        "--exclude-module=unittest",
        "--exclude-module=email",
        "--exclude-module=http.server",
        "--exclude-module=pydoc",
        "--exclude-module=lib2to3",
        "--noconfirm",
        "--clean",
    ]
