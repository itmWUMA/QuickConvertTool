"""Unit tests for the Battery converter."""

import pytest
from src.converters.battery import BatteryConverter


class TestBatteryConverter:
    """Test suite for BatteryConverter."""

    @pytest.fixture
    def converter(self):
        """Create a BatteryConverter instance for testing."""
        return BatteryConverter()

    def test_converter_name(self, converter):
        """Test that the converter has the correct name."""
        assert converter.name == "Battery"

    def test_supported_units(self, converter):
        """Test that all expected units are supported."""
        expected_units = ["mAh", "Ah", "Wh", "kWh"]
        assert set(converter.units) == set(expected_units)

    def test_parameters_config(self, converter):
        """Test that the parameter configuration is correct."""
        params = converter.parameters
        assert params is not None
        assert "voltage" in params
        assert params["voltage"]["label"] == "Voltage (V)"
        assert params["voltage"]["default"] == "3.7"
        assert params["voltage"]["required"] is True

    def test_mah_to_ah(self, converter):
        """Test conversion from milliampere-hours to ampere-hours."""
        assert converter.convert(1000, "mAh", "Ah") == 1.0
        assert converter.convert(2000, "mAh", "Ah") == 2.0
        assert converter.convert(500, "mAh", "Ah") == 0.5

    def test_ah_to_mah(self, converter):
        """Test conversion from ampere-hours to milliampere-hours."""
        assert converter.convert(1, "Ah", "mAh") == 1000
        assert converter.convert(2.5, "Ah", "mAh") == 2500

    def test_wh_to_kwh(self, converter):
        """Test conversion from watt-hours to kilowatt-hours."""
        assert converter.convert(1000, "Wh", "kWh") == 1.0
        assert converter.convert(500, "Wh", "kWh") == 0.5

    def test_kwh_to_wh(self, converter):
        """Test conversion from kilowatt-hours to watt-hours."""
        assert converter.convert(1, "kWh", "Wh") == 1000
        assert converter.convert(2.5, "kWh", "Wh") == 2500

    def test_mah_to_wh_with_voltage(self, converter):
        """Test conversion from mAh to Wh with voltage parameter."""
        result = converter.convert(1000, "mAh", "Wh", voltage=3.7)
        assert abs(result - 3.7) < 0.0001

    def test_ah_to_wh_with_voltage(self, converter):
        """Test conversion from Ah to Wh with voltage parameter."""
        result = converter.convert(2.5, "Ah", "Wh", voltage=12.0)
        assert abs(result - 30.0) < 0.0001

    def test_wh_to_mah_with_voltage(self, converter):
        """Test conversion from Wh to mAh with voltage parameter."""
        result = converter.convert(3.7, "Wh", "mAh", voltage=3.7)
        assert abs(result - 1000) < 0.1

    def test_wh_to_ah_with_voltage(self, converter):
        """Test conversion from Wh to Ah with voltage parameter."""
        result = converter.convert(30.0, "Wh", "Ah", voltage=12.0)
        assert abs(result - 2.5) < 0.0001

    def test_kwh_to_ah_with_voltage(self, converter):
        """Test conversion from kWh to Ah with voltage parameter."""
        result = converter.convert(1.0, "kWh", "Ah", voltage=3.7)
        assert abs(result - 270.27027) < 0.01

    def test_ah_to_kwh_with_voltage(self, converter):
        """Test conversion from Ah to kWh with voltage parameter."""
        result = converter.convert(100.0, "Ah", "kWh", voltage=3.7)
        assert abs(result - 0.37) < 0.001

    def test_same_unit_conversion(self, converter):
        """Test conversion when source and target units are the same."""
        assert converter.convert(100, "mAh", "mAh") == 100
        assert converter.convert(5.5, "Ah", "Ah") == 5.5
        assert converter.convert(10, "Wh", "Wh") == 10
        assert converter.convert(2.5, "kWh", "kWh") == 2.5

    def test_zero_value(self, converter):
        """Test conversion of zero value."""
        assert converter.convert(0, "mAh", "Wh", voltage=3.7) == 0
        assert converter.convert(0, "Wh", "Ah", voltage=12.0) == 0

    def test_negative_value(self, converter):
        """Test conversion of negative value."""
        result = converter.convert(-1000, "mAh", "Wh", voltage=3.7)
        assert abs(result - (-3.7)) < 0.0001

    def test_different_voltages(self, converter):
        """Test conversion with different voltage values."""
        result1 = converter.convert(1000, "mAh", "Wh", voltage=3.7)
        result2 = converter.convert(1000, "mAh", "Wh", voltage=12.0)
        result3 = converter.convert(1000, "mAh", "Wh", voltage=5.0)

        assert abs(result1 - 3.7) < 0.0001
        assert abs(result2 - 12.0) < 0.0001
        assert abs(result3 - 5.0) < 0.0001

    def test_small_value_conversion(self, converter):
        """Test conversion of very small values."""
        result = converter.convert(1, "mAh", "Wh", voltage=3.7)
        assert abs(result - 0.0037) < 0.0001

    def test_large_value_conversion(self, converter):
        """Test conversion of very large values."""
        result = converter.convert(100000, "mAh", "Wh", voltage=3.7)
        assert abs(result - 370.0) < 0.01

    def test_charge_to_energy_mah_to_kwh(self, converter):
        """Test conversion from mAh to kWh."""
        result = converter.convert(100000, "mAh", "kWh", voltage=3.7)
        assert abs(result - 0.37) < 0.001

    def test_energy_to_charge_kwh_to_mah(self, converter):
        """Test conversion from kWh to mAh."""
        result = converter.convert(0.37, "kWh", "mAh", voltage=3.7)
        assert abs(result - 100000) < 1

    def test_invalid_from_unit(self, converter):
        """Test that invalid source unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "invalid", "mAh")

    def test_invalid_to_unit(self, converter):
        """Test that invalid target unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "mAh", "invalid")

    def test_validate_unit(self, converter):
        """Test unit validation."""
        converter.validate_unit("mAh")
        converter.validate_unit("Ah")
        converter.validate_unit("Wh")
        converter.validate_unit("kWh")

        with pytest.raises(ValueError):
            converter.validate_unit("invalid")

    def test_invalid_voltage_zero(self, converter):
        """Test that zero voltage raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "mAh", "Wh", voltage=0)

    def test_invalid_voltage_negative(self, converter):
        """Test that negative voltage raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "mAh", "Wh", voltage=-5.0)

    def test_default_voltage_parameter(self, converter):
        """Test that default voltage is used when not provided."""
        result = converter.convert(1000, "mAh", "Wh")
        assert abs(result - 3.7) < 0.0001

    def test_precision_consistency(self, converter):
        """Test that conversions are consistent (round-trip)."""
        # Convert 1000 mAh to Wh, then back to mAh
        wh = converter.convert(1000, "mAh", "Wh", voltage=3.7)
        mah = converter.convert(wh, "Wh", "mAh", voltage=3.7)
        assert abs(mah - 1000) < 0.1

    def test_voltage_5v_conversion(self, converter):
        """Test conversion with 5V (USB standard voltage)."""
        result = converter.convert(2000, "mAh", "Wh", voltage=5.0)
        assert abs(result - 10.0) < 0.0001

    def test_voltage_12v_conversion(self, converter):
        """Test conversion with 12V (car battery voltage)."""
        result = converter.convert(50, "Ah", "Wh", voltage=12.0)
        assert abs(result - 600.0) < 0.01
