from django.db import models

# Create your models here.



class HotelBooking(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    hotel = models.ForeignKey("hotel.hotel", on_delete=models.CASCADE)
    room = models.ForeignKey("hotel.hotel_rooms", on_delete=models.CASCADE)

    check_in = models.DateField()
    check_out = models.DateField()
    guest_count = models.PositiveIntegerField()

    is_for_self = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    special_request = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.first_name} at {self.hotel.name}"