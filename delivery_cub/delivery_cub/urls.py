from django.urls import include, path
from rest_framework import routers
from django.shortcuts import redirect

from app.cart import views as cart_views
from app.order import views as order_views
from app.restaurant import views as restaurant_views
from app.user import views as user_views


router = routers.DefaultRouter()
router.register(r"cart", cart_views.CartViewSet, basename="cart")
router.register(r"cart-position", cart_views.CartPositionViewSet, basename="cart-position")
router.register(r"order", order_views.OrderViewSet, basename="order")
router.register(r"ordered-dish", order_views.OrderedDishViewSet, basename="ordered-dish")
router.register(r"restaurant", restaurant_views.RestaurantViewSet, basename="restaurant")
router.register(r"dish", restaurant_views.DishViewSet, basename="dish")
router.register(r"user", user_views.UserViewSet, basename="user")


urlpatterns = [
    path("", lambda _: redirect("api/")),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
