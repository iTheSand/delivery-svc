from drf_yasg import openapi
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema

PARCEL_REGISTER_VIEW_CREATE_SCHEMA = swagger_auto_schema(
    responses={201: openapi.Response("Parcel ID")}
)

PARCELS_VIEW_LIST_SCHEMA = swagger_auto_schema(
    manual_parameters=[
        Parameter(
            "content_type",
            required=False,
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="clothes, electronics or other",
        ),
        Parameter(
            "delivery_cost",
            required=False,
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="null or not_null",
        ),
    ]
)

ADMIN_UPDATE_VIEW_GET_SCHEMA = swagger_auto_schema(auto_schema=None)
