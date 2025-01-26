import uuid

from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, status, views, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from app.restaurant.models import RestaurantDish, Restaurant
from app.restaurant.serializers import (
    DishSerializer,
    RestaurantSerializer,
    RestaurantWithDishSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all().order_by("name")
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


class DishViewSet(viewsets.ModelViewSet):
    queryset = RestaurantDish.objects.all().order_by("restaurant")
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticated]


class MenuAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="restaurant",
                description="Filter by restaurant",
                required=False,
                type=uuid.UUID,
                many=True,
            ),
            OpenApiParameter(
                name="dish_title",
                description="Filter by dish title",
                required=False,
                type=str,
                many=True,
            ),
        ],
        responses={status.HTTP_200_OK: RestaurantWithDishSerializer},
    )
    def get(self, request: Request, **kwargs):
        restaurant_ids = request.query_params.getlist("restaurant")
        dish_titles = request.query_params.getlist("dish_title")

        query = Q()
        if restaurant_ids:
            query &= Q(pk__in=restaurant_ids)
        if dish_titles:
            dish_title_query = Q()
            for title in dish_titles:
                dish_title_query |= Q(dishes__title__icontains=title)
            query &= dish_title_query

        filtered_restaurants = (
            Restaurant.objects.prefetch_related("dishes").filter(query).distinct()
        )

        return Response(
            RestaurantWithDishSerializer(filtered_restaurants, many=True).data,
            status.HTTP_200_OK,
        )
