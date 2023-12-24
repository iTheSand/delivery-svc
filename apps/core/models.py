from django.db import models


class ParcelType(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ParcelType"
        verbose_name_plural = "ParcelTypes"


class Parcel(models.Model):
    NEW = "NEW"
    CALCULATED = "CALCULATED"
    STATUS_CHOICES = [(NEW, NEW), (CALCULATED, CALCULATED)]

    name = models.CharField(verbose_name="Name", max_length=255)
    weight = models.FloatField(verbose_name="Weight (kg)")
    type = models.ForeignKey(
        ParcelType, verbose_name="Type", related_name="parcel", on_delete=models.CASCADE
    )
    declared_cost = models.FloatField(verbose_name="Declared cost ($)")
    delivery_cost = models.FloatField(
        verbose_name="Delivery cost (₽)", blank=True, null=True
    )
    status = models.CharField(
        verbose_name="Status", max_length=255, choices=STATUS_CHOICES, default=NEW
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Parcel"
        verbose_name_plural = "Parcels"
