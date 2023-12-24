"""
Collection of celery tasks
"""
import logging

from django.db.models import F
from django_redis import get_redis_connection

from apps.core.models import Parcel
from apps.external_api.cbr_api import get_currency_rates
from delivery.celery import app

logger = logging.getLogger("django")


@app.task
def processing_new_parcels(key="USD_RATE"):
    """
    Processing new parcels and calculating the cost of delivery.

    :param key: key to get a value from cache
    :return: None
    """

    redis_conn = get_redis_connection("default")

    usd_rate = redis_conn.get(key)
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
def cache_usd_exchange_rate(key="USD_RATE"):
    """
    Recording USD exchange rate in cache.

    :param key: key for writing value to cache
    :return: usd rate
    """

    currency_rates = get_currency_rates()
    usd_rate = currency_rates["Valute"]["USD"]["Value"]

    redis_conn = get_redis_connection("default")
    redis_conn.set(key, usd_rate)

    logger.info(
        {
            "cache_usd_exchange_rate": {
                f"Value of USD exchange rate ({usd_rate}) is written in cache"
            }
        }
    )

    return usd_rate
