from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializers
# Create your views here.
from .models import Category
class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializers