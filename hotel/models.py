from django.db import models

# Create your models here.


class hotel(models.Model):
    
    HOTEL_CATEGORY_CHOICES = [
        ('Budget', 'Budget'),
        ('Mid_range', 'Mid-range'),
        ('Premium', 'Premium'),
        ('Boutique', 'Boutique'),
        # Add more as needed
    ]

    hotel_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

    user = models.OneToOneField("users.User", on_delete=models.CASCADE, null=True, blank=True, related_name ="hotel")
    name = models.CharField(max_length=255)
    
    category = models.CharField(max_length=50, choices=HOTEL_CATEGORY_CHOICES, default='Budget')
    property_type = models.ForeignKey("masters.property_type", on_delete=models.CASCADE, null=True, blank=True)
    no_of_rooms = models.IntegerField()

    amenities = models.ManyToManyField("masters.amenity", blank=True)
    address = models.TextField()
    city = models.ForeignKey("masters.city", on_delete=models.CASCADE, null=True, blank=True)
    landmark = models.TextField(null=True, blank=True)

    pincode = models.IntegerField()
    star_rating = models.IntegerField(null=True, blank=True)
    overall_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    main_image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    is_featured = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Legal & Tax Info
    gst_number = models.CharField(
        max_length=15,
        help_text="GST Number (15 characters, e.g., 29ABCDE1234F2Z5)",
        null=True,
        blank=True
    )
    gst_certificate = models.FileField(
        upload_to='hotel_docs/gst_certificates/',
        null=True,
        blank=True,
        help_text="Upload GST Certificate (PDF/Image)"
    )
    pan_number = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="PAN Card Number (optional)"
    )

    # ✅ Bank Details
    account_holder_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=30, null=True, blank=True)
    ifsc_code = models.CharField(max_length=15, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    bank_document = models.FileField(
        upload_to='hotel_docs/bank_docs/',
        null=True,
        blank=True,
        help_text="Upload Cancelled Cheque or Bank Passbook (Image/PDF)"
    )


    def save(self, *args, **kwargs):
    # First save to get ID
        if not self.hotel_id:
            super().save(*args, **kwargs)  # Save once to get ID
            self.hotel_id = f"RS-{self.id:03d}"
            super().save(update_fields=["hotel_id"])  # Save only hotel_id
        else:
            super().save(*args, **kwargs)



    def __str__(self):
        return self.name

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=hotel)
def sync_user_status_with_hotel(sender, instance, **kwargs):
    if instance.user:
        if instance.user.is_active != instance.is_active:
            instance.user.is_active = instance.is_active
            instance.user.save(update_fields=["is_active"])


class HotelImage(models.Model):
    hotel = models.ForeignKey(hotel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_gallery/')

    def __str__(self):
        return f"{self.hotel.name} Image"



class hotel_rooms(models.Model):

    ROOM_TYPE_CHOICES = [
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
        ('suite', 'Suite'),
        # Add more as needed
    ]
    

    ROOM_PACKAGE_CHOICES = [
        ('room_only', 'Room Only'),
        ('breakfast', 'Breakfast Included'),
        ('breakfast_lunch', 'Breakfast + Lunch'),
        ('breakfast_dinner', 'Breakfast + Dinner'),
        ('all_meals', 'Breakfast + Lunch + Dinner'),
    ]

    hotel = models.ForeignKey("hotel.hotel", on_delete=models.CASCADE, related_name="rooms", null=True, blank=True)
    room_type = models.ForeignKey("masters.room_type", on_delete=models.CASCADE, related_name="rooms")
    main_image = models.ImageField(upload_to='hotels/', null=True, blank=True)
   

    title = models.CharField(
        max_length=50,
        choices=ROOM_PACKAGE_CHOICES,
        default='room_only'
    )

    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    refundable = models.BooleanField(default=True)
    meals_included = models.BooleanField(default=False)
    bed_type = models.CharField(max_length=100, blank=True)  # e.g., "1 Queen Bed + 1 Double Bed"
    capacity = models.CharField(max_length=100, blank=True)  # e.g., "2 Adults, 1 Child"
    view = models.CharField(max_length=100, blank=True)  # e.g., "Beach View"
    room_amenities = models.ManyToManyField('masters.room_amenity', blank=True)  # Optional: for extra features

    def __str__(self):
        return f" {self.room_type} - ₹{self.price_per_night}"



class hotel_roomsImage(models.Model):
    hotel_rooms = models.ForeignKey(hotel_rooms, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_rooms_gallery/')

    def __str__(self):
        return f"{self.hotel.name} Image"



class HotelAvailability(models.Model):
    hotel = models.ForeignKey("hotel.hotel", on_delete=models.CASCADE)
    date = models.DateField()
    is_open = models.BooleanField(default=True)

    class Meta:
        unique_together = ('hotel', 'date')

    def __str__(self):
        return f"{self.hotel.name} - {self.date} - {'Open' if self.is_open else 'Closed'}"



class RoomAvailability(models.Model):
    room = models.ForeignKey("hotel_rooms", on_delete=models.CASCADE)
    date = models.DateField()
    available_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('room', 'date')

    def __str__(self):
        return f"{self.room} - {self.date} - {self.available_count} available"
