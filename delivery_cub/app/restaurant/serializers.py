from rest_framework import serializers

from app.restaurant.models import Dish, Restaurant


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class RestaurantDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = (
            "id",
            "name",
            "price",
        )


class RestaurantSerializer(serializers.ModelSerializer):
    dishes = RestaurantDishSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "dishes"
        )
