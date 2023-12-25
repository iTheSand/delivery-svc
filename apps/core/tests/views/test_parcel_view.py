from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.tests.factories import ParcelFactory
from apps.core.views import SESSION_DICT_KEY


class ParcelViewTestCase(APITestCase):
    path = "/core/parcels"

    def test_parcel_not_found(self):
        parcel = ParcelFactory()

        response = self.client.get(f"{self.path}/{parcel.id}")

        self.assertFalse(self.client.session.get(SESSION_DICT_KEY))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertDictEqual({"detail": "Not found."}, response.json())

    def test_success(self):
        parcel = ParcelFactory()

        session = self.client.session
        session[SESSION_DICT_KEY] = [parcel.id]
        session.save()

        response = self.client.get(f"{self.path}/{parcel.id}")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(
            {
                "id": parcel.id,
                "name": parcel.name,
                "weight": parcel.weight,
                "type": parcel.type.name,
                "declared_cost": parcel.declared_cost,
                "delivery_cost": parcel.delivery_cost,
            },
            response.json(),
        )
