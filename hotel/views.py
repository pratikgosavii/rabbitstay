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

def render_pdf_view(request, booking_id):
    # booking = get_object_or_404(HotelBooking, id=booking_id)
    # html_string = render_to_string('from_owner_to_hotel_invoice.html', {'booking': booking})

    # result = io.BytesIO()
    # pdf_status = pisa.CreatePDF(src=html_string, dest=result, encoding='UTF-8')

    # if pdf_status.err:
    #     return HttpResponse('PDF generation failed', status=500)

    # response = HttpResponse(result.getvalue(), content_type='application/pdf')
    # response['Content-Disposition'] = f'inline; filename="invoice_{booking_id}.pdf"'
    # return response

    pass
