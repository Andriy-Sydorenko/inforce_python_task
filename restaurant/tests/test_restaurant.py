from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from restaurant.models import Restaurant
from restaurant.serializers import RestaurantSerializer

RESTAURANT_URL = reverse("restaurant:restaurant-list")


def sample_restaurant(**params):
    defaults = {"name": "Test Restaurant Name"}
    defaults.update(params)

    return Restaurant.objects.create(**defaults)


class UnauthenticatedRestaurantApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(RESTAURANT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRestaurantApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_restaurants_list_access(self):
        sample_restaurant()
        sample_restaurant(name="Sample restaurant")

        response = self.client.get(RESTAURANT_URL)

        restaurant = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurant, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_restaurant_forbidden(self):
        payload = {"name": "Test name"}
        response = self.client.post(RESTAURANT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminRestaurantApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_restaurant_list_admin_access(self):
        sample_restaurant()
        sample_restaurant(name="Sample restaurant")

        response = self.client.get(RESTAURANT_URL)

        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_restaurant_permitted(self):
        payload = {"name": "Test name"}
        response = self.client.post(RESTAURANT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
