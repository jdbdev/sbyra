from django.shortcuts import render
from django.urls import include, path

from . import views

"""Racing URL Configurations - includes all pages related to yacht racing"""


app_name = "racing"

urlpatterns = [
    path("", views.racing_home, name="racing_home"),
    path("yachts/", views.list_yachts, name="list_yachts"),
]
