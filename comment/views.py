from rest_framework import viewsets, status
from rest_framework.response import Response

from order.models import Order
from .serializers import CommentSerializer
from permisstion.authentication import Authentication
from .models import Comment
from order.const.status import OrderStatus
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [Authentication] 
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
   
    def create(self, request):
        data = request.data
        comment = data.get("comment", None)
        product = data.get("product", None)
        if not comment and not product:
            return Response({"message":"Comment is null"},status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(user_id=request.user.get('id'), order_detail__product_id=product, status=OrderStatus.DONE).exists()
        if order:
          data.update({'user' : request.user.get('id')})
          serializer = CommentSerializer(data=data)
          if serializer.is_valid(raise_exception=True):
              serializer.save()
              return Response({"comment": serializer.data, "message": "Comment success"}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Ban chung tung mua san pham nay'}, status=status.HTTP_400_BAD_REQUEST)

