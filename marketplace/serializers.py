from rest_framework import serializers
from .models import Chef, Menus, Booking
from core.serializers import UserSerializer


class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = [
            "id",
            "dish_name",
            "description",
            "price",
        ]


class BookingSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "client",
            "event_date",
            "start_time",
            "end_time",
            "location",
            "total_price",
            "status",
            "created_at",
        ]


class ChefSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menus = MenusSerializer(many=True, read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)  # Optional

    class Meta:
        model = Chef
        fields = [
            "id",
            "user",
            "bio",
            "specialties",
            "experience_years",
            "rate_per_event",
            "location",
            "availability",
            "menus",
            "bookings",
        ]
