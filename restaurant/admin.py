from django.contrib import admin
from restaurant.models import Restaurant, Menu, Vote


admin.site.register(Menu)
admin.site.register(Vote)

@admin.register(Restaurant)
class CarAdmin(admin.ModelAdmin):
    search_fields = ("name", )


# @admin.register(Menu)
# class CarAdmin(admin.ModelAdmin):
#     search_fields = ("name")
#     list_filter = ("manufacturer", "drivers")
#
#
# @admin.register(Vote)
# class CarAdmin(admin.ModelAdmin):
#     search_fields = ("name")
#     list_filter = ("manufacturer", "drivers")
