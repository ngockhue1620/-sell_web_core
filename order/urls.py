from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import OrderViewSet

router = SimpleRouter()
router.register("", OrderViewSet, "order")

urlpatterns = [
    path("", include(router.urls)),
]
