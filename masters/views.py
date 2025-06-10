from django.shortcuts import render

from masters.filters import EventFilter

# Create your views here.


from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from .serializers import *

from users.permissions import *

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





# @login_required(login_url='login_admin')
# def add_doctor(request):

#     if request.method == 'POST':

#         forms = doctor_Form(request.POST, request.FILES)

#         if forms.is_valid():
#             forms.save()
#             return redirect('list_doctor')
#         else:
#             print(forms.errors)
#             context = {
#                 'form': forms
#             }
#             return render(request, 'add_doctor.html', context)
    
#     else:

#         forms = doctor_Form()

#         context = {
#             'form': forms
#         }
#         return render(request, 'add_doctor.html', context)


# from django.views.decorators.csrf import csrf_exempt

# @login_required(login_url='login_admin')
# @csrf_exempt 
# def add_doctor_json(request):

#     if request.method == 'POST':
#         form = doctor_Form(request.POST, request.FILES)
        
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'status': 'success', 'message': 'Doctor added successfully'}, status=201)
#         else:
#             return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

        

# @login_required(login_url='login_admin')
# def update_doctor(request, doctor_id):

#     if request.method == 'POST':

#         instance = doctor.objects.get(id=doctor_id)

#         print('-------------------')
#         print('-------------------')
#         print('-------------------')
#         print(instance.user)

#         updated_request = request.POST.copy()
#         updated_request.update({'user': instance.user})

#         forms = doctor_Form(updated_request, request.FILES, instance=instance)

#         print(forms.instance.user)

#         if forms.is_valid():
#             forms.save()
#             return redirect('list_doctor')
#         else:
#             print(forms.errors)
    
#     else:

#         instance = doctor.objects.get(id=doctor_id)
#         forms = doctor_Form(instance=instance)

#         context = {
#             'form': forms
#         }
#         return render(request, 'add_doctor.html', context)

        

from django.http import JsonResponse



@login_required(login_url='login_admin')
def add_coupon(request):

    if request.method == 'POST':

        forms = coupon_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_coupon')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_coupon.html', context)
    
    else:

        forms = coupon_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_coupon.html', context)

        

@login_required(login_url='login_admin')
def update_coupon(request, coupon_id):

    if request.method == 'POST':

        instance = coupon.objects.get(id=coupon_id)

        forms = coupon_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_coupon')
        else:
            print(forms.errors)
    
    else:

        instance = coupon.objects.get(id=coupon_id)
        forms = coupon_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_coupon.html', context)

        

@login_required(login_url='login_admin')
def delete_coupon(request, coupon_id):

    coupon.objects.get(id=coupon_id).delete()

    return HttpResponseRedirect(reverse('list_coupon'))


@login_required(login_url='login_admin')
def list_coupon(request):

    data = coupon.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_coupon.html', context)


from django.http import JsonResponse
from .filters import *

class get_coupon(ListAPIView):
    queryset = coupon.objects.all()
    serializer_class = coupon_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields
    filterset_class = couponFilter  # enables filtering on all fields



@login_required(login_url='login_admin')
def add_event(request):

    if request.method == 'POST':

        forms = event_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_event')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_event.html', context)
    
    else:

        forms = event_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_event.html', context)

        

@login_required(login_url='login_admin')
def update_event(request, event_id):

    if request.method == 'POST':

        instance = event.objects.get(id=event_id)

        forms = event_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_event')
        else:
            print(forms.errors)
    
    else:

        instance = event.objects.get(id=event_id)
        forms = event_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_event.html', context)

        

@login_required(login_url='login_admin')
def delete_event(request, event_id):

    event.objects.get(id=event_id).delete()

    return HttpResponseRedirect(reverse('list_event'))


@login_required(login_url='login_admin')
def list_event(request):

    data = event.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_event.html', context)


from django.http import JsonResponse

class get_event(ListAPIView):
    queryset = event.objects.all()
    serializer_class = event_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter  # enables filtering on all fields


    def get_queryset(self):
        return event.objects.filter(start_date__gte=now()).order_by('start_date')


def add_testimonials(request):
    
    if request.method == "POST":

        forms = testimonials_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_testimonials')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_testimonials.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_testimonials.html', { 'form' : testimonials_Form()})

def update_testimonials(request, testimonials_id):
    
    instance = testimonials.objects.get(id = testimonials_id)

    if request.method == "POST":

        forms = testimonials_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_testimonials')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_testimonials.html', context)

    
    else:

        # create first row using admin then editing only

        forms = testimonials_Form(instance=instance)
                
        context = {
            'form': forms
        }
        
        return render(request, 'add_testimonials.html', context)


def list_testimonials(request):

    data = testimonials.objects.all()

    return render(request, 'list_testimonials.html', {'data' : data})


def delete_testimonials(request, testimonials_id):

    data = testimonials.objects.get(id = testimonials_id).delete()

    return redirect('list_testimonials')



from django.views import View


class get_testimonials(ListAPIView):
    queryset = testimonials.objects.all()
    serializer_class = testimonials_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields



def add_food_menu(request):
    
    if request.method == "POST":

        forms = food_menu_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_food_menu')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_food_menu.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_food_menu.html', { 'form' : food_menu_Form()})

def update_food_menu(request, food_menu_id):
    
    instance = food_menu.objects.get(id = food_menu_id)

    if request.method == "POST":

        forms = food_menu_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_food_menu')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_food_menu.html', context)

    
    else:

        # create first row using admin then editing only

        forms = food_menu_Form(instance=instance)
                
        context = {
            'form': forms
        }
        
        return render(request, 'add_food_menu.html', context)


def list_food_menu(request):

    data = food_menu.objects.all()

    return render(request, 'list_food_menu.html', {'data' : data})


def delete_food_menu(request, food_menu_id):

    data = food_menu.objects.get(id = food_menu_id).delete()

    return redirect('list_food_menu')



from django.views import View


class get_food_menu(ListAPIView):
    queryset = food_menu.objects.all()
    serializer_class = food_menu_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = food_menuFilter  # enables filtering on all fields


def add_amenity(request):
    
    if request.method == "POST":

        forms = amenity_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_amenity')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_amenity.html', context)


    else:

        # create first row using admin then editing only

        

        return render(request, 'add_amenity.html', { 'form' : amenity_Form()})

def update_amenity(request, amenity_id):
    
    instance = amenity.objects.get(id = amenity_id)

    if request.method == "POST":

        forms = amenity_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_amenity')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_amenity.html', context)
    
    else:

        # create first row using admin then editing only

        forms = amenity_Form(instance=instance)
        
        context = {
                'form': forms
            }

        return render(request, 'add_amenity.html', forms)


def list_amenity(request):

    data = amenity.objects.all()

    return render(request, 'list_amenity.html', {'data' : data})


def delete_amenity(request, amenity_id):

    data = amenity.objects.get(id = amenity_id).delete()

    return redirect('list_amenity')


from django.views import View



class get_amenity(ListAPIView):
    queryset = amenity.objects.all()
    serializer_class = amenity_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields

def add_room_amenity(request):
    
    if request.method == "POST":

        forms = room_amenity_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_room_amenity')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_room_amenity.html', context)


    else:

        # create first row using admin then editing only

        

        return render(request, 'add_room_amenity.html', { 'form' : room_amenity_Form()})

def update_room_amenity(request, room_amenity_id):
    
    instance = room_amenity.objects.get(id = room_amenity_id)

    if request.method == "POST":

        forms = room_amenity_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_room_amenity')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_room_amenity.html', context)
    
    else:

        # create first row using admin then editing only

        forms = room_amenity_Form(instance=instance)
        
        context = {
                'form': forms
            }

        return render(request, 'add_room_amenity.html', forms)


def list_room_amenity(request):

    data = room_amenity.objects.all()

    return render(request, 'list_room_amenity.html', {'data' : data})


def delete_room_amenity(request, room_amenity_id):

    data = room_amenity.objects.get(id = room_amenity_id).delete()

    return redirect('list_room_amenity')


from django.views import View



class get_room_amenity(ListAPIView):
    queryset = room_amenity.objects.all()
    serializer_class = room_amenity_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields

def add_room_type(request):
    
    if request.method == "POST":

        forms = room_type_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_room_type')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_room_type.html', context)


    else:

        # create first row using admin then editing only

        

        return render(request, 'add_room_type.html', { 'form' : room_type_Form()})

def update_room_type(request, room_type_id):
    
    instance = room_type.objects.get(id = room_type_id)

    if request.method == "POST":

        forms = room_type_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_room_type')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_room_type.html', context)
    
    else:

        # create first row using admin then editing only

        forms = room_type_Form(instance=instance)
        
        context = {
                'form': forms
            }

        return render(request, 'add_room_type.html', forms)


def list_room_type(request):

    data = room_type.objects.all()

    return render(request, 'list_room_type.html', {'data' : data})


def delete_room_type(request, room_type_id):

    data = room_type.objects.get(id = room_type_id).delete()

    return redirect('list_room_type')


from django.views import View



class get_room_type(ListAPIView):
    queryset = room_type.objects.all()
    serializer_class = room_type_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields


def add_product_category(request):
    
    if request.method == "POST":

        forms = product_category_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_product_category')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_product_category.html', context)


    else:

        # create first row using admin then editing only

        

        return render(request, 'add_product_category.html', { 'form' : product_category_Form()})

def update_product_category(request, product_category_id):
    
    instance = product_category.objects.get(id = product_category_id)

    if request.method == "POST":

        forms = product_category_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_product_category')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_product_category.html', context)
    
    else:

        # create first row using admin then editing only

        forms = product_category_Form(instance=instance)

        return render(request, 'add_product_category.html', {'form' : forms})


def list_product_category(request):

    data = product_category.objects.all()

    return render(request, 'list_product_category.html', {'data' : data})


def delete_product_category(request, product_category_id):

    data = product_category.objects.get(id = product_category_id).delete()

    return redirect('list_product_category')


from django.views import View



class get_product_category(ListAPIView):
    queryset = product_category.objects.all()
    serializer_class = product_category_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = product_categoryFilter
    


from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

 
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser



class customer_address_ViewSet(ModelViewSet):

    permission_classes = [IsCustomer]

    serializer_class = customer_address_serializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsCustomer]  # Or use IsAuthenticated if needed

    def get_queryset(self):
        return customer_address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        

def update_customer_address(request, customer_address_id):
    
    instance = customer_address.objects.get(id = customer_address_id)

    if request.method == "POST":

        forms = customer_address_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_customer_address')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_customer_address.html', context)
    
    else:

        # create first row using admin then editing only

        forms = customer_address_Form(instance=instance)
        
        context = {
                'form': forms
            }

        return render(request, 'add_customer_address.html', context)


def list_customer_address(request):

    data = customer_address.objects.all()

    return render(request, 'list_customer_address.html', {'data' : data})


def delete_customer_address(request, customer_address_id):

    data = customer_address.objects.get(id = customer_address_id).delete()

    return redirect('list_customer_address')


from django.views import View



class get_customer_address(ListAPIView):
    queryset = customer_address.objects.all()
    serializer_class = customer_address_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields

    def get_queryset(self):
        return customer_address.objects.filter(user=self.request.user)

def add_symptom(request):
    
    if request.method == "POST":

        forms = symptom_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_symptom')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_symptom.html', context)


    else:

        # create first row using admin then editing only

        

        return render(request, 'add_symptom.html', { 'form' : symptom_Form()})

def update_symptom(request, symptom_id):
    
    instance = symptom.objects.get(id = symptom_id)

    if request.method == "POST":

        forms = symptom_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_symptom')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_symptom.html', context)
    
    else:

        # create first row using admin then editing only

        forms = symptom_Form(instance=instance)

        context = {
            'form': forms
        }

        return render(request, 'add_symptom.html', context)


def list_symptom(request):

    data = symptom.objects.all()

    return render(request, 'list_symptom.html', {'data' : data})


def delete_symptom(request, symptom_id):

    data = symptom.objects.get(id = symptom_id).delete()

    return redirect('list_symptom')


class get_symptom(ListAPIView):
    queryset = symptom.objects.all()
    serializer_class = symptom_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields
    filterset_class = symptomFilter  # enables filtering on all fields




def add_service_category(request):
    
    if request.method == "POST":

        forms = service_category_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_service_category')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services_category.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_services_category.html', { 'form' : service_category_Form()})

def update_service_category(request, service_category_id):
    
    instance = service_category.objects.get(id = service_category_id)

    if request.method == "POST":

        forms = service_category_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_service_category')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services_category.html', context)

    
    else:

        # create first row using admin then editing only
        
        forms = service_category_Form(instance=instance)

        context = {
            'form': forms
        }

        return render(request, 'add_services_category.html', context)


def list_service_category(request):

    data = service_category.objects.all()

    return render(request, 'list_services_category.html', {'data' : data})


def delete_service_category(request, service_category_id):

    data = service_category.objects.get(id = service_category_id).delete()

    return redirect('list_service_category')


class get_service_category(ListAPIView):
    queryset = service_category.objects.all()
    serializer_class = service_category_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = service_categoryFilter  # enables filtering on all fields



def add_service_subcategory(request):
    
    if request.method == "POST":

        forms = service_subcategory_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_service_subcategory')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services_subcategory.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_services_subcategory.html', { 'form' : service_subcategory_Form()})

def update_service_subcategory(request, service_subcategory_id):
    
    instance = service_subcategory.objects.get(id = service_subcategory_id)

    if request.method == "POST":

        forms = service_subcategory_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_services_subcategory')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services_subcategory.html', context)

    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_services_subcategory.html', {'data' : instance})


def list_service_subcategory(request):

    data = service_subcategory.objects.all()

    return render(request, 'list_services_subcategory.html', {'data' : data})


def delete_service_subcategory(request, service_subcategory_id):

    data = service_subcategory.objects.get(id = service_subcategory_id).delete()

    return redirect('list_service_subcategory')



class get_service_subcategory(ListAPIView):
    queryset = service_subcategory.objects.all()
    serializer_class = service_subcategory_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields



def add_service(request):
    
    if request.method == "POST":

        forms = service_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_service')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_services.html', { 'form' : service_Form()})

def update_service(request, service_id):
    
    instance = service.objects.get(id = service_id)

    if request.method == "POST":

        forms = service_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_service')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_services.html', context)

    
    else:

        # create first row using admin then editing only

        forms = service_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_services.html', context)


def list_service(request):

    data = service.objects.all()

    return render(request, 'list_services.html', {'data' : data})


def delete_service(request, service_id):

    data = service.objects.get(id = service_id).delete()

    return redirect('list_service')


class get_service(ListAPIView):
  
    
    queryset = service.objects.all()
    serializer_class = service_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = serviceFilter  # enables filtering on all fields


from django_filters.rest_framework import DjangoFilterBackend


@login_required(login_url='login_admin')
def add_test(request):

    if request.method == 'POST':

        forms = test_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_test')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_test.html', context)
    
    else:

        forms = test_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_test.html', context)

        

@login_required(login_url='login_admin')
def update_test(request, test_id):

    if request.method == 'POST':

        instance = test.objects.get(id=test_id)

        forms = test_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_test')
        else:
            print(forms.errors)
    
    else:

        instance = test.objects.get(id=test_id)
        forms = test_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_test.html', context)

        

@login_required(login_url='login_admin')
def delete_test(request, test_id):

    test.objects.get(id=test_id).delete()

    return HttpResponseRedirect(reverse('list_test'))


@login_required(login_url='login_admin')
def list_test(request):

    data = test.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_test.html', context)


from django.http import JsonResponse


class get_test(ListAPIView):
    queryset = test.objects.all()
    serializer_class = test_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = testFilter  # enables filtering on all fields


@login_required(login_url='login_admin')
def add_dog_breed(request):

    if request.method == 'POST':

        forms = dog_breed_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_dog_breed')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_dog_breed.html', context)
    
    else:

        forms = dog_breed_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_dog_breed.html', context)

        

@login_required(login_url='login_admin')
def update_dog_breed(request, dog_breed_id):

    if request.method == 'POST':

        instance = dog_breed.objects.get(id=dog_breed_id)

        forms = dog_breed_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_dog_breed')
        else:
            print(forms.errors)
    
    else:

        instance = dog_breed.objects.get(id=dog_breed_id)
        forms = dog_breed_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_dog_breed.html', context)

        

@login_required(login_url='login_admin')
def delete_dog_breed(request, dog_breed_id):

    dog_breed.objects.get(id=dog_breed_id).delete()

    return HttpResponseRedirect(reverse('list_dog_breed'))


@login_required(login_url='login_admin')
def list_dog_breed(request):

    data = dog_breed.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_dog_breed.html', context)


from django.http import JsonResponse



class get_dog_breed(ListAPIView):
    queryset = dog_breed.objects.all()
    serializer_class = dog_breed_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields

@login_required(login_url='login_admin')
def add_cat_breed(request):

    if request.method == 'POST':

        forms = cat_breed_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_cat_breed')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_cat_breed.html', context)
    
    else:

        forms = cat_breed_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_cat_breed.html', context)

        

@login_required(login_url='login_admin')
def update_cat_breed(request, cat_breed_id):

    if request.method == 'POST':

        instance = cat_breed.objects.get(id=cat_breed_id)

        forms = cat_breed_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_cat_breed')
        else:
            print(forms.errors)
    
    else:

        instance = cat_breed.objects.get(id=cat_breed_id)
        forms = cat_breed_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_cat_breed.html', context)

        

@login_required(login_url='login_admin')
def delete_cat_breed(request, cat_breed_id):

    cat_breed.objects.get(id=cat_breed_id).delete()

    return HttpResponseRedirect(reverse('list_cat_breed'))


@login_required(login_url='login_admin')
def list_cat_breed(request):

    data = cat_breed.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_cat_breed.html', context)


from django.http import JsonResponse



class get_cat_breed(ListAPIView):
    queryset = cat_breed.objects.all()
    serializer_class = cat_breed_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields


@login_required(login_url='login_admin')
def add_product(request):

    if request.method == 'POST':

        forms = product_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_product')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_product.html', context)
    
    else:

        forms = product_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_product.html', context)

        

@login_required(login_url='login_admin')
def update_product(request, product_id):

    if request.method == 'POST':

        instance = product.objects.get(id=product_id)

        forms = product_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_product')
        else:
            print(forms.errors)
    
    else:

        instance = product.objects.get(id=product_id)
        forms = product_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_product.html', context)

        

@login_required(login_url='login_admin')
def delete_product(request, product_id):

    product.objects.get(id=product_id).delete()

    return HttpResponseRedirect(reverse('list_product'))


@login_required(login_url='login_admin')
def list_product(request):

    data = product.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_product.html', context)


from django.http import JsonResponse


class get_product(ListAPIView):
    queryset = product.objects.all()
    serializer_class = product_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields
    filterset_class = productFilter  # enables filtering on all fields

@login_required(login_url='login_admin')
def add_consultation_type(request):

    if request.method == 'POST':

        forms = consultation_type_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_consultation_type')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_consultation_type.html', context)
    
    else:

        forms = consultation_type_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_consultation_type.html', context)

        

@login_required(login_url='login_admin')
def update_consultation_type(request, consultation_type_id):

    if request.method == 'POST':

        instance = consultation_type.objects.get(id=consultation_type_id)

        forms = consultation_type_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_consultation_type')
        else:
            print(forms.errors)
    
    else:

        instance = consultation_type.objects.get(id=consultation_type_id)
        forms = consultation_type_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_consultation_type.html', context)

        

@login_required(login_url='login_admin')
def delete_consultation_type(request, consultation_type_id):

    consultation_type.objects.get(id=consultation_type_id).delete()

    return HttpResponseRedirect(reverse('list_consultation_type'))


@login_required(login_url='login_admin')
def list_consultation_type(request):

    data = consultation_type.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_consultation_type.html', context)


from django.http import JsonResponse


class get_consultation_type(ListAPIView):
    queryset = consultation_type.objects.all()
    serializer_class = consultation_type_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields
    filterset_class = consultation_typeFilter  # enables filtering on all fields

@login_required(login_url='login_admin')
def add_online_consultation_type(request):

    if request.method == 'POST':

        forms = online_consultation_type_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_online_consultation_type')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_online_consultation_type.html', context)
    
    else:

        forms = online_consultation_type_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_online_consultation_type.html', context)

        

@login_required(login_url='login_admin')
def update_online_consultation_type(request, online_consultation_type_id):

    if request.method == 'POST':

        instance = online_consultation_type.objects.get(id=online_consultation_type_id)

        forms = online_consultation_type_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_online_consultation_type')
        else:
            print(forms.errors)
    
    else:

        instance = online_consultation_type.objects.get(id=online_consultation_type_id)
        forms = online_consultation_type_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_online_consultation_type.html', context)

        

@login_required(login_url='login_admin')
def delete_online_consultation_type(request, online_consultation_type_id):

    online_consultation_type.objects.get(id=online_consultation_type_id).delete()

    return HttpResponseRedirect(reverse('list_online_consultation_type'))


@login_required(login_url='login_admin')
def list_online_consultation_type(request):

    data = online_consultation_type.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_online_consultation_type.html', context)


from django.http import JsonResponse


class get_online_consultation_type(ListAPIView):
    queryset = online_consultation_type.objects.all()
    serializer_class = online_consultation_type_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields
    filterset_class = online_consultation_typeFilter  # enables filtering on all fields


@login_required(login_url='login_admin')
def add_vaccination(request):

    if request.method == 'POST':

        forms = vaccination_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_vaccination')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_vaccination.html', context)
    
    else:

        forms = vaccination_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_vaccination.html', context)

        

@login_required(login_url='login_admin')
def update_vaccination(request, vaccination_id):

    if request.method == 'POST':

        instance = vaccination.objects.get(id=vaccination_id)

        forms = vaccination_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_vaccination')
        else:
            print(forms.errors)
    
    else:

        instance = vaccination.objects.get(id=vaccination_id)
        forms = vaccination_Form(instance=instance)

        context = {
            'form': forms
        }
        
        return render(request, 'add_vaccination.html', context)

        

@login_required(login_url='login_admin')
def delete_vaccination(request, vaccination_id):

    vaccination.objects.get(id=vaccination_id).delete()

    return HttpResponseRedirect(reverse('list_vaccination'))


@login_required(login_url='login_admin')
def list_vaccination(request):

    data = vaccination.objects.all()

    print(data)


    context = {
        'data': data
    }
    return render(request, 'list_vaccination.html', context)


from django.http import JsonResponse


class get_vaccination(ListAPIView):
    queryset = vaccination.objects.all()
    serializer_class = vaccination_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields





def add_home_banner(request):
    
    if request.method == "POST":

        forms = home_banner_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_home_banner')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }

            return render(request, 'add_home_banner.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_home_banner.html', { 'form' : home_banner_Form()})

def update_home_banner(request, home_banner_id):
    
    instance = home_banner.objects.get(id = home_banner_id)

    if request.method == "POST":


        instance = home_banner.objects.get(id=home_banner_id)

        forms = home_banner_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_home_banner')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }

            return render(request, 'add_home_banner.html', context)

    
    else:

        # create first row using admin then editing only

        forms = home_banner_Form(instance=instance)
                
        context = {
            'form': forms
        }

        return render(request, 'add_home_banner.html', context)


def list_home_banner(request):

    data = home_banner.objects.all()

    return render(request, 'list_home_banner.html', {'data' : data})


def delete_home_banner(request, home_banner_id):

    data = home_banner.objects.get(id = home_banner_id).delete()

    return redirect('list_home_banner')


from django.views import View

def get_home_banner(request):
  
    filtered_qs = home_bannerFilter(request.GET, queryset=home_banner.objects.all()).qs

    serialized_data = HomeBannerSerializer(filtered_qs, many=True, context={'request': request}).data
    return JsonResponse({"data": serialized_data}, status=200)


