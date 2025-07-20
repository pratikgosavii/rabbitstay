
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.db.models import Count
# from petprofile.models import *


from customer.models import *
from hotel.models import *
from django.db.models import Sum


from django.shortcuts import render
from django.db.models import Sum
import json

@login_required(login_url='login_admin')
def dashboard(request):
    bookings_count = HotelBooking.objects.count()
    hotels_count = hotel.objects.count()
    total_collection = HotelBooking.objects.filter(status="completed").aggregate(total=Sum('total_amount'))['total'] or 0

    # Example chart data
    market_data = [
        {'month': 'Jan', 'growth': 15, 'drop': -10},
        {'month': 'Feb', 'growth': 18, 'drop': -6},
        {'month': 'Mar', 'growth': 20, 'drop': -9},
        {'month': 'Apr', 'growth': 22, 'drop': -4},
        {'month': 'May', 'growth': 17, 'drop': -8},
    ]

    # Example location data
    locations = [
        {'name': 'Delhi', 'percentage': 75},
        {'name': 'Hyderabad', 'percentage': 55},
        {'name': 'Mumbai', 'percentage': 85},
    ]

    context = {
        'bookings_count': bookings_count,
        'hotels_count': hotels_count,
        'total_collection': round(total_collection / 1_000_000, 2),  # in Millions
        'percentage_change': 7,  # Replace with actual logic
        'current_week_order_count': 0,  # Replace with actual logic
        'market_data_json': json.dumps(market_data),
        'locations': locations
    }

    return render(request, 'adminDashboard.html', context)






