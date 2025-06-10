from django.db import models

# Create your models here.


class hotel(models.Model):

    user = models.OneToOneField("users.User", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    amenities = models.ManyToManyField("masters.amenity", blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    star_rating = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    includes_taxes = models.BooleanField(default=True)
    free_breakfast = models.BooleanField(default=False)
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
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hotel.name} Image"