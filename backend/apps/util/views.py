from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import(
    RetrieveModelMixin, 
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet

action_permissions = {
        "list": [ IsAuthenticated ],
        "retrieve": [ IsAuthenticated ],
        # "partial_update": [ IsAuthenticated, IsAdminUser],
        # "destroy": [ IsAuthenticated, IsAdminUser ],
        "create": [ IsAuthenticated ]
    }


class BaseViewSet(CreateModelMixin,
                RetrieveModelMixin,
                ListModelMixin,
                UpdateModelMixin, 
                DestroyModelMixin,
                GenericViewSet):
    
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'
    lookup_value_regex = '[0-9a-f-]{36}'

    def get_permissions(self):
        if self.action in ['destroy', 'partial_update']:
            raise PermissionDenied()
        else:
            self.permission_classes = action_permissions[self.action] 
            return super().get_permissions()
