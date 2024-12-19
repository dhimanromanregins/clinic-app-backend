from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, id_number, first_name, last_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone number must be set')
        if not id_number:
            raise ValueError('The ID number must be set')

        user = self.model(
            phone_number=phone_number,
            id_number=id_number,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, id_number, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, id_number, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    id_number = models.CharField(max_length=18, unique=True)
    is_parent = models.BooleanField(default=True)
    is_child = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)
    device_token = models.CharField(max_length=255, null=True, blank=True)


    # Password field is provided by AbstractBaseUser, but you can add a custom password field if desired
    password = models.CharField(max_length=255)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['id_number', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"




class Banner(models.Model):
    image = models.ImageField(upload_to='banners/', verbose_name='Banner Image')
    def __str__(self):
        # Get the file name from the image field path
        return os.path.basename(self.image.name)

class Notifications(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user}"
