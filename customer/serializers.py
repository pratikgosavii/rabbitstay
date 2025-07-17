from rest_framework import serializers
from .models import HotelBooking
from hotel.models import *


from datetime import timedelta


 
class HotelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelBooking
        exclude = ['user']  # user added in view

    def validate(self, data):
        room = data.get('room')
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        if not room or not check_in or not check_out:
            raise serializers.ValidationError("Room, check-in, and check-out are required.")

        # Check availability on each date
        date = check_in
        while date < check_out:
            try:
                avail = RoomAvailability.objects.get(room=room, date=date)
                if avail.available_count < 1:
                    raise serializers.ValidationError(
                        f"Room not available on {date}. Please choose a different date."
                    )
            except RoomAvailability.DoesNotExist:
                raise serializers.ValidationError(
                    f"Room availability not set for {date}. Please contact support."
                )
            date += timedelta(days=1)

        return data
    
    


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'image']


class HotelRoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = hotel_roomsImage
        fields = ['id', 'image']


class HotelRoomSerializer(serializers.ModelSerializer):
    hotel_details = serializers.SerializerMethodField()  # to avoid recursive nesting issues
    room_type_name = serializers.CharField(source='room_type.name', read_only=True)
    images = HotelRoomImageSerializer(many=True, read_only=True)  # room images

    class Meta:
        model = hotel_rooms
        fields = [
            'id', 'room_type', 'room_type_name', 'title', 'price_per_night',
            'refundable', 'meals_included', 'capacity', 'view', 'bed_type',
            'images', 'hotel_details'
        ]
        read_only_fields = ['hotel_details']

    def get_hotel_details(self, obj):
        # avoid full hotel -> rooms -> hotel recursion
        return {
            'id': obj.hotel.id,
            'name': obj.hotel.name,
            'hotel_id': obj.hotel.hotel_id,
            'city': obj.hotel.city.name if obj.hotel.city else None,
            'address': obj.hotel.address,
        }


class HotelSerializer(serializers.ModelSerializer):
    rooms = HotelRoomSerializer(many=True, read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)
    city = serializers.StringRelatedField()  # or use CitySerializer if needed
    amenities = serializers.StringRelatedField(many=True)  # or use AmenitySerializer
    main_image = serializers.ImageField(required=False)

    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()

    class Meta:
        model = hotel
        fields = [
            'id', 'name', 'hotel_id', 'user', 'category', 'no_of_rooms',
            'amenities', 'address', 'city', 'landmark', 'pincode',
            'star_rating', 'overall_rating', 'main_image', 'profit_margin',
            'is_featured', 'description', 'is_active', 'created_at',
            'gst_number', 'gst_certificate', 'pan_number',
            'account_holder_name', 'account_number', 'ifsc_code', 'bank_name', 'bank_document',
            'rooms', 'images',

            'min_price', 'max_price'
        ]

    def get_min_price(self, obj):
        prices = obj.rooms.values_list('price_per_night', flat=True)
        return min(prices) if prices else None

    def get_max_price(self, obj):
        prices = obj.rooms.values_list('price_per_night', flat=True)
        return max(prices) if prices else None