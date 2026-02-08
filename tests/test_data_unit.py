"""Unit tests for the DataUnit converter."""

import pytest
from src.converters.data_unit import DataUnitConverter


class TestDataUnitConverter:
    """Test suite for DataUnitConverter."""

    @pytest.fixture
    def converter(self):
        """Create a DataUnitConverter instance for testing."""
        return DataUnitConverter()

    def test_supported_units(self, converter):
        """Test that all expected units are supported."""
        expected_units = [
            "bit",
            "byte",
            "KB",
            "MB",
            "GB",
            "TB",
            "KiB",
            "MiB",
            "GiB",
            "TiB",
        ]
        assert set(converter.units) == set(expected_units)

    def test_same_unit_conversion(self, converter):
        """Test conversion when source and target units are the same."""
        assert converter.convert(100, "bit", "bit") == 100
        assert converter.convert(5.5, "MB", "MB") == 5.5

    def test_bit_byte_conversion(self, converter):
        """Test conversion between bit and byte."""
        assert converter.convert(8, "bit", "byte") == 1
        assert converter.convert(1, "byte", "bit") == 8

    def test_decimal_prefix_conversion(self, converter):
        """Test conversion between KB/MB/GB using 1024 base."""
        assert converter.convert(1, "KB", "byte") == 1024
        assert converter.convert(1, "MB", "KB") == 1024
        assert converter.convert(1, "GB", "MB") == 1024

    def test_binary_prefix_conversion(self, converter):
        """Test conversion between binary prefixed units."""
        assert converter.convert(1, "KiB", "byte") == 1024
        assert converter.convert(1, "MiB", "KiB") == 1024
        assert converter.convert(1, "GiB", "MiB") == 1024

    def test_cross_prefix_conversion(self, converter):
        """Test conversion between KB and KiB with equal base."""
        assert converter.convert(1, "KB", "KiB") == 1

    def test_large_value_conversion(self, converter):
        """Test conversion of large magnitude values."""
        result = converter.convert(1, "TiB", "bit")
        assert abs(result - 8796093022208) < 0.1

    def test_invalid_from_unit(self, converter):
        """Test that invalid source unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "invalid", "bit")

    def test_invalid_to_unit(self, converter):
        """Test that invalid target unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "bit", "invalid")
