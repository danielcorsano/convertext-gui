"""Build Windows .exe using PyInstaller."""

import PyInstaller.__main__
import sys
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
ICON_PATH = PROJECT_ROOT / "convertext_gui" / "assets" / "icon.ico"

def build_windows():
    """Build Windows executable."""

    args = [
        str(PROJECT_ROOT / "convertext_gui" / "gui.py"),
        "--name=ConverText",
        "--noconsole",
        "--onefile",
        f"--icon={ICON_PATH}" if ICON_PATH.exists() else "",
        "--add-data=convertext_gui/assets;convertext_gui/assets",  # Note: semicolon for Windows
        "--hidden-import=convertext",
        "--hidden-import=convertext.converters",
        "--hidden-import=convertext.core",
        "--hidden-import=convertext.config",
        "--hidden-import=convertext.registry",
        "--hidden-import=tkinter",
        "--hidden-import=ttkbootstrap",
        "--hidden-import=queue",
        # Size optimizations (--strip not supported on Windows)
        "--exclude-module=test",
        "--exclude-module=unittest",
        "--exclude-module=email",
        "--exclude-module=http.server",
        "--exclude-module=pydoc",
        "--exclude-module=lib2to3",
        "--noconfirm",
        "--clean",
    ]

    # Remove empty icon arg if file doesn't exist
    args = [arg for arg in args if arg]

    print("Building Windows executable...")
    if ICON_PATH.exists():
        print(f"Icon: {ICON_PATH}")
    else:
        print("Warning: icon.ico not found, building without icon")

    PyInstaller.__main__.run(args)

    print("\nBuild complete!")
    print(f"Executable: {PROJECT_ROOT}/dist/ConverText.exe")
    print("\nTo test:")
    print("  dist\\ConverText.exe")

if __name__ == "__main__":
    build_windows()
