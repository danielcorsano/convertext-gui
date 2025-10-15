"""Pytest configuration for GUI tests."""

import pytest
import sys
from pathlib import Path


# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_convertext_engine():
    """Mock convertext engine for testing."""
    from unittest.mock import Mock
    engine = Mock()
    engine.convert = Mock()
    return engine


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
