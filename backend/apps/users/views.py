import json
from dj_rest_auth.utils import jwt_encode

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_auth.views import PasswordResetView
from rest_auth.registration.views import (
    VerifyEmailView,
    RegisterView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.mixins import(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from django.conf import settings
from django.shortcuts import redirect
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django import forms
from django.urls import reverse
from django.shortcuts import get_object_or_404

from apps.users.models import User
from apps.users.serializers import(
    UserDetailsSerializer,
    UserProfileSerializer,
)
from apps.util.utils import get_s3_url, send_push_notification


class VerifyEmailView(VerifyEmailView):

    def get(self, request, *args, **kwargs):
        kwargs.update(request.data)
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        user = confirmation.email_address.user
        return redirect("/")


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(phone_number=request.user.phone_number).first()
        return Response(user.info, status=status.HTTP_200_OK)
