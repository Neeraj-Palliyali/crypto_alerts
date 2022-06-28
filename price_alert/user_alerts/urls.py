from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AlertsViewSet

router = DefaultRouter(trailing_slash  = False)

router.register(r"alert", AlertsViewSet, basename= "alert")


urlpatterns = [
    path("api/", include(router.urls))
]
