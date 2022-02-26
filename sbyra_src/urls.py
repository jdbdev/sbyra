from django.contrib import admin
from django.urls import include, path

"""sbyra_src URL Configurations"""

urlpatterns = [
    path("admin/", admin.site.urls),
]
