from rest_framework import permissions, viewsets

from app.rate.models import Rate
from app.rate.serializers import RateSerializer


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all().order_by("restaurant")
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticated]
