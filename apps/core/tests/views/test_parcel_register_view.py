from rest_framework.test import APITestCase

from apps.core.tests.views.parcel_register_base_tests import ParcelRegisterBaseTests


class ParcelRegisterViewTestCase(ParcelRegisterBaseTests, APITestCase):
    path = "/core/parcel-register"
