"""Data size unit converter implementation."""

from typing import List
from ..core.converter import Converter


class DataUnitConverter(Converter):
    """
    Converter for data size units.

    Supports: bit, byte, KB, MB, GB, TB, KiB, MiB, GiB, TiB
    Base unit: bit
    """

    _TO_BITS = {
        "bit": 1.0,
        "byte": 8.0,
        "KB": 8_192.0,
        "MB": 8_388_608.0,
        "GB": 8_589_934_592.0,
        "TB": 8_796_093_022_208.0,
        "KiB": 8_192.0,
        "MiB": 8_388_608.0,
        "GiB": 8_589_934_592.0,
        "TiB": 8_796_093_022_208.0,
    }

    @property
    def name(self) -> str:
        """Return the display name of this converter."""
        return "数据单位"

    @property
    def units(self) -> List[str]:
        """Return a list of all supported units."""
        return list(self._TO_BITS.keys())

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert a value from one data size unit to another.

        Args:
            value: The numerical value to convert
            from_unit: The source unit
            to_unit: The target unit

        Returns:
            float: The converted value

        Raises:
            ValueError: If either unit is not supported
        """
        self.validate_unit(from_unit)
        self.validate_unit(to_unit)

        if from_unit == to_unit:
            return value

        bits = value * self._TO_BITS[from_unit]
        return bits / self._TO_BITS[to_unit]
