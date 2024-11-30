from rest_framework import serializers

from app.restaurant.models import Dish, Restaurant


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"


class RestaurantDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = (
            "id",
            "title",
            "price",
        )


class RestaurantSerializer(serializers.ModelSerializer):
    dishes = RestaurantDishSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "dishes",
        )


class AddDishToCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

    def valid_quantity(self, value: int):
        if value < 1:
            raise serializers.ValidationError(
                "Количество товара не может быть меньше нуля"
            )
