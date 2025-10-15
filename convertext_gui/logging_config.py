"""Logging configuration for GUI."""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logging(debug=False):
    """Configure logging for the application."""
    # Create logs directory
    log_dir = Path.home() / ".convertext"
    log_dir.mkdir(exist_ok=True)

    # Log file with timestamp
    log_file = log_dir / f"gui_{datetime.now().strftime('%Y%m%d')}.log"

    # Configure root logger
    level = logging.DEBUG if debug else logging.INFO

    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # File handler (always logs DEBUG level)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler (respects debug flag)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)

    if debug:
        root_logger.addHandler(console_handler)

    return log_file


def is_development_mode():
    """Check if running from source (development) vs built executable."""
    return not getattr(sys, 'frozen', False)
