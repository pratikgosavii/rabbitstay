from rest_framework import serializers
from .models import HotelBooking

class HotelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelBooking
        fields = '__all__'
