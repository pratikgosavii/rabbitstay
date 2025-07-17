# filters.py
import django_filters
from customer.models import HotelBooking
from .models import *
from masters.models import *
from users.models import *
from django import forms


    
class HotelFilter(django_filters.FilterSet):
    hotel_id = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Hotel ID'
    )

    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Hotel Name'
    )

    category = django_filters.ChoiceFilter(
        choices=hotel.HOTEL_CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Category'
    )

    no_of_rooms = django_filters.NumberFilter(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Number of Rooms'
    )

    amenities = django_filters.ModelMultipleChoiceFilter(
        queryset=amenity.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label='Amenities'
    )

    city = django_filters.ModelChoiceFilter(
        field_name='city',
        queryset=city.objects.all(),
        label="City",
        widget=forms.Select(attrs={'class': 'form-select'})
    )


    landmark = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Landmark'
    )

    pincode = django_filters.NumberFilter(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Pincode'
    )

    star_rating = django_filters.NumberFilter(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Star Rating'
    )

    overall_rating = django_filters.NumberFilter(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Overall Rating'
    )

    profit_margin = django_filters.NumberFilter(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Profit Margin'
    )

    is_featured = django_filters.BooleanFilter(
        widget=forms.Select(choices=[('', 'All'), ('true', 'Yes'), ('false', 'No')],
                            attrs={'class': 'form-select'}),
        label='Featured',
        method='filter_boolean'
    )

    is_active = django_filters.BooleanFilter(
        widget=forms.Select(choices=[('', 'All'), ('true', 'Active'), ('false', 'Inactive')],
                            attrs={'class': 'form-select'}),
        label='Status',
        method='filter_boolean'
    )

    gst_number = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='GST Number'
    )

    pan_number = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='PAN Number'
    )

    account_holder_name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Account Holder Name'
    )

    account_number = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Account Number'
    )

    ifsc_code = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='IFSC Code'
    )

    bank_name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Bank Name'
    )

    created_at = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Created At'
    )

    description = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label='Description'
    )

    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Owner'
    )

    class Meta:
        model = hotel
        fields = [
            'user', 'hotel_id', 'name', 'category', 'no_of_rooms', 'amenities', 'city',
            'landmark', 'pincode', 'star_rating', 'overall_rating', 'profit_margin',
            'is_featured', 'is_active', 'gst_number', 'pan_number', 'account_holder_name',
            'account_number', 'ifsc_code', 'bank_name', 'created_at', 'description'
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request and not request.user.is_superuser:
            self.filters.pop('user', None)

    def filter_boolean(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(**{name: True})
        elif value == 'false':
            return queryset.filter(**{name: False})
        return queryset
    


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