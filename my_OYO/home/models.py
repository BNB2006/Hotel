from django.db import models
from accounts.models import Hotel, HotelUser
from datetime import date

# Create your models here.
class HotelBooking(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    hotel = models.ForeignKey(Hotel, on_delete= models.CASCADE, related_name="bookings")
    booking_user = models.ForeignKey(HotelUser, on_delete=models.CASCADE)
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.hotel.hotel_name} for {self.booking_user.first_name} ({self.status})"
    
    @property
    def computed_status(self):
        """Returns the current status based on dates, preserving cancelled status"""
        today = date.today()
        if self.status == "cancelled":
            return "cancelled"
        if self.booking_start_date > today:
            return "upcoming"
        elif self.booking_start_date <= today <= self.booking_end_date:
            return "ongoing"
        elif today > self.booking_end_date:
            return "completed"
        return self.status
    