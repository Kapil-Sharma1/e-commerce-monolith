import json
from dj_rest_auth.utils import jwt_encode
from google.oauth2 import id_token
from google.auth import transport

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from apps.users.models import User, Address
from apps.users.serializers import(
    UserDetailsSerializer,
    UserAddressSerializer
)
from apps.util.two_factor import TwoFactor
from apps.util.views import BaseViewSet

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(phone_number=request.user.phone_number).first()
        return Response(user.info, status=status.HTTP_200_OK)


class LoginOTPAPIView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number', "")
        if not phone_number:
            return Response(
                data={
                    'message': 'Phone number is required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if settings.DEBUG:
            return Response(
                data={
                    "message": "OTP is sent. Please check your Phone message box",
                    "data": {
                        "Status": "Success",
                        "Details": "ec3a1388-9207-4cb2-89e1-cba24cdee304"
                    }
                },
            )
        two_factor = TwoFactor()
        response = two_factor.generate_otp(
            phone_number=phone_number
        )

        if response.status_code == 200:
            return Response(
                data={
                    'message': 'OTP is sent. Please check your Phone message box',
                    'data': response.json()
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)


class LoginOTPVerifyAPIView(APIView):

    def post(self, request):

        otp = request.data.get('otp', "")
        if not otp:
            return Response(
                data={
                    'message': 'OTP is required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        otp_session_id = request.data.get('otp_session_id', "")
        if not otp_session_id:
            return Response(
                data={
                    'message': 'otp_session_id is required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        phone_number = request.data.get('phone_number', "")
        if not phone_number:
            return Response(
                data={
                    'message': 'Phone number is required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        fcm_token = request.data.get('fcm_token', "")
        if not fcm_token:
            return Response(
                data={
                    'message': 'fcm token is required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if settings.DEBUG:
            # In debug mode, you can automatically verify the default OTP.
            default_otp = "123456"
            otp = request.data.get('otp', "")
            if default_otp != otp:
                return Response({"detail": "OTP doesnot matched"},
                                status=status.HTTP_400_BAD_REQUEST)

            return self.generate_token(request, phone_number=phone_number, fcm_token=fcm_token) 

        two_factor = TwoFactor()
        response = two_factor.verify_otp(
            otp=otp,
            otp_session_id=otp_session_id,
        )

        if response.status_code == 200:
            return self.generate_token(request, phone_number=phone_number, fcm_token=fcm_token)
        else:
            return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)

    def generate_token(self, request, phone_number, fcm_token):
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            user = User.objects.create(phone_number=phone_number)

        user.save()
        user_details = UserDetailsSerializer(user, context={'request': request}).data

        access_token, refresh_token = jwt_encode(user)
        return Response(
            data={
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
                'user': user_details
            },
            status=status.HTTP_200_OK
        )


class GoogleSignUpLoginAPIView(APIView):

    def post(self, request):

        token = request.data.get('token')
        if not token:
            return Response(
                data={'message': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        google_auth_request = transport.requests.Request()
        google_client_id = settings.GOOGLE_CLIENT_ID

        try:
            id_info = id_token.verify_oauth2_token(
                token, google_auth_request, google_client_id)
        
        except ValueError as e:
            return Response(
                data={
                    'message': 'Either token is invalid or expired'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.filter(email=id_info['email']).first()
        if not user:
            user_data = {
                'email': id_info['email']
            }
            if 'given_name' in id_info:
                user_data['first_name'] = id_info['given_name']
            if 'family_name' in id_info:
                user_data['last_name'] = id_info['family_name']
            
            user = User.objects.create(**user_data)

        user_details = UserDetailsSerializer(user).data
        
        access_token, refresh_token = jwt_encode(user)
        return Response(
            data={
                'access_token' : str(access_token),
                'refresh_token' : str(refresh_token),
                'user' : user_details
            },
            status=status.HTTP_200_OK
        )


class UserAddressViewSet(BaseViewSet):

    queryset = Address.objects.all()
    serializer_class = UserAddressSerializer  

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = Address.objects.filter(
            user=self.request.user
        )
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        else:
            return super().get_permissions()
        
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Check if is_default=True is passed in the request data
        if serializer.validated_data.get('is_default'):
            # Find the existing default address for the user
            default_address = Address.objects.filter(user=request.user, is_default=True).first()

            # If a default address exists, update it to not be the default anymore
            if default_address and default_address != instance:
                default_address.is_default = False
                default_address.save()

        self.perform_update(serializer)
        return Response(serializer.data)
