# Contributing to ConverText GUI

Thank you for your interest in contributing to ConverText GUI!

## Reporting Issues

**Bug Reports**: Include the following:
- Operating system and version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Log files (Help → View Logs in the app)

**Feature Requests**: Describe the use case and why the feature would be valuable.

## Development Setup

### Prerequisites
- Python 3.10-3.13
- Poetry for dependency management
- tkinter support (pre-installed on most systems)

### Setup

```bash
# Clone both repositories
git clone https://github.com/danielcorsano/convertext.git
git clone https://github.com/danielcorsano/convertext-gui.git

# Install dependencies
cd convertext-gui
poetry install --with dev,build

# Run from source
poetry run convertext-gui

# Run tests
poetry run pytest
```

### macOS tkinter setup

If you encounter `No module named _tkinter`:

```bash
brew install tcl-tk
env \
  PATH="$(brew --prefix tcl-tk)/bin:$PATH" \
  LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \
  CPPFLAGS="-I$(brew --prefix tcl-tk)/include" \
  PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
  PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
  pyenv install --force 3.13.3

poetry env remove --all
poetry install
```

## Code Guidelines

- **Style**: Follow PEP 8
- **Comments**: Minimal - use descriptive names and docstrings
- **Modularity**: Keep functions focused and reusable
- **Testing**: Add tests for new features

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes with clear commit messages
4. Run tests: `poetry run pytest`
5. Push and create a pull request

**PR Guidelines**:
- Describe what the PR does and why
- Reference related issues
- Include screenshots for UI changes
- Ensure all tests pass

## Building

Build executables using the build scripts:

```bash
# macOS
poetry run python build_scripts/build_macos.py

# Windows (on Windows)
poetry run python build_scripts/build_windows.py

# Linux (on Linux)
poetry run python build_scripts/build_linux.py
```

Or use GitHub Actions (triggers on version tags).

## Code of Conduct

- Be respectful and constructive
- Focus on the technical merits
- Help newcomers learn and contribute

## Questions?

Open a GitHub Discussion for general questions or use Issues for bugs/features.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
