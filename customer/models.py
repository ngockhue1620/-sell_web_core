from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  avatar = models.TextField(null= True)
  phone = models.CharField(max_length=15, blank=True)
  fullname = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True) 
