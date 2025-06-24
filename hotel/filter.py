# filters.py
import django_filters
from customer.models import HotelBooking
from .models import *
from users.models import *
from django import forms


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