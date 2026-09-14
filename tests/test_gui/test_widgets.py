"""Tests for GUI widgets."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


class TestFileList:
    """Tests for FileList widget."""

    def test_add_files(self, tk_root):
        """Test adding files to the list."""
        from convertext_gui.widgets import FileList

        file_list = FileList(tk_root)
        file_list.add_files(["/tmp/test1.pdf", "/tmp/test2.docx"])

        assert len(file_list.files) == 2
        assert file_list.files[0] == Path("/tmp/test1.pdf")
        assert file_list.files[1] == Path("/tmp/test2.docx")

    def test_add_duplicate_files(self, tk_root):
        """Test that duplicate files are not added."""
        from convertext_gui.widgets import FileList

        file_list = FileList(tk_root)
        file_list.add_files(["/tmp/test.pdf"])
        file_list.add_files(["/tmp/test.pdf"])

        assert len(file_list.files) == 1

    def test_clear(self, tk_root):
        """Test clearing the file list."""
        from convertext_gui.widgets import FileList

        file_list = FileList(tk_root)
        file_list.add_files(["/tmp/test1.pdf", "/tmp/test2.docx"])
        file_list.clear()

        assert len(file_list.files) == 0
        assert len(file_list.file_widgets) == 0


class TestFileTypes:
    """Tests for the shared file dialog filter."""

    def test_covers_every_registry_source(self):
        """Every format convertext can read must be selectable in the browser."""
        from convertext.converters.loader import load_converters
        from convertext.registry import get_registry
        from convertext_gui.widgets import FILE_TYPES

        load_converters()
        offered = {pat.lstrip('*.') for _, pats in FILE_TYPES for pat in pats}
        missing = set(get_registry().list_supported_formats()) - offered
        assert not missing, f"file dialog cannot select: {sorted(missing)}"

    def test_patterns_are_sequences_not_joined_strings(self):
        """Semicolon-joined patterns are a Win32 form Tk mishandles elsewhere."""
        from convertext_gui.widgets import FILE_TYPES

        for label, patterns in FILE_TYPES:
            assert isinstance(patterns, tuple), label
            assert not any(';' in p for p in patterns), label


class TestConversionThread:
    """Tests for ConversionThread."""

    def _thread(self, **kwargs):
        from convertext_gui.threads import ConversionThread

        params = dict(
            files=[Path("/tmp/test.pdf")],
            formats=["txt"],
            output_dir=None,
            overwrite=False,
            keep_intermediate=False,
            callback=Mock(),
        )
        params.update(kwargs)
        return ConversionThread(**params)

    def test_thread_initialization(self):
        """Test thread initializes with correct parameters."""
        files = [Path("/tmp/test.pdf")]
        formats = ["txt", "epub"]
        output_dir = Path("/tmp/output")
        callback = Mock()

        thread = self._thread(
            files=files,
            formats=formats,
            output_dir=output_dir,
            overwrite=True,
            callback=callback,
        )

        assert thread.files == files
        assert thread.formats == formats
        assert thread.output_dir == output_dir
        assert thread.overwrite is True
        assert thread.keep_intermediate is False
        assert thread.callback is callback

    def test_thread_conversion_success(self):
        """Test successful conversion."""
        mock_result = SimpleNamespace(
            success=True,
            source_path=Path("/tmp/test.pdf"),
            target_path=Path("/tmp/test.txt"),
            error=None,
        )
        thread = self._thread()

        with patch('convertext_gui.threads.ConversionEngine') as engine_cls:
            engine_cls.return_value.convert.return_value = mock_result
            thread.run()

            engine_cls.return_value.convert.assert_called_once()

        assert len(thread.results) == 1
        assert thread.results[0].success is True

    def test_thread_conversion_failure(self):
        """Test conversion failure handling."""
        thread = self._thread()

        with patch('convertext_gui.threads.ConversionEngine') as engine_cls:
            engine_cls.return_value.convert.side_effect = Exception("Conversion failed")
            thread.run()

        assert len(thread.results) == 1
        assert thread.results[0].success is False
        assert "Conversion failed" in thread.results[0].error

    def test_gui_settings_passed_as_engine_overrides(self):
        """GUI settings must reach the engine as overrides.

        convertext applies overrides after the per-file directory config, so
        passing them any other way lets a stray convertext.yaml win.
        """
        thread = self._thread(output_dir=Path("/tmp/output"), overwrite=True)

        with patch('convertext_gui.threads.ConversionEngine') as engine_cls:
            engine_cls.return_value.convert.return_value = SimpleNamespace(
                success=True,
                source_path=Path("/tmp/test.pdf"),
                target_path=Path("/tmp/output/test.txt"),
                error=None,
            )
            thread.run()

        overrides = engine_cls.call_args.kwargs['overrides']
        assert overrides == {'output': {'overwrite': True, 'directory': '/tmp/output'}}

    def test_unchecked_overwrite_is_explicit(self):
        """An unchecked box must override a config file's overwrite: true."""
        thread = self._thread(overwrite=False)

        with patch('convertext_gui.threads.ConversionEngine') as engine_cls:
            engine_cls.return_value.convert.return_value = SimpleNamespace(
                success=True,
                source_path=Path("/tmp/test.pdf"),
                target_path=Path("/tmp/test.txt"),
                error=None,
            )
            thread.run()

        assert engine_cls.call_args.kwargs['overrides']['output']['overwrite'] is False


class TestLoggingConfig:
    """Tests for logging configuration."""

    def test_development_mode_detection(self):
        """Test development mode detection."""
        from convertext_gui.logging_config import is_development_mode

        assert is_development_mode() is True

    def test_setup_logging(self):
        """Test logging setup."""
        from convertext_gui.logging_config import setup_logging
        import logging

        log_file = setup_logging(debug=True)

        assert log_file.exists()
        assert log_file.name.startswith("gui_")

        logger = logging.getLogger()
        assert logger.level == logging.DEBUG
