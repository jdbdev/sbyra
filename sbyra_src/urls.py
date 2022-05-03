from django.contrib import admin
from django.urls import include, path

"""sbyra_src URL Configurations"""

urlpatterns = [
    path("", include("sbyra_src.content.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("racing/", include("sbyra_src.racing.urls")),
]
