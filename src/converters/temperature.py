"""Temperature unit converter implementation."""

from typing import List
from ..core.converter import Converter


class TemperatureConverter(Converter):
    """
    Converter for temperature units.

    Supports: Celsius (C), Fahrenheit (F), Kelvin (K)
    Base unit: Celsius (C)

    Conversion formulas:
    - C to F: (C × 9/5) + 32
    - C to K: C + 273.15
    - F to C: (F - 32) × 5/9
    - K to C: K - 273.15
    """

    _UNITS = ["C", "F", "K"]

    @property
    def name(self) -> str:
        """Return the display name of this converter."""
        return "温度"

    @property
    def units(self) -> List[str]:
        """Return a list of all supported units."""
        return self._UNITS.copy()

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert a value from one temperature unit to another.

        Args:
            value: The numerical value to convert
            from_unit: The source unit (C, F, or K)
            to_unit: The target unit (C, F, or K)

        Returns:
            float: The converted value

        Raises:
            ValueError: If either unit is not supported
        """
        # Validate units
        self.validate_unit(from_unit)
        self.validate_unit(to_unit)

        # If units are the same, return the original value
        if from_unit == to_unit:
            return value

        # Convert to Celsius first
        celsius = self._to_celsius(value, from_unit)

        # Convert from Celsius to target unit
        result = self._from_celsius(celsius, to_unit)

        return result

    def _to_celsius(self, value: float, from_unit: str) -> float:
        """
        Convert any temperature unit to Celsius.

        Args:
            value: The temperature value
            from_unit: The source unit

        Returns:
            float: Temperature in Celsius
        """
        if from_unit == "C":
            return value
        elif from_unit == "F":
            return (value - 32) * 5 / 9
        elif from_unit == "K":
            return value - 273.15
        else:
            raise ValueError(f"Unknown unit: {from_unit}")

    def _from_celsius(self, celsius: float, to_unit: str) -> float:
        """
        Convert Celsius to any temperature unit.

        Args:
            celsius: Temperature in Celsius
            to_unit: The target unit

        Returns:
            float: Temperature in the target unit
        """
        if to_unit == "C":
            return celsius
        elif to_unit == "F":
            return (celsius * 9 / 5) + 32
        elif to_unit == "K":
            return celsius + 273.15
        else:
            raise ValueError(f"Unknown unit: {to_unit}")
