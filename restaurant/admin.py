from django.contrib import admin

from restaurant.models import Menu, Restaurant, Vote


@admin.register(Restaurant)
class CarAdmin(admin.ModelAdmin):
    search_fields = ("name", )


@admin.register(Menu)
class CarAdmin(admin.ModelAdmin):
    search_fields = ("restaurant__name", )
    list_filter = ("restaurant", )


@admin.register(Vote)
class CarAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "menu__restaurant__name", "vote_date")
    list_filter = ("menu__restaurant__name", )
