from django import forms
from .models import Reservation

class BookingForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'party_size']

