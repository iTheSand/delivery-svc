"""
Collection of celery tasks
"""
from delivery.celery import app
from apps.external_api.cbr_api import get_currency_rates
from django_redis import get_redis_connection


@app.task
def cache_usd_exchange_rate(key="USD_RATE"):
    currency_rates = get_currency_rates()
    usd_rate = currency_rates["Valute"]["USD"]["Value"]

    redis_conn = get_redis_connection("default")
    redis_conn.set(key, usd_rate)
