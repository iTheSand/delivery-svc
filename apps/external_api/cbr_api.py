import logging

from requests import request

logger = logging.getLogger("django")


def get_currency_rates():
    """
    External API for obtaining current exchange rates.

    :return: response
    """

    method, url = "GET", "https://www.cbr-xml-daily.ru/daily_json.js"
    response = request(method=method, url=url)

    logger.info(
        {
            "get_currency_rates": {
                "path": f"{method} {url}",
                "response_status_code": response.status_code,
                "response_text": response.text,
            }
        }
    )

    return response
