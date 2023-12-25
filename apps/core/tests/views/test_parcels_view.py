from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import Parcel, ParcelType
from apps.core.tests.factories import ParcelFactory
from apps.core.views import SESSION_DICT_KEY


class ParcelViewTestCase(APITestCase):
    path = "/core/parcels"

    def test_parcels_not_found(self):
        ParcelFactory.create_batch(2)

        response = self.client.get(self.path)

        self.assertFalse(self.client.session.get(SESSION_DICT_KEY))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(
            {"count": 0, "next": None, "previous": None, "results": []}, response.json()
        )

    def test_success(self):
        parcels_count = 3
        parcels = ParcelFactory.create_batch(parcels_count)

        session = self.client.session
        session[SESSION_DICT_KEY] = [parcel.id for parcel in parcels]
        session.save()

        response = self.client.get(self.path)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(
            {
                "count": parcels_count,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": parcel.id,
                        "name": parcel.name,
                        "weight": parcel.weight,
                        "type": parcel.type.name,
                        "declared_cost": parcel.declared_cost,
                        "delivery_cost": parcel.delivery_cost,
                    }
                    for parcel in parcels
                ],
            },
            response.json(),
        )

    def test_type_filter(self):
        others_parcels = ParcelFactory.create_batch(2)
        clothes_parcel = ParcelFactory(type=ParcelType.objects.get(name="clothes"))

        session = self.client.session
        session[SESSION_DICT_KEY] = [parcel.id for parcel in others_parcels]
        session[SESSION_DICT_KEY].append(clothes_parcel.id)
        session.save()

        response = self.client.get(f"{self.path}?content_type=clothes")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": clothes_parcel.id,
                        "name": clothes_parcel.name,
                        "weight": clothes_parcel.weight,
                        "type": clothes_parcel.type.name,
                        "declared_cost": clothes_parcel.declared_cost,
                        "delivery_cost": clothes_parcel.delivery_cost,
                    }
                ],
            },
            response.json(),
        )

    def test_delivery_cost_filter(self):
        others_parcels = ParcelFactory.create_batch(2)
        processed_parcel = ParcelFactory(delivery_cost=50, status=Parcel.CALCULATED)

        session = self.client.session
        session[SESSION_DICT_KEY] = [parcel.id for parcel in others_parcels]
        session[SESSION_DICT_KEY].append(processed_parcel.id)
        session.save()

        response = self.client.get(f"{self.path}?delivery_cost=not_null")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": processed_parcel.id,
                        "name": processed_parcel.name,
                        "weight": processed_parcel.weight,
                        "type": processed_parcel.type.name,
                        "declared_cost": processed_parcel.declared_cost,
                        "delivery_cost": processed_parcel.delivery_cost,
                    }
                ],
            },
            response.json(),
        )

    def test_pagination(self):
        parcels_count = 10
        new_parcels = ParcelFactory.create_batch(parcels_count)

        session = self.client.session
        session[SESSION_DICT_KEY] = [parcel.id for parcel in new_parcels]
        session.save()

        response = self.client.get(f"{self.path}?page_size=5")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(
            {
                "count": parcels_count,
                "next": "http://testserver/core/parcels?page=2&page_size=5",
                "previous": None,
                "results": [
                    {
                        "id": parcel.id,
                        "name": parcel.name,
                        "weight": parcel.weight,
                        "type": parcel.type.name,
                        "declared_cost": parcel.declared_cost,
                        "delivery_cost": parcel.delivery_cost,
                    }
                    for parcel in new_parcels[:5]
                ],
            },
            response.json(),
        )
