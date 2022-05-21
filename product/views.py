import imp
from rest_framework import viewsets, status
from .serializers import ProductSerializer, ProductDetailSerializer
from .models import Product
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination
from .models import  Product
from django.shortcuts import get_object_or_404
class ProductViewSet(viewsets.ModelViewSet, PageNumberPagination):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
 
  def list(self, request):
    keyword=request.GET.get("keyword", None)
    if not keyword:
      products = Product.objects.all().order_by("-id")
    else:
      products = Product.objects.filter(name__icontains= keyword).order_by("-id")
    if products:      
      page = self.paginate_queryset(products)
      serializer = ProductDetailSerializer(page, many=True)
      return self.get_paginated_response(serializer.data)
    return Response({'message': 'No products exist'}, status=status.HTTP_404_NOT_FOUND)    
  parser_classes= [MultiPartParser, ]

  def create(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      headers = self.get_success_headers(serializer.data)
      return Response({"message": "Thêm sản phẩm thành công"}, status=status.HTTP_201_CREATED, headers=headers)

  def retrieve(self, request, pk=None):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK) 


  