from django import forms
from .models import Reservation
from django.forms.widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class BookingForm(forms.ModelForm):
    # YEAR_CHOICES = ['2022', '2023'] add two year booking window
    # MONTH_CHOICES = ['April', 'May', 'June'] add only future dates selectable
    TIME_CHOICES = (
        ('17:00', '5:00 PM'),
        ('17:15', '5:15 PM'),
        ('17:30', '5:30 PM'),
        ('17:45', '5:45 PM'),
        ('18:00', '6:00 PM'),
        ('18:15', '6:15 PM'),
        ('18:30', '6:30 PM'),
        ('18:45', '6:45 PM'),
        ('19:00', '7:00 PM'),
        ('19:15', '7:15 PM'),
        ('19:30', '7:30 PM'),
        ('19:45', '7:45 PM'),
        ('20:00', '8:00 PM'),
        ('20:15', '8:15 PM'),
        ('20:30', '8:30 PM'),
        ('20:45', '8:45 PM'),
        ('21:00', '9:00 PM'),
        ('21:15', '9:15 PM'),
        ('21:30', '9:30 PM'),
        ('21:45', '9:45 PM'),
        ('22:00', '10:00 PM'),
    )
    time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.RadioSelect)
    # party_size = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    party_size = forms.IntegerField(min_value=1, max_value=6)
    # date = forms.DateField(widget=forms.SelectDateWidget( years=YEAR_CHOICES))
    date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    # time = forms.ChoiceField(label='Time', choices=[(f'{hour:02d}:{minute:02d}', f'{hour:02d}:{minute:02d}') for hour in range(17, 22) for minute in range(0, 60, 15)])
    # time = forms.ChoiceField(label='Time', choices=[(f'{hour:02d}:{minute:02d}', f'{hour:02d}:{minute:02d}') for hour in range(17, 22) for minute in range(0, 60, 15)], widget=forms.Select(attrs={'class': 'form-select'})) With CSS STYLING
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'special_requests', 'party_size']

