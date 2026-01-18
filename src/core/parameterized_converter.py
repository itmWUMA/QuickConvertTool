"""Parameterized converter base class for converters with extra parameters."""

from typing import List, Optional, Dict, Any
from .converter import Converter


class ParameterizedConverter(Converter):
    """
    Base class for converters that require additional parameters.

    This extends the Converter base class to support conversion operations
    that need extra parameters beyond value, from_unit, and to_unit.

    Subclasses should implement the _convert_with_params method to handle
    parameterized conversions.
    """

    @property
    def parameters(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        Return parameter configuration for this converter.

        Returns None if no parameters are needed. Otherwise returns a dict
        where keys are parameter names and values are configuration dicts with
        the following structure:
            {
                "label": "Display label for the parameter",
                "default": "Default value as string",
                "required": True/False
            }

        Returns:
            Optional[Dict[str, Dict[str, Any]]]: Parameter configuration or None
        """
        return None

    def convert(self, value: float, from_unit: str, to_unit: str, **kwargs) -> float:
        """
        Convert a value from one unit to another with optional parameters.

        Args:
            value: The numerical value to convert
            from_unit: The source unit
            to_unit: The target unit
            **kwargs: Additional parameters required by the converter

        Returns:
            float: The converted value

        Raises:
            ValueError: If either unit is not supported or parameters are invalid
        """
        self.validate_unit(from_unit)
        self.validate_unit(to_unit)

        if from_unit == to_unit:
            return value

        return self._convert_with_params(value, from_unit, to_unit, **kwargs)

    def _convert_with_params(self, value: float, from_unit: str, to_unit: str, **kwargs) -> float:
        """
        Perform the actual conversion with parameters.

        Subclasses must implement this method to handle the conversion logic.

        Args:
            value: The numerical value to convert
            from_unit: The source unit
            to_unit: The target unit
            **kwargs: Additional parameters from the user

        Returns:
            float: The converted value

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _convert_with_params method"
        )
