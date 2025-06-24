from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static




from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'customer-address', customer_address_ViewSet, basename='test-booking')


urlpatterns = [

    path('vendor-dashboard/', vendor_dashboard, name='vendor_dashboard'),

    path('add-hotel/', add_hotel, name='add_hotel'),
    path('view-hotel/', view_hotel, name='view_hotel'),
    path('update-hotel/<hotel_id>', update_hotel, name='update_hotel'),
    path('delete-hotel/<hotel_id>', delete_hotel, name='delete_hotel'),
    path('list-hotel/', list_hotel, name='list_hotel'),

    path('delete-hotel-image/<int:image_id>/', delete_hotel_image, name='delete_hotel_image'),

    path('add-hotel-rooms/', add_hotel_rooms, name='add_hotel_rooms'),
    path('update-hotel-rooms/<hotel_rooms_id>', update_hotel_rooms, name='update_hotel_rooms'),
    path('delete-hotel-rooms/<hotel_rooms_id>', delete_hotel_rooms, name='delete_hotel_rooms'),
    path('list-hotel-rooms/', list_hotel_rooms, name='list_hotel_rooms'),
    
    path('delete-hotel-room-image/<int:image_id>/', delete_hotel_room_image, name='delete_hotel_room_image'),
    
    path('list-hotel-bookings/', list_hotel_bookings, name='list_hotel_bookings'),
    path('update-hotel-bookings/<booking_id>', update_hotel_bookings, name='update_hotel_bookings'),

    path('list-hotel-earning/', list_hotel_earning, name='list_hotel_earning'),
    path('hotel-invoice/<booking_id>', render_pdf_view, name='render_pdf_view'),



]  + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)