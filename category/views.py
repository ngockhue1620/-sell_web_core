
from rest_framework import viewsets
from .serializers import CategorySerializers
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from .const.category_constain import CategoryStatus
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# Create your views here.
from .models import Category


class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.filter(is_activate=CategoryStatus.ACTIVE)
  serializer_class = CategorySerializers
  parser_classes= [MultiPartParser, ]
  
  # def create(self, request, *args, **kwargs):
  #     serializer = self.get_serializer(data=request.data)
  #     serializer.is_valid(raise_exception=True)
  #     self.perform_create(serializer)
  #     headers = self.get_success_headers(serializer.data)
  #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
  
  # def list(self, request):
  #   fl = {}
  #   isactiveCategory = request.GET.get('isactive', isactive.ACTIVE)
  #   fl.update({'isactive': isactiveCategory})
  #   category = Category.objects.filter(**fl)
  #   serializer = CategorySerializers(category, many =True)
  #   return Response(serializer.data, status=status.HTTP_200_OK)


  
  def partial_update(self, request, pk=None):
    category = get_object_or_404(Category, id=pk)
    serialzer = CategorySerializers(category, data=request.data, partial=True)
    if serialzer.is_valid(raise_exception=True):
      serialzer.save()
      return Response({"message": "Thành Công", "data": serialzer.data}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
  
  