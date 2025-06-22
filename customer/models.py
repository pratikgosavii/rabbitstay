from django.db import models

# Create your models here.



from decimal import Decimal

class HotelBooking(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
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

     # Financial fields
    base_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Room rate * nights")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Service Tax or Other")
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="GST component")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Final price to user")
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out and self.room:
            nights = (self.check_out - self.check_in).days or 1
            base = self.room.price_per_night * nights

            tax_percent_decimal = self.tax_percent / Decimal('100')  # e.g. 5% as 0.05
            gst_percent = Decimal('0.18')  # fixed GST 18%

            tax = base * tax_percent_decimal
            gst = base * gst_percent
            total = base + tax + gst

            self.base_amount = base
            self.tax_amount = tax
            self.gst_amount = gst
            self.total_amount = total

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Booking for {self.first_name} at {self.hotel.name}"