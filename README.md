# ConverText GUI

Desktop GUI application for ConverText file converter with Monaco monospace typography and minimalist black/yellow design.

Convert between all major document and ebook formats with a single terminal command. Get editable .txt or .md from PDF or ebook formats or make ebooks/PDFs from editable text formats. Work on multiple files at the same time and send them anywhere in the file system instantly.

## Features

- Click-to-browse file selection
- Batch file processing
- All formats supported by ConverText (PDF, DOCX, EPUB, MOBI, etc.)
- Real-time conversion progress with ETA
- Monaco monospace interface
- Black background with yellow accents
- Debug console for verbose logging
- Automatic output directory detection
- Cross-platform (Windows, macOS, Linux)

## Installation

Download the standalone application for your platform:

- **Windows**: ConverText.exe
- **macOS**: ConverText.app
- **Linux**: ConverText.AppImage

No Python installation required!

## Usage

1. Launch ConverText
2. Click "Browse..." to select files
3. Select output formats (EPUB, HTML, TXT, MOBI, FB2, etc.)
4. Choose output directory (defaults to source file location)
5. Click "Convert"

The application shows conversion progress with percentage and ETA. When complete, you can open the output folder directly.

## Keyboard Shortcuts

- `Ctrl+O` - Open file browser
- `Ctrl+Enter` - Start conversion
- `Ctrl+D` - Toggle debug console
- `Ctrl+Q` or `Escape` - Quit application

## Supported Formats

**Input**: PDF, DOCX, DOC, ODT, RTF, TXT, Markdown, HTML, EPUB, MOBI, AZW, FB2

**Output**: TXT, Markdown, HTML, EPUB, MOBI, FB2

## Development

Requires Python 3.10-3.13 with tkinter support and the convertext library.

```bash
# Install dependencies
poetry install

# Run from source
poetry run convertext-gui

# Run tests
poetry run pytest

# Install with development dependencies
poetry install --with dev
```

### macOS tkinter setup

If you get "No module named _tkinter":

```bash
# Install tcl-tk
brew install tcl-tk

# Rebuild Python with tkinter support
env \
  PATH="$(brew --prefix tcl-tk)/bin:$PATH" \
  LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \
  CPPFLAGS="-I$(brew --prefix tcl-tk)/include" \
  PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
  PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
  pyenv install --force 3.13.3

# Reinstall poetry environment
poetry env remove --all
poetry install
```

## License

MIT License
