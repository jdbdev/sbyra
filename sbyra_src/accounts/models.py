from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from sbyra_src.accounts.managers import UserManager

from .validators import validate_postal_code

"""
Custom User model implementation using django-allauth for email authentication. AbstractBaseUser allows Users to be created
in the admin panel with email to match django-allauth authentication. Once User is created, profile is automatically
generated via signal. 

Adjust forms and related classes to include:

- Default fields for AbstractBaseUser: ID, password, last_login
- Default fields for PermissionsMixin: is_superuser
- Additional fields for Custom User model: first_name, last_name, email, date_joined, is_staff

"""


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email for authentication"""

    email = models.EmailField(
        _("email address"),
        max_length=75,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        _("first name"), max_length=75, blank=True
    )
    last_name = models.CharField(
        _("last name"), max_length=75, blank=True
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text="Designates whether User can log into admin site",
    )
    is_active = models.BooleanField(
        _("active status"),
        default=False,
        help_text="Toggles active status. Deselect instead of deleting account",
    )
    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
        help_text="Records when User first joins site",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        full_name = (f"{self.first_name} {self.last_name}").strip()
        return full_name

    def __str__(self):
        return self.email


class Profile(models.Model):
    """User Profile associated with User model instance via OneToOne relationship. Admin purposes only, no public profile page"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    is_skipper = models.BooleanField(_("skipper status"), default=False)
    city = models.CharField(_("city/town"), max_length=100)
    province = models.CharField(_("province"), max_length=100)
    street_name = models.CharField(_("street name"), max_length=100)
    street_number = models.IntegerField(_("street number"))
    postal_code = models.CharField(
        _("postal code"),
        max_length=7,
        validators=[validate_postal_code],
    )  # create custom validator for postal codes!
