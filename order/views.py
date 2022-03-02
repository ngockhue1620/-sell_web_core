from lib2to3.pgen2 import token
from msilib.schema import ReserveCost
from rest_framework import viewsets, status
from rest_framework.response import Response

from order.models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from permisstion.authentication import Authentication, Token
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [Authentication]

    def list(self, request):
        orders = Order.objects.filter(user_id = request.user.get('id'))
        serializer = OrderSerializer(orders, many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        data = request.data
        order_detail = data.get("order_detail", None)
        if not order_detail:
            return Response({"message":"Order Detail is null"},status=status.HTTP_400_BAD_REQUEST)
        list_id = []
        index =0
        for product in order_detail:
            id = product.get("id", None)
            product.get("quantity")
            if id:
                list_id.append(id)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            order_detail[index]['product'] = id
            index +=1
        set_id = set(list_id)
        if len(list_id) != len(set_id):
            return Response(
                {"message": "Duplicate item"}, status=status.HTTP_400_BAD_REQUEST
            )
     
        # self.initial_data.update({"user": user})
        data.update({
            "user": request.user.get('id')
        })
        serializer = OrderSerializer(data=data)
        print(serializer.is_valid())
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"order": serializer.data, "message": "Order success"}, status=status.HTTP_201_CREATED)
