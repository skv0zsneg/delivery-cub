from rest_framework import serializers

from app.restaurant.models import Dish, Restaurant


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantWithDishSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "dishes",
        )
