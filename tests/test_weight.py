"""Unit tests for the Weight converter."""

import pytest
from src.converters.weight import WeightConverter


class TestWeightConverter:
    """Test suite for WeightConverter."""

    @pytest.fixture
    def converter(self):
        """Create a WeightConverter instance for testing."""
        return WeightConverter()

    def test_converter_name(self, converter):
        """Test that the converter has the correct name."""
        assert converter.name == "Weight"

    def test_supported_units(self, converter):
        """Test that all expected units are supported."""
        expected_units = ["kg", "g", "mg", "ton", "lb", "oz"]
        assert set(converter.units) == set(expected_units)

    def test_same_unit_conversion(self, converter):
        """Test conversion when source and target units are the same."""
        assert converter.convert(100, "kg", "kg") == 100
        assert converter.convert(5.5, "lb", "lb") == 5.5

    def test_kilogram_to_gram(self, converter):
        """Test conversion from kilograms to grams."""
        assert converter.convert(1, "kg", "g") == 1000
        assert converter.convert(2.5, "kg", "g") == 2500

    def test_gram_to_kilogram(self, converter):
        """Test conversion from grams to kilograms."""
        assert converter.convert(1000, "g", "kg") == 1
        assert converter.convert(500, "g", "kg") == 0.5

    def test_kilogram_to_milligram(self, converter):
        """Test conversion from kilograms to milligrams."""
        assert converter.convert(1, "kg", "mg") == 1000000
        result = converter.convert(0.001, "kg", "mg")
        assert abs(result - 1000) < 0.01

    def test_ton_to_kilogram(self, converter):
        """Test conversion from tons to kilograms."""
        assert converter.convert(1, "ton", "kg") == 1000
        assert converter.convert(0.5, "ton", "kg") == 500

    def test_kilogram_to_pound(self, converter):
        """Test conversion from kilograms to pounds."""
        result = converter.convert(1, "kg", "lb")
        assert abs(result - 2.20462) < 0.00001

    def test_pound_to_kilogram(self, converter):
        """Test conversion from pounds to kilograms."""
        result = converter.convert(2.20462, "lb", "kg")
        assert abs(result - 1.0) < 0.00001

    def test_ounce_to_gram(self, converter):
        """Test conversion from ounces to grams."""
        result = converter.convert(1, "oz", "g")
        assert abs(result - 28.349523125) < 0.000001

    def test_pound_to_ounce(self, converter):
        """Test conversion from pounds to ounces."""
        result = converter.convert(1, "lb", "oz")
        assert abs(result - 16) < 0.01

    def test_zero_value(self, converter):
        """Test conversion of zero value."""
        assert converter.convert(0, "kg", "g") == 0
        assert converter.convert(0, "lb", "oz") == 0

    def test_negative_value(self, converter):
        """Test conversion of negative value (mass difference)."""
        result = converter.convert(-10, "kg", "g")
        assert result == -10000

    def test_small_value(self, converter):
        """Test conversion of very small values."""
        result = converter.convert(1, "mg", "kg")
        assert abs(result - 0.000001) < 0.0000001

    def test_large_value(self, converter):
        """Test conversion of large values."""
        result = converter.convert(5, "ton", "g")
        assert result == 5000000

    def test_invalid_from_unit(self, converter):
        """Test that invalid source unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "invalid", "kg")

    def test_invalid_to_unit(self, converter):
        """Test that invalid target unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "kg", "invalid")

    def test_validate_unit(self, converter):
        """Test unit validation."""
        converter.validate_unit("kg")  # Should not raise
        converter.validate_unit("lb")  # Should not raise

        with pytest.raises(ValueError):
            converter.validate_unit("invalid")
