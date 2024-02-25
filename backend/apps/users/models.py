from uuid import uuid4
import time
from django.contrib.auth.models import(
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.db.models import Sum

from apps.util.models import NCAbstractBaseModel
from apps.util.utils import get_s3_url

def profile_photo(instance, filename):
    return f'user/{instance.uid}/profile_photo/{filename}'


class UserManager(BaseUserManager):
    def _create_user(self, email, phone_number, password, is_staff,
                     is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email, and password.
        """
        user = self.model(
            email=self.normalize_email(email) if email else None,
            phone_number=phone_number,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=timezone.now(),
            registered_at=timezone.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        is_staff = extra_fields.pop('is_staff', False)
        is_superuser = extra_fields.pop('is_superuser', False)
        return self._create_user(email, phone_number, password, is_staff,
                                 is_superuser, **extra_fields)

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        return self._create_user(email, phone_number, password, is_staff=True,
                                 is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(unique=True, default=uuid4, editable=False)
    email = models.EmailField(verbose_name='Email', 
                            max_length=128, 
                            null=True, blank=True)
    first_name = models.CharField(
        verbose_name='First name', max_length=32, default='', blank=True)
    last_name = models.CharField(
        verbose_name='Last name', max_length=32, default='', blank=True)
    phone_number = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(verbose_name='Active', default=True)
    is_staff = models.BooleanField(verbose_name='Staff', default=False)
    registered_at = models.DateTimeField(
        verbose_name='Registered at', auto_now_add=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField(max_length=8, null=True, blank=True)
    city = models.CharField(max_length=108, default='jaipur')
    state = models.CharField(max_length=108, default='rajasthan')
    profile_photo = models.ImageField(max_length=500, 
                                    upload_to=profile_photo,
                                    null=True,
                                    blank=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'

    objects = UserManager()


    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def info(self):
        profile_photo_url = get_s3_url(self.profile_photo.name) if self.profile_photo else None

        return {
            'uid': self.uid,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'profile_photo': profile_photo_url,
            'city' : self.city,
            'state': self.state,
            'registered_at': self.registered_at,
            'date_of_birth': self.date_of_birth,
        }

    def __str__(self):
        if self.email:
            return self.email
        return f'{self.full_name} - {self.phone_number}'
