"""QuickConvertTool - Main application entry point."""

from .core.registry import get_global_registry
from .converters import LengthConverter, TemperatureConverter, WeightConverter, BatteryConverter
from .ui import MainWindow


def main():
    """
    Main entry point for QuickConvertTool.

    Initializes all converters, registers them with the global registry,
    and launches the GUI application.
    """
    # Get the global registry
    registry = get_global_registry()

    # Register all converters
    registry.register(LengthConverter())
    registry.register(TemperatureConverter())
    registry.register(WeightConverter())
    registry.register(BatteryConverter())

    # Create and run the main window
    app = MainWindow(registry)
    app.run()


if __name__ == "__main__":
    main()
