from django import forms
from .models import Reservation

class BookingForm(forms.ModelForm):
    party_size = forms.IntegerField(min_value=1, max_value=6)
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'special_requests', 'party_size']

