from django.shortcuts import render

# Create your views here.



from rest_framework import viewsets
from .models import HotelBooking
from .serializers import HotelBookingSerializer

class HotelBookingViewSet(viewsets.ModelViewSet):
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
