"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls import url
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from apps.users.views import VerifyEmailView
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='NEX API')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include(('apps.users.urls', 'users'), namespace='auth-api')),

    path('api/swagger/', schema_view),
    re_path(r'api/auth/registration/account-confirm-email/',
            VerifyEmailView.as_view(), name='account_email_verification_sent'),

    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

    # # catch all the rest
    # url(r"^.*$", TemplateView.as_view(template_name="index.html")),
]   