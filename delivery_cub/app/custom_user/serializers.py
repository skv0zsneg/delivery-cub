from rest_framework import serializers

from app.custom_user.models import CartPosition, CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class CartPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartPosition
        fields = "__all__"
