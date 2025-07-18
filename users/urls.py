from django.urls import path

from .views import *


from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')



urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login-admin/', login_admin, name='login_admin'),
    path('login-vendor/', login_vendor, name='login_vendor'),
    path('login-staff/', login_staff, name='login_staff'),

    path('vendor-request/', vendor_request, name='vendor_request'),

    path('register-vendor/', register_vendor, name='register_vendor'),
    path('active-vendor-request/<user_id>', activate_vendor_request, name='activate_vendor_request'),

    path('update-user/', UserUpdateView.as_view(), name='UserUpdateView'),
    path('get-user/', UsergetView.as_view(), name='UsergetView'),
    path('reset-password/', ResetPasswordView.as_view(), name='ResetPasswordView'),
    
    path('logout-staff/', staff_logout_page, name='staff_logout'),
    path('logout-vendor/', vendor_logout_page, name='vendor_logout'),
    path('logout/', logout_page, name='logout'),
    
    path('customer-user-list/', customer_user_list, name='customer_user_list'),
    path('provider-user-list/', provider_user_list, name='provider_user_list'),
    path('list-custome-user/', list_custom_user, name='list_custom_user'),


    path('user-booking-history/<user_id>', user_booking_history, name='user_booking_history'),
    path('hotel-booking-history/<user_id>', hotel_booking_history, name='hotel_booking_history'),



    path('add-custome-user/', add_custom_user, name='add_custom_user'),
    path('custom-user-update/<int:user_id>/', update_custom_user, name='update_custom_user'),
    path('custom-user-delete/<int:user_id>/', delete_custom_user, name='delete_custom_user'),


] + router.urls
