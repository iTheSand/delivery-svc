from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.models import Parcel, ParcelType


class RoundField(serializers.FloatField):
    @staticmethod
    def to_representation(value, **kwargs):
        return round(value, 2)


class ParcelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelType
        fields = ("id", "name")


class ParcelRegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=3, max_length=255)
    type = serializers.PrimaryKeyRelatedField(queryset=ParcelType.objects.all())
    declared_cost = RoundField()

    class Meta:
        model = Parcel
        fields = ("name", "weight", "type", "declared_cost")

    @staticmethod
    def validate_weight(value):
        if value <= 0:
            raise ValidationError(f"Value {value} must be a positive number")
        return value

    @staticmethod
    def validate_declared_cost(value):
        if value <= 0:
            raise ValidationError(f"Value {value} must be a positive number")
        return round(value, 2)


class ParcelsSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    declared_cost = RoundField()
    delivery_cost = RoundField()

    @staticmethod
    def get_type(obj):
        return obj.type.name

    class Meta:
        model = Parcel
        fields = ("id", "name", "weight", "type", "declared_cost", "delivery_cost")
