from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.custom_user.models import CartPosition, CustomUser
from app.custom_user.serializers import (
    AddDishToCartSerializer,
    CartPositionSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=AddDishToCartSerializer,
        responses={status.HTTP_201_CREATED: CartPositionSerializer},
    )
    @action(detail=True, methods=["POST"])
    def add_dish_to_cart(self, request, **kwargs):
        serializer = AddDishToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: CustomUser = self.get_object()

        try:
            cart_position = CartPosition.objects.get(
                user=user,
                dish_id=serializer.validated_data["dish_id"],
            )
            cart_position.quantity += serializer.validated_data["quantity"]
            cart_position.save()
        except CartPosition.DoesNotExist:
            cart_position = CartPosition.objects.create(
                user=user,
                dish_id=serializer.validated_data["dish_id"],
                quantity=serializer.validated_data["quantity"],
            )

        return Response(
            CartPositionSerializer(cart_position).data,
            status=status.HTTP_201_CREATED,
        )


class CartPositionViewSet(viewsets.ModelViewSet):
    queryset = CartPosition.objects.all()
    serializer_class = CartPositionSerializer
    permission_classes = [permissions.IsAuthenticated]
