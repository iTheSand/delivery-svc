from rest_framework.test import APITestCase

from apps.core.models import ParcelType
from apps.core.serializers import ParcelTypeSerializer


class ParcelTypesViewTestCase(APITestCase):
    def test_success(self):
        response = self.client.get("/core/parcel-types")

        self.assertListEqual(
            ParcelTypeSerializer(ParcelType.objects.all(), many=True).data,
            response.json(),
        )
