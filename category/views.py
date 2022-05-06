from unicodedata import category
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializers
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from .const.isactive import isactive
# Create your views here.
from .models import Category
class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializers
  parser_classes= [MultiPartParser, ]
  
  # def create(self, request, *args, **kwargs):
  #     serializer = self.get_serializer(data=request.data)
  #     serializer.is_valid(raise_exception=True)
  #     self.perform_create(serializer)
  #     headers = self.get_success_headers(serializer.data)
  #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
  
  def list(self, request):
    fl = {}
    isactiveCategory = request.GET.get('isactive', isactive.ACTIVE)
    fl.update({'isactive': isactiveCategory})
    category = Category.objects.filter(**fl)
    serializer = CategorySerializers(category, many =True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def update(self, request, pk=None):
    category = Category.objects.get(id=pk)
    category.isactive = isactive.DONE
    category.save()
    return Response(status=status.HTTP_200_OK)