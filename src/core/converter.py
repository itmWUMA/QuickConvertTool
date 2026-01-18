"""Abstract base class for all converters."""

from abc import ABC, abstractmethod
from typing import List


class Converter(ABC):
    """
    Abstract base class for all unit converters.

    All converter implementations must inherit from this class and implement
    the required properties and methods.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the display name of this converter.

        Returns:
            str: Human-readable name (e.g., "Length", "Temperature")
        """
        pass

    @property
    @abstractmethod
    def units(self) -> List[str]:
        """
        Return a list of all supported units for this converter.

        Returns:
            List[str]: List of unit names (e.g., ["m", "km", "cm"])
        """
        pass

    @abstractmethod
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
        pass

    def validate_unit(self, unit: str) -> None:
        """
        Validate that a unit is supported by this converter.

        Args:
            unit: The unit to validate

        Raises:
            ValueError: If the unit is not supported
        """
        if unit not in self.units:
            raise ValueError(
                f"Unsupported unit '{unit}' for {self.name} converter. "
                f"Supported units: {', '.join(self.units)}"
            )
