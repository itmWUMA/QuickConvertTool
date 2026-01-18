"""Unit tests for the Temperature converter."""

import pytest
from src.converters.temperature import TemperatureConverter


class TestTemperatureConverter:
    """Test suite for TemperatureConverter."""

    @pytest.fixture
    def converter(self):
        """Create a TemperatureConverter instance for testing."""
        return TemperatureConverter()

    def test_converter_name(self, converter):
        """Test that the converter has the correct name."""
        assert converter.name == "Temperature"

    def test_supported_units(self, converter):
        """Test that all expected units are supported."""
        expected_units = ["C", "F", "K"]
        assert set(converter.units) == set(expected_units)

    def test_same_unit_conversion(self, converter):
        """Test conversion when source and target units are the same."""
        assert converter.convert(100, "C", "C") == 100
        assert converter.convert(32, "F", "F") == 32
        assert converter.convert(273.15, "K", "K") == 273.15

    def test_celsius_to_fahrenheit(self, converter):
        """Test conversion from Celsius to Fahrenheit."""
        assert converter.convert(0, "C", "F") == 32
        assert converter.convert(100, "C", "F") == 212
        result = converter.convert(37, "C", "F")
        assert abs(result - 98.6) < 0.1

    def test_fahrenheit_to_celsius(self, converter):
        """Test conversion from Fahrenheit to Celsius."""
        assert converter.convert(32, "F", "C") == 0
        assert converter.convert(212, "F", "C") == 100
        result = converter.convert(98.6, "F", "C")
        assert abs(result - 37) < 0.1

    def test_celsius_to_kelvin(self, converter):
        """Test conversion from Celsius to Kelvin."""
        assert converter.convert(0, "C", "K") == 273.15
        result = converter.convert(100, "C", "K")
        assert abs(result - 373.15) < 0.01

    def test_kelvin_to_celsius(self, converter):
        """Test conversion from Kelvin to Celsius."""
        assert converter.convert(273.15, "K", "C") == 0
        result = converter.convert(373.15, "K", "C")
        assert abs(result - 100) < 0.01

    def test_fahrenheit_to_kelvin(self, converter):
        """Test conversion from Fahrenheit to Kelvin."""
        result = converter.convert(32, "F", "K")
        assert abs(result - 273.15) < 0.01

    def test_kelvin_to_fahrenheit(self, converter):
        """Test conversion from Kelvin to Fahrenheit."""
        result = converter.convert(273.15, "K", "F")
        assert abs(result - 32) < 0.01

    def test_negative_celsius(self, converter):
        """Test conversion with negative Celsius values."""
        result = converter.convert(-40, "C", "F")
        assert abs(result - (-40)) < 0.01  # -40C == -40F

    def test_absolute_zero(self, converter):
        """Test conversion of absolute zero."""
        result = converter.convert(-273.15, "C", "K")
        assert abs(result - 0) < 0.01

    def test_invalid_from_unit(self, converter):
        """Test that invalid source unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "invalid", "C")

    def test_invalid_to_unit(self, converter):
        """Test that invalid target unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "C", "invalid")

    def test_validate_unit(self, converter):
        """Test unit validation."""
        converter.validate_unit("C")  # Should not raise
        converter.validate_unit("F")  # Should not raise
        converter.validate_unit("K")  # Should not raise

        with pytest.raises(ValueError):
            converter.validate_unit("invalid")
