# ConverText GUI

Desktop GUI application for ConverText file converter.

## Features

- Drag-and-drop file conversion
- Batch processing
- All formats supported by ConverText
- Modern dark-themed interface
- Cross-platform (Windows, macOS, Linux)

## Installation

Download the standalone application for your platform:

- **Windows**: ConvertExt.exe
- **macOS**: ConvertExt.app
- **Linux**: ConvertExt.AppImage

No Python installation required!

## Usage

1. Launch the application
2. Drag files into the drop zone (or click to browse)
3. Select output formats (EPUB, HTML, TXT, etc.)
4. Choose output directory
5. Click "Convert"

The application will show progress and open the output folder when complete.

## Keyboard Shortcuts

- `Ctrl+O` - Open file browser
- `Ctrl+Enter` - Start conversion
- `Escape` - Close window

## Supported Formats

**Input**: PDF, DOCX, DOC, ODT, RTF, TXT, Markdown, HTML, EPUB, MOBI, AZW, FB2

**Output**: TXT, Markdown, HTML, EPUB, MOBI, FB2

## Development

Requires Python 3.10-3.13 and the convertext library.

```bash
poetry install
convertext-gui
```

## License

MIT License
