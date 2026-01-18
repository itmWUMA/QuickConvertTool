"""Unit tests for the Length converter."""

import pytest
from src.converters.length import LengthConverter


class TestLengthConverter:
    """Test suite for LengthConverter."""

    @pytest.fixture
    def converter(self):
        """Create a LengthConverter instance for testing."""
        return LengthConverter()

    def test_converter_name(self, converter):
        """Test that the converter has the correct name."""
        assert converter.name == "Length"

    def test_supported_units(self, converter):
        """Test that all expected units are supported."""
        expected_units = ["m", "km", "cm", "mm", "mile", "yard", "ft", "inch"]
        assert set(converter.units) == set(expected_units)

    def test_same_unit_conversion(self, converter):
        """Test conversion when source and target units are the same."""
        assert converter.convert(100, "m", "m") == 100
        assert converter.convert(5.5, "km", "km") == 5.5

    def test_meter_to_kilometer(self, converter):
        """Test conversion from meters to kilometers."""
        assert converter.convert(1000, "m", "km") == 1.0
        assert converter.convert(500, "m", "km") == 0.5

    def test_meter_to_centimeter(self, converter):
        """Test conversion from meters to centimeters."""
        assert converter.convert(1, "m", "cm") == 100
        assert converter.convert(2.5, "m", "cm") == 250

    def test_meter_to_foot(self, converter):
        """Test conversion from meters to feet."""
        result = converter.convert(1, "m", "ft")
        assert abs(result - 3.28084) < 0.00001

    def test_foot_to_meter(self, converter):
        """Test conversion from feet to meters."""
        result = converter.convert(3.28084, "ft", "m")
        assert abs(result - 1.0) < 0.00001

    def test_mile_to_kilometer(self, converter):
        """Test conversion from miles to kilometers."""
        result = converter.convert(1, "mile", "km")
        assert abs(result - 1.609344) < 0.000001

    def test_inch_to_centimeter(self, converter):
        """Test conversion from inches to centimeters."""
        result = converter.convert(1, "inch", "cm")
        assert abs(result - 2.54) < 0.001

    def test_zero_value(self, converter):
        """Test conversion of zero value."""
        assert converter.convert(0, "m", "km") == 0
        assert converter.convert(0, "ft", "inch") == 0

    def test_negative_value(self, converter):
        """Test conversion of negative value."""
        result = converter.convert(-10, "m", "cm")
        assert result == -1000

    def test_invalid_from_unit(self, converter):
        """Test that invalid source unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "invalid", "m")

    def test_invalid_to_unit(self, converter):
        """Test that invalid target unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "m", "invalid")

    def test_validate_unit(self, converter):
        """Test unit validation."""
        converter.validate_unit("m")  # Should not raise
        converter.validate_unit("km")  # Should not raise

        with pytest.raises(ValueError):
            converter.validate_unit("invalid")
