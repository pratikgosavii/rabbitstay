from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import *


# def login_page(request):
#     forms = LoginForm()
#     if request.method == 'POST':
#         forms = LoginForm(request.POST)
#         if forms.is_valid():
#             username = forms.cleaned_data['username']
#             password = forms.cleaned_data['password']
#             print(username)
#             print(password)
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)

#                 if user.is_doctor:
#                     print('---------------------------------')
#                     print('---------------------------------')
#                     print('---------------------------------')
#                 return redirect('dashboard')
#             else:
#                 messages.error(request, 'wrong username password')
#     context = {'form': forms}
#     return render(request, 'adminLogin.html', context)

from firebase_admin import auth as firebase_auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import  User  # Your custom user model


class SignupView(APIView):

    def post(self, request):
        id_token = request.data.get("idToken")
        user_type = request.data.get("user_type")
        name = request.data.get("name")
        email = request.data.get("email")

        if not id_token or not user_type:
            return Response({"error": "idToken and user_type are required"}, status=400)

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            mobile = decoded_token.get("phone_number")
            uid = decoded_token.get("uid")

            if not mobile:
                return Response({"error": "Phone number not found in Firebase token"}, status=400)

            # Role flags
            role_flags = {
                "is_customer": False,
                "is_doctor": False,
                "is_daycare": False,
                "is_service_provider": False
            }

            if f"is_{user_type}" not in role_flags:
                return Response({"error": "Invalid user_type"}, status=400)

            user = User.objects.filter(mobile=mobile).first()
            created = False

            if user:
                # Already exists – check role
                existing_roles = [key for key, value in {
                    "customer": user.is_customer,
                    "doctor": user.is_doctor,
                    "daycare": user.is_daycare,
                    "service_provider": user.is_service_provider
                }.items() if value]

                if existing_roles and user_type not in existing_roles:
                    return Response({
                        "error": f"This number is already registered as a {existing_roles[0]}. Cannot register again as {user_type}."
                    }, status=400)

                if user.firebase_uid != uid:
                    user.firebase_uid = uid
                    user.save()

            else:
                role_flags[f"is_{user_type}"] = True

                # Ensure email is unique
                if email and User.objects.filter(email=email).exists():
                    return Response({"error": "This email is already in use."}, status=400)

                user = User.objects.create(
                    mobile=mobile,
                    firebase_uid=uid,
                    first_name=name or "",
                    email=email or decoded_token.get("email", ""),
                    **role_flags
                )
                created = True

            # Create wallet if not customer
            wallet_amount = None
           
              
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "mobile": user.mobile,
                    "email": user.email,
                    "name": f"{user.first_name or ''} {user.last_name or ''}".strip(),
                    "user_type": (
                        "doctor" if user.is_doctor else
                        "daycare" if user.is_daycare else
                        "customer" if user.is_customer else
                        "service_provider" if user.is_service_provider else
                        "unknown"
                    ),
                    "created": created
                }
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class LoginAPIView(APIView):

    def post(self, request):
        id_token = request.data.get("idToken")

        if not id_token:
            return Response({"error": "id_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token["uid"]
            phone_number = decoded_token.get("phone_number")
            email = decoded_token.get("email")

            if not phone_number:
                return Response({"error": "Phone number not found in token"}, status=400)

            user = User.objects.filter(mobile=phone_number).first()
            created = False

            if user:
                if user.firebase_uid != uid:
                    user.firebase_uid = uid
                    user.save()

                refresh = RefreshToken.for_user(user)

                # Include wallet amount only for non-customer
               
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "mobile": user.mobile,
                        "email": user.email,
                        "user_type": (
                            "doctor" if user.is_doctor else
                            "daycare" if user.is_daycare else
                            "customer" if user.is_customer else
                            "service_provider" if user.is_service_provider else
                            "unknown"
                        ),
                        "name": f"{user.first_name or ''} {user.last_name or ''}".strip(),
                        "created": created
                    }
                })

            else:
                return Response({"error": "no user found, try to signup"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        





from .permissions import *


class UsergetView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        user = request.user
        return Response({
            "name": user.first_name,
            "email": user.email,
        })

class UserUpdateView(APIView):
    permission_classes = [IsCustomer]

    def put(self, request):
        user = request.user
        name = request.data.get("name")
        email = request.data.get("email")

        updated = False

        if name:
            user.first_name = name
            updated = True

        if email:
            user.email = email
            updated = True

        if updated:
            user.save()
            return Response({"message": "Profile updated successfully."})
        else:
            return Response({"message": "No changes provided."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        id_token = request.data.get("idToken")
        new_password = request.data.get("new_password")

        if not id_token or not new_password:
            return Response({"error": "idToken and new_password are required"}, status=400)

        try:
            # Decode the token to get UID
            decoded = firebase_auth.verify_id_token(id_token)
            uid = decoded.get("uid")

            # Update Firebase password
            firebase_auth.update_user(uid, password=new_password)

            return Response({"message": "Password updated successfully."})

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        



def login_admin(request):

    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data['email']
            password = forms.cleaned_data['password']
            print(email)
            print(password)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'adminLogin.html', {'error': 'Invalid email or password'})
            
            if user:
                if user.check_password(password):
                    if user.is_superuser:
                        login(request, user)
                        return redirect('dashboard')
                    else:
                        messages.error(request, 'You are not superuser')
                        context = {'form': forms}
                        return render(request, 'adminLogin.html', context)
                else:
                    return render(request, 'adminLogin.html', {'error': 'Invalid email or password'})

            else:
                messages.error(request, 'wrong username password')
    context = {'form': forms}
    return render(request, 'adminLogin.html', context)

import firebase_admin
from firebase_admin import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json




def register_vendor(request):

    if request.method == 'POST':

        print('----------------------')


        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([first_name, last_name, email, mobile, password, confirm_password]):
            return render(request, 'vendor_register.html', {'error': 'All fields are required.'})

        if password != confirm_password:
            return render(request, 'vendor_register.html', {'error': 'Passwords do not match.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'vendor_register.html', {'error': 'Email already registered.'})

        if User.objects.filter(mobile=mobile).exists():
            return render(request, 'vendor_register.html', {'error': 'Mobile number already registered.'})

        print(request.POST)
        # Create the user
        user = User.objects.create_user(
            email=email,
            mobile=mobile,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_service_provider=True
        )

        login(request, user)
        return redirect('vendor_dashboard')

    return render(request, 'vendor_register.html')
        

def login_vendor(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password')
                return render(request, 'vendorLogin.html', {'form': form})

            if user.check_password(password):
                if user.is_service_provider:
                    login(request, user)

                    print('------------------')

                    print(request.user)


                    
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Access denied: not a service provider')
            else:
                messages.error(request, 'Invalid email or password')

    return render(request, 'vendorLogin.html', {'form': form})


# def resgister_page(request):

#     forms = registerForm()
#     if request.method == 'POST':
#         forms = registerForm(request.POST)
#         if forms.is_valid():
#             forms.save()
#             username = forms.cleaned_data['username']
#             password = forms.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             if user:
                
#                 messages.error(request, 'user already exsist')
#                 return redirect('dashboard')
#             else:
#                 return redirect('resgister')
#         else:
#             print(forms.errors)
#     else:
#         print(forms.as_p)

#         context = {'form': forms}

#         return render(request, 'users/resgister.html', context)


def logout_page(request):
    logout(request)
    return redirect('login_admin')

def customer_user_list(request):

    data = User.objects.all()

    return render(request, 'user_list.html', { 'data' : data})

def provider_user_list(request):

    data = User.objects.all()

    return render(request, 'user_list.html', { 'data' : data})




def user_booking_history(request, user_id):

    data = User.objects.all()

    return render(request, 'user_booking_history.html', { 'data' : data})

def hotel_booking_history(request, user_id):

    data = User.objects.all()

    return render(request, 'hotel_booking_history.html', { 'data' : data})
