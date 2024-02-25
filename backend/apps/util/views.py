from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import(
    RetrieveModelMixin, 
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin
)
from rest_framework.viewsets import GenericViewSet


class BaseViewSet(CreateModelMixin,
                RetrieveModelMixin,
                GenericViewSet
            ):
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'


class BaseListViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'
