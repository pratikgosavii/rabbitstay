from django.shortcuts import render

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


@login_required(login_url='login_admin')
def list_hotel(request):

    data = hotel.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_hotel.html', context)




