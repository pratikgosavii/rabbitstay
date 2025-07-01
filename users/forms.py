from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'email',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'type': 'password'
    }))


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  # Import your User model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('mobile', 'email')  # Only show mobile + optional email

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('mobile', 'email', 'is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_service_provider')



        
class VendorRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['mobile', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


from django import forms
from django.contrib.auth.models import Group
from users.models import User  # adjust if needed



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'email', 'password', 'group', 'is_active']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            self.save_m2m()
        return user