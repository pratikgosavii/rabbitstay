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
def add_hotel(request):

    if request.method == 'POST':

        form = hotel_Form(request.POST, request.FILES)
        
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.user = request.user  # Assign the user here
            hotel.save()
            form.save_m2m()  # Save the many-to-many relationships
            
            return redirect('list_hotel')
        
        else:
            print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'add_hotel.html', context)
        
    else:

        form = hotel_Form()

        return render(request, 'add_hotel.html', {'form': form})

        

@login_required(login_url='login_admin')
def update_hotel(request, hotel_id):

    if request.method == 'POST':

        instance = hotel.objects.get(id=hotel_id)

        forms = hotel_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_hotel')
        
        else:
            print(forms.errors)
            context = {
                    'form': forms
                }
            return render(request, 'add_hotel.html', context)
        
    else:

        instance = hotel.objects.get(id=hotel_id)
        forms = hotel_Form(instance=instance)

        context = {
            'form': forms
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


@login_required
def add_hotel_vendor(request):
    if request.method == 'POST':
        form = hotel_Form(request.POST, request.FILES)
        if form.is_valid():
            hotel_instance = form.save(commit=False)
            hotel_instance.user = request.user  # Set logged-in user
            hotel_instance.save()
            form.save_m2m()
            return redirect('list_hotel_vendor')
        else:
            print(form.errors)
    else:
        form = hotel_Form()

    return render(request, 'add_hotel.html', {'form': form})


@login_required
def update_hotel_vendor(request, hotel_id):
    instance = get_object_or_404(hotel, id=hotel_id, user=request.user)

    if request.method == 'POST':
        form = hotel_Form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('list_hotel_vendor')
        else:
            print(form.errors)
    else:
        form = hotel_Form(instance=instance)

    return render(request, 'add_hotel.html', {'form': form})


@login_required
def delete_hotel_vendor(request, hotel_id):
    instance = get_object_or_404(hotel, id=hotel_id, user=request.user)
    instance.delete()
    return HttpResponseRedirect(reverse('list_hotel_vendor'))


@login_required
def list_hotel_vendor(request):
    data = hotel.objects.filter(user=request.user).prefetch_related(
        Prefetch('rooms', queryset=hotel_rooms.objects.select_related('room_type').prefetch_related('room_amenities'))
    )
    context = {
        'data': data
    }
    return render(request, 'list_hotel.html', context)



@login_required(login_url='login_admin')
def add_hotel_rooms(request):

    if request.method == 'POST':

        form = hotel_rooms_Form(request.POST, request.FILES)
        
        if form.is_valid():
            hotel_rooms = form.save(commit=False)
            hotel_rooms.user = request.user  # Assign the user here
            hotel_rooms.save()
            form.save_m2m()  # Save the many-to-many relationships
            
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

    if request.method == 'POST':

        instance = hotel_rooms.objects.get(id=hotel_rooms_id)

        forms = hotel_rooms_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_hotel_rooms')
        
        else:
            print(forms.errors)
            context = {
                    'form': forms
                }
            return render(request, 'add_hotel_rooms.html', context)
        
    else:

        instance = hotel_rooms.objects.get(id=hotel_rooms_id)
        forms = hotel_rooms_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_hotel_rooms.html', context)

        

@login_required(login_url='login_admin')
def delete_hotel_rooms(request, hotel_rooms_id):

    hotel_rooms.objects.get(id=hotel_rooms_id).delete()

    return HttpResponseRedirect(reverse('list_hotel_rooms'))


@login_required(login_url='login_admin')
def list_hotel_rooms(request):

    data = hotel_rooms.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_hotel_rooms.html', context)






@login_required(login_url='login_admin')
def add_hotel_rooms_vendor(request):

    if request.method == 'POST':

        form = hotel_rooms_Form(request.POST, request.FILES)
        
        if form.is_valid():
            hotel_rooms = form.save(commit=False)
            hotel_rooms.user = request.user  # Assign the user here
            hotel_rooms.save()
            form.save_m2m()  # Save the many-to-many relationships
            
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
def update_hotel_rooms_vendor(request, hotel_rooms_id):

    if request.method == 'POST':

        instance = hotel_rooms.objects.get(id=hotel_rooms_id)

        forms = hotel_rooms_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_hotel_rooms')
        
        else:
            print(forms.errors)
            context = {
                    'form': forms
                }
            return render(request, 'add_hotel_rooms.html', context)
        
    else:

        instance = hotel_rooms.objects.get(id=hotel_rooms_id)
        forms = hotel_rooms_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_hotel_rooms.html', context)

        

@login_required(login_url='login_admin')
def delete_hotel_rooms_vendor(request, hotel_rooms_id):

    hotel_rooms.objects.get(id=hotel_rooms_id).delete()

    return HttpResponseRedirect(reverse('list_hotel_rooms'))


@login_required(login_url='login_admin')
def list_hotel_rooms_vendor(request):

    data = hotel_rooms.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_hotel_rooms.html', context)




