from rest_framework import serializers
from .models import Category


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image", "image_url", "is_activate"]
        extra_kwargs = {
            "image": {"required": False, "allow_null": False},
            "image_url": {"required": False, "allow_null": True},
            "is_activate": {"required": False, "allow_null": True},
        }

    def update(self, instance, validated_data):        
        for key, value in validated_data.items():
            if getattr(instance, key) != value:
                setattr(instance, key, value)  
        instance.save()
        return instance