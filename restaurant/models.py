from django.db import models

from config import settings


class Restaurant(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    post_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    # TODO: additionally implement Items model for creating dishes to include in menu_items
    menu_items = models.TextField()

    @property
    def votes_count(self):
        return self.votes.count()

    # TODO: add ordering for menus by votes_count in serializers

    def __str__(self):
        return f"Menu of the '{self.restaurant.name}' restaurant"


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="votes")
    vote_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-vote_date"]

    def __str__(self):
        return f"Vote from {self.user.full_name} for {self.menu.restaurant.name}| DATE: {self.vote_date}"
