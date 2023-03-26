from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (  # existing Django forms
    UserChangeForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

""" All form fields must match model field types and configuration in accounts.models.User class. """

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    """Custom registration form for User model"""

    email = forms.EmailField(
        label="Email",
        max_length=100,
        help_text=_("required"),
        # error_messages={"a valid email is required to register"},
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=75,
        help_text=_("required"),
        # error_messages={"your first name is required to register"},
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=75,
        help_text=_("required"),
        # error_messages={"your last name is required to register"},
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=_("required"),
    )
    password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput,
        help_text=_("Must match Password"),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        )


class CustomUserChangeForm(UserChangeForm):
    """Form to update User information"""

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
