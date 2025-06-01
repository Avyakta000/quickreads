from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator

from django.utils import timezone
from rest_framework_api_key.models import AbstractAPIKey

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('viewer', 'Viewer'),
        ('author', 'Author'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    # is_email_verified = models.BooleanField(default=False)
    # role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='viewer')
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', "last_name"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin


# Application API Key
class ApplicationAPIKey(AbstractAPIKey):
    # Who or what is using this key?
    client_name = models.CharField(max_length=255)
    client_type = models.CharField(
        max_length=50,
        choices=[("internal", "Internal"), ("third_party", "Third Party"),],
        default="third_party"
    )
    application = models.CharField(max_length=100, blank=True, help_text="Which app/service uses this key")
    purpose = models.TextField(blank=True, help_text="Describe purpose of key usage")

    # Usage control
    is_unlimited = models.BooleanField(default=False)
    usage_limit = models.PositiveIntegerField(default=1000)
    usage_count = models.PositiveIntegerField(default=0)

    # Lifecycle tracking
    is_active = models.BooleanField(default=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    # Ownership / Audit
    created_by = models.ForeignKey('myaccount.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Application API Key"
        verbose_name_plural = "Application API Keys"

    def increment_usage(self):
        """Tracks usage and enforces limits if not unlimited."""
        if not self.is_unlimited:
            if self.usage_count > self.usage_limit:
                return False
        self.usage_count += 1
        self.last_used_at = timezone.now()
        self.save(update_fields=["usage_count", "last_used_at"])
        return True

    def has_quota(self):
        """Returns True if the key can be used."""
        return self.is_active and (self.is_unlimited or self.usage_count < self.usage_limit)
    