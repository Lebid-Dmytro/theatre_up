from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from cinema_up_project.docs.schema import schema_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("cinema_up_project.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", obtain_auth_token),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
