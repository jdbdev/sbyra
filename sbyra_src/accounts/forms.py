from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """Form to create a new User"""

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    """Form to update User information"""

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")
