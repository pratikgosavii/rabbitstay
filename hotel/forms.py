from django import forms
from .models import *
from masters.models import *

class hotel_Form(forms.ModelForm):
   
    amenities = forms.ModelMultipleChoiceField(
        queryset=amenity.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select select2',
            'id': 'id_amenities'
        }),
        required=False
    )

    class Meta:
        model = hotel
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'no_of_rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'star_rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'overall_rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'profit_margin': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # ✅ GST Fields
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 29ABCDE1234F2Z5'}),
            'gst_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),

            # ✅ PAN Field
            'pan_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),

            # ✅ Bank Fields
            'account_holder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




class hotel_rooms_Form(forms.ModelForm):

    room_amenities = forms.ModelMultipleChoiceField(
    queryset=room_amenity.objects.all(),
    widget=forms.SelectMultiple(attrs={
        'class': 'form-select select2',  # important class!
        'id': 'id_room_amenities'
    }),
        required=False
    )

    class Meta:
        model = hotel_rooms
        fields = '__all__'
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-control'}),  # it's a choice field
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
            'refundable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meals_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bed_type': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control'}),
            'view': forms.TextInput(attrs={'class': 'form-control'}),
        }


