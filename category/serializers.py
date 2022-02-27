from rest_framework import serializers
from .models import Category


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "image", "image_url"]
        extra_kwargs = {
            "image": {"required": False, "allow_null": True},
            "image_url": {"required": False, "allow_null": True},
        }
