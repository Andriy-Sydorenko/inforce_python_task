import datetime

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify
from config import settings


class Restaurant(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True)

    def generate_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    post_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    menu_items = models.TextField()
    slug = models.SlugField(max_length=255, blank=True)

    def generate_slug(self) -> str:
        slug_base = f"{self.restaurant.name} {datetime.date.today()}"
        return slugify(slug_base)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Menu of the '{self.restaurant.name}' restaurant"


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="votes")
    vote_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=255, blank=True)

    class Meta:
        ordering = ["-vote_date"]

    def generate_slug(self):
        slug_base = f"user-{self.user.email.split('@')[0]}-vote-{datetime.datetime.now()}"
        return slugify(slug_base)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vote from {self.user.full_name} for {self.menu.restaurant.name} | DATE: {self.vote_date}"
