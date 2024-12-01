from decimal import Decimal
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


class DishIdAndQuantitySerializer(serializers.Serializer):
    dish_id = serializers.UUIDField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)

    def validate_dish_id(self, value: UUID):
        try:
            Dish.objects.get(pk=value)
        except Dish.DoesNotExist:
            raise serializers.ValidationError(f"Dish with pk {value} dose not exist.")
        return value

    def validate_quantity(self, value: int):
        if value <= 0:
            raise serializers.ValidationError("Quantity cannot be lower or equal to 0")
        return value


class DishInCartSerializer(serializers.Serializer):
    cart_position_id = serializers.UUIDField()
    dish_title = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()

    def validate_cart_position_id(self, value: UUID):
        try:
            CartPosition.objects.get(pk=value)
        except CartPosition.DoesNotExist:
            raise serializers.ValidationError(f"CartPosition with pk {value} dose not exist.")
        return value

    def validate_quantity(self, value: int):
        if value <= 0:
            raise serializers.ValidationError("Quantity cannot be lower or equal to 0")
        return value

    def validate_price(self, value: Decimal):
        if value <= 0:
            raise serializers.ValidationError("Price cannot be lower or equal to 0")
        return value


class CartSerializer(serializers.Serializer):
    total_price = serializers.FloatField()
    positions = DishInCartSerializer(many=True)

    def validate_total_price(self, value: Decimal):
        if value < 0:
            raise serializers.ValidationError("Total price cannot be lower or equal to 0")
        return value
