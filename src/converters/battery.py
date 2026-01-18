"""Battery capacity converter implementation."""

from typing import List
from ..core.parameterized_converter import ParameterizedConverter


class BatteryConverter(ParameterizedConverter):
    """
    Converter for battery capacity units.

    Supports: milliampere-hour (mAh), ampere-hour (Ah), watt-hour (Wh), kilowatt-hour (kWh)
    Base units: Ah for charge, Wh for energy

    Conversion formulas:
    - Charge units: 1 Ah = 1000 mAh
    - Energy units: 1 kWh = 1000 Wh
    - Charge to energy: Wh = (Ah × voltage)
    - Energy to charge: Ah = (Wh / voltage)
    """

    _CHARGE_UNITS = ["mAh", "Ah"]
    _ENERGY_UNITS = ["Wh", "kWh"]

    @property
    def name(self) -> str:
        """Return the display name of this converter."""
        return "Battery"

    @property
    def units(self) -> List[str]:
        """Return a list of all supported units."""
        return self._CHARGE_UNITS + self._ENERGY_UNITS

    @property
    def parameters(self) -> dict:
        """
        Return parameter configuration for voltage.

        Returns:
            dict: Configuration for the voltage parameter
        """
        return {
            "voltage": {
                "label": "Voltage (V)",
                "default": "3.7",
                "required": True
            }
        }

    def _convert_with_params(self, value: float, from_unit: str, to_unit: str, voltage: float = 3.7, **kwargs) -> float:
        """
        Convert battery capacity units with voltage parameter.

        Args:
            value: The numerical value to convert
            from_unit: The source unit
            to_unit: The target unit
            voltage: The voltage in volts (default 3.7V for lithium batteries)
            **kwargs: Additional ignored parameters

        Returns:
            float: The converted value

        Raises:
            ValueError: If voltage is invalid
        """
        if voltage <= 0:
            raise ValueError(f"Voltage must be positive, got {voltage}V")

        from_charge = from_unit in self._CHARGE_UNITS
        to_charge = to_unit in self._CHARGE_UNITS

        if from_charge and to_charge:
            return self._convert_charge(value, from_unit, to_unit)
        elif not from_charge and not to_charge:
            return self._convert_energy(value, from_unit, to_unit)
        elif from_charge and not to_charge:
            return self._convert_charge_to_energy(value, from_unit, to_unit, voltage)
        else:
            return self._convert_energy_to_charge(value, from_unit, to_unit, voltage)

    def _convert_charge(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert between charge units (mAh, Ah)."""
        from_mah = self._to_mah(value, from_unit)
        return self._from_mah(from_mah, to_unit)

    def _convert_energy(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert between energy units (Wh, kWh)."""
        from_wh = self._to_wh(value, from_unit)
        return self._from_wh(from_wh, to_unit)

    def _convert_charge_to_energy(self, value: float, from_unit: str, to_unit: str, voltage: float) -> float:
        """Convert from charge units to energy units."""
        ah = self._to_ah(value, from_unit)
        wh = ah * voltage
        return self._from_wh(wh, to_unit)

    def _convert_energy_to_charge(self, value: float, from_unit: str, to_unit: str, voltage: float) -> float:
        """Convert from energy units to charge units."""
        wh = self._to_wh(value, from_unit)
        ah = wh / voltage
        return self._from_ah(ah, to_unit)

    def _to_mah(self, value: float, unit: str) -> float:
        """Convert any charge unit to mAh."""
        if unit == "mAh":
            return value
        elif unit == "Ah":
            return value * 1000
        else:
            raise ValueError(f"Unknown charge unit: {unit}")

    def _from_mah(self, mAh: float, unit: str) -> float:
        """Convert from mAh to any charge unit."""
        if unit == "mAh":
            return mAh
        elif unit == "Ah":
            return mAh / 1000
        else:
            raise ValueError(f"Unknown charge unit: {unit}")

    def _to_ah(self, value: float, unit: str) -> float:
        """Convert any charge unit to Ah."""
        if unit == "Ah":
            return value
        elif unit == "mAh":
            return value / 1000
        else:
            raise ValueError(f"Unknown charge unit: {unit}")

    def _from_ah(self, ah: float, unit: str) -> float:
        """Convert from Ah to any charge unit."""
        if unit == "Ah":
            return ah
        elif unit == "mAh":
            return ah * 1000
        else:
            raise ValueError(f"Unknown charge unit: {unit}")

    def _to_wh(self, value: float, unit: str) -> float:
        """Convert any energy unit to Wh."""
        if unit == "Wh":
            return value
        elif unit == "kWh":
            return value * 1000
        else:
            raise ValueError(f"Unknown energy unit: {unit}")

    def _from_wh(self, wh: float, unit: str) -> float:
        """Convert from Wh to any energy unit."""
        if unit == "Wh":
            return wh
        elif unit == "kWh":
            return wh / 1000
        else:
            raise ValueError(f"Unknown energy unit: {unit}")
