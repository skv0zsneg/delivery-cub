from rest_framework import serializers

from app.order.models import Order, OrderedDish


class OrderedDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedDish
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderWithDishesSerializer(serializers.ModelSerializer):
    ordered_dishes = OrderedDishSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "create_datetime",
            "total_price",
            "ordered_dishes",
        )
