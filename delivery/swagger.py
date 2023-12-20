from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["https", "http"]
        return schema


SchemaView = get_schema_view(
    openapi.Info(
        title="Delivery service API",
        default_version="v1",
        description="Provides access to the calculation of the cost of parcel delivery",
        terms_of_service="",
        contact=openapi.Contact(name="t.me/ithesand"),
        license=openapi.License(name="BSD License"),
    ),
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=(AllowAny,),
    public=True,
)
