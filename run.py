#!/usr/bin/env python
"""
QuickConvertTool - Launcher script

This script provides a convenient way to run the application from the
project root directory.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the main application
from src.main import main

if __name__ == "__main__":
    main()
