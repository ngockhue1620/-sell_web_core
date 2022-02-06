from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
# Create your views here.
from .models import Category, Product
class ProductViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer