from django.db import models
from django.conf import settings


class Chef(models.Model):
    bio = models.TextField()
    specialties = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField()
    rate_per_event = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    availability = models.BooleanField(default=True)
    
    user = models.OneToOneField(  # one chef = one user
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chef_profile"
    )

    def __str__(self):
        return f"Chef {self.user.email} - {self.specialties}"

class Menus(models.Model):
    dish_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    chef = models.ForeignKey(
        Chef,
        on_delete=models.CASCADE,
        related_name="menus"
    )

    def __str__(self):
        return f"{self.dish_name} by {self.chef.user.email}"


class Booking(models.Model):
    CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    chef = models.ForeignKey(
        Chef,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.client.email} with Chef {self.chef.user.email}"