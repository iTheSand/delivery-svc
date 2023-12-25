from unittest.mock import patch

from django.test import TestCase

from apps.core.exceptions import BadCurrencyRatesResponse
from apps.core.tasks import cache_usd_exchange_rate


class CurrencyRatesResponse:
    def __init__(self, status_code=200, usd_rate=90):
        self.status_code = status_code
        self.usd_rate = usd_rate

    def json(self):
        return {"Valute": {"USD": {"Value": self.usd_rate}}}


class CacheUsdExchangeRateTaskTestCase(TestCase):
    def test_raise_exception(self):
        get_currency_rates_patcher = patch("apps.core.tasks.get_currency_rates")
        get_currency_rates = get_currency_rates_patcher.start()
        get_currency_rates.return_value = CurrencyRatesResponse(status_code=500)

        with self.assertRaises(BadCurrencyRatesResponse):
            cache_usd_exchange_rate()

        get_currency_rates_patcher.stop()

    def test_success(self):
        expected_value = 30

        get_currency_rates_patcher = patch("apps.core.tasks.get_currency_rates")
        get_redis_connection_patcher = patch("apps.core.tasks.get_redis_connection")
        get_currency_rates = get_currency_rates_patcher.start()
        get_redis_connection_patcher.start()

        get_currency_rates.return_value = CurrencyRatesResponse(usd_rate=expected_value)

        actual_value = cache_usd_exchange_rate()

        get_currency_rates_patcher.stop()
        get_redis_connection_patcher.stop()

        self.assertEqual(expected_value, actual_value)
