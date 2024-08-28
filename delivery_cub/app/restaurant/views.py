from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from app.restaurant.models import Dish, Restaurant
from app.restaurant.serializers import DishSerializer, RestaurantSerializer

# Filters

class RestaurantFilter(filters.FilterSet):
    id = filters.NumberFilter(
        label="ID ресторана",
        lookup_expr="exact",
    )
    dish_name = filters.CharFilter(
        label="Название блюда",
        field_name="dishes__name",
        lookup_expr="icontains",
    )

    class Meta:
        model = Restaurant
        fields = []


# ViewSets

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RestaurantFilter
    permission_classes = [permissions.IsAuthenticated]


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticated]
