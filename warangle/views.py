
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.db.models import Count
# from petprofile.models import *


from customer.models import *
from hotel.models import *
from masters.models import *
from django.db.models import Sum


from django.shortcuts import render
from django.db.models import Sum
import json



def get_booking_percent_by_city():
    total_bookings = HotelBooking.objects.count()

    if total_bookings == 0:
        return {}

    # Assuming hotel model has a `city` field
    city_data = (
        HotelBooking.objects
        .values('hotel__city__name')
        .annotate(city_count=Count('id'))
    )

    # Format output with percentage
    result = {
        entry['hotel__city__name']: round((entry['city_count'] / total_bookings) * 100, 2)
        for entry in city_data
    }

    return result


from django.db.models import Sum
from django.utils.timezone import now
from calendar import month_name
from collections import defaultdict
from datetime import timedelta


def get_monthly_booking_data():
    today = now().date()
    data = defaultdict(int)

    for i in range(12):
        month_date = today.replace(day=1) - timedelta(days=30 * i)
        month = month_date.month
        year = month_date.year

        count = HotelBooking.objects.filter(created_at__year=year, created_at__month=month).count()
        data[month_name[month]] = count

    # Reverse to make chronological (oldest to newest)
    return dict(reversed(data.items()))


@login_required(login_url='login_admin')
def dashboard(request):
    bookings_count = HotelBooking.objects.count()
    hotels_count = hotel.objects.count()
    city_count = city.objects.count()
    total_collection = HotelBooking.objects.filter(status="completed").aggregate(total=Sum('total_amount'))['total'] or 0

    result = get_booking_percent_by_city()

    monthly_data = get_monthly_booking_data()
    months = list(monthly_data.keys())
    bookings = list(monthly_data.values())

    print(months)
    print(bookings)

  

    context = {
        'bookings_count': bookings_count,
        'hotels_count': hotels_count,
        'city_count': city_count,
        'total_collection': round(total_collection),
        'result': result,

        "months": months,
        "bookings": bookings,
    }

    return render(request, 'adminDashboard.html', context)






