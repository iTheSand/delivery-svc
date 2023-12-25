from unittest.mock import patch

from django.test import TestCase

from apps.core.models import Parcel
from apps.core.tasks import USD_RATE_CACHE_KEY, processing_parcel
from apps.core.tests.factories import ParcelFactory


class ProcessingParcelTaskTestCase(TestCase):
    def test_success(self):
        parcel = ParcelFactory()

        get_redis_connection_patcher = patch("apps.core.tasks.get_redis_connection")
        get_redis_connection = get_redis_connection_patcher.start()
        get_redis_connection.return_value = {USD_RATE_CACHE_KEY: 30}

        self.assertEqual(Parcel.NEW, parcel.status)
        processing_parcel(parcel.id)

        get_redis_connection_patcher.stop()

        parcel.refresh_from_db()
        self.assertEqual(Parcel.CALCULATED, parcel.status)
