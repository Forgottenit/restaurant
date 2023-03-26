from django import forms
from .models import Reservation
from django.forms.widgets import DateInput

class BookingForm(forms.ModelForm):
    YEAR_CHOICES = ['2022', '2023']
    # MONTH_CHOICES = ['April', 'May', 'June']
    party_size = forms.IntegerField(min_value=1, max_value=6)
    # date = forms.DateField(widget=forms.SelectDateWidget( years=YEAR_CHOICES))
    date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'special_requests', 'party_size']

