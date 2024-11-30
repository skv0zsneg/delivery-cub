from django.shortcuts import redirect
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from app.custom_user import views as cart_views
from app.custom_user import views as user_views
from app.order import views as order_views
from app.rate import views as rate_views
from app.restaurant import views as restaurant_views

router = routers.DefaultRouter()
router.register(r"cart-position", cart_views.CartPositionViewSet, basename="cart-position")
router.register(r"dish", restaurant_views.DishViewSet, basename="dish")
router.register(r"order", order_views.OrderViewSet, basename="order")
router.register(r"ordered-dish", order_views.OrderedDishViewSet, basename="ordered-dish")
router.register(r"rate", rate_views.RateViewSet, basename="rate")
router.register(r"restaurant", restaurant_views.RestaurantViewSet, basename="restaurant")
router.register(r"user", user_views.UserViewSet, basename="user")

api_views = [
    path(r"api/menu", restaurant_views.MenuAPIView.as_view(), name="menu"),
]

urlpatterns = [
    path("", lambda _: redirect("api/docs/")),
    path("api/", lambda _: redirect("docs/")),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]

urlpatterns += api_views
