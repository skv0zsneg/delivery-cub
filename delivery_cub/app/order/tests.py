from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.custom_user.models import CustomUser
from app.order.models import Order, OrderedDish


class OrderedDishTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.order = Order.objects.create(user=self.user, total_price=100.00)
        self.ordered_dish = OrderedDish.objects.create(
            order=self.order,
            restaurant_name="Test Restaurant",
            dish_title="Test Dish",
            dish_price=50.00,
            dish_quantity=2,
        )

    def test_list_ordered_dishes(self):
        url = reverse("ordered-dish-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_ordered_dish(self):
        url = reverse("ordered-dish-detail", args=[self.ordered_dish.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["dish_title"], "Test Dish")

    def test_create_ordered_dish(self):
        url = reverse("ordered-dish-list")
        data = {
            "order": self.order.id,
            "restaurant_name": "New Restaurant",
            "dish_title": "New Dish",
            "dish_price": 30.00,
            "dish_quantity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderedDish.objects.count(), 2)
        self.assertEqual(OrderedDish.objects.get(id=response.data["id"]).dish_title, "New Dish")

    def test_update_ordered_dish(self):
        url = reverse("ordered-dish-detail", args=[self.ordered_dish.id])
        data = {
            "order": self.order.id,
            "restaurant_name": "Updated Restaurant",
            "dish_title": "Updated Dish",
            "dish_price": 40.00,
            "dish_quantity": 3,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ordered_dish.refresh_from_db()
        self.assertEqual(self.ordered_dish.dish_title, "Updated Dish")

    def test_delete_ordered_dish(self):
        url = reverse("ordered-dish-detail", args=[self.ordered_dish.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderedDish.objects.count(), 0)


class OrderTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.order = Order.objects.create(user=self.user, total_price=100.00)

    def test_list_orders(self):
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_order(self):
        url = reverse("order-detail", args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_price"], "100.00")

    def test_create_order(self):
        url = reverse("order-list")
        data = {"user": self.user.id, "total_price": 200.00}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=response.data["id"]).total_price, 200.00)

    def test_update_order(self):
        url = reverse("order-detail", args=[self.order.id])
        data = {"user": self.user.id, "total_price": 150.00}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_price, 150.00)

    def test_delete_order(self):
        url = reverse("order-detail", args=[self.order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
