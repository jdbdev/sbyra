from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom object manager for User model"""

    def _create_user(
        self,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):
        """
        Higher level function called by create_user(), create_staff() and create_superuser().
        Provides validation for required fields; email, first_name, last_name
        """
        if not email:
            raise ValueError(_("Members must have an email address"))
        email = self.normalize_email(email)

        if not first_name:
            raise ValueError(_("You must enter a first name"))

        if not last_name:
            raise ValueError(_("You must enter a last name"))

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(
            email, first_name, last_name, password, **extra_fields
        )

    def create_staffuser(
        self,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        if extra_fields.get("is_saff") is not True:
            raise ValueError("Staff status must be set to True")
        return self._create_user(
            email, password, first_name, last_name**extra_fields
        )

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superuser status must be set to True for superuser")
            )
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                _("Staff status must be set to True for a superuser")
            )
        if extra_fields.get("is_active") is not True:
            raise ValueError(
                _("Active status must be set to True for a superuser")
            )

        return self._create_user(
            email, first_name, last_name, password, **extra_fields
        )
