from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayViewSet, PerformanceViewSet, ReservationViewSet


router = DefaultRouter()
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
