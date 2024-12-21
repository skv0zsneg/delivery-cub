from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.common.constants import RateMarkEnum
from app.custom_user.models import CustomUser
from app.rate.models import Rate
from app.restaurant.models import Restaurant


class RateTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.rate = Rate.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            rate=RateMarkEnum.EXCELLENT.grade,
            comment="Excellent service!",
        )

    def test_list_rates(self):
        url = reverse("rate-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_rate(self):
        url = reverse("rate-detail", args=[self.rate.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["comment"], "Excellent service!")

    def test_create_rate(self):
        url = reverse("rate-list")
        data = {
            "user": self.user.id,
            "restaurant": self.restaurant.id,
            "rate": RateMarkEnum.GOOD.grade,
            "comment": "Good service!",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rate.objects.count(), 2)
        self.assertEqual(Rate.objects.get(id=response.data["id"]).comment, "Good service!")

    def test_update_rate(self):
        url = reverse("rate-detail", args=[self.rate.id])
        data = {
            "user": self.user.id,
            "restaurant": self.restaurant.id,
            "rate": RateMarkEnum.NORMAL.grade,
            "comment": "Normal service!",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.rate.refresh_from_db()
        self.assertEqual(self.rate.comment, "Normal service!")

    def test_delete_rate(self):
        url = reverse("rate-detail", args=[self.rate.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Rate.objects.count(), 0)
