import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.custom_user.models import CartPosition, CustomUser
from app.order.models import Order, OrderedDish
from app.restaurant.models import RestaurantDish, Restaurant


class UserTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.dish = RestaurantDish.objects.create(
            restaurant=self.restaurant,
            title="Test Dish",
            description="Test Description",
            price=10.00,
        )

    def test_list_users(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_user(self):
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_create_user(self):
        url = reverse("user-list")
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "balance": 0.0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(id=response.data["id"]).username, "newuser")

    def test_create_user_with_negative_balance(self):
        url = reverse("user-list")
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "balance": -100.0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        url = reverse("user-detail", args=[self.user.id])
        data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "balance": 100.0,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")

    def test_delete_user(self):
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 0)


class CartPositionTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.dish = RestaurantDish.objects.create(
            restaurant=self.restaurant,
            title="Test Dish",
            description="Test Description",
            price=10.00,
        )

    def test_add_dish_to_cart(self):
        url = reverse("user-add-dish-to-cart", args=[self.user.id])
        data = {"dish_id": self.dish.id, "quantity": 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartPosition.objects.count(), 1)
        self.assertEqual(CartPosition.objects.get(user=self.user).quantity, 2)

    def test_remove_dish_from_cart(self):
        cart_position = CartPosition.objects.create(user=self.user, dish=self.dish, quantity=2)
        url = reverse("user-remove-dish-from-cart", args=[self.user.id])
        data = {"dish_id": self.dish.id, "quantity": 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_position.refresh_from_db()
        self.assertEqual(cart_position.quantity, 1)

    def test_remove_dish_from_cart_not_found(self):
        url = reverse("user-remove-dish-from-cart", args=[self.user.id])
        data = {"dish_id": uuid.uuid4(), "quantity": 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_cart(self):
        CartPosition.objects.create(user=self.user, dish=self.dish, quantity=2)
        url = reverse("user-list-cart", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["positions"]), 1)
        self.assertEqual(response.data["total_price"], 20.00)

    def test_pay_cart(self):
        self.user.balance = 100.00
        self.user.save()
        CartPosition.objects.create(user=self.user, dish=self.dish, quantity=2)

        url = reverse("user-pay-cart", args=[self.user.id])
        self.assertEqual(Order.objects.count(), 0)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 80.00)
        self.assertEqual(CartPosition.objects.count(), 0)
        self.assertEqual(Order.objects.count(), 1)

        ordered_dish = OrderedDish.objects.first()
        self.assertEqual(ordered_dish.dish_price, self.dish.price)
        self.assertEqual(ordered_dish.dish_title, self.dish.title)
        self.assertEqual(ordered_dish.restaurant_name, self.dish.restaurant.name)

    def test_pay_cart_insufficient_funds(self):
        self.user.balance = 10.00
        self.user.save()
        CartPosition.objects.create(user=self.user, dish=self.dish, quantity=2)
        url = reverse("user-pay-cart", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Not enough funds on the balance")

    def test_top_up_balance(self):
        url = reverse("user-top-up-balance", args=[self.user.id])
        data = {"amount": 50.00}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 50.00)

    def test_orders(self):
        CartPosition.objects.create(user=self.user, dish=self.dish, quantity=2)
        self.user.balance = 100.00
        self.user.save()
        url = reverse("user-pay-cart", args=[self.user.id])
        response = self.client.get(url)

        url = reverse("user-orders", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_count"], 1)
        self.assertEqual(response.data["total_sum"], 20.00)
