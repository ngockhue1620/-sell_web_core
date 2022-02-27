from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "quantity",
            "image",
            "image_url",
            "category",
            "id",
        ]
        optional_fields = ["image", "image_url"]
        extra_kwargs = {
            "image": {"required": False, "allow_null": True},
            "image_url": {"required": False, "allow_null": True},
        }
