# pylint: disable=consider-using-f-string

from factory import Sequence
from factory.django import DjangoModelFactory

from apps.core.models import Parcel, ParcelType


class ParcelFactory(DjangoModelFactory):
    class Meta:
        model = Parcel

    name = Sequence("test_parcel_{}".format)
    weight = Sequence(lambda n: 1 + n)
    type = ParcelType.objects.last()
    declared_cost = Sequence(lambda n: 3 + n)
