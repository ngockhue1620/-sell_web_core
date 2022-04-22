from rest_framework import serializers
from .models import Comment
from customer.serializer import UserSerializers

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'
    optinal = ['image', 'image_url']


class GetCommentSerializer(serializers.ModelSerializer):
  user = UserSerializers()
  class Meta:
    model = Comment
    fields = ['comment', 'user', 'product', 'created_at', 'image', 'image_url']