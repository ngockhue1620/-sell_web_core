from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import OrderViewSet, OrderDetailViewSet

router = SimpleRouter()
router.register("", OrderViewSet, "order")
router.register("detail", OrderDetailViewSet, "order_detail")
urlpatterns = [
    path("", include(router.urls)),
]
