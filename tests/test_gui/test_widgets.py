"""Tests for GUI widgets."""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch


class TestFileList:
    """Tests for FileList widget."""

    def test_add_files(self):
        """Test adding files to the list."""
        # Mock tkinter to avoid display requirement
        with patch('convertext_gui.widgets.ttk'), \
             patch('convertext_gui.widgets.tk'):

            from convertext_gui.widgets import FileList

            # Create mock parent
            parent = Mock()
            file_list = FileList(parent)

            # Add files
            files = ["/tmp/test1.pdf", "/tmp/test2.docx"]
            file_list.add_files(files)

            # Verify files were added
            assert len(file_list.files) == 2
            assert file_list.files[0] == Path("/tmp/test1.pdf")
            assert file_list.files[1] == Path("/tmp/test2.docx")

    def test_add_duplicate_files(self):
        """Test that duplicate files are not added."""
        with patch('convertext_gui.widgets.ttk'), \
             patch('convertext_gui.widgets.tk'):

            from convertext_gui.widgets import FileList

            parent = Mock()
            file_list = FileList(parent)

            # Add same file twice
            file_list.add_files(["/tmp/test.pdf"])
            file_list.add_files(["/tmp/test.pdf"])

            # Should only have one file
            assert len(file_list.files) == 1

    def test_clear(self):
        """Test clearing the file list."""
        with patch('convertext_gui.widgets.ttk'), \
             patch('convertext_gui.widgets.tk'):

            from convertext_gui.widgets import FileList

            parent = Mock()
            file_list = FileList(parent)

            # Add files then clear
            file_list.add_files(["/tmp/test1.pdf", "/tmp/test2.docx"])
            file_list.clear()

            # Verify cleared
            assert len(file_list.files) == 0
            assert len(file_list.file_widgets) == 0


class TestConversionThread:
    """Tests for ConversionThread."""

    def test_thread_initialization(self):
        """Test thread initializes with correct parameters."""
        from convertext_gui.threads import ConversionThread

        engine = Mock()
        files = [Path("/tmp/test.pdf")]
        formats = ["txt", "epub"]
        output_dir = Path("/tmp/output")
        callback = Mock()

        thread = ConversionThread(
            engine=engine,
            files=files,
            formats=formats,
            output_dir=output_dir,
            overwrite=True,
            keep_intermediate=False,
            callback=callback
        )

        assert thread.engine == engine
        assert thread.files == files
        assert thread.formats == formats
        assert thread.output_dir == output_dir
        assert thread.overwrite is True
        assert thread.keep_intermediate is False

    def test_thread_conversion_success(self):
        """Test successful conversion."""
        from convertext_gui.threads import ConversionThread
        from types import SimpleNamespace

        # Mock successful conversion
        mock_result = SimpleNamespace(
            success=True,
            source_path=Path("/tmp/test.pdf"),
            target_path=Path("/tmp/test.txt"),
            error=None
        )

        engine = Mock()
        engine.convert = Mock(return_value=mock_result)
        callback = Mock()

        thread = ConversionThread(
            engine=engine,
            files=[Path("/tmp/test.pdf")],
            formats=["txt"],
            output_dir=None,
            overwrite=False,
            keep_intermediate=False,
            callback=callback
        )

        thread.run()

        # Verify conversion was called
        engine.convert.assert_called_once()
        assert len(thread.results) == 1
        assert thread.results[0].success is True

    def test_thread_conversion_failure(self):
        """Test conversion failure handling."""
        from convertext_gui.threads import ConversionThread

        # Mock failed conversion
        engine = Mock()
        engine.convert = Mock(side_effect=Exception("Conversion failed"))
        callback = Mock()

        thread = ConversionThread(
            engine=engine,
            files=[Path("/tmp/test.pdf")],
            formats=["txt"],
            output_dir=None,
            overwrite=False,
            keep_intermediate=False,
            callback=callback
        )

        thread.run()

        # Verify error was handled
        assert len(thread.results) == 1
        assert thread.results[0].success is False
        assert "Conversion failed" in thread.results[0].error


class TestLoggingConfig:
    """Tests for logging configuration."""

    def test_development_mode_detection(self):
        """Test development mode detection."""
        from convertext_gui.logging_config import is_development_mode

        # In test environment, should be development mode
        assert is_development_mode() is True

    def test_setup_logging(self):
        """Test logging setup."""
        from convertext_gui.logging_config import setup_logging
        import logging

        log_file = setup_logging(debug=True)

        # Verify log file was created
        assert log_file.exists()
        assert log_file.name.startswith("gui_")

        # Verify logging is configured
        logger = logging.getLogger()
        assert logger.level == logging.DEBUG
