from rest_framework import permissions, viewsets

from app.cart.models import Cart, CartPosition
from app.cart.serializers import CartSerializer, CartPositionSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]


class CartPositionViewSet(viewsets.ModelViewSet):
    queryset = CartPosition.objects.all()
    serializer_class = CartPositionSerializer
    permission_classes = [permissions.IsAuthenticated]
