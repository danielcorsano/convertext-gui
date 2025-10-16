"""Build macOS .app bundle using PyInstaller."""

import PyInstaller.__main__
import sys
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
ICON_PATH = PROJECT_ROOT / "convertext_gui" / "assets" / "icon.icns"

def build_macos():
    """Build macOS application bundle."""

    args = [
        str(PROJECT_ROOT / "convertext_gui" / "gui.py"),
        "--name=ConverText",
        "--windowed",
        "--onedir",  # Changed from onefile - better for macOS .app bundles
        f"--icon={ICON_PATH}",
        "--add-data=convertext_gui/assets:convertext_gui/assets",
        "--hidden-import=convertext",
        "--hidden-import=convertext.converters",
        "--hidden-import=convertext.core",
        "--hidden-import=convertext.config",
        "--hidden-import=convertext.registry",
        "--hidden-import=tkinter",
        "--hidden-import=ttkbootstrap",
        "--hidden-import=queue",
        "--noconfirm",
        "--clean",
    ]

    print("Building macOS application...")
    print(f"Icon: {ICON_PATH}")

    PyInstaller.__main__.run(args)

    print("\n✓ Build complete!")
    print(f"Application: {PROJECT_ROOT}/dist/ConverText.app")
    print("\nTo test:")
    print("  open dist/ConverText.app")

if __name__ == "__main__":
    build_macos()
