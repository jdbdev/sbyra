from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

"""
Custom User model implementation using django-allauth for email authentication. Email field provided by allauth.
Profile is automatically created via signal when CustomUser is created.  

"""


class CustomUser(AbstractUser):
    """Custom user model that uses email for login / autentication via allauth"""

    username = None
    email = models.EmailField(
        _("email address"), blank=False, unique=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


class SkipperProfile(models.Model):
    """CustomUser Profile associated with CustomUser model instance via OneToOne relationship"""

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_skipper = models.BooleanField(_("skipper status"), default=False)
    city = models.CharField(_("city/town"), max_length=100)
    province = models.CharField(_("province"), max_length=100)
    street_name = models.CharField(_("street name"), max_length=100)
    street_number = models.IntegerField(_("street number"))
