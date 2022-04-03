from statistics import mode
from django.db import models
from customer.models import User
from product.models import Product

class Comment(models.Model):
    comment = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(
        User, related_name="comments", on_delete=models.SET_NULL, null=True
    )
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/comment", null=True)
    image_url = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)