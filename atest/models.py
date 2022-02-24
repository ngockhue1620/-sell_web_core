from django.db import models

# Create your models here.
class Atest(models.Model):
  name = models.CharField(max_length=255)
  image = models.ImageField(upload_to = 'images/%Y/%m')
  test = models.IntegerField()
  def __str__(self):
    return self.name