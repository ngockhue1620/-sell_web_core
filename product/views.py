from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import ProductSerializer, ProductDetailSerializer
from .models import Product
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

# Create your views here.
from .models import Category, Product
class ProductViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  parser_classes= [MultiPartParser, ]

  def create(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      headers = self.get_success_headers(serializer.data)
      return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

  def retrieve(self, request, pk=None):
    product = Product.objects.get(id=pk)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)