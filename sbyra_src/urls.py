from django.contrib import admin
from django.urls import include, path

"""
sbyra_src URL Configurations and namespace;

accounts: app_name='accounts'
racing: app_name='racing'
content: app_name='content'

"""

urlpatterns = [
    path("", include("sbyra_src.content.urls")),
    path("admin/", admin.site.urls),
    path(
        "accounts/",
        include("sbyra_src.accounts.urls", namespace="accounts"),
    ),
    path(
        "racing/", include("sbyra_src.racing.urls", namespace="racing")
    ),
]
