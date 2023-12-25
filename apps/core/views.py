import logging

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core import docs, tasks
from apps.core.models import Parcel, ParcelType
from apps.core.serializers import (
    ParcelRegisterSerializer,
    ParcelsSerializer,
    ParcelTypeSerializer,
)

logger = logging.getLogger("django")

SESSION_DICT_KEY = "user_parcels"


class ParcelTypeView(viewsets.ModelViewSet):
    model = ParcelType
    serializer_class = ParcelTypeSerializer
    queryset = ParcelType.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Getting data about all parcel types.
        """

        # pylint: disable=useless-super-delegation
        return super().list(request, *args, **kwargs)


@method_decorator(name="create", decorator=docs.PARCEL_REGISTER_VIEW_CREATE_SCHEMA)
class ParcelRegisterView(viewsets.ModelViewSet):
    model = Parcel
    instance = None
    serializer_class = ParcelRegisterSerializer

    def create(self, *args, **kwargs):
        """
        Create an instance of model
        and write information about it to session data.
        """

        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        self.instance = serializer.save()

        if SESSION_DICT_KEY not in self.request.session:
            self.request.session[SESSION_DICT_KEY] = []

        self.request.session[SESSION_DICT_KEY].append(self.instance.id)
        self.request.session.modified = True

        logger.info(
            {
                "ParcelRegisterView.create": {
                    f"An instance was created (id: {self.instance.id}) "
                    f"and recorded in user's session data "
                    f"({self.request.session.session_key}: "
                    f"{self.request.session[SESSION_DICT_KEY]})."
                }
            }
        )

        return Response({"parcel_id": self.instance.id}, status=status.HTTP_201_CREATED)


class ParcelRegisterAndProcessingView(ParcelRegisterView):
    def create(self, *args, **kwargs):
        """
        Create and processing an instance of model
        and write information about it to session data.
        """

        super().create(*args, **kwargs)
        tasks.processing_parcel.delay(parcel_id=self.instance.id)

        return Response({"parcel_id": self.instance.id}, status=status.HTTP_201_CREATED)


class ParcelsResultsPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = "page_size"


@method_decorator(name="list", decorator=docs.PARCELS_VIEW_LIST_SCHEMA)
class ParcelsView(viewsets.ModelViewSet):
    model = Parcel
    serializer_class = ParcelsSerializer
    pagination_class = ParcelsResultsPagination

    def get_queryset(self):
        """
        Retrieving objects from db that belong to user within his session.
        """

        session_data = self.request.session.get(SESSION_DICT_KEY, [])

        logger.info(
            {
                "ParcelsView.get_queryset": {
                    f"Instances corresponding to IDs in session data "
                    f"({self.request.session.session_key}: {session_data}) are selected"
                }
            }
        )

        return Parcel.objects.filter(id__in=session_data).order_by("id")

    def retrieve(self, request, *args, **kwargs):
        """
        Getting data about a specific user's parcel within his session.
        """

        # pylint: disable=useless-super-delegation
        return super().retrieve(request, *args, **kwargs)

    def list(self, *args, **kwargs):
        """
        Getting data about all user's parcels within his session.
        """

        content_type = self.request.query_params.get("content_type")
        delivery_cost = self.request.query_params.get("delivery_cost")

        queryset = self.get_queryset()

        if content_type:
            queryset = queryset.filter(type__name=content_type)

        if delivery_cost:
            if delivery_cost.lower() == "null":
                queryset = queryset.filter(delivery_cost__isnull=True)
            elif delivery_cost.lower() == "not_null":
                queryset = queryset.filter(delivery_cost__isnull=False)

        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.serializer_class(paginated_queryset, many=True)

        return self.get_paginated_response(serializer.data)


@method_decorator(name="get", decorator=docs.ADMIN_UPDATE_VIEW_GET_SCHEMA)
class ParcelsProcessingAdminUpdateView(APIView):
    """
    View for manually starting a task in admin panel for debugging.
    """

    @staticmethod
    def get(*args, **kwargs):
        tasks.processing_new_parcels.delay()

        return redirect(reverse("admin:core_parcel_changelist"))


@method_decorator(name="get", decorator=docs.ADMIN_UPDATE_VIEW_GET_SCHEMA)
class CachingUSDExchangeRate(APIView):
    """
    View for manually starting a task in admin panel for debugging.
    """

    @staticmethod
    def get(*args, **kwargs):
        tasks.cache_usd_exchange_rate.delay()

        return redirect(reverse("admin:core_parcel_changelist"))
