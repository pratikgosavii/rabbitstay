import django_filters
from .models import *

class EventFilter(django_filters.FilterSet):
    class Meta:
        model = event
        exclude = ['image']  # ⛔ Exclude unsupported field

class testFilter(django_filters.FilterSet):
    class Meta:
        model = test
        exclude = ['image']  # ⛔ Exclude unsupported field

class couponFilter(django_filters.FilterSet):
    class Meta:
        model = coupon
        exclude = ['image']  # ⛔ Exclude unsupported field

class symptomFilter(django_filters.FilterSet):
    class Meta:
        model = symptom
        exclude = ['image']  # ⛔ Exclude unsupported field

class productFilter(django_filters.FilterSet):
    class Meta:
        model = product
        exclude = ['image']  # ⛔ Exclude unsupported field

class food_menuFilter(django_filters.FilterSet):
    class Meta:
        model = food_menu
        exclude = ['image']  # ⛔ Exclude unsupported field

class serviceFilter(django_filters.FilterSet):
    class Meta:
        model = service
        exclude = ['image']  # ⛔ Exclude unsupported field

class product_categoryFilter(django_filters.FilterSet):
    class Meta:
        model = product_category
        exclude = ['image']  # ⛔ Exclude unsupported field

class service_categoryFilter(django_filters.FilterSet):
    class Meta:
        model = service_category
        exclude = ['image']  # ⛔ Exclude unsupported field

class consultation_typeFilter(django_filters.FilterSet):
    class Meta:
        model = consultation_type
        exclude = ['image']  # ⛔ Exclude unsupported field

class home_bannerFilter(django_filters.FilterSet):
    class Meta:
        model = home_banner
        exclude = ['image']  # ⛔ Exclude unsupported field

class online_consultation_typeFilter(django_filters.FilterSet):
    class Meta:
        model = online_consultation_type
        exclude = ['image']  # ⛔ Exclude unsupported field
