from django.contrib import admin

from apps.core.models import Parcel, ParcelType


@admin.register(ParcelType)
class ParcelTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)

    @staticmethod
    def has_delete_permission(request, obj=None, **kwargs):
        return False


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "weight",
        "type",
        "declared_cost",
        "delivery_cost",
        "status",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")
