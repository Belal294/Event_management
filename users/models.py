from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import os

# Function to return default profile picture path
def default_profile_picture():
    return 'profile_pics/default.jpg'

class CustomUser(AbstractUser):
    """
    Custom User Model with additional fields:
    - phone_number: Stores user’s phone number with validation
    - profile_picture: Stores user’s profile image
    - bio: Short user bio
    - role: Defines user role (Admin, Organizer, Participant)
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('participant', 'Participant'),
    )

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
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_set", blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """ Override save method to ensure default profile picture exists """
        if not self.profile_picture:
            self.profile_picture = default_profile_picture()
        super().save(*args, **kwargs)
