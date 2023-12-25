from django.urls import path

from apps.core import views

app_name = "core"

urlpatterns = [
    path(
        "parcel-types",
        views.ParcelTypeView.as_view({"get": "list"}),
        name="parcel-types",
    ),
    path(
        "parcel-register",
        views.ParcelRegisterView.as_view({"post": "create"}),
        name="parcel-register",
    ),
    path(
        "parcel-register-and-processing",
        views.ParcelRegisterAndProcessingView.as_view({"post": "create"}),
        name="parcel-register-and-processing",
    ),
    path(
        "parcels/<int:pk>",
        views.ParcelsView.as_view({"get": "retrieve"}),
        name="parcel",
    ),
    path("parcels", views.ParcelsView.as_view({"get": "list"}), name="parcels"),
    path(
        "parcels-processing/admin-update",
        views.ParcelsProcessingAdminUpdateView.as_view(),
        name="parcels-processing-admin-update",
    ),
    path(
        "caching-usd-exchange-rate/admin-update",
        views.CachingUSDExchangeRate.as_view(),
        name="caching-usd-exchange-rate-admin-update",
    ),
]
