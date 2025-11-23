from rest_framework_nested import routers
from django.urls import path, include
from .views import ChefViewSet, MenusViewSet, BookingViewSet

router = routers.DefaultRouter()
router.register('chefs', ChefViewSet, basename='chef')
router.register('menus', MenusViewSet, basename='menu')
router.register('bookings', BookingViewSet, basename='booking')

# Nested router for menus under chefs
chefs_router = routers.NestedDefaultRouter(router, 'chefs', lookup='chef')
chefs_router.register('menus', MenusViewSet, basename='chef-menus')
chefs_router.register('bookings', BookingViewSet, basename='chef-bookings')

urlpatterns = router.urls + chefs_router.urls