from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import os

class CustomUser(AbstractUser):
    # Phone number and profile picture are already here
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Enter a valid phone number (9-15 digits, with optional + prefix).")
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_regex],
        blank=True, 
        null=True
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        default=default_profile_picture,  
        blank=True
    )

    bio = models.TextField(blank=True, null=True)

    # New role field
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',  # Default role is 'user'
    )

    def __str__(self):
        return self.username
