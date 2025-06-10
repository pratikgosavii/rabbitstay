from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static




from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'customer-address', customer_address_ViewSet, basename='test-booking')


urlpatterns = [

    path('add-hotel/', add_hotel, name='add_hotel'),
    path('update-hotel/<hotel_id>', update_hotel, name='update_hotel'),
    path('delete-hotel/<hotel_id>', delete_hotel, name='delete_hotel'),
    path('list-hotel/', list_hotel, name='list_hotel'),
    

]  + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)