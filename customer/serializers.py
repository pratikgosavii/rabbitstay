from rest_framework import serializers
from .models import *
from hotel.models import *


from datetime import timedelta


from rest_framework import serializers
from datetime import date as today_date, timedelta
from datetime import date, timedelta

 

    


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


from masters.serializers import *

class HotelSerializer(serializers.ModelSerializer):
    rooms = HotelRoomSerializer(many=True, read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)
    city = serializers.StringRelatedField()  # or use CitySerializer if needed
    amenities = amenity_serializer(many=True, read_only=True)  # or use AmenitySerializer
    property_type = property_type_serializer(many=True, read_only=True)  # or use AmenitySerializer
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
            'rooms', 'images', 'is_recommended', 'property_type',

            'min_price', 'max_price'
        ]

    def get_min_price(self, obj):
        prices = obj.rooms.values_list('price_per_night', flat=True)
        return min(prices) if prices else None

    def get_max_price(self, obj):
        prices = obj.rooms.values_list('price_per_night', flat=True)
        return max(prices) if prices else None
    


    
class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['id', 'subject', 'booking', 'is_resolved', 'created_at']
        read_only_fields = ['id', 'is_resolved', 'created_at']




class TicketMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    is_from_user = serializers.SerializerMethodField()

    class Meta:
        model = TicketMessage
        fields = ['id', 'ticket', 'sender', 'sender_name', 'message', 'created_at', 'is_from_user']
        read_only_fields = ['sender', 'created_at']

    def get_is_from_user(self, obj):
        request = self.context.get('request')
        return obj.sender == request.user if request else False
    


    
class HotelBookingSerializer(serializers.ModelSerializer):
    
    room = serializers.PrimaryKeyRelatedField(
        queryset=hotel_rooms.objects.all(), write_only=True
    )
    hotel = serializers.PrimaryKeyRelatedField(
        queryset=hotel.objects.all(), write_only=True
    )

    # Read-only nested output fields
    room_details = HotelRoomSerializer(source='room', read_only=True)
    hotel_details = HotelSerializer(source='hotel', read_only=True)

    class Meta:
        model = HotelBooking
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user if 'context' in kwargs and 'request' in kwargs['context'] else None
        super().__init__(*args, **kwargs)

        if user and not user.is_superuser:
            self.fields['status'].choices = [('completed', 'Completed')]

    def validate(self, data):
        room = data.get('room')
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        if not room or not check_in or not check_out:
            raise serializers.ValidationError("Room, check-in, and check-out are required.")

        if check_in < date.today():
            raise serializers.ValidationError("Check-in cannot be in the past.")

        if check_in >= check_out:
            raise serializers.ValidationError("Check-out must be after check-in.")

        # Room availability check
        num_days = (check_out - check_in).days
        required_dates = {check_in + timedelta(days=i) for i in range(num_days)}

        availabilities = RoomAvailability.objects.filter(
            room=room,
            date__range=(check_in, check_out - timedelta(days=1))
        )

        found_dates = {a.date for a in availabilities if a.available_count >= 1}
        missing = required_dates - found_dates
        if missing:
            missing_str = ", ".join(str(d) for d in sorted(missing))
            raise serializers.ValidationError(f"Room not available on: {missing_str}")

        return data

        

class FavouriteHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = favouritehotel
        fields = ['id', 'user', 'hotel']  # Include 'user' but make it read-only
        read_only_fields = ['user']  