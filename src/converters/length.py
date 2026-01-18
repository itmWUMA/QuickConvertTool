"""Length unit converter implementation."""

from typing import List
from ..core.converter import Converter


class LengthConverter(Converter):
    """
    Converter for length units.

    Supports: meter, kilometer, centimeter, millimeter, mile, yard, foot, inch
    Base unit: meter (m)
    """

    # Conversion factors to meters (1 unit = X meters)
    _TO_METERS = {
        "m": 1.0,
        "km": 1000.0,
        "cm": 0.01,
        "mm": 0.001,
        "mile": 1609.344,
        "yard": 0.9144,
        "ft": 0.3048,
        "inch": 0.0254,
    }

    @property
    def name(self) -> str:
        """Return the display name of this converter."""
        return "Length"

    @property
    def units(self) -> List[str]:
        """Return a list of all supported units."""
        return list(self._TO_METERS.keys())

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert a value from one length unit to another.

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

        # Convert to base unit (meters) then to target unit
        meters = value * self._TO_METERS[from_unit]
        result = meters / self._TO_METERS[to_unit]

        return result
