from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.custom_user.models import CustomUser
from app.restaurant.models import Dish, Restaurant


class RestaurantTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.restaurant1 = Restaurant.objects.create(name="Restaurant 1")
        self.restaurant2 = Restaurant.objects.create(name="Restaurant 2")

        self.dish1 = Dish.objects.create(
            restaurant=self.restaurant1,
            title="Dish 1",
            description="Description 1",
            price=10.00,
        )
        self.dish2 = Dish.objects.create(
            restaurant=self.restaurant1,
            title="Dish 2",
            description="Description 2",
            price=20.00,
        )
        self.dish3 = Dish.objects.create(
            restaurant=self.restaurant2,
            title="Dish 3",
            description="Description 3",
            price=30.00,
        )

    def test_list_restaurants(self):
        url = reverse("restaurant-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_restaurant(self):
        url = reverse("restaurant-detail", args=[self.restaurant1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Restaurant 1")

    def test_create_restaurant(self):
        url = reverse("restaurant-list")
        data = {"name": "New Restaurant"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 3)
        self.assertEqual(Restaurant.objects.get(id=response.data["id"]).name, "New Restaurant")

    def test_update_restaurant(self):
        url = reverse("restaurant-detail", args=[self.restaurant1.id])
        data = {"name": "Updated Restaurant"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.restaurant1.refresh_from_db()
        self.assertEqual(self.restaurant1.name, "Updated Restaurant")

    def test_delete_restaurant(self):
        url = reverse("restaurant-detail", args=[self.restaurant1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Restaurant.objects.count(), 1)


class DishTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.restaurant = Restaurant.objects.create(name="Restaurant")
        self.dish1 = Dish.objects.create(
            restaurant=self.restaurant,
            title="Dish 1",
            description="Description 1",
            price=10.00,
        )
        self.dish2 = Dish.objects.create(
            restaurant=self.restaurant,
            title="Dish 2",
            description="Description 2",
            price=20.00,
        )

    def test_list_dishes(self):
        url = reverse("dish-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_dish(self):
        url = reverse("dish-detail", args=[self.dish1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Dish 1")

    def test_create_dish(self):
        url = reverse("dish-list")
        data = {
            "restaurant": self.restaurant.id,
            "title": "New Dish",
            "description": "Description",
            "price": "30.00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dish.objects.count(), 3)
        self.assertEqual(Dish.objects.get(id=response.data["id"]).title, "New Dish")

    def test_update_dish(self):
        url = reverse("dish-detail", args=[self.dish1.id])
        data = {
            "restaurant": self.restaurant.id,
            "title": "Updated Dish",
            "description": "Updated Description",
            "price": "40.00",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dish1.refresh_from_db()
        self.assertEqual(self.dish1.title, "Updated Dish")

    def test_delete_dish(self):
        url = reverse("dish-detail", args=[self.dish1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dish.objects.count(), 1)

    def test_create_dish_with_negative_price(self):
        url = reverse("dish-list")
        data = {
            "restaurant": self.restaurant.id,
            "title": "New Dish",
            "description": "Description",
            "price": "-30.00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_dish_with_zero_price(self):
        url = reverse("dish-list")
        data = {
            "restaurant": self.restaurant.id,
            "title": "New Dish",
            "description": "Description",
            "price": "0.0",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dish.objects.count(), 3)
        self.assertEqual(Dish.objects.get(id=response.data["id"]).title, "New Dish")
        self.assertEqual(Dish.objects.get(id=response.data["id"]).price, Decimal(0.0))


class MenuTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.restaurant1 = Restaurant.objects.create(name="Restaurant 1")
        self.restaurant2 = Restaurant.objects.create(name="Restaurant 2")

        self.dish1 = Dish.objects.create(
            restaurant=self.restaurant1,
            title="Dish 1",
            description="Description 1",
            price=10.00,
        )
        self.dish2 = Dish.objects.create(
            restaurant=self.restaurant1,
            title="Dish 2",
            description="Description 2",
            price=20.00,
        )
        self.dish3 = Dish.objects.create(
            restaurant=self.restaurant2,
            title="Dish 3",
            description="Description 3",
            price=30.00,
        )

    def test_filter_by_restaurant(self):
        url = reverse("menu")
        response = self.client.get(url, {"restaurant": self.restaurant1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Restaurant 1")

    def test_filter_by_dish_title(self):
        url = reverse("menu")
        response = self.client.get(url, {"dish_title": "Dish 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Restaurant 1")

    def test_filter_by_restaurant_and_dish_title(self):
        url = reverse("menu")
        response = self.client.get(
            url, {"restaurant": self.restaurant1.id, "dish_title": "Dish 2"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Restaurant 1")

    def test_no_filter(self):
        url = reverse("menu")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
