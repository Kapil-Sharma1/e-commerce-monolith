from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from apps.users.views import (
     UserInfoView,  
     VerifyEmailView,
)
from . import views

app_name = 'apps.auth'

router = DefaultRouter()

urlpatterns = router.urls


urlpatterns += [
     path(f"", include("dj_rest_auth.urls")),


     re_path(r'registration/account-confirm-email/(?P<key>[-:\w]+)',
          VerifyEmailView.as_view(), name='account_confirm_email'),

     path('user-info/', UserInfoView.as_view(), name='user-info'),
]
