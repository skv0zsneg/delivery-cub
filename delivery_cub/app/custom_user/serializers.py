from uuid import UUID

from rest_framework import serializers

from app.custom_user.models import CartPosition, CustomUser
from app.restaurant.models import Dish


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class CartPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartPosition
        fields = "__all__"


class AddDishToCartSerializer(serializers.Serializer):
    dish_id = serializers.UUIDField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)

    def validate_quantity(self, value: int):
        if value <= 0:
            raise serializers.ValidationError("Quantity cannot be lower or equal to 0")
        return value

    def validate_dish_id(self, value: UUID):
        try:
            Dish.objects.get(pk=value)
        except Dish.DoesNotExist:
            raise serializers.ValidationError(f"Dish with PK {value} dose not exist")
        return value
