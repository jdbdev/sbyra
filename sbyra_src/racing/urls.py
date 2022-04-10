from django.shortcuts import render
from django.urls import include, path

from . import views

"""Racing URL Configurations - includes all pages related to yacht racing"""


app_name = "racing"

urlpatterns = [
    path("", views.racing_home, name="racing-home"),
    path("yachts/", views.list_yachts, name="list-yachts"),
    # <datatype:data>
    path(
        "yachts/<slug:slug>", views.yacht_details, name="yacht-details"
    ),
]
