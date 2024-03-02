from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from apps.users.views import(
     UserInfoView,
     LoginOTPAPIView,
     LoginOTPVerifyAPIView,
     GoogleSignUpLoginAPIView,
     UserAddressViewSet
)
from . import views

app_name = 'apps.auth'

router = DefaultRouter()

router.register('user-address', UserAddressViewSet, basename='user-address-api')

urlpatterns = router.urls


urlpatterns += [
     path(f"", include("dj_rest_auth.urls")),

     path('user-info/', UserInfoView.as_view(), name='user-info'),
     path('mobile-login/', LoginOTPAPIView.as_view(), name='login-otp-generate-API'),
     path('login-verify-otp/', LoginOTPVerifyAPIView.as_view(), name='login-otp-verify-API'),
     path('google-login/', GoogleSignUpLoginAPIView.as_view(), name='google-login'),
]
