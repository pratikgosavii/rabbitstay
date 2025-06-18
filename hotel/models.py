from django.db import models

# Create your models here.


class hotel(models.Model):

    user = models.OneToOneField("users.User", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    amenities = models.ManyToManyField("masters.amenity", blank=True)
    address = models.TextField()
    city = models.ForeignKey("masters.city", on_delete=models.CASCADE, null=True, blank=True)
    star_rating = models.IntegerField()
    overall_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    main_image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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

    hotel = models.ForeignKey("hotel.hotel", on_delete=models.CASCADE, related_name="rooms")
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
        return f"{self.get_room_type_display()} - {self.title} - ₹{self.price_per_night}"



class hotel_roomsImage(models.Model):
    hotel_rooms = models.ForeignKey(hotel_rooms, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_rooms_gallery/')

    def __str__(self):
        return f"{self.hotel.name} Image"