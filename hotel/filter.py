# filters.py
import django_filters
from customer.models import HotelBooking
from .models import *
from users.models import *
from django import forms


class HotelFilter(django_filters.FilterSet):
    
    hotel_id = django_filters.CharFilter(
        label='Hotel ID',
        method='filter_hotel_id',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        empty_label="All Users",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    created_at = django_filters.DateFilter(
        field_name='created_at',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Created On"
    )

    

    is_active = django_filters.BooleanFilter(
        field_name='is_active',
        widget=forms.Select(choices=[('', 'All'), ('true', 'Active'), ('false', 'Inactive')],
                            attrs={'class': 'form-select'}),
        label='Status',
        method='filter_is_active'
    )

    class Meta:
        model = hotel
        fields = ['user', 'hotel_id', 'created_at', 'is_active']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Hide user filter for non-admins
        if request and not request.user.is_superuser:
            self.filters.pop('user', None)

    def filter_is_active(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(is_active=True)
        elif value == 'false':
            return queryset.filter(is_active=False)
        return queryset

class HotelRoomFilter(django_filters.FilterSet):
 

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