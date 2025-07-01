from django.db import models

# Create your models here.



from decimal import Decimal

class HotelBooking(models.Model):
    
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    
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

    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    commission_gst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    tds_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="1% TDS on subtotal")
    tcs_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="1% TCS on subtotal")

    hotel_earning = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out and self.room:
            nights = (self.check_out - self.check_in).days or 1
            base = self.room.price_per_night * nights

            # Determine GST Rate
            gst_percent = Decimal('0.12') if base < 7500 else Decimal('0.18')
            gst = base * gst_percent
            subtotal = base + gst

            # Commission and its GST
            commission_percent = Decimal('0.10')
            commission = base * commission_percent
            commission_gst_percent = Decimal('0.18')
            commission_gst = commission * commission_gst_percent

            # TCS and TDS
            tcs_percent = Decimal('0.5')
            tds_percent = Decimal('0.1')
            tcs_amount = base * tcs_percent
            tds_amount = base * tds_percent

            # Final Amount to User
            total_amount = subtotal

            # Hotel's Earning
            hotel_net = subtotal - commission - commission_gst - tds_amount

            # Save fields
            self.base_amount = base
            self.gst_amount = gst
            self.total_amount = total_amount
            self.tax_amount = tcs_amount  # optional, or keep tax_amount separate
            self.commission_amount = commission
            self.commission_gst = commission_gst
            self.tds_amount = tds_amount
            self.tcs_amount = tcs_amount
            self.hotel_earning = hotel_net

        super().save(*args, **kwargs)


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and not user.is_superuser:
            self.fields['status'].choices = [('completed', 'Completed')]

    def __str__(self):
        return f"Booking for {self.first_name} at {self.hotel.name}"