from django.contrib import admin
from django.urls import include, path

from . import views

"""Content URL Configurations - includes blog posts, articles, upcoming events, etc"""

app_name = "content"

urlpatterns = [
    path("", views.home_page, name="home_page"),
]
