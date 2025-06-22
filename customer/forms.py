from django import forms
from .models import HotelBooking

class HotelBookingStatusForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if name != 'status':
                field.disabled = True  # disables in HTML + protects in backend
