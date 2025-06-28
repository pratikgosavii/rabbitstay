from django.shortcuts import get_object_or_404, render

from masters.filters import EventFilter

# Create your views here.


from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import HttpResponseRedirect

from users.permissions import *

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





@login_required(login_url='login_admin')
def vendor_dashboard(request):

    return render(request, 'vendor_dashboard.html')




@login_required(login_url='login_admin')
def add_hotel(request):

    if request.method == 'POST':

        form = hotel_Form(request.POST, request.FILES)
        if not request.user.is_superuser:
            form.fields.pop('profit_margin')
        if form.is_valid():
            hotel = form.save(commit=False)
            if not request.user.is_superuser:
                hotel.user = request.user  # auto-assign vendor user
            hotel.save()
            form.save_m2m()  # Save the many-to-many relationships
            
            for img in request.FILES.getlist('image'):
                HotelImage.objects.create(hotel=hotel, image=img)

            return redirect('list_hotel')
        
        else:
            print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'add_hotel.html', context)
        
    else:

        print(request.user)

        if request.user.is_superuser:

            print('1111')

        elif request.user.is_service_provider:

            print('----------434-----------')
        form = hotel_Form()

        context = { 
                'form': forms, 
        }

        return render(request, 'add_hotel.html', )


@login_required(login_url='login_admin')
def view_hotel(request):

    user_hotel = get_object_or_404(
        hotel.objects.prefetch_related(
            Prefetch(
                'rooms',
                queryset=hotel_rooms.objects.select_related('room_type').prefetch_related('room_amenities')
            )
        ),
        user=request.user
    )

    context = {
        'data': user_hotel # wrapped in a list if template expects iterable
    }

    return render(request, 'view_hotel.html', context)    

@login_required(login_url='login_admin')
def update_hotel(request, hotel_id):

    instance = hotel.objects.get(id = hotel_id)

    if request.method == 'POST':

        instance = hotel.objects.get(id=hotel_id)

        forms = hotel_Form(request.POST, request.FILES, instance=instance)
        if not request.user.is_superuser:
            forms.fields.pop('profit_margin')
        
        if forms.is_valid():
            hotels = forms.save(commit=False)
            if not request.user.is_superuser:
                hotels.user = request.user  # auto-assign vendor user
            hotels.save()
            forms.save_m2m() 

            for img in request.FILES.getlist('image'):
                HotelImage.objects.create(hotel=instance, image=img)

            return redirect('list_hotel')
        
        else:
            print(forms.errors)
            context = {
                    'form': forms,
                    'existing_images': instance.images.all() if instance else None

                }
            return render(request, 'add_hotel.html', context)
        
    else:

        forms = hotel_Form(instance=instance)

        context = { 
                
                'form': forms, 
                'existing_images': instance.images.all() if instance else None
        }

        return render(request, 'add_hotel.html', context)

        

@login_required(login_url='login_admin')
def delete_hotel(request, hotel_id):

    hotel.objects.get(id=hotel_id).delete()

    return HttpResponseRedirect(reverse('list_hotel'))


from django.db.models import Prefetch

@login_required(login_url='login_admin')
def list_hotel(request):

    data = hotel.objects.prefetch_related(
        Prefetch('rooms', queryset=hotel_rooms.objects.select_related('room_type').prefetch_related('room_amenities'))
    )
    context = {
        'data': data
    }
    return render(request, 'list_hotel.html', context)


@login_required(login_url='login_admin')
def delete_hotel_image(request, image_id):
    image = get_object_or_404(HotelImage, id=image_id)

    hotel_id = image.hotel.id  # To redirect back to edit page
    image.delete()

    print('-----------------------------------------')

    print(hotel_id)


    return redirect('update_hotel', hotel_id=hotel_id)



@login_required(login_url='login_admin')
def add_hotel_rooms(request):

    if request.method == 'POST':

        form = hotel_rooms_Form(request.POST, request.FILES)
        
        if form.is_valid():
             # Assign the user here
            instance = form.save()
            form.save_m2m()  # Save the many-to-many relationships
            
            for img in request.FILES.getlist('image'):
                HotelImage.objects.create(hotel=instance, image=img)
            
            return redirect('list_hotel_rooms')
        
        else:
            print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'add_hotel_rooms.html', context)
        
    else:

        form = hotel_rooms_Form()

        return render(request, 'add_hotel_rooms.html', {'form': form})

        

@login_required(login_url='login_admin')
def update_hotel_rooms(request, hotel_rooms_id):
    instance = get_object_or_404(hotel_rooms, id=hotel_rooms_id)

    if request.method == 'POST':
        form = hotel_rooms_Form(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            room = form.save(commit=False)
            room.save()
            form.save_m2m()

            for img in request.FILES.getlist('image'):
                hotel_roomsImage.objects.create(hotel_rooms=room, image=img)

            return redirect('list_hotel_rooms')
        else:
            print(form.errors)
    else:
        form = hotel_rooms_Form(instance=instance)

    context = {
        'form': form,
        'existing_images': instance.images.all() if instance else None
    }
    return render(request, 'add_hotel_rooms.html', context)
        

@login_required(login_url='login_admin')
def delete_hotel_rooms(request, hotel_rooms_id):

    hotel_rooms.objects.get(id=hotel_rooms_id).delete()

    return HttpResponseRedirect(reverse('list_hotel_rooms'))


@login_required(login_url='login_admin')
def delete_hotel_room_image(request, image_id):
    image = get_object_or_404(hotel_roomsImage, id=image_id)

    hotel_rooms_id = image.hotel_rooms.id  # To redirect back to edit page
    image.delete()

    print('-----------------------------------------')

    print(hotel_rooms_id)


    return redirect('update_hotel_rooms', hotel_rooms_id=hotel_rooms_id)


@login_required(login_url='login_admin')
def list_hotel_rooms(request):

    data = hotel_rooms.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_hotel_rooms.html', context)


from customer.models import *

@login_required(login_url='login_admin')
def list_hotel_bookings(request):
    queryset = HotelBooking.objects.all() if request.user.is_superuser else HotelBooking.objects.filter(hotel__user=request.user)

    filterset = HotelBookingFilter(request.GET, queryset=queryset, request = request)
    filtered_bookings = filterset.qs

    total_earning = filtered_bookings.aggregate(total=Sum('hotel_earning'))['total'] or 0

    context = {
        'data': filtered_bookings,
        'filterset': filterset,
        'total_earning': total_earning,
    }
    return render(request, 'list_hotel_bookings.html', context)




from customer.forms import *

@login_required(login_url='login_admin')
def update_hotel_bookings(request, booking_id):

    if request.user.is_superuser:
        
        instance = HotelBooking.objects.get(id = booking_id)

    else:

        instance = HotelBooking.objects.get(hotel__user = request.user, id = booking_id)

    if request.method == 'POST':

        print('--------------------')

        form = HotelBookingStatusForm(request.POST, instance=instance)

        print('--------------------')

        if form.is_valid():
            form.save()
            print('--------------------')


            return redirect('list_hotel_bookings')
        
        else:

            print('------12--------------')


            print(form.errors)
            context = {
            
                'form' : form
            }
            return render(request, 'update_hotel_bookings.html', context)

    
    else:


        form = HotelBookingStatusForm(instance = instance)

        context = {
        
            'form' : form
        }
        return render(request, 'update_hotel_bookings.html', context)




from django.db.models import Sum

from .filter import *

@login_required(login_url='login_admin')
def list_hotel_earning(request):
    
    queryset = HotelBooking.objects.all() if request.user.is_superuser else HotelBooking.objects.filter(hotel__user=request.user)

    filterset = HotelBookingFilter(request.GET, queryset=queryset, request = request)
    filtered_bookings = filterset.qs

    total_earning = filtered_bookings.aggregate(total=Sum('hotel_earning'))['total'] or 0

    context = {
        'data': filtered_bookings,
        'filterset': filterset,
        'total_earning': total_earning,
    }
    return render(request, 'list_hotel_earning.html', context)



# from django.shortcuts import get_object_or_404
# from django.template.loader import render_to_string
# from django.http import HttpResponse
# from xhtml2pdf import pisa
# import io

# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from reportlab.platypus import Table, TableStyle
# import io
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from reportlab.platypus import Table, TableStyle
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from django.template.loader import render_to_string
# import io

import tempfile
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse  # optional, if returning a JSON response
from django.conf import settings  #

from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.mail import EmailMessage
from django.http import JsonResponse
import tempfile
from hotel.models import HotelBooking  # adjust this to your model

def render_pdf_view(request, booking_id):
    booking = HotelBooking.objects.get(id=booking_id)

    # Render HTML template
    html_string = render_to_string('from_owner_to_hotel_invoice.html', {'booking': booking, 'request': request})

    # Generate PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(temp_pdf.name)
        temp_pdf.seek(0)

        # Send email with attachment
        email = EmailMessage(
            subject="Booking Invoice",
            body="Attached is the invoice for your booking.",
            from_email="no-reply@yourdomain.com",
            to=['pratikgosavi654@gmail.com'],  # or any recipient
        )
        email.attach(f"invoice_{booking_id}.pdf", temp_pdf.read(), "application/pdf")
        email.send()

    return JsonResponse({'message': 'Invoice sent successfully'})




    # booking = get_object_or_404(HotelBooking, id=booking_id)
    # buffer = io.BytesIO()
    # pdf = canvas.Canvas(buffer, pagesize=A4)
    # width, height = A4

    # net_amount = booking.total_amount - booking.hotel_earning
    #   # Draw logo image (update the path to your actual logo file)
    # pdf.drawImage("static/images/rabitlogo.png.", x=50, y=770, width=120, height=40)
    # y = height - 80
     
    # pdf.setStrokeColor(colors.HexColor("#cccccc"))  # Light grey
    # pdf.line(50, y - 4, width - 50, y - 4)
    # pdf.setLineWidth(1)
    
    # # Header
    # pdf.setFont("Times-Bold", 16)
    # pdf.setFillColor(colors.black)
    # pdf.drawRightString(width - 50, height - 50, f"{booking.hotel.name}")
    # pdf.setFont("Times-Roman", 12)

    # pdf.drawRightString(width - 50, height - 65, f"{booking.hotel.city.name}, India")

    # y = height - 100

    # # Section: Primary Guest Details
    # pdf.setFont("Times-Bold", 12)
    # pdf.drawString(50, y, "PRIMARY GUEST DETAILS")
    # pdf.setStrokeColor(colors.HexColor("#cccccc"))  # Light grey
    # pdf.setLineWidth(0.5)  # Thinner line
    # pdf.line(50, y - 4, width - 50, y - 4)
    # pdf.setLineWidth(1)  # Optional: reset if needed later

    # y -= 20
    # pdf.setFont("Times-Roman", 12)
    # pdf.drawString(50, y, f"👤 {booking.first_name} {booking.last_name}")
    # y -= 15
    # pdf.drawString(50, y, f"Check-in: {booking.check_in}")
    # y -= 15
    # pdf.drawString(50, y, f"Check-out: {booking.check_out}")
    # y -= 15
    # pdf.drawString(50, y, f"Total Guests: {booking.guest_count}")

    # # Booking Info
    # y -= 30
    # pdf.setFont("Times-Bold", 12)
    # pdf.drawString(50, y, "BOOKING INFO")
    # pdf.setStrokeColor(colors.HexColor("#cccccc"))  # Light grey
    # pdf.setLineWidth(0.5)  # Thinner line
    # pdf.line(50, y - 4, width - 50, y - 4)
    # pdf.setLineWidth(1)  # Optional: reset if needed later

    # y -= 20
    # pdf.setFont("Times-Roman", 12)
    # pdf.drawString(50, y, f"Booking ID: {booking.id}")
    # pdf.drawString(250, y, f"Status: {booking.status}")
    # y -= 15
    # pdf.drawString(50, y, f"Booked on: {booking.created_at.strftime('%b %d, %Y, %I:%M %p')}")
    # pdf.drawString(250, y, "Payment: Paid Online")

    # # Room Details
    # y -= 30
    # pdf.setFont("Times-Bold", 12)
    # pdf.drawString(50, y, "ROOM DETAILS")
    # pdf.setStrokeColor(colors.HexColor("#cccccc"))  # Light grey
    # pdf.setLineWidth(0.5)  # Thinner line
    # pdf.line(50, y - 4, width - 50, y - 4)
    # pdf.setLineWidth(1)  # Optional: reset if needed later

    # y -= 20
    # pdf.setFont("Times-Roman", 12)
    # pdf.drawString(50, y, f"Room: {booking.room.room_type}")
    # y -= 15
    # pdf.drawString(50, y, f"Inclusions: {booking.special_request or 'Room Only'}")
    # y -= 15
    # pdf.drawString(50, y, "Cancellation Policy: This is a non-refundable, non-amendable tariff.")

    # # Payment
    # y -= 30
    # pdf.setFont("Times-Bold", 12)
    # pdf.drawString(50, y, "PAYMENT")
    # pdf.setStrokeColor(colors.HexColor("#cccccc"))  # Light grey
    # pdf.setLineWidth(0.5)  # Thinner line
    # pdf.line(50, y - 4, width - 50, y - 4)
    # pdf.setLineWidth(1)  # Optional: reset if needed later

    # y -= 20
    # pdf.setFont("Times-Roman", 12)
    # pdf.drawString(50, y, f"Property Gross Charges: ₹ {booking.total_amount:.2f}")
    # pdf.drawString(300, y, f"Payable to Property: ₹ {booking.hotel_earning:.2f}")

    # # Table
    # y -= 40
    # pdf.setFont("Times-Bold", 12)
    # pdf.drawString(50, y, "ROOM WISE PAYMENT BREAKUP (in ₹)")
    # pdf.setStrokeColor(colors.HexColor("#cccccc"))  # Light grey
    # pdf.setLineWidth(0.5)  # Thinner line
    # pdf.line(50, y - 4, width - 50, y - 4)
    # pdf.setLineWidth(1)  # Optional: reset if needed later

    # y -= 20

    # from reportlab.platypus import SimpleDocTemplate
    # table_data = [
    #     ["Date", "Room Charges", "Extra Adult/Child", "Taxes", "Gross Charges", "Commission", "Net Rate"],
    #     [str(booking.check_in),
    #      f"{booking.base_amount:.2f}",
    #      "0.00",
    #      f"{booking.gst_amount:.2f}",
    #      f"{booking.total_amount:.2f}",
    #      f"{booking.total_amount - booking.hotel_earning:.2f}",
    #      f"{booking.hotel_earning:.2f}"]
    # ]
    # t = Table(table_data, colWidths=[75]*7)
    # t.setStyle(TableStyle([
    # ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
    # ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    # ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
    # ('FONTSIZE', (0, 0), (-1, -1), 9),
    # ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # header
    # ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),  # numeric alignment
    # ('LINEBELOW', (0, 0), (-1, 0), 1, colors.grey),
    # ('LINEBELOW', (0, -1), (-1, -1), 1, colors.lightgrey),
    # ('GRID', (0, 1), (-1, -1), 0.3, colors.HexColor("#dddddd")),
    # ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    # ('TOPPADDING', (0, 0), (-1, -1), 6),
    # ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    # ]))

    # t.wrapOn(pdf, width, height)
    # t.drawOn(pdf, 50, y - 50)

    # # Final Calculation
    # y -= 130
    # pdf.setFont("Times-Bold", 12)
    # pdf.drawString(50, y, "FINAL CALCULATION")
    # pdf.setStrokeColor(colors.HexColor("#cccccc"))  # Light grey
    # pdf.setLineWidth(0.5)  # Thinner line
    # pdf.line(50, y - 4, width - 50, y - 4)
    # pdf.setLineWidth(1)  # Optional: reset if needed later

    # y -= 20
    # pdf.setFont("Times-Roman", 12)
    # pdf.drawString(50, y, f"1. Room Charges: ₹ {booking.base_amount:.2f}")
    # y -= 15
    # pdf.drawString(50, y, f"2. Extra Adult/Child Charges: ₹ 0.00")
    # y -= 15
    # pdf.drawString(50, y, f"3. Property Taxes: ₹ {booking.gst_amount:.2f}")
    # y -= 15
    # pdf.drawString(50, y, f"4. Service Charges: ₹ 0.00")
    # y -= 20
    # pdf.setFont("Times-Bold", 10)
    # pdf.drawString(50, y, f"(A) Property Gross Charges: ₹ {booking.total_amount:.2f}")

    # pdf.showPage()
    # pdf.save()
    # buffer.seek(0)
    # return HttpResponse(buffer, content_type='application/pdf')
