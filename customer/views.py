from django.shortcuts import get_object_or_404, render

# Create your views here.



from rest_framework import viewsets
from .models import HotelBooking
from .serializers import HotelBookingSerializer

from datetime import timedelta
from rest_framework.exceptions import ValidationError
from django.db import transaction
from datetime import timedelta


class HotelBookingViewSet(viewsets.ModelViewSet):
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            booking = serializer.save(user=self.request.user)

            room = booking.room
            check_in = booking.check_in
            check_out = booking.check_out
            total_days = (check_out - check_in).days
            dates = [check_in + timedelta(days=i) for i in range(total_days)]

            availabilities = RoomAvailability.objects.select_for_update().filter(
                room=room,
                date__in=dates
            )

            if availabilities.count() != total_days:
                raise ValidationError("Some dates are missing availability records.")

            for avail in availabilities:
                if avail.available_count < 1:
                    raise ValidationError(f"Room not available on {avail.date}.")
                avail.available_count -= 1
                avail.save()
   


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
    

    

    

class AvailableHotelsAPIView(APIView):
    def get(self, request):
        city = request.query_params.get('city')
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')

        if not city or not check_in or not check_out:
            return Response({"error": "city, check_in, and check_out are required."}, status=400)

        try:
            check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        if check_in >= check_out:
            return Response({"error": "check_out must be after check_in"}, status=400)

        if check_in < date.today():
            return Response({"error": "check_in cannot be in the past."}, status=400)

        # Step 1: Get all rooms from hotels in the given city
        rooms = hotel_rooms.objects.select_related('hotel').filter(hotel__city=city)

        # Step 2: Get all availabilities for the room/date range
        room_ids = rooms.values_list('id', flat=True)
        days = (check_out - check_in).days
        required_dates = {check_in + timedelta(days=i) for i in range(days)}

        availabilities = RoomAvailability.objects.filter(
            room_id__in=room_ids,
            date__range=(check_in, check_out - timedelta(days=1)),
            available_count__gte=1
        ).values('room_id', 'date')

        # Step 3: Build room → available_dates mapping
        from collections import defaultdict
        room_to_dates = defaultdict(set)
        for entry in availabilities:
            room_to_dates[entry['room_id']].add(entry['date'])

        # Step 4: Filter rooms that are available for all required dates
        valid_room_ids = [room_id for room_id, dates in room_to_dates.items() if required_dates.issubset(dates)]

        # Step 5: Get unique hotels from those rooms
        available_hotels = hotel.objects.filter(rooms__id__in=valid_room_ids).distinct()

        return Response(HotelSerializer(available_hotels, many=True).data)



from datetime import datetime, time, timedelta

class CancelBookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = HotelBooking.objects.get(id=booking_id, user=request.user)
        except HotelBooking.DoesNotExist:
            return Response({'error': 'Booking not found or unauthorized'}, status=404)

        if booking.status == 'cancelled':
            return Response({'message': 'Booking already cancelled'}, status=400)

        # Calculate check-in datetime as 9 AM on the check-in date
        checkin_datetime = datetime.combine(booking.check_in, time(hour=9, minute=0))

        # Calculate current datetime
        now = datetime.now()

        # Ensure cancellation is at least 24 hours in advance
        if now > checkin_datetime - timedelta(hours=24):
            return Response({'error': 'Cannot cancel less than 24 hours before check-in (9 AM)'}, status=400)

        # Cancel the booking
        booking.status = 'cancelled'
        booking.save()

        return Response({'message': 'Booking cancelled successfully'}, status=200)



from rest_framework import viewsets, permissions

        
class SupportTicketViewSet(viewsets.ModelViewSet):
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



from rest_framework import status



class TicketMessageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        ticket_id = request.query_params.get('ticket_id')
        if not ticket_id:
            return Response({'error': 'ticket_id is required'}, status=400)

        messages = TicketMessage.objects.filter(ticket__id=ticket_id).order_by('created_at')
        serializer = TicketMessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        ticket_id = request.data.get('ticket')
        message = request.data.get('message')

        if not ticket_id or not message:
            return Response({'error': 'ticket and message are required'}, status=400)

        ticket = get_object_or_404(SupportTicket, id=ticket_id)

        new_message = TicketMessage.objects.create(
            ticket=ticket,
            sender=request.user,
            message=message
        )

        serializer = TicketMessageSerializer(new_message, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
