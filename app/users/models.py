from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
import app.users.constants as _const
from app.utils.storages import return_image_upload_path


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have a staff.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is superuser admin.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(blank=True, null=True, max_length=254, unique=True)
    username = None
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'tb_user'

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email


class UserProfile(models.Model):
    GENDERS = (
        (_const.OTHER, _const.OTHER),
        (_const.MALE, _const.MALE),
        (_const.FEMALE, _const.FEMALE)
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_relate_profile')
    address = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to=return_image_upload_path, blank=True)
    gender = models.IntegerField(choices=GENDERS, default=0)
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'tb_user_profile'
