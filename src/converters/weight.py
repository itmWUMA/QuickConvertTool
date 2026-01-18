"""Weight unit converter implementation."""

from typing import List
from ..core.converter import Converter


class WeightConverter(Converter):
    """
    Converter for weight/mass units.

    Supports: kilogram, gram, milligram, ton, pound, ounce
    Base unit: kilogram (kg)
    """

    # Conversion factors to kilograms (1 unit = X kilograms)
    _TO_KILOGRAMS = {
        "kg": 1.0,
        "g": 0.001,
        "mg": 0.000001,
        "ton": 1000.0,
        "lb": 0.45359237,
        "oz": 0.028349523125,
    }

    @property
    def name(self) -> str:
        """Return the display name of this converter."""
        return "Weight"

    @property
    def units(self) -> List[str]:
        """Return a list of all supported units."""
        return list(self._TO_KILOGRAMS.keys())

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert a value from one weight unit to another.

        Args:
            value: The numerical value to convert
            from_unit: The source unit
            to_unit: The target unit

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

        # Convert to base unit (kilograms) then to target unit
        kilograms = value * self._TO_KILOGRAMS[from_unit]
        result = kilograms / self._TO_KILOGRAMS[to_unit]

        return result
