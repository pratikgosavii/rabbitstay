# filters.py
import django_filters
from hotel.models import hotel, hotel_rooms

class HotelFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.CharFilter(lookup_expr='icontains')
    pincode = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = hotel
        fields = ['city', 'state', 'pincode']


class HotelRoomFilter(django_filters.FilterSet):
    room_type = django_filters.NumberFilter(field_name='room_type__id')
    title = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    refundable = django_filters.BooleanFilter()
    meals_included = django_filters.BooleanFilter()

    # 👇 Optional fields (recommended)
    bed_type = django_filters.CharFilter(lookup_expr='icontains')
    capacity = django_filters.CharFilter(lookup_expr='icontains')
    view = django_filters.CharFilter(lookup_expr='icontains')

    # 👇 Many-to-many: room amenities by ID
    room_amenities = django_filters.ModelMultipleChoiceFilter(
        field_name='room_amenities__id',
        to_field_name='id',
        queryset=hotel_rooms._meta.get_field('room_amenities').related_model.objects.all()
    )

    class Meta:
        model = hotel_rooms
        fields = [
            'room_type',
            'title',
            'price_min',
            'price_max',
            'refundable',
            'meals_included',
            'bed_type',
            'capacity',
            'view',
            'room_amenities',
        ]