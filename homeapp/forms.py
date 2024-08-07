# forms.py
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django import forms
from .models import Room,Booking
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['email']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'description', 'price']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'description', 'price', 'available', 'room_pic']


class BookingForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']