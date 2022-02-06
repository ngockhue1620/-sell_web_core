from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet
router = SimpleRouter()
router.register('', CategoryViewSet, 'category')

urlpatterns = [
    path('', include(router.urls)),
]

