from dj_rest_auth.serializers import PasswordChangeSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

from rest_framework import serializers

from django.conf import settings
from django.db import transaction
from django.db.models import Sum

from apps.users.models import User
from apps.util.serializers import UIDField
from apps.util.utils import send_email, get_s3_url

    
class UserDetailsSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('uid', 'email', 'first_name', 'last_name',
            'full_name', 'city', 'state', 'profile_photo', 
            'phone_number')
        
    def get_profile_photo(self, obj):
        return get_s3_url(obj.profile_photo.name) if obj.profile_photo else None
    

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)

        profile_photo = self.context['request'].data.get('profile_photo')
        if profile_photo:
            instance.profile_photo = profile_photo

        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('uid', 'email', 'first_name', 'last_name',
                'phone_number', 'is_active', 'full_name', 
                'city')


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class NCPasswordChangeSerializer(PasswordChangeSerializer):

    def save(self):
        self.set_password_form.save()
        send_email(
            subject="Reset Password Successfully",
            recipient_email=[self.user.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            text_template_path="mail/reset_password_confirm.txt",
            html_template_path="mail/reset_password_confirm.html",
            merge_data={"first_name": self.user.first_name})
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)
