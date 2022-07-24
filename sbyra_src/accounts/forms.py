from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (  # existing Django forms
    UserChangeForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

""" All form fields must match model field types and configuration in accounts.models.User class. """


class RegistrationForm(forms.ModelForm):
    """Custom registration form for User model"""

    email = forms.EmailField(
        label="Enter valid email",
        max_length=100,
        help_text=_("Email required"),
        error_messages={"Required": "Please enter a valid email"},
    )
    first_name = forms.CharField(
        label="Last Name",
        max_length=75,
        help_text=_("First name required"),
    )
    last_name = forms.CharField(
        label="First Name",
        max_length=75,
        help_text=_("Last name required"),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=_("Password required"),
    )
    password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput,
        help_text=_("Required: Repeat Password"),
    )

    class Meta:
        model = get_user_model()
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
        model = get_user_model()
        fields = ("email", "first_name", "last_name")
