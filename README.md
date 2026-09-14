# ConverText GUI

Desktop GUI application for ConverText file converter with Monaco monospace typography and minimalist black/yellow design.

Convert between all major document and ebook formats with a single click. Get editable .txt or .md from PDF or ebook formats, or create ebooks, PDFs, and Word documents from any supported format. Work on multiple files at the same time and send them anywhere in the file system instantly.

## Features

- Click-to-browse file selection
- Batch file processing
- Real-time conversion progress with ETA
- Debug console for verbose logging
- Automatic output directory detection
- Cross-platform (Windows, macOS, Linux)

MOBI output carries the source's own chapter navigation, tappable chapter links, a Go To
table of contents and a cover thumbnail. Inline images are carried from EPUB, HTML, DOCX
and PDF sources into EPUB and MOBI output.

## Installation

Download the latest release for your platform from [GitHub Releases](https://github.com/danielcorsano/convertext-gui/releases):

- **macOS**: ConverText.dmg
- **Windows**: ConverText.exe
- **Linux**: ConverText-linux.tar.gz

No Python installation required. The macOS build gets the most testing; please report
Windows and Linux issues on GitHub Issues.

## Usage

1. Launch ConverText
2. Click "Browse..." to select files
3. Select output formats (PDF, DOCX, RTF, TXT, Markdown, HTML, EPUB, MOBI, FB2)
4. Choose output directory (defaults to source file location)
5. Click "Convert"

The application shows conversion progress with percentage and ETA. When complete, you can open the output folder directly.

## Keyboard Shortcuts

- `Ctrl+O` - Open file browser
- `Ctrl+Enter` - Start conversion
- `Ctrl+D` - Toggle debug console
- `Ctrl+Q` or `Escape` - Quit application

## Supported Formats

**Input**: PDF, DOCX, DOC, ODT, RTF, TXT, Markdown, HTML, EPUB, MOBI, AZW, AZW3, FB2

**Output**: PDF, DOCX, RTF, TXT, Markdown, HTML, EPUB, MOBI, FB2

AZW3 output is not offered: it is still beta upstream and unreliable on Kindle devices.
Use MOBI for Kindle. Reading `.azw` and `.azw3` files works normally.

## 💝 Support This Project

If you find this tool helpful, please consider [sponsoring the project](https://github.com/sponsors/danielcorsano). I created and maintain this software alone as a public service, and donations help me improve it and develop requested features. If I get $99 of donations, I will use it to pay for the Apple developer program so I can make iOS versions of all my open source apps.

Your support makes a real difference in keeping this project active and growing. Thank you!

## License

MIT License
