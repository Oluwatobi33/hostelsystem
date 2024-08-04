# forms.py
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django import forms
from .models import Booking  # Assuming you have a Booking model
from .models import Booking, Room
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['email']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'email', 
            'username', 
            'matric_number', 
            'application_number', 
            'level', 
            'phone_no', 
            'department', 
            'programme',
            'user_type'  # Add if needed
        ]