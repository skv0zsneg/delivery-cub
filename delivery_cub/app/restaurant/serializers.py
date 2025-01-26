from rest_framework import serializers

from app.restaurant.models import RestaurantDish, Restaurant


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDish
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
