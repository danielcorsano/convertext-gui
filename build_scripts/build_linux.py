"""Build Linux executable using PyInstaller."""

import PyInstaller.__main__
from pathlib import Path
from build_scripts.common import PROJECT_ROOT, get_common_args

ICON_PATH = PROJECT_ROOT / "convertext_gui" / "assets" / "icon.png"

def build_linux():
    """Build Linux executable."""

    args = [
        str(PROJECT_ROOT / "convertext_gui" / "gui.py"),
        "--name=convertext-gui",
        "--onefile",
        f"--icon={ICON_PATH}" if ICON_PATH.exists() else "",
        "--add-data=convertext_gui/assets:convertext_gui/assets",
        "--strip",
        *get_common_args(),
    ]

    args = [arg for arg in args if arg]

    print("Building Linux executable...")
    if ICON_PATH.exists():
        print(f"Icon: {ICON_PATH}")
    else:
        print("Warning: icon.png not found, building without icon")

    PyInstaller.__main__.run(args)

    print("\nBuild complete!")
    print(f"Executable: {PROJECT_ROOT}/dist/convertext-gui")
    print("\nTo test:")
    print("  ./dist/convertext-gui")
    print("\nTo create AppImage:")
    print("  See: https://appimage.org/")

if __name__ == "__main__":
    build_linux()
