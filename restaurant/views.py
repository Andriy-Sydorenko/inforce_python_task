import datetime

from django.db.models import Count, Prefetch
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from restaurant.models import Restaurant, Menu, Vote
from restaurant.serializers import RestaurantSerializer, RestaurantDetailSerializer, MenuSerializer, MenuListSerializer, MenuDetailSerializer, VoteSerializer
from restaurant.permissions import IsAdminOrIfAuthenticatedReadOnly


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    # lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return RestaurantSerializer
        if self.action == "retrieve":
            return RestaurantDetailSerializer

        return RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    votes_prefetch = Prefetch("votes", queryset=Vote.objects.select_related("user"))
    queryset = (Menu.objects.select_related("restaurant", )
                .prefetch_related(votes_prefetch)
                .annotate(votes_count=Count("votes")))

    serializer_class = MenuSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    # lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return MenuListSerializer
        if self.action == "retrieve":
            return MenuDetailSerializer
        return MenuSerializer

    @action(detail=False, methods=["GET"], url_path="current-day-menus")
    def current_day_menus(self, request):
        today = datetime.date.today()
        menus = Menu.objects.select_related("restaurant").filter(post_date=today)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="most-voted-today-menu")
    def most_voted_today_menu(self, request):
        today = datetime.date.today()
        menu = (Menu.objects.select_related('restaurant')
                .filter(post_date=today)
                .annotate(votes_count=Count('votes'))
                .order_by('-votes_count').first())

        if menu:
            serializer = MenuSerializer(menu)
            return Response(serializer.data)
        return Response({'detail': 'No menus found for today.'})


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.select_related("user", "menu", "menu__restaurant")
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated, ]

    # lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Vote.objects.select_related("user", "menu", "menu__restaurant")

        return Vote.objects.select_related("user", "menu", "menu__restaurant").filter(user=user)

    def perform_create(self, serializer):
        menu = self.request.data.get('menu')
        user = self.request.user

        if Vote.objects.filter(user=user, vote_date=timezone.localdate()).exists():
            raise serializers.ValidationError('You have already voted for the menu today!')

        serializer.save(user=self.request.user)
