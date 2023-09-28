import datetime

from rest_framework import serializers

from restaurant.models import Menu, Restaurant, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name")


class RestaurantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "description")


class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.CharField(source="restaurant.name")
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Menu
        fields = (
            "id",
            "restaurant",
            "post_date",
            "update_date",
            "menu_items",
            "votes_count",
        )


class VoteForMenuSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email")

    class Meta:
        model = Vote
        fields = ("id", "user_email", "vote_date")


class MenuListSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Menu
        fields = (
            "id",
            "restaurant",
            "post_date",
            "update_date",
            "menu_items",
            "votes_count",
        )


class MenuDetailSerializer(serializers.ModelSerializer):
    restaurant = serializers.CharField(source="restaurant.name")
    votes = VoteForMenuSerializer(many=True, read_only=True)
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Menu
        fields = (
            "id",
            "restaurant",
            "post_date",
            "update_date",
            "menu_items",
            "votes_count",
            "votes",
        )


class VoteSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    restaurant_name = serializers.CharField(
        source="menu.restaurant.name", read_only=True
    )
    menu_post_date = serializers.DateField(
        source="menu.post_date", read_only=True
    )
    menu_items = serializers.CharField(
        source="menu.menu_items", read_only=True
    )
    menu = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.filter(post_date=datetime.date.today())
    )

    class Meta:
        model = Vote
        fields = (
            "id",
            "user_email",
            "restaurant_name",
            "menu_post_date",
            "menu_items",
            "vote_date",
            "menu",
        )
