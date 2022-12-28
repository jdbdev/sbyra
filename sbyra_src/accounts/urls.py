from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.account_register, name="register"),
    path("update/", views.account_update, name="update"),
]
