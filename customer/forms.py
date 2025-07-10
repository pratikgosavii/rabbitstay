from django import forms
from .models import HotelBooking

class HotelBookingStatusForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = '__all__'

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # extract the user from the view
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if name != 'status':
                field.disabled = True  # disable all except status

        if user and not user.is_superuser:
            # remove 'confirmed' and 'cancelled' options
            self.fields['status'].choices = [
                choice for choice in self.fields['status'].choices
                if choice[0] not in ['confirmed', 'cancelled']
            ]