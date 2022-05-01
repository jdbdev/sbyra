from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

"""
Members of the pulic and potential race members can create a User account.
- If a User registers a yacht, is_skipper field set to True via signal
- The field skipper_name will be updated with first name and last name for racing records
"""


class CustomUser(AbstractUser):
    """Custom user model for all registered members and uses email for login / autentication"""

    pass
