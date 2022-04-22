from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import ProductSerializer, ProductDetailSerializer
from .models import Product
from rest_framework.response import Response
# Create your views here.
from .models import Category, Product
class ProductViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

  def retrieve(self, request, pk=None):
    product = Product.objects.get(id=pk)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)