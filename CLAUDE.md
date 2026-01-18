# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

QuickConvertTool is a desktop conversion utility application designed for extensibility and ease of use. The tool supports various types of conversions including:
- Unit conversions (length, weight, temperature, etc.)
- Currency conversions
- Other extensible conversion types

**Key Design Goals:**
- **Extensibility**: The framework must allow easy addition of new conversion types
- **Reusability**: Components should be modular and reusable
- **User-friendly**: Simple desktop interface for quick conversions
- **Developer-friendly**: Clean architecture for programmers to extend functionality

## Project Context

- **Developer Background**: The primary user is a game programmer with limited frontend experience
- **Communication**: Use Chinese (中文) when communicating with the user, but keep code, comments, and technical documentation in English for broader compatibility
- **Current State**: This is a new project being set up from scratch

## Architecture Principles

When developing this codebase, follow these architectural principles:

1. **Plugin/Module Architecture**: Design conversion types as independent modules that can be registered with the core framework
2. **Separation of Concerns**: Keep UI, business logic, and data layers separated
3. **Configuration-driven**: Allow conversions to be defined via configuration where possible
4. **Type Safety**: Use strong typing to prevent runtime errors

## Technology Stack Considerations

Since the developer has game programming experience but limited frontend knowledge, consider:
- Desktop frameworks that are approachable (Electron, Tauri, or native solutions)
- Clear separation between UI and logic layers
- Well-documented, mainstream technologies with good tooling support

## Recommended Project Structure

```
src/
  core/           # Core conversion engine and framework
  converters/     # Individual conversion modules
  ui/             # User interface components
  config/         # Configuration files
  utils/          # Shared utilities
tests/            # Test files
docs/             # Documentation
```

## Development Workflow

When adding new conversion types:
1. Create a new module in `converters/` following the established interface
2. Register the converter with the core engine
3. Update configuration if needed
4. Add tests for the new converter

## Important Notes

- Prioritize code clarity over cleverness given the developer's background
- Provide clear examples when introducing new patterns
- Keep the UI simple and intuitive
- Ensure all conversion logic is testable independently of the UI
