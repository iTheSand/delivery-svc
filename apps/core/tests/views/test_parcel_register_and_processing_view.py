from unittest.mock import call, patch

from rest_framework.test import APITestCase

from apps.core.tests.views.parcel_register_base_tests import ParcelRegisterBaseTests


class ParcelRegisterAndProcessingViewTestCase(ParcelRegisterBaseTests, APITestCase):
    path = "/core/parcel-register-and-processing"

    @patch("apps.core.tasks.processing_parcel.delay")
    def test_success(self, processing_parcel_task):
        super().test_success()

        processing_parcel_task.assert_has_calls([call(parcel_id=self.parcel.id)])
