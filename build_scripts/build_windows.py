"""Build Windows .exe using PyInstaller."""

import PyInstaller.__main__
import sys
from pathlib import Path
from build_scripts.common import PROJECT_ROOT, get_common_args

ICON_PATH = PROJECT_ROOT / "convertext_gui" / "assets" / "icon.ico"

def build_windows():
    """Build Windows executable."""

    # Check that convertext package exists
    convertext_path = PROJECT_ROOT.parent / "convertext"
    if not convertext_path.exists():
        print(f"\n❌ ERROR: convertext package not found at {convertext_path}")
        print("   Make sure the convertext package is in ../convertext/")
        print("   Clone it with: cd .. && git clone https://github.com/danielcorsano/convertext.git")
        sys.exit(1)

    print(f"✓ Found convertext package at {convertext_path}")

    args = [
        str(PROJECT_ROOT / "convertext_gui" / "gui.py"),
        "--name=ConverText",
        "--noconsole",
        "--onefile",
        f"--icon={ICON_PATH}" if ICON_PATH.exists() else "",
        "--add-data=convertext_gui/assets;convertext_gui/assets",
        *get_common_args(),
    ]

    args = [arg for arg in args if arg]

    print("\nBuilding Windows executable...")
    if ICON_PATH.exists():
        print(f"Icon: {ICON_PATH}")
    else:
        print("⚠ Warning: icon.ico not found, building without icon")

    PyInstaller.__main__.run(args)

    print("\n✓ Build complete!")
    print(f"Executable: {PROJECT_ROOT}/dist/ConverText.exe")
    print("\nTo test:")
    print("  dist\\ConverText.exe")
    print("\nTo distribute:")
    print("  Upload dist/ConverText.exe to GitHub releases")

if __name__ == "__main__":
    build_windows()
