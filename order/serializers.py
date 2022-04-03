from rest_framework import serializers
from .models import Order, OrderDetail
from product.serializers import ProductSerializer 

class GetOrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderDetail
        fields = ["product", "price", "id", "quantity"]

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ["product", "price", "id", "quantity"]

class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True, required = True)

    class Meta:
        model = Order
        fields = [
            "created_at",
            "note",
            "user",
            "address",
            "phone",
            "total",
            "status",
            "order_detail",
            "id",
        ]
        optional_fields = ["note", "created_at"]
        extra_kwargs = {
            'user': {'write_only': True},
            'created_at': {'read_only': True}
        }

    def create(self, validated_data):
        order_details = validated_data.pop("order_detail")       
        order = Order.objects.create(**validated_data,status = 1)
        for product in order_details:
            OrderDetail.objects.create(
                product=product.get('product'),
                quantity=product.get("quantity"),
                price=product.get("price"),
                order=order,            
            )
        return order

class GetOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "created_at",
            "note",
            "user",
            "address",
            "phone",
            "total",
            "status",
            "id",
        ]
        optional_fields = ["note", "created_at"]
        extra_kwargs = {
            'user': {'write_only': True},
            'created_at': {'read_only': True}
        }



