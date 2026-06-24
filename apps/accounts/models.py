"""
Custom User model — MUST be created before the first migration.
We extend AbstractUser so we keep all of Django's auth machinery
(groups, permissions, password hashing) while adding our own fields.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extended user model.
    We use email as the login identifier (USERNAME_FIELD = 'email').
    """

    # Make email unique — it is our login username
    email = models.EmailField('email address', unique=True)

    # Extra profile fields
    phone = models.CharField(
        max_length=15, blank=True, null=True,
        help_text='10-digit mobile number'
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/', blank=True, null=True,
        help_text='Profile picture'
    )
    date_of_birth = models.DateField(blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email to log in, not username
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table     = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        full = f'{self.first_name} {self.last_name}'.strip()
        return full or self.email

    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]

    @property
    def avatar_url(self):
        """Return avatar URL or None if no avatar set."""
        if self.avatar:
            return self.avatar.url
        return None