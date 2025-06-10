from django.contrib import admin
from .models import *

# Register your models here.

from .models import *

admin.site.register(amenity)
admin.site.register(coupon)
admin.site.register(service_category)
admin.site.register(service_subcategory)
admin.site.register(service)
admin.site.register(symptom)
admin.site.register(customer_address)
admin.site.register(testimonials)
admin.site.register(vaccination)
admin.site.register(online_consultation_type)