from django.test import TestCase
from requests_mock import Mocker

from apps.external_api.cbr_api import get_currency_rates


class CbrApiTestCase(TestCase):
    @Mocker()
    def test_success(self, request_mock):
        expected_json_data = {"Valute": {"USD": {"Value": 90.5, "Previous": 91.1}}}

        request_mock.get(
            "https://www.cbr-xml-daily.ru/daily_json.js", json=expected_json_data
        )

        self.assertDictEqual(expected_json_data, get_currency_rates())
