# filters.py
import django_filters
from customer.models import HotelBooking
from .models import *
from masters.models import *
from users.models import *
from django import forms


    
class HotelFilter(django_filters.FilterSet):
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

    city = django_filters.ModelChoiceFilter(
        queryset=city.objects.all(),
        label='City'
    )

    amenities = django_filters.ModelMultipleChoiceFilter(
        field_name='amenities',
        queryset=amenity.objects.all(),
        to_field_name='id',
        conjoined=True,
        label='Amenities'
    )

    class Meta:
        model = hotel
        fields = [
            'name', 'hotel_id', 'user', 'category',
            'city', 'amenities'
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Restrict 'user' field for non-superusers
        if request and not request.user.is_superuser:
            self.filters.pop('user', None)

        # Apply 'form-control' to all visible fields
        for field in self.form.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs.update({'class': 'form-control'})


  


class HotelRoomFilter(django_filters.FilterSet):
 

    hotel_id = django_filters.CharFilter(
        label='Hotel ID',
        method='filter_hotel_id',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    hotel = django_filters.ModelChoiceFilter(
        queryset=hotel.objects.all(),
        empty_label="All hotels",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = hotel_rooms
        fields = ['hotel', 'hotel_id']  # ✅ include hotel_id here!

    def filter_hotel_id(self, queryset, name, value):
        return queryset.filter(hotel__hotel_id__icontains=value)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)



    


class HotelBookingFilter(django_filters.FilterSet):
    
    
    hotel = django_filters.ModelChoiceFilter(
        queryset= hotel.objects.all(),
        empty_label="All Hotels",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    user = django_filters.ModelChoiceFilter(
        queryset= User.objects.all(),
        empty_label="All users",
        widget=forms.Select(attrs={'class': 'form-select'})
    )



    check_in = django_filters.DateFilter(
        field_name='check_in',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    check_out = django_filters.DateFilter(
        field_name='check_out',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = HotelBooking
        fields = ['user', 'hotel', 'check_in', 'check_out']


    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Hide hotel filter for non-admins
        if request and not request.user.is_superuser:
            self.filters.pop('hotel', None)
            self.filters.pop('user', None)