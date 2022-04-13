from django.shortcuts import render
from django.urls import include, path

from . import views

"""Racing URL Configurations - includes all pages related to yacht racing"""


app_name = "racing"

urlpatterns = [
    path("", views.racing_home, name="racing-home"),
    path("yachts/", views.list_yachts, name="list-yachts"),
    path(
        "yachts/register",
        views.yacht_register,
        name="yacht-register",
    ),
    # <datatype:data> data can be str, int or slug
    path(
        "yachts/<slug:slug>", views.yacht_details, name="yacht-details"
    ),
]
