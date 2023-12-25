"""
Collection of celery tasks
"""
import logging

from django.db.models import F
from django_redis import get_redis_connection
from rest_framework import status

from apps.core.exceptions import BadCurrencyRatesResponse
from apps.core.models import Parcel
from apps.external_api.cbr_api import get_currency_rates
from delivery.celery import app

logger = logging.getLogger("django")

USD_RATE_CACHE_KEY = "USD_RATE"


@app.task
def cache_usd_exchange_rate():
    """
    Recording USD exchange rate in cache.

    :return: usd exchange rate
    """

    response = get_currency_rates()
    if response.status_code != status.HTTP_200_OK:
        raise BadCurrencyRatesResponse

    currency_rates = response.json()
    usd_rate = currency_rates["Valute"]["USD"]["Value"]

    get_redis_connection("default").set(USD_RATE_CACHE_KEY, usd_rate)

    logger.info(
        {
            "cache_usd_exchange_rate": {
                f"Value of USD exchange rate ({usd_rate}) is written in cache"
            }
        }
    )

    return usd_rate


@app.task
def processing_new_parcels():
    """
    Processing new parcels and calculating the cost of delivery.

    :return: None
    """

    usd_rate = get_redis_connection("default").get(USD_RATE_CACHE_KEY)
    if not usd_rate:
        usd_rate = cache_usd_exchange_rate()

    Parcel.objects.filter(status=Parcel.NEW).update(
        delivery_cost=(F("weight") * 0.5 + F("declared_cost") * 0.01) * usd_rate,
        status=Parcel.CALCULATED,
    )

    logger.info(
        {"processing_new_parcels": {"Parcels with NEW status have been processed"}}
    )


@app.task
def processing_parcel(parcel_id):
    """
    Processing parcel and calculating the cost of delivery.

    :param parcel_id: param to process an object with current id
    :return: None
    """

    usd_rate = get_redis_connection("default").get(USD_RATE_CACHE_KEY)
    if not usd_rate:
        usd_rate = cache_usd_exchange_rate()

    Parcel.objects.filter(id=parcel_id).update(
        delivery_cost=(F("weight") * 0.5 + F("declared_cost") * 0.01) * usd_rate,
        status=Parcel.CALCULATED,
    )

    logger.info(
        {"processing_parcel": {f"Parcel (id: {parcel_id}) have been processed"}}
    )
