from django.shortcuts import render

# Create your views here.



from rest_framework import viewsets
from .models import HotelBooking
from .serializers import HotelBookingSerializer

from datetime import timedelta


class HotelBookingViewSet(viewsets.ModelViewSet):
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


   


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from hotel.models import hotel
from hotel.filters import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from hotel.models import hotel, hotel_rooms
from .filters import HotelRoomFilter


class HotelListAPIView(generics.ListAPIView):
    queryset = hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter

    def get_filterset_kwargs(self):
        kwargs = super().get_filterset_kwargs()
        kwargs['request'] = self.request
        return kwargs


class HotelDetailAPIView(generics.RetrieveAPIView):
    queryset = hotel.objects.all()
    serializer_class = HotelSerializer  # this one includes rooms and images
    lookup_url_kwarg = 'hotel_id'



class HotelRoomListAPIView(generics.ListAPIView):
    serializer_class = HotelRoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelRoomFilter

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return hotel_rooms.objects.filter(hotel_id=hotel_id)



class HotelRoomDetailAPIView(generics.RetrieveAPIView):
    queryset = hotel_rooms.objects.all()
    serializer_class = HotelRoomSerializer
    lookup_url_kwarg = 'room_id'  # matches your URL param





from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.db.models import Count
from datetime import datetime



class AvailableRoomsAPIView(generics.ListAPIView):
    serializer_class = HotelRoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelRoomFilter  # your existing filterset

    def get_queryset(self):
        from_date_str = self.request.query_params.get('from_date')
        to_date_str = self.request.query_params.get('to_date')

        if not from_date_str or not to_date_str:
            raise ValidationError("Both 'from_date' and 'to_date' are required.")

        from datetime import datetime
        try:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

        if to_date < from_date:
            raise ValidationError("'to_date' must be after 'from_date'.")

        total_days = (to_date - from_date).days + 1

        availability_qs = RoomAvailability.objects.filter(
            date__gte=from_date,
            date__lte=to_date,
            available_count__gt=0
        )

        # Rooms that are available on all dates in range
        available_room_ids = (
            availability_qs.values('room')
            .annotate(available_days=Count('date', distinct=True))
            .filter(available_days=total_days)
            .values_list('room', flat=True)
        )

        # Start with rooms available on all dates
        qs = hotel_rooms.objects.filter(id__in=available_room_ids)

        # Now apply your existing filterset filtering for other fields
        filterset = HotelRoomFilter(self.request.GET, queryset=qs)
        return filterset.qs
    

    