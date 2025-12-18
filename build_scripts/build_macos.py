"""Build macOS .app bundle using PyInstaller."""

import PyInstaller.__main__
import os
import sys
import subprocess
from pathlib import Path
from build_scripts.common import PROJECT_ROOT, get_common_args

ICON_PATH = PROJECT_ROOT / "convertext_gui" / "assets" / "icon.icns"
ASSETS_PATH = PROJECT_ROOT / "convertext_gui" / "assets"

def build_macos():
    """Build macOS application bundle."""

    # Check that convertext package exists
    convertext_path = PROJECT_ROOT.parent / "convertext"
    if not convertext_path.exists():
        print(f"\n❌ ERROR: convertext package not found at {convertext_path}")
        print("   Make sure the convertext package is in ../convertext/")
        print("   Clone it with: cd .. && git clone https://github.com/danielcorsano/convertext.git")
        sys.exit(1)

    print(f"✓ Found convertext package at {convertext_path}")

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

    print("\n✓ Build complete!")
    print(f"Application: {PROJECT_ROOT}/dist/ConverText.app")

    # Create DMG for distribution
    print("\nCreating DMG for distribution...")
    dmg_path = PROJECT_ROOT / "dist" / "ConverText.dmg"
    app_path = PROJECT_ROOT / "dist" / "ConverText.app"

    # Remove old DMG if exists
    if dmg_path.exists():
        dmg_path.unlink()

    # Create DMG using hdiutil
    try:
        subprocess.run([
            "hdiutil", "create",
            "-volname", "ConverText",
            "-srcfolder", str(app_path),
            "-ov",
            "-format", "UDZO",
            str(dmg_path)
        ], check=True)
        print(f"\n✓ DMG created: {dmg_path}")
        print(f"  Size: {dmg_path.stat().st_size / (1024*1024):.1f} MB")
    except subprocess.CalledProcessError as e:
        print(f"\n⚠ Warning: Failed to create DMG: {e}")
        print("  The .app file is still available for distribution")

    print("\nTo test:")
    print("  open dist/ConverText.app")
    print("\nTo distribute:")
    print("  Upload dist/ConverText.dmg to GitHub releases")

if __name__ == "__main__":
    build_macos()
