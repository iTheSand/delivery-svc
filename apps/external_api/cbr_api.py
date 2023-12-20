import logging

from requests import request

logger = logging.getLogger("django")


def get_currency_rates():
    response = request("GET", f"https://www.cbr-xml-daily.ru/daily_json.js")
    response_body = response.json()

    logger.info(
        {
            "Get currency rates": {
                "response_status_code": response.status_code,
                "response_body": response_body,
            }
        }
    )

    return response_body
