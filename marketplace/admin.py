from django.contrib import admin
from .models import Chef, Menus, Booking

# Register your models here.
@admin.register(Menus)
class MenusAdmin(admin.ModelAdmin):
    list_display = ('id', 'dish_name', 'price', 'chef')
    search_fields = ('dish_name', 'chef__user__username')
    list_filter = ('price',)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'chef', 'event_date', 'status', 'total_price')
    search_fields = ('client__user__username', 'chef__user__username', 'location')
    list_filter = ('status', 'event_date')


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio', 'specialties', 'experience_years', 'rate_per_event', 'location', 'availability')
    search_fields = ('user__username', 'specialties', 'location')
    list_filter = ('experience_years', 'rate_per_event', 'availability')