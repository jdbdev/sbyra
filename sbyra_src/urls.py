from django.contrib import admin
from django.urls import include, path

"""sbyra_src URL Configurations"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "", include("sbyra_src.content.urls")
    ),  # links to blog and all base content
    path(
        "racing/", include("sbyra_src.racing.urls")
    ),  # links to all racing related content
]
