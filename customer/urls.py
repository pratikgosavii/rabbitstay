from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static




from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'hotel-bookings', HotelBookingViewSet)


urlpatterns = [


    path('hotels/', HotelListAPIView.as_view(), name='hotel-list'),
    path('hotels/<int:hotel_id>/', HotelDetailAPIView.as_view(), name='hotel-detail'),

    path('hotels/<int:hotel_id>/rooms/', HotelRoomListAPIView.as_view(), name='hotel-room-list'),
    path('room/<int:room_id>/', HotelRoomDetailAPIView.as_view(), name='room-detail'),

    path('available-rooms/', AvailableRoomsAPIView.as_view(), name='available-rooms'),

]  + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)