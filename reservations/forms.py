from django import forms
from .models import Reservation
from django.forms.widgets import DateInput, RadioSelect
from django.core.exceptions import ValidationError
from datetime import datetime


# Check todays date and time 
class FutureDateField(forms.DateField):
    def validate(self, value):
        super().validate(value)
        now = datetime.now().date()
        if value < now:
            raise ValidationError("Booking date cannot be in the past.")


class BookingForm(forms.ModelForm):
    TIME_CHOICES = (
        ('13:00', '1:00 PM'),
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

    party_size = forms.IntegerField(min_value=1, max_value=6)
    date = FutureDateField(widget=DateInput(attrs={'type': 'date'}))
    time = forms.ChoiceField(choices=TIME_CHOICES, widget=RadioSelect)

    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'special_requests', 'party_size']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            now = datetime.now()
            input_datetime = datetime.combine(date, datetime.strptime(time, "%H:%M").time())

            if input_datetime < now:
                self.add_error('time', ValidationError("Booking time cannot be in the past."))