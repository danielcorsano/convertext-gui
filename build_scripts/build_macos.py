"""Build macOS .app bundle using PyInstaller."""

import PyInstaller.__main__
import sys
import os
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
ICON_PATH = PROJECT_ROOT / "convertext_gui" / "assets" / "icon.icns"
ASSETS_PATH = PROJECT_ROOT / "convertext_gui" / "assets"

def build_macos():
    """Build macOS application bundle."""

    # Change to project root for relative paths
    os.chdir(PROJECT_ROOT)

    args = [
        str(PROJECT_ROOT / "convertext_gui" / "gui.py"),
        "--name=ConverText",
        "--windowed",
        "--onedir",  # Changed from onefile - better for macOS .app bundles
        f"--icon={ICON_PATH}",
        f"--add-data={ASSETS_PATH}{os.pathsep}convertext_gui/assets",
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
    print(f"Assets: {ASSETS_PATH}")

    PyInstaller.__main__.run(args)

    # Clean up redundant ConverText directory created by onedir mode
    import shutil
    redundant_dir = PROJECT_ROOT / "dist" / "ConverText"
    if redundant_dir.exists():
        shutil.rmtree(redundant_dir)
        print(f"\nCleaned up: {redundant_dir}")

    print("\n✓ Build complete!")
    print(f"Application: {PROJECT_ROOT}/dist/ConverText.app")
    print("\nTo test:")
    print("  open dist/ConverText.app")

if __name__ == "__main__":
    build_macos()
