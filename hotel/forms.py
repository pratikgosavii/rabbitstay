from django import forms
from .models import *
from masters.models import *

class hotel_Form(forms.ModelForm):
   
    amenities = forms.ModelMultipleChoiceField(
    queryset=amenity.objects.all(),
    widget=forms.SelectMultiple(attrs={
        'class': 'form-select select2',  # important class!
        'id': 'id_amenities'
    }),
        required=False
    )


    free_cancellation_till = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = hotel
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'star_rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
            'overall_rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
       
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
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
            'refundable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meals_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bed_type': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control'}),
            'view': forms.TextInput(attrs={'class': 'form-control'}),
        }