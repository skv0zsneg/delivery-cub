from rest_framework import permissions, viewsets

from app.order.models import OrderedDish, Order
from app.order.serializers import OrderSerializer, OrderedDishSerializer


class OrderedDishViewSet(viewsets.ModelViewSet):
    queryset = OrderedDish.objects.all()
    serializer_class = OrderedDishSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
