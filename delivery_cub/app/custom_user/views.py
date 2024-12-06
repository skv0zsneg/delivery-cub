from decimal import Decimal

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.custom_user.models import CartPosition, CustomUser
from app.custom_user.serializers import (
    CartPositionSerializer,
    CartSerializer,
    DishIdAndQuantitySerializer,
    DishInCartSerializer,
    TopUpBalanceSerializer,
    UserSerializer,
)
from app.order.models import Order, OrderedDish
from app.order.serializers import OrderSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=DishIdAndQuantitySerializer,
        responses={status.HTTP_201_CREATED: CartPositionSerializer},
    )
    @action(detail=True, methods=["POST"], url_path="add-dish-to-cart")
    def add_dish_to_cart(self, request, **kwargs):
        serializer = DishIdAndQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()

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

    @extend_schema(
        request=DishIdAndQuantitySerializer,
        responses={
            status.HTTP_200_OK: CartPositionSerializer,
            status.HTTP_404_NOT_FOUND: str,
        },
    )
    @action(detail=True, methods=["POST"], url_path="remove-dish-from-cart")
    def remove_dish_from_cart(self, request, **kwargs):
        serializer = DishIdAndQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        dish_id = serializer.validated_data["dish_id"]

        try:
            cart_position = CartPosition.objects.get(
                user=self.get_object(),
                dish_id=serializer.validated_data["dish_id"],
            )
        except CartPosition.DoesNotExist:
            return Response(
                f"Position for dish with pk '{dish_id}' for user "
                f"with pk '{user.pk}' does not exist",
                status=status.HTTP_404_NOT_FOUND,
            )

        cart_position.quantity -= serializer.validated_data["quantity"]
        if cart_position.quantity <= 0:
            cart_position.delete()[0]
            response_result = {}
        else:
            cart_position.save()
            response_result = CartPositionSerializer(cart_position).data

        return Response(
            response_result,
            status=status.HTTP_200_OK,
        )

    @extend_schema(responses={status.HTTP_200_OK: CartSerializer})
    @action(detail=True, methods=["GET"], url_path="list-cart")
    def list_cart(self, request, **kwargs):
        user = self.get_object()
        cart_positions = CartPosition.objects.select_related("dish").filter(user=user)

        dish_in_carts = []
        total_price = 0
        for cart_position in cart_positions:
            total_price_for_dish = cart_position.quantity * cart_position.dish.price
            total_price += total_price_for_dish
            dish_in_cart_serializer = DishInCartSerializer(
                data={
                    "cart_position_id": cart_position.pk,
                    "dish_title": cart_position.dish.title,
                    "quantity": cart_position.quantity,
                    "price": total_price_for_dish,
                }
            )
            dish_in_cart_serializer.is_valid(raise_exception=True)
            dish_in_carts.append(dish_in_cart_serializer.data)

        cart_serializer = CartSerializer(
            data={
                "total_price": total_price,
                "positions": dish_in_carts,
            },
        )
        cart_serializer.is_valid(raise_exception=True)

        return Response(
            cart_serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(responses={status.HTTP_200_OK: OrderSerializer})
    @action(detail=True, methods=["GET"], url_path="pay-cart")
    def pay_cart(self, request, **kwargs):
        user = self.get_object()
        cart_positions = CartPosition.objects.select_related("dish").filter(user=user)

        ordered_dishes = []
        total_price = Decimal(0)
        order = Order(user=user, total_price=0)
        for cart_position in cart_positions:
            total_price_for_dish = cart_position.quantity * cart_position.dish.price
            total_price += total_price_for_dish
            ordered_dishes.append(
                OrderedDish(
                    order=order,
                    restaurant_name=cart_position.dish.restaurant.name,
                    dish_title=cart_position.dish.title,
                    dish_price=cart_position.dish.price,
                    dish_quantity=cart_position.quantity,
                )
            )

        if total_price > user.balance:
            # TODO: добавить статус `success: false` для фронта
            return Response(
                "Not enough funds on the balance",
                status=status.HTTP_200_OK,
            )

        user.balance = user.balance - total_price
        order.total_price = total_price

        user.save()
        order.save()
        OrderedDish.objects.bulk_create(ordered_dishes)
        cart_positions.delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=TopUpBalanceSerializer,
        responses={
            status.HTTP_200_OK: UserSerializer,
        },
    )
    @action(detail=True, methods=["POST"], url_path="top-up-balance")
    def top_up_balance(self, request, **kwargs):
        serializer = TopUpBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.balance += Decimal(serializer.validated_data["amount"])
        user.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK,
        )


class CartPositionViewSet(viewsets.ModelViewSet):
    queryset = CartPosition.objects.all()
    serializer_class = CartPositionSerializer
    permission_classes = [permissions.IsAuthenticated]
