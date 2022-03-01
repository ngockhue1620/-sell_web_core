from rest_framework import serializers
from .models import Order, OrderDetail
from permisstion.token import Token

class OrderDetailSerializer(serializers.ModelSerializer):
    # product = serializers.CharField()
    class Meta:
        model = OrderDetail
        fields = ["product", "price", "id", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True, required = True)

    class Meta:
        model = Order
        fields = [
            "note",
            "user",
            "address",
            "phone",
            "total",
            "order_detail",
            "id",
        ]
        optional_fields = ["note"]
        extra_kwargs = {
            'user': {'write_only': True},
        }

    def create(self, validated_data):
        order_details = validated_data.pop("order_detail")
        print(validated_data)
       
        order = Order.objects.create(**validated_data)
        for product in order_details:
            print(product)
            OrderDetail.objects.create(
                product=product.get('product'),
                quantity=product.get("quantity"),
                price=product.get("price"),
                order=order,
            )

        return order
