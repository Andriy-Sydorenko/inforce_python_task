import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from restaurant.models import Menu, Restaurant, Vote
from restaurant.serializers import VoteSerializer

VOTE_URL = reverse("restaurant:vote-list")


def sample_restaurant(**params):
    defaults = {
        "name": f"Sample Restaurant {uuid.uuid4()}",
    }
    defaults.update(params)
    return Restaurant.objects.create(**defaults)


def sample_menu(restaurant=None):
    if not restaurant:
        restaurant = sample_restaurant()
    return Menu.objects.create(restaurant=restaurant, menu_items="item1, item2")


def sample_vote(user, menu):
    return Vote.objects.create(user=user, menu=menu)


class UnauthenticatedVoteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(VOTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedVoteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_vote_list_access(self):
        menu = sample_menu()
        sample_vote(user=self.user, menu=menu)

        response = self.client.get(VOTE_URL)

        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_vote_permitted(self):
        menu = sample_menu()
        payload = {
            "user": self.user.id,
            "menu": menu.id,
        }
        response = self.client.post(VOTE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminVoteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_vote_list_admin_access(self):
        menu = sample_menu()
        sample_vote(user=self.user, menu=menu)

        response = self.client.get(VOTE_URL)

        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
