from rest_framework import serializers

from app.order.models import OrderedDish, Order


class OrderedDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedDish
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
