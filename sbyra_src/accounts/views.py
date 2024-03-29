from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)

from .forms import RegistrationForm
from .models import User
from .tokens import account_activation_token


@login_required
def dashboard(request):
    return render(request, "accounts/user/dashboard", {})


def account_register(request):
    """Account registration function that also verifies if user is already registered and sends activation email"""
    if request.user.is_authenticated:
        return redirect("racing:racing-home")

    if request.method == "POST":
        # 01 get the POST data:
        register_form = RegistrationForm(request.POST)
        # 02 Validate and capture POST data:
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data["email"]
            user.first_name = register_form.cleaned_data["first_name"]
            user.last_name = register_form.cleaned_data["last_name"]
            user.set_password(register_form.cleaned_data["password"])
            user.is_active = False  # set as default in User model
            user.save()

            # 03 Generate activation email:
            current_site = get_current_site(request)
            subject = "Activate your SBYRA account"
            message = render_to_string(
                "accounts/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(
                        force_bytes(user.pk)
                    ),  # bytestring to base64 string for url use.
                    "token": account_activation_token.make_token(user),
                },
            )

            # 04 Send activation email (email_user() calls send_mail() function in models.py.User)
            user.email_user(subject=subject, message=message)
            return HttpResponse(
                "Thank you for registering! An activation email has been sent."
            )

    else:
        register_form = RegistrationForm()

    return render(
        request,
        "accounts/registration/register.html",
        {"form": register_form},
    )


def account_activate(
    request, uidb64, token
):  # refer to accounts.urls.py for passed parameters uidb64 and token
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(
        user, token
    ):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("racing:dashboard")
    else:
        return redirect(
            request, "accounts/registration/activation_failed.html"
        )


@login_required
def account_update(request):
    """Account update function"""

    account_form = RegistrationForm(instance=request.user)
    # account_profile = ProfileForm(instance=request.user)

    template = ""
    context = ""
    return render(request, template, context)
