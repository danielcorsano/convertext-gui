"""Basic GUI tests."""

import pytest
from unittest.mock import Mock, patch


class TestGUIBasics:
    """Basic GUI initialization tests."""

    def test_version_import(self):
        """Test version can be imported."""
        from convertext_gui import __version__
        assert __version__ == "0.1.0"

    def test_logging_config_import(self):
        """Test logging config imports."""
        from convertext_gui.logging_config import setup_logging, is_development_mode
        assert callable(setup_logging)
        assert callable(is_development_mode)

    def test_widgets_import(self):
        """Test widgets can be imported."""
        # These will fail without display, but we can test the imports exist
        with patch('convertext_gui.widgets.ttk'), \
             patch('convertext_gui.widgets.tk'):
            from convertext_gui.widgets import FileList
            assert FileList is not None

    def test_threads_import(self):
        """Test threads module imports."""
        from convertext_gui.threads import ConversionThread
        assert ConversionThread is not None


class TestConfigurationHandling:
    """Test configuration and state management."""

    def test_format_selection_state(self):
        """Test format selection state management."""
        import tkinter as tk

        # Create mock format vars
        format_vars = {
            'txt': tk.BooleanVar(value=True),
            'epub': tk.BooleanVar(value=False),
            'html': tk.BooleanVar(value=True)
        }

        # Get selected formats
        selected = [fmt for fmt, var in format_vars.items() if var.get()]

        assert 'txt' in selected
        assert 'html' in selected
        assert 'epub' not in selected
        assert len(selected) == 2

    def test_output_directory_handling(self):
        """Test output directory path handling."""
        from pathlib import Path

        output_dir = None  # Default: same as source

        # Test preset directories
        desktop = Path.home() / "Desktop"
        downloads = Path.home() / "Downloads"

        assert desktop.exists() or downloads.exists()  # At least one should exist

    def test_overwrite_flag(self):
        """Test overwrite flag handling."""
        import tkinter as tk

        overwrite_var = tk.BooleanVar(value=False)
        assert overwrite_var.get() is False

        overwrite_var.set(True)
        assert overwrite_var.get() is True
