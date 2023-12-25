# pylint: disable=no-member

from rest_framework import status

from apps.core.models import Parcel
from apps.core.views import SESSION_DICT_KEY


class ParcelRegisterBaseTests:
    path = None
    parcel = None

    # pylint: disable=redefined-builtin
    @staticmethod
    def get_request_body(name="test_name", weight=2.0, type=3, declared_cost=4.0):
        return {
            "name": name,
            "weight": weight,
            "type": type,
            "declared_cost": declared_cost,
        }

    def test_success(self):
        self.assertFalse(Parcel.objects.exists())
        self.assertFalse(self.client.session.get(SESSION_DICT_KEY))

        request_body = self.get_request_body()
        response = self.client.post(self.path, data=request_body, format="json")

        self.parcel = Parcel.objects.get()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertDictEqual({"parcel_id": self.parcel.id}, response.json())
        self.assertEqual(self.parcel.id, self.client.session[SESSION_DICT_KEY][0])

    def test_validate_fields(self):
        request_body = self.get_request_body(
            name="q", weight=-1.0, type=4, declared_cost=0.0
        )
        response = self.client.post(self.path, data=request_body, format="json")

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            {
                "name": ["Ensure this field has at least 3 characters."],
                "weight": [f"Value {request_body['weight']} must be a positive number"],
                "type": [
                    f"Invalid pk \"{request_body['type']}\" - object does not exist."
                ],
                "declared_cost": [
                    f"Value {request_body['declared_cost']} must be a positive number"
                ],
            },
            response.json(),
        )
