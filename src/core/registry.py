"""Converter registry for managing and accessing all converters."""

from typing import Dict, List, Type
from .converter import Converter


class ConverterRegistry:
    """
    Central registry for all converter implementations.

    This class manages converter instances and provides a unified interface
    for accessing them.
    """

    def __init__(self):
        """Initialize the registry with an empty converter dictionary."""
        self._converters: Dict[str, Converter] = {}

    def register(self, converter: Converter) -> None:
        """
        Register a converter instance.

        Args:
            converter: An instance of a Converter subclass

        Raises:
            ValueError: If a converter with the same name is already registered
        """
        if converter.name in self._converters:
            raise ValueError(
                f"Converter '{converter.name}' is already registered"
            )
        self._converters[converter.name] = converter

    def get_converter(self, name: str) -> Converter:
        """
        Retrieve a converter by name.

        Args:
            name: The name of the converter to retrieve

        Returns:
            Converter: The requested converter instance

        Raises:
            KeyError: If no converter with the given name is registered
        """
        if name not in self._converters:
            raise KeyError(f"No converter named '{name}' is registered")
        return self._converters[name]

    def get_all_converters(self) -> List[Converter]:
        """
        Get a list of all registered converters.

        Returns:
            List[Converter]: List of all converter instances
        """
        return list(self._converters.values())

    def get_converter_names(self) -> List[str]:
        """
        Get a list of all registered converter names.

        Returns:
            List[str]: List of converter names
        """
        return list(self._converters.keys())

    def has_converter(self, name: str) -> bool:
        """
        Check if a converter with the given name is registered.

        Args:
            name: The name to check

        Returns:
            bool: True if the converter is registered, False otherwise
        """
        return name in self._converters

    def unregister(self, name: str) -> None:
        """
        Unregister a converter by name.

        Args:
            name: The name of the converter to unregister

        Raises:
            KeyError: If no converter with the given name is registered
        """
        if name not in self._converters:
            raise KeyError(f"No converter named '{name}' is registered")
        del self._converters[name]

    def clear(self) -> None:
        """Remove all registered converters."""
        self._converters.clear()


# Global registry instance
_global_registry = ConverterRegistry()


def get_global_registry() -> ConverterRegistry:
    """
    Get the global converter registry instance.

    Returns:
        ConverterRegistry: The global registry
    """
    return _global_registry
