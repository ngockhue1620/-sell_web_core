from django.db import models
from category.models import Category

class Product(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  price = models.BigIntegerField()
  quantity = models.IntegerField()
  image = models.ImageField(upload_to = 'images/%Y/%m')
  activate= models.BooleanField(default=True)
  category = models.ForeignKey(Category, related_name='products',on_delete=models.SET_NULL, null= True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
