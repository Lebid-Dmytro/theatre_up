from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("cinema_up_project.urls")),
    path("api/user/", include("user.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", obtain_auth_token),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
