from rest_framework import routers

from restaurant.views import MenuViewSet, RestaurantViewSet, VoteViewSet

router = routers.DefaultRouter()
router.register("restaurants", RestaurantViewSet)
router.register("menus", MenuViewSet)
router.register("votes", VoteViewSet)

urlpatterns = router.urls

app_name = "restaurant"
