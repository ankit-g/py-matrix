# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `pyneorain`, a Python terminal screensaver that creates a Matrix-style rain effect with characters from multiple languages (Sanskrit, English, Greek, Kannada, and numbers). The project has both synchronous and asynchronous implementations.

## Architecture

The codebase consists of:

- `pyneorain.py`: Main synchronous implementation with the `Bar` class and matrix rain logic
- `v2rain.py`: Asynchronous version using asyncio with producer-consumer pattern and signal handling
- `config/config.toml`: Configuration file defining character sets for different languages
- `setup.py`: Package configuration for PyPI distribution

### Core Components

- **Bar class** (`pyneorain.py:20`): Represents individual falling character streams with position tracking, length, and gap management
- **Matrix rendering**: 2D array representing terminal screen, updated by Bar objects
- **Character sets**: Defined in both hardcoded arrays and config TOML file
- **Terminal handling**: Uses `blessed` library for cursor control and terminal manipulation

## Development Commands

### Running the Application
```bash
python pyneorain.py          # Synchronous version
python v2rain.py             # Asynchronous version
pyneorain                    # If installed via pip
```

### Building and Publishing
```bash
python setup.py sdist        # Build source distribution
twine upload dist/*          # Publish to PyPI
```

### Development Tools
```bash
make clean                   # Clean build artifacts and logs
make publish                 # Build and publish to PyPI
```

### Profiling (from README)
```bash
kernprof -l pyneorain.py     # Line profiling
python -m line_profiler pyneorain.py.lprof  # View line profile
mprof run pyneorain.py       # Memory profiling
mprof plot                   # Plot memory usage
```

## Dependencies

Core dependencies (from setup.py):
- `blessed`: Terminal control and formatting
- `six`: Python 2/3 compatibility
- `wcwidth`: Character width calculation

Development dependencies include profiling tools (`line-profiler`, `memory-profiler`) and build tools (`twine`, `ruff` for linting).

## Key Implementation Details

- The async version (`v2rain.py`) uses signal handlers for SIGWINCH (resize) and SIGINT (interrupt)
- Character rendering uses ANSI escape codes for green coloring
- Matrix updates happen at 24 FPS (1/24 second sleep)
- Terminal resize is handled by reinitializing the matrix and columns
- The Bar class manages individual character streams with configurable length and gaps