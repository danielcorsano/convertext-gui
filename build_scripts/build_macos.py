"""Build macOS .app bundle using PyInstaller."""

import PyInstaller.__main__
import os
from pathlib import Path
from build_scripts.common import PROJECT_ROOT, get_common_args

ICON_PATH = PROJECT_ROOT / "convertext_gui" / "assets" / "icon.icns"
ASSETS_PATH = PROJECT_ROOT / "convertext_gui" / "assets"

def build_macos():
    """Build macOS application bundle."""

    os.chdir(PROJECT_ROOT)

    args = [
        str(PROJECT_ROOT / "convertext_gui" / "gui.py"),
        "--name=ConverText",
        "--windowed",
        "--onedir",
        f"--icon={ICON_PATH}",
        f"--add-data={ASSETS_PATH}{os.pathsep}convertext_gui/assets",
        "--strip",
        *get_common_args(),
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

    print("\nBuild complete!")
    print(f"Application: {PROJECT_ROOT}/dist/ConverText.app")
    print("\nTo test:")
    print("  open dist/ConverText.app")

if __name__ == "__main__":
    build_macos()
