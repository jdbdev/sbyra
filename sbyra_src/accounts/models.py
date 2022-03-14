from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

"""
Members of the pulic and potential race members can create a User account.
- If a User registers a yacht, is_skipper field set to True via signal
- The field skipper_name will be updated with first name and last name for racing records
"""


class MemberManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        created,
        modified,
        is_skipper,
        is_staff,
        is_active,
    ):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
        )


class Member(AbstractBaseUser, PermissionsMixin):
    """Custom User model. Members are required to enter first name and last name for sbyra documentation"""

    email = models.EmailField(help_text=_("email address"), unique=True)
    username = models.CharField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_skipper = models.BooleanField(
        default=False, help_text=_("are you a skipper?")
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        if self.username:
            return self.username
        else:
            return f"{self.first_name} {self.last_name}"


class SkipperProfile(models.Model):
    """Required information for Members that are skippers and registering a Yacht"""

    first_name = models.CharField(
        max_length=50, help_text=_("first name")
    )
    last_name = models.CharField(
        max_length=50, help_text=_("last name")
    )
    phone_number = models.CharField(max_length=10)  # required
    address_city = models.CharField(max_length=75)  # optional?
    address_street = models.CharField(max_length=25)  # optional?
    address_postal = models.CharField(max_length=6)  # optional?
    yacht = (
        models.ForeignKey()
    )  # add automatically when registering Yacht

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
