"""Basic GUI tests."""

from pathlib import Path
from unittest.mock import patch


class TestGUIBasics:
    """Basic GUI initialization tests."""

    def test_version_import(self):
        """Test version matches the packaged version."""
        import tomllib
        from convertext_gui import __version__

        pyproject = Path(__file__).parents[2] / "pyproject.toml"
        declared = tomllib.loads(pyproject.read_text())["tool"]["poetry"]["version"]
        assert __version__ == declared

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


class TestFormatSelection:
    """Test which formats the GUI offers as conversion targets."""

    def test_beta_formats_excluded_from_targets(self):
        """AZW3 is beta upstream and must not be offered as an output format."""
        from convertext.converters.loader import load_converters
        from convertext.registry import get_registry
        from convertext_gui.gui import BETA_FORMATS

        load_converters()
        targets = set()
        for fmts in get_registry().list_supported_formats().values():
            targets.update(fmts)

        assert 'azw3' in targets, "registry no longer offers azw3; drop BETA_FORMATS"
        assert 'mobi' in targets - BETA_FORMATS
        assert not (targets - BETA_FORMATS) & BETA_FORMATS

    def test_beta_input_formats_unaffected(self):
        """Filtering azw3 output must not remove azw/azw3/mobi as inputs."""
        from convertext.converters.loader import load_converters
        from convertext.registry import get_registry

        load_converters()
        sources = get_registry().list_supported_formats()
        for fmt in ('azw', 'azw3', 'mobi'):
            assert fmt in sources


class TestConfigurationHandling:
    """Test configuration and state management."""

    def test_format_selection_state(self, tk_root):
        """Test format selection state management."""
        import tkinter as tk

        format_vars = {
            'txt': tk.BooleanVar(master=tk_root, value=True),
            'epub': tk.BooleanVar(master=tk_root, value=False),
            'html': tk.BooleanVar(master=tk_root, value=True)
        }

        selected = [fmt for fmt, var in format_vars.items() if var.get()]

        assert 'txt' in selected
        assert 'html' in selected
        assert 'epub' not in selected
        assert len(selected) == 2

    def test_output_directory_handling(self):
        """Test output directory path handling."""
        desktop = Path.home() / "Desktop"
        downloads = Path.home() / "Downloads"

        assert desktop.exists() or downloads.exists()

    def test_overwrite_flag(self, tk_root):
        """Test overwrite flag handling."""
        import tkinter as tk

        overwrite_var = tk.BooleanVar(master=tk_root, value=False)
        assert overwrite_var.get() is False

        overwrite_var.set(True)
        assert overwrite_var.get() is True
