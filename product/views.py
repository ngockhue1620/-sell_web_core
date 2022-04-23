from ast import keyword
from rest_framework.decorators import action
from unicodedata import name
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
 
  def list(self, request):
    # product?keyword=quan&&price=12
    keyword=request.GET.get("keyword", None)
    if not keyword:
      products = Product.objects.all()
    else:
      products = Product.objects.filter(name__icontains= keyword)
    if products:
      serializer = ProductDetailSerializer(products, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'message': 'No products exist'}, status=status.HTTP_404_NOT_FOUND)    

  def retrieve(self, request, pk=None):
    product = Product.objects.get(id=pk)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


  