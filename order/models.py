from itertools import product
from pyexpat import model
from statistics import mode
from django.db import models
from customer.models import User
from product.models import Product
class Order(models.Model):
  note = models.CharField(max_length=255, null=True)
  user = models.ForeignKey(User, related_name='order', on_delete= models.SET_NULL, null=True)
  address = models.CharField(max_length=255) 
  phone = models.CharField(max_length=20)
  product_quantity = models.IntegerField()
  total = models.BigIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class OrderDetail(models.Model):
  product = models.ForeignKey(Product, related_name='order_detail', on_delete= models.SET_NULL, null=True)
  price = models.BigIntegerField()
  quantity = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
