"""Pytest configuration for GUI tests."""

import pytest
import sys
from pathlib import Path


# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def tk_root():
    """Real Tk root window, shared across tests. Skips when no display."""
    import tkinter as tk

    try:
        root = tk.Tk()
    except tk.TclError as e:
        pytest.skip(f"No display available: {e}")

    root.withdraw()
    yield root
    root.destroy()


@pytest.fixture
def sample_files(tmp_path):
    """Create sample files for testing."""
    files = []
    for i in range(3):
        file = tmp_path / f"test{i}.txt"
        file.write_text(f"Sample content {i}")
        files.append(file)
    return files


@pytest.fixture
def sample_formats():
    """Sample output formats."""
    return ["txt", "html", "epub"]
