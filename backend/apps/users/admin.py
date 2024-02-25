from allauth.socialaccount.models import(
    SocialToken, 
    SocialAccount, 
    SocialApp
)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.template.response import TemplateResponse

from apps.users.models import User
from apps.users.forms import UserChangeForm, UserCreationForm
from apps.util.admin import BaseModelAdmin


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['id', 'uid', 'full_name', 'email', 
                    'phone_number']
    fieldsets = [
        ['Auth', {'fields': ['uid', 'email', 'password']}],
        ['Personal info', {'fields': [
            'last_name', 'first_name', 'phone_number', 
            'date_of_birth', 'city', 'state', 'profile_photo'


        ]}],
        ['Settings', {'fields': ['is_active', 'is_staff', 'is_superuser']}],
        ['Groups', {'fields': ['groups']}],
        ['Important dates', {'fields': ['last_login', 'registered_at']}],
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        [None, {'classes': ['wide'],
                'fields': ['email', 'first_name', 'last_name', 'phone_number',
                           'password1', 'password2'
                ]}],
    ]
    search_fields = ['email', 'phone_number']
    ordering = ['email']
    readonly_fields = ['uid', 'last_login', 'registered_at']


admin.site.register(User, UserAdmin)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
