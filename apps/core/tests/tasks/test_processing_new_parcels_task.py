from unittest.mock import patch

from django.test import TestCase

from apps.core.models import Parcel
from apps.core.tasks import USD_RATE_CACHE_KEY, processing_new_parcels
from apps.core.tests.factories import ParcelFactory


class ProcessingNewParcelsTaskTestCase(TestCase):
    def test_success(self):
        new_parcels_count = 2
        ParcelFactory.create_batch(new_parcels_count)

        get_redis_connection_patcher = patch("apps.core.tasks.get_redis_connection")
        get_redis_connection = get_redis_connection_patcher.start()
        get_redis_connection.return_value = {USD_RATE_CACHE_KEY: 30}

        processing_new_parcels()

        get_redis_connection_patcher.stop()

        self.assertEqual(
            new_parcels_count, Parcel.objects.filter(status=Parcel.CALCULATED).count()
        )
