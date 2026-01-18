"""Unit tests for the Currency converter."""

import time
from unittest.mock import patch, Mock
import pytest
import requests
from src.converters.currency import CurrencyConverter


class TestCurrencyConverter:
    """Test suite for CurrencyConverter."""

    @pytest.fixture
    def converter(self):
        """Create a CurrencyConverter instance for testing."""
        # Reset cache before each test
        CurrencyConverter._cached_rates = None
        CurrencyConverter._cache_timestamp = None
        return CurrencyConverter()

    @pytest.fixture
    def mock_api_response(self):
        """Create a mock API response with multiple currencies."""
        return {
            "result": "success",
            "base_code": "USD",
            "rates": {
                "USD": 1.0,
                "CNY": 7.0,
                "EUR": 0.85,
                "JPY": 110.0,
                "GBP": 0.73,
                "KRW": 1180.0,
                "HKD": 7.8,
                "AUD": 1.35,
                "CAD": 1.25,
                "SGD": 1.35
            }
        }

    def test_converter_name(self, converter):
        """Test that the converter has the correct name."""
        assert converter.name == "货币"

    def test_supported_units(self, converter):
        """Test that all expected units are supported."""
        expected_units = [
            "CNY(人民币)", "USD(美元)", "EUR(欧元)", "JPY(日元)",
            "GBP(英镑)", "KRW(韩元)", "HKD(港币)", "AUD(澳元)",
            "CAD(加元)", "SGD(新币)"
        ]
        assert set(converter.units) == set(expected_units)

    def test_unit_parsing(self, converter):
        """Test unit string parsing."""
        assert converter._parse_unit("CNY(人民币)") == "CNY"
        assert converter._parse_unit("USD(美元)") == "USD"

    @patch('requests.get')
    def test_usd_to_cny(self, mock_get, converter, mock_api_response):
        """Test conversion from USD to CNY."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert result == 700.0

    @patch('requests.get')
    def test_cny_to_usd(self, mock_get, converter, mock_api_response):
        """Test conversion from CNY to USD."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = converter.convert(700, "CNY(人民币)", "USD(美元)")
        assert result == 100.0

    @patch('requests.get')
    def test_same_unit_conversion(self, mock_get, converter):
        """Test conversion when source and target units are the same."""
        # Should not call API for same unit conversion
        assert converter.convert(100, "USD(美元)", "USD(美元)") == 100
        assert converter.convert(500, "CNY(人民币)", "CNY(人民币)") == 500
        mock_get.assert_not_called()

    @patch('requests.get')
    def test_zero_value(self, mock_get, converter, mock_api_response):
        """Test conversion of zero value."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        assert converter.convert(0, "USD(美元)", "CNY(人民币)") == 0
        assert converter.convert(0, "CNY(人民币)", "USD(美元)") == 0

    @patch('requests.get')
    def test_negative_value(self, mock_get, converter, mock_api_response):
        """Test conversion of negative value."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = converter.convert(-100, "USD(美元)", "CNY(人民币)")
        assert result == -700.0

    @patch('requests.get')
    def test_decimal_values(self, mock_get, converter, mock_api_response):
        """Test conversion with decimal values."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = converter.convert(10.5, "USD(美元)", "CNY(人民币)")
        assert abs(result - 73.5) < 0.01

    @patch('requests.get')
    def test_large_values(self, mock_get, converter, mock_api_response):
        """Test conversion with large values."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = converter.convert(1000000, "USD(美元)", "CNY(人民币)")
        assert result == 7000000.0

    @patch('requests.get')
    def test_cache_mechanism(self, mock_get, converter, mock_api_response):
        """Test that caching works correctly."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # First call should fetch from API
        converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert mock_get.call_count == 1

        # Second call should use cache
        converter.convert(200, "USD(美元)", "CNY(人民币)")
        assert mock_get.call_count == 1  # Still 1, not called again

        # Third call should still use cache
        converter.convert(300, "CNY(人民币)", "USD(美元)")
        assert mock_get.call_count == 1  # Still 1

    @patch('requests.get')
    def test_cache_expiration(self, mock_get, converter, mock_api_response):
        """Test that cache expires after the specified duration."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # First call
        converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert mock_get.call_count == 1

        # Simulate time passing beyond cache duration
        CurrencyConverter._cache_timestamp = time.time() - 601  # 601 seconds ago

        # Should fetch from API again
        converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert mock_get.call_count == 2

    @patch('requests.get')
    def test_api_timeout_error(self, mock_get, converter):
        """Test handling of API timeout error."""
        mock_get.side_effect = requests.Timeout("Connection timeout")

        with pytest.raises(ValueError) as exc_info:
            converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert "网络请求超时" in str(exc_info.value)

    @patch('requests.get')
    def test_api_connection_error(self, mock_get, converter):
        """Test handling of API connection error."""
        mock_get.side_effect = requests.ConnectionError("Connection failed")

        with pytest.raises(ValueError) as exc_info:
            converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert "无法连接到汇率服务器" in str(exc_info.value)

    @patch('requests.get')
    def test_api_request_exception(self, mock_get, converter):
        """Test handling of general request exception."""
        mock_get.side_effect = requests.RequestException("Request failed")

        with pytest.raises(ValueError) as exc_info:
            converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert "获取汇率失败" in str(exc_info.value)

    @patch('requests.get')
    def test_api_invalid_status(self, mock_get, converter):
        """Test handling of invalid API response status."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": "error"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with pytest.raises(ValueError) as exc_info:
            converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert "API返回状态异常" in str(exc_info.value)

    @patch('requests.get')
    def test_api_missing_currency_rate(self, mock_get, converter):
        """Test handling of missing currency rate in API response."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "result": "success",
            "rates": {"USD": 1, "CNY": 7.0}  # Missing other currencies
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with pytest.raises(ValueError) as exc_info:
            converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert "未找到以下货币汇率" in str(exc_info.value)

    @patch('requests.get')
    def test_api_invalid_json(self, mock_get, converter):
        """Test handling of invalid JSON response."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with pytest.raises(ValueError) as exc_info:
            converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert "解析汇率数据失败" in str(exc_info.value)

    def test_invalid_from_unit(self, converter):
        """Test that invalid source unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "INVALID", "USD(美元)")

    def test_invalid_to_unit(self, converter):
        """Test that invalid target unit raises ValueError."""
        with pytest.raises(ValueError):
            converter.convert(100, "USD(美元)", "INVALID")

    def test_validate_unit(self, converter):
        """Test unit validation."""
        converter.validate_unit("CNY(人民币)")
        converter.validate_unit("USD(美元)")

        with pytest.raises(ValueError):
            converter.validate_unit("INVALID")

    @patch('requests.get')
    def test_precision_consistency(self, mock_get, converter, mock_api_response):
        """Test that conversions are consistent (round-trip)."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Convert USD to CNY, then back to USD
        cny = converter.convert(100, "USD(美元)", "CNY(人民币)")
        usd = converter.convert(cny, "CNY(人民币)", "USD(美元)")
        assert abs(usd - 100) < 0.01

    @patch('requests.get')
    def test_different_exchange_rates(self, mock_get, converter, mock_api_response):
        """Test conversion with different exchange rates."""
        # First rate: 1 USD = 7.0 CNY
        mock_response1 = Mock()
        response1 = mock_api_response.copy()
        response1["rates"]["CNY"] = 7.0
        mock_response1.json.return_value = response1
        mock_response1.raise_for_status = Mock()
        mock_get.return_value = mock_response1

        result1 = converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert result1 == 700.0

        # Reset cache and change rate
        CurrencyConverter._cached_rates = None
        CurrencyConverter._cache_timestamp = None

        # Second rate: 1 USD = 6.5 CNY
        mock_response2 = Mock()
        response2 = mock_api_response.copy()
        response2["rates"]["CNY"] = 6.5
        mock_response2.json.return_value = response2
        mock_response2.raise_for_status = Mock()
        mock_get.return_value = mock_response2

        result2 = converter.convert(100, "USD(美元)", "CNY(人民币)")
        assert result2 == 650.0

    @patch('requests.get')
    def test_api_request_timeout_value(self, mock_get, converter, mock_api_response):
        """Test that API request uses correct timeout value."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        converter.convert(100, "USD(美元)", "CNY(人民币)")

        # Verify timeout parameter
        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs['timeout'] == 5

    @patch('requests.get')
    def test_small_decimal_conversion(self, mock_get, converter, mock_api_response):
        """Test conversion with very small decimal values."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = converter.convert(0.01, "USD(美元)", "CNY(人民币)")
        assert abs(result - 0.07) < 0.001

    @patch('requests.get')
    def test_eur_to_jpy(self, mock_get, converter, mock_api_response):
        """Test conversion between two non-USD currencies (EUR to JPY)."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # EUR -> USD -> JPY: 100 EUR / 0.85 * 110 = 12941.18
        result = converter.convert(100, "EUR(欧元)", "JPY(日元)")
        assert abs(result - 12941.18) < 0.5

    @patch('requests.get')
    def test_gbp_to_cny(self, mock_get, converter, mock_api_response):
        """Test conversion between GBP and CNY."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # GBP -> USD -> CNY: 100 GBP / 0.73 * 7.0 = 958.90
        result = converter.convert(100, "GBP(英镑)", "CNY(人民币)")
        assert abs(result - 958.90) < 0.5

    @patch('requests.get')
    def test_multi_currency_support(self, mock_get, converter, mock_api_response):
        """Test that all configured currencies can be converted."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Test a few key conversions to ensure all currencies work
        currencies = ["CNY(人民币)", "EUR(欧元)", "JPY(日元)", "GBP(英镑)"]
        
        for from_curr in currencies:
            for to_curr in currencies:
                if from_curr != to_curr:
                    # Should not raise an exception
                    result = converter.convert(100, from_curr, to_curr)
                    assert result > 0

    @patch('requests.get')
    def test_usd_to_all_currencies(self, mock_get, converter, mock_api_response):
        """Test conversion from USD to all supported currencies."""
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        test_cases = [
            ("CNY(人民币)", 700.0),
            ("EUR(欧元)", 85.0),
            ("JPY(日元)", 11000.0),
            ("GBP(英镑)", 73.0),
            ("KRW(韩元)", 118000.0),
            ("HKD(港币)", 780.0),
            ("AUD(澳元)", 135.0),
            ("CAD(加元)", 125.0),
            ("SGD(新币)", 135.0)
        ]

        for currency, expected in test_cases:
            result = converter.convert(100, "USD(美元)", currency)
            assert abs(result - expected) < 0.01, f"Failed for {currency}"

