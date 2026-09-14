# Release Notes

Desktop application for converting between text, document, and ebook formats.

## v0.3.0 (2026-09-14)

Built on convertext 0.4.0.

### Fixed

- Output directory and the Overwrite checkbox are now always respected. A `convertext.yaml`
  in the source file's directory (or any parent) could silently override both.
- An unchecked Overwrite box now overrides `overwrite: true` from a configuration file,
  instead of being ignored.

### Changed

- MOBI output carries the source's own chapter navigation, tappable chapter links, a Go To
  table of contents and a cover thumbnail.
- Inline images are carried from EPUB, HTML, DOCX and PDF sources into EPUB and MOBI output.
- DOCX, PDF and EPUB convert directly to EPUB and MOBI rather than through a lossy
  intermediate format.
- AZW3 is no longer offered as an output format — it is still beta upstream and unreliable
  on Kindle devices. Use MOBI for Kindle. Reading `.azw` and `.azw3` files is unaffected.
- The file browser can now select `.htm` and `.markdown` files.

### Supported Formats

**Input**: PDF, DOCX, DOC, ODT, RTF, TXT, Markdown, HTML, EPUB, MOBI, AZW, AZW3, FB2

**Output**: PDF, DOCX, RTF, TXT, Markdown, HTML, EPUB, MOBI, FB2

### Keyboard Shortcuts

- `Ctrl+O` - Open file browser
- `Ctrl+Enter` - Start conversion
- `Ctrl+D` - Toggle debug console
- `Ctrl+Q` or `Escape` - Quit application

### Builds

- **macOS**: ConverText.dmg
- **Windows**: ConverText.exe
- **Linux**: ConverText-linux.tar.gz

## v0.1.0-beta (2025-10-19)

Initial beta release on all three platforms.
