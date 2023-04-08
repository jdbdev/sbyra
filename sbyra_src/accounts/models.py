from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
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
    """Custom user model that uses email for authentication and confirmation"""

    email = models.EmailField(
        _("email address"),
        max_length=100,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=75,
        blank=True,
        help_text="required",
    )
    last_name = models.CharField(
        _("last name"),
        max_length=75,
        blank=True,
        help_text="required",
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text="Designates whether User can log into admin site",
    )
    is_email_verified = models.BooleanField(
        _("verified email"),
        default=False,
        help_text="toggles True if user has verified account by email",
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
    date_updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["last_name"]

    def get_full_name(self):
        full_name = (f"{self.first_name} {self.last_name}").strip()
        return full_name

    def email_user(self, subject, message, *arg, **kwargs):
        """additional wraper over django's send_mail() function"""
        send_mail(
            subject,
            message,
            "1@1.com",
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    """User Profile associated with User model instance via OneToOne relationship. Admin purposes only, no public profile page"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_skipper = models.BooleanField(_("skipper status"), default=False)
    country = CountryField(_("country"), blank=True)
    city = models.CharField(_("city/town"), max_length=100)
    province = models.CharField(_("province"), max_length=100)
    street_name = models.CharField(
        _("street name"), max_length=100, blank=True
    )
    street_number = models.IntegerField(
        _("street number"), blank=True, null=True
    )
    postal_code = models.CharField(
        _("postal code"),
        max_length=7,
        help_text=_("format: A1AA1A"),
        validators=[validate_postal_code],
    )  # refer to validators.py for custom validators

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
