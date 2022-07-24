from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)

from .forms import RegistrationForm
from .models import User
from .tokens import account_activation_token


def account_register(request):
    """Account registration function that also verifies if user is logged in"""
    if request.user.is_authenticated:
        return redirect("racing:racing-home")

    if request.method == "POST":
        # get the POST data:
        register_form = RegistrationForm(request.POST)
        # Validate and capture POST data:
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data["email"]
            user.first_name = register_form.cleaned_data["first_name"]
            user.last_name = register_form.cleaned_data["last_name"]
            user.set_password(register_form.cleaned_data["password"])
            user.is_active = False  # set as default in User model
            user.save()
            # Generate activation email:
            current_site = get_current_site(request)
            subject = "Activate your SBYRA account"
            message = render_to_string(
                "accounts/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            # Send activation email
            user.email_user(subject=subject, message=message)
            return HttpResponse(
                "Thank you for registering! An activation email has been sent."
            )

    else:
        register_form = RegistrationForm()
        template = "accounts/registration/register.html"
        context = {"form": register_form}
        return render(request, template, context)


@login_required
def account_update(request):
    """Account update function"""
    template = ""
    context = ""
    return render(request, template, context)
