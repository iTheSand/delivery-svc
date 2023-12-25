from django.test import TestCase
from requests_mock import Mocker
from rest_framework import status

from apps.external_api.cbr_api import get_currency_rates


class CbrApiTestCase(TestCase):
    @Mocker()
    def test_server_error(self, request_mock):
        request_mock.get(
            "https://www.cbr-xml-daily.ru/daily_json.js",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        response = get_currency_rates()

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

    @Mocker()
    def test_success(self, request_mock):
        expected_json_data = {"Valute": {"USD": {"Value": 90.5, "Previous": 91.1}}}

        request_mock.get(
            "https://www.cbr-xml-daily.ru/daily_json.js", json=expected_json_data
        )

        response = get_currency_rates()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected_json_data, response.json())
