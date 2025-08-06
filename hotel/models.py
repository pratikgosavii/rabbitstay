from django.db import models

# Create your models here.


class hotel(models.Model):
    
     name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Hotel Name'
    )

    hotel_id = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Hotel ID'
    )

    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='User'
    )

    category = django_filters.ChoiceFilter(
        choices=hotel.HOTEL_CATEGORY_CHOICES,
        label='Category'
    )

    property_type = django_filters.ModelChoiceFilter(
        queryset=property_type.objects.all(),
        label='Property Type'
    )

    city = django_filters.ModelChoiceFilter(
        queryset=city.objects.all(),
        label='City'
    )

    amenities = django_filters.ModelMultipleChoiceFilter(
        field_name='amenities',
        queryset=amenity.objects.all(),
        conjoined=True,
        label='Amenities'
    )

    pincode = django_filters.NumberFilter(
        field_name='pincode',
        label='Pincode'
    )

    star_rating = django_filters.NumberFilter(
        field_name='star_rating',
        label='Star Rating'
    )

    overall_rating = django_filters.NumberFilter(
        field_name='overall_rating',
        label='Overall Rating'
    )

    is_featured = django_filters.BooleanFilter(
        field_name='is_featured',
        label='Is Featured'
    )

    is_recommended = django_filters.BooleanFilter(
        field_name='is_recommended',
        label='Is Recommended'
    )

    is_active = django_filters.BooleanFilter(
        field_name='is_active',
        label='Is Active'
    )

    go_live = django_filters.BooleanFilter(
        field_name='go_live',
        label='Go Live'
    )

    class Meta:
        model = hotel
        fields = [
            'name', 'hotel_id', 'user', 'category', 'property_type',
            'city', 'amenities', 'pincode', 'star_rating',
            'overall_rating', 'is_featured', 'is_recommended',
            'is_active', 'go_live'
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Hide user filter for non-admins
        if request and not request.user.is_superuser:
            self.filters.pop('user', None)

        # Add Bootstrap class to fields
        for field in self.form.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs.update({'class': 'form-control'})
                

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
    
    max_guest_count = models.IntegerField()

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
