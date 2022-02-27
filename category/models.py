from django.db import models

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=255)
  image = models.ImageField(upload_to = 'images/category')  
  image_url = models.TextField(null=True)
  def __str__(self):
    return self.name