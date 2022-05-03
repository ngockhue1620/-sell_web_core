from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Prefetch
from order.models import Order, OrderDetail
from product.models import Product
from .serializers import OrderSerializer, GetOrderSerializer, GetOrderDetailSerializer
from .const.status import OrderStatus
from permisstion.authentication import Authentication, Token
from .service.order_service import OrderService
from rest_framework.decorators import action

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [Authentication]

    def list(self, request):
        fl = {}
        status_order = request.GET.get('status', OrderStatus.IN_PROGRESS)
        is_admin = request.user.get("admin", False)
        fl.update({'status': status_order})
        if request.user and not is_admin:
            fl.update({'status': status_order, 'user_id': request.user.get('id')})
        orders = Order.objects.filter(**fl)
        if is_admin:
            serializer = OrderSerializer(orders, many =True)
        else:
            serializer = GetOrderSerializer(orders, many =True)
        if is_admin and int(status_order) == OrderStatus.IN_PROGRESS:            
            orders = OrderService.handle_order_status(serializer.data)
            return Response(orders, status=status.HTTP_200_OK)
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

    def update(self, request, pk=None):
        if not request.user.get("admin", False):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            order = Order.objects.get(id=pk)
            order.status = OrderStatus.DONE
            order_details = OrderDetail.objects.filter(order_id = order.id)
            product_ids = []
            order_detail_temp = {}
            for detail in order_details:

                product_ids.append(detail.product.id)
                order_detail_temp[f"{detail.product.id}"] = detail
            products =  Product.objects.filter(id__in = product_ids)
            update_list = []
            for product in products:
                if int(product.quantity) > int(order_detail_temp[f"{product.id}"].quantity):
                    product.quantity  =  int(product.quantity) - int(order_detail_temp[f"{product.id}"].quantity)
                else:
                    return Response({"message": "Khong du hang"}, status=status.HTTP_400_BAD_REQUEST)
                update_list.append(product)
            Product.objects.bulk_update(update_list,["quantity"])
            order.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods = ["get"], detail=False, url_path="list_check", permission_classes=[])
    def list_check(self, request):
        
        orders = Order.objects.all()
       
        serializer = GetOrderSerializer(orders, many =True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class OrderDetailViewSet(viewsets.ViewSet):
    # permission_classes = [Authentication]   


    def retrieve(self, request, pk=None):      
        data = OrderDetail.objects.filter(order_id = pk)
        if data:
            serizlizer = GetOrderDetailSerializer(data, many=True)
            return Response(serizlizer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Order is not exists'}, status=status.HTTP_404_NOT_FOUND)
        