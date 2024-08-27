from rest_framework import serializers

from app.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "last_login",
            "date_joined",
        )
