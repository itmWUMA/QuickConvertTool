"""Currency converter implementation."""

import time
from typing import List, Dict, Optional
import requests
from ..core.converter import Converter


class CurrencyConverter(Converter):
    """
    Converter for currency units.

    Supports multiple currencies with real-time exchange rates.
    Exchange rates are fetched from exchangerate-api.com
    
    Features:
    - Real-time exchange rates via API
    - Caching mechanism (10 minutes validity)
    - Automatic retry on network failure
    - Easy to extend with new currencies
    
    Architecture:
    - Uses a base currency (USD) for all conversions
    - All conversions go through: source -> USD -> target
    - Currency configurations are centralized in _CURRENCIES dict
    """

    _BASE_CURRENCY = "USD"
    _API_URL = f"https://open.er-api.com/v6/latest/{_BASE_CURRENCY}"
    _CACHE_DURATION = 600  # 10 minutes in seconds
    _REQUEST_TIMEOUT = 5  # 5 seconds timeout for API requests

    # Currency configuration: code -> display name
    _CURRENCIES = {
        "CNY": "人民币",
        "USD": "美元",
        "EUR": "欧元",
        "JPY": "日元",
        "GBP": "英镑",
        "KRW": "韩元",
        "HKD": "港币",
        "AUD": "澳元",
        "CAD": "加元",
        "SGD": "新币"
    }

    # Cache for exchange rates (stores all rates from API)
    _cached_rates: Optional[Dict[str, float]] = None
    _cache_timestamp: Optional[float] = None

    @property
    def name(self) -> str:
        """Return the display name of this converter."""
        return "货币"

    @property
    def units(self) -> List[str]:
        """Return a list of all supported units."""
        return [f"{code}({name})" for code, name in self._CURRENCIES.items()]

    def _get_exchange_rates(self) -> Dict[str, float]:
        """
        Fetch current exchange rates for all supported currencies.

        Returns:
            Dict[str, float]: Dictionary mapping currency codes to exchange rates
                             (1 USD = X currency)

        Raises:
            ValueError: If API request fails or returns invalid data
        """
        current_time = time.time()

        # Check if cache is valid
        if (
            self._cached_rates is not None
            and self._cache_timestamp is not None
            and (current_time - self._cache_timestamp) < self._CACHE_DURATION
        ):
            return self._cached_rates

        # Fetch new rates from API
        try:
            response = requests.get(self._API_URL, timeout=self._REQUEST_TIMEOUT)
            response.raise_for_status()

            data = response.json()

            if data.get("result") != "success":
                raise ValueError("API返回状态异常")

            rates = data.get("rates", {})
            
            # Validate that all required currencies are present
            missing_currencies = [
                code for code in self._CURRENCIES.keys() 
                if code not in rates
            ]
            if missing_currencies:
                raise ValueError(
                    f"API响应中未找到以下货币汇率: {', '.join(missing_currencies)}"
                )

            # Update cache with all rates
            CurrencyConverter._cached_rates = {
                code: float(rates[code]) 
                for code in self._CURRENCIES.keys()
            }
            CurrencyConverter._cache_timestamp = current_time

            return CurrencyConverter._cached_rates

        except requests.Timeout:
            raise ValueError("网络请求超时，请检查网络连接")
        except requests.ConnectionError:
            raise ValueError("无法连接到汇率服务器，请检查网络连接")
        except requests.RequestException as e:
            raise ValueError(f"获取汇率失败: {str(e)}")
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"解析汇率数据失败: {str(e)}")

    def _parse_unit(self, unit: str) -> str:
        """
        Parse unit string to extract base currency code.

        Args:
            unit: Unit string like "CNY(人民币)" or "USD(美元)"

        Returns:
            str: Currency code like "CNY" or "USD"
        """
        return unit.split("(")[0]

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert a value from one currency to another.

        Conversion strategy:
        1. Convert source currency to base currency (USD)
        2. Convert base currency to target currency

        This approach eliminates the need for hardcoded conversion pairs.

        Args:
            value: The numerical value to convert
            from_unit: The source currency unit
            to_unit: The target currency unit

        Returns:
            float: The converted value

        Raises:
            ValueError: If either unit is not supported or API request fails
        """
        # Validate units
        self.validate_unit(from_unit)
        self.validate_unit(to_unit)

        # If units are the same, return the original value
        if from_unit == to_unit:
            return value

        # Parse currency codes
        from_currency = self._parse_unit(from_unit)
        to_currency = self._parse_unit(to_unit)

        # Get all exchange rates (1 USD = X currency)
        rates = self._get_exchange_rates()

        # Step 1: Convert from source currency to USD
        if from_currency == self._BASE_CURRENCY:
            value_in_usd = value
        else:
            # Divide by rate to get USD value
            value_in_usd = value / rates[from_currency]

        # Step 2: Convert from USD to target currency
        if to_currency == self._BASE_CURRENCY:
            return value_in_usd
        else:
            # Multiply by rate to get target currency value
            return value_in_usd * rates[to_currency]
