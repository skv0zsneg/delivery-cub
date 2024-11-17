from rest_framework import permissions, viewsets

from app.custom_user.models import CartPosition, CustomUser
from app.custom_user.serializers import CartPositionSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CartPositionViewSet(viewsets.ModelViewSet):
    queryset = CartPosition.objects.all()
    serializer_class = CartPositionSerializer
    permission_classes = [permissions.IsAuthenticated]
