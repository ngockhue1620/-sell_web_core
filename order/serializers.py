from rest_framework import serializers
from .models import Order, OrderDetail


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

    def create(self, validated_data):
        print(validated_data)
        order_details = validated_data.pop("order_detail")
        print(order_details)
        order = Order.objects.create(**validated_data, user_id=1)
        for product in order_details:
            print(product)
            OrderDetail.objects.create(
                product=product.get('product'),
                quantity=product.get("quantity"),
                price=product.get("price"),
                order=order,
            )

        return order
