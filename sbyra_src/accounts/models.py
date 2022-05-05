from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

"""
Custom User model implementation using django-allauth for email authentication. AbstractBaseUser allows Users to be created
in the admin panel with email to match django-allauth authentication. Once User is created, profile is automatically
generated via signal. 

1. Override User model provided by django.contrib.auth
2. Create Custom UserManager that inherits from BaseUserManager
3. Define methods User and Superuser creating methods (include fields in Custom User model)
4. Create Custom User model that inherits from AbstractBaseUser
5. Add fields required by application
6. Modify UserCreationForm and UserChangeForm to match User model fields

Default fields for AbstractBaseUser: ID, password, last_login

"""


class UserManager(BaseUserManager):
    """Custom object manager for User model"""

    def _create_user(self, email, password=None, **extra_fields):
        """Higher level function called by create_user(), create_staff() and create_superuser()"""
        if not email:
            raise ValueError("Members must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return User

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        if extra_fields.get("is_saff") is not True:
            raise ValueError("Staff status must be set to True")
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser status must be set to True")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """Custom user model that uses email for authentication"""

    email = models.EmailField(
        _("email address"),
        max_length=60,
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
        default=True,
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
        # "first_name",
        # "last_name",
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
    """User Profile associated with User model instance via OneToOne relationship"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_skipper = models.BooleanField(_("skipper status"), default=False)
    city = models.CharField(_("city/town"), max_length=100)
    province = models.CharField(_("province"), max_length=100)
    street_name = models.CharField(_("street name"), max_length=100)
    street_number = models.IntegerField(_("street number"))
