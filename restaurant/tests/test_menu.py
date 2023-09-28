import uuid

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from restaurant.models import Menu, Restaurant
from restaurant.serializers import MenuListSerializer

MENU_URL = reverse("restaurant:menu-list")


def sample_restaurant(**params):
    defaults = {
        "name": f"Sample Restaurant {uuid.uuid4()}",
        "description": "Sample description",
    }
    defaults.update(params)

    return Restaurant.objects.create(**defaults)


def sample_menu(**params):
    restaurant = sample_restaurant()

    defaults = {
        "restaurant": restaurant,
        "menu_items": "item1, item2, item3",
    }
    defaults.update(params)

    return Menu.objects.create(**defaults)


class UnauthenticatedMenuApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(MENU_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedMenuApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_menus_list_access(self):
        sample_menu()
        sample_menu()

        response = self.client.get(MENU_URL)

        menus = Menu.objects.all().annotate(votes_count=Count("votes"))
        serializer = MenuListSerializer(menus, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_menu_forbidden(self):
        payload = {
            "restaurant": "",
            "menu_items": "item1, item2, item3",
        }
        response = self.client.post(MENU_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminMenuApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_menu_list_admin_access(self):
        sample_menu()
        restaurant2 = sample_restaurant(name="Second restaurant")
        sample_menu(restaurant=restaurant2)

        response = self.client.get(MENU_URL)

        menus = Menu.objects.all().annotate(votes_count=Count("votes"))
        serializer = MenuListSerializer(menus, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
