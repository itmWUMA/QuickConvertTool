# Agent Guidelines for QuickConvertTool

This document provides guidance for agentic coding assistants working on this Python-based desktop conversion utility.

## Commands

### Running the Application
```bash
# Run the application
python run.py

# Alternative method
python -m src.main
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run single test file
pytest tests/test_length.py -v

# Run specific test function
pytest tests/test_length.py::TestLengthConverter::test_meter_to_kilometer -v

# Run tests with coverage report
pytest tests/ --cov=src --cov-report=html

# Run tests in a specific class
pytest tests/test_length.py::TestLengthConverter -v
```

### Code Quality (Optional)
```bash
# Format code (if black is installed)
black src/ tests/

# Lint code (if pylint is installed)
pylint src/
```

## Code Style Guidelines

### Import Organization
- Standard library imports first
- Third-party imports second
- Local imports third (use relative imports within the package)
```python
import tkinter as tk
from typing import List, Optional
from .core.converter import Converter
```

### Type Annotations
- All functions must have type hints
- Use `typing` module for generic types
- Return types in properties and methods
```python
def convert(self, value: float, from_unit: str, to_unit: str) -> float:
    pass
```

### Docstrings
- Use triple double-quoted docstrings
- Include Args, Returns, and Raises sections where applicable
- One-line summary followed by detailed description
```python
def convert(self, value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a value from one unit to another.

    Args:
        value: The numerical value to convert
        from_unit: The source unit
        to_unit: The target unit

    Returns:
        float: The converted value

    Raises:
        ValueError: If either unit is not supported
    """
```

### Naming Conventions
- **Classes**: PascalCase (e.g., `LengthConverter`, `MainWindow`)
- **Functions/Methods**: snake_case (e.g., `get_converter`, `_on_unit_changed`)
- **Variables**: snake_case (e.g., `from_unit_var`, `to_meters`)
- **Constants**: ALL_CAPS with leading underscore for private class constants (e.g., `_TO_METERS`, `_UNITS`)
- **Private members**: Leading underscore (e.g., `_to_celsius`, `_create_widgets`)

### Error Handling
- Validate inputs and raise `ValueError` with descriptive messages
- Use context managers where appropriate
- Gracefully handle expected exceptions in UI code
```python
if unit not in self.units:
    raise ValueError(
        f"Unsupported unit '{unit}' for {self.name} converter. "
        f"Supported units: {', '.join(self.units)}"
    )
```

### File Structure
- Each converter in `src/converters/` inherits from `Converter` ABC
- Tests mirror the `src/` structure in `tests/`
- Use `__init__.py` for clean imports
- Entry point: `src/main.py`

### Architecture Principles
- **Plugin pattern**: Converters are registered dynamically
- **Single responsibility**: Each converter handles one conversion type
- **Separation of concerns**: UI layer independent of conversion logic
- **Type safety**: Strong typing throughout the codebase

### Adding New Converters
1. Create class inheriting from `Converter` in `src/converters/`
2. Implement `name`, `units` properties and `convert()` method
3. Register in `src/main.py`
4. Add comprehensive tests in `tests/`

### Testing Guidelines
- Use pytest framework
- Create test classes for each converter (e.g., `TestLengthConverter`)
- Use fixtures for setup
- Test edge cases: zero, negative, invalid inputs, same unit
- Name tests descriptively: `test_meter_to_kilometer`

### Communication Language
- **Code/comments**: English for international compatibility
- **User communication**: Chinese (中文) as per CLAUDE.md

### Important Notes
- No comments in code unless asked by user
- Keep tests independent and fast
- Follow existing patterns when adding features
- Tkinter for UI - keep desktop GUI simple and responsive
