from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import os

def default_profile_picture():
    return 'profile_pics/default.jpg'  # Ensure this file exists in media directory

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Enter a valid phone number (9-15 digits, with optional + prefix).")
    )

    phone_number = models.CharField(
    max_length=15,
    unique=True,
    validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Enter a valid phone number (9-15 digits, with optional + prefix).")
    )],
    blank=True, 
    null=True
)


    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        default=default_profile_picture,  
        blank=True
    )

    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
