from django import forms
from django.forms.widgets import DateInput, RadioSelect
from django.core.exceptions import ValidationError
from datetime import date, datetime, time, timedelta
from django.utils import timezone
from .models import Reservation
from django.core.validators import MinValueValidator
from django.template.loader import render_to_string

# Capacity of Restaurant set at 50 and Each Booking to last one hour
MAX_CAPACITY = 50
BOOKING_DURATION = timedelta(hours=1)


# Function to display time options for bookings
def time_choices(start_hour, end_hour, interval_minutes):
    choices = []
    current_time = time(hour=start_hour)
    end_time = time(hour=end_hour)

    while current_time <= end_time:
        formatted_time = current_time.strftime('%H:%M')
        formatted_time_display = current_time.strftime('%-I:%M %p')
        choices.append((formatted_time, formatted_time_display))
        current_time = (datetime.combine(date.today(), current_time)
                        + timedelta(minutes=interval_minutes)).time()

    return choices


"""
Possibility to add or Change opening hours (Format is 24hrs, with opening hr,
closing hr and intervals of availability)
"""
DINNER_TIME_CHOICES = time_choices(13, 22, 15)


class BookingForm(forms.ModelForm):

    # Max booking capacity for each booking set to 6
    party_size = forms.IntegerField(min_value=1, max_value=6)

     # Add a MinValueValidator to date field to ensure the selected date is not in the past
    date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        validators=[
            MinValueValidator(limit_value=date.today(), message="Booking date cannot be in the past.")
        ]
    )

    # Display time options as DINNER_TIME_CHOICES as Radio buttons
    time = forms.ChoiceField(choices=DINNER_TIME_CHOICES, widget=RadioSelect)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control custom-input'})
        self.fields['email'].widget.attrs.update({'class': 'form-control custom-input'})
        self.fields['date'].widget.attrs.update({'class': 'form-control custom-input'})
        self.fields['time'].widget.attrs.update({'class': 'custom-radio'})
        self.fields['special_requests'].widget.attrs.update({'class': 'form-control custom-textarea'})
        self.fields['party_size'].widget.attrs.update({'class': 'form-control custom-select'})

    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time',
                  'special_requests', 'party_size']

    """
    Function to calculate total guests for all reservations at a specific
    time and at set intervals
    """
    def guests_during_booking(self, reservations,
                              interval_start, interval_end):
        return sum(
            reservation.party_size
            for reservation in reservations
            if (
                (
                    reservation_start := timezone.make_aware(
                            datetime.combine(self.cleaned_data['date'],
                                             reservation.time),
                            timezone.get_current_timezone()
                    )
                    )
                ) < interval_end
            ) and (reservation_start + BOOKING_DURATION > interval_start)

    # Main validation function for the form
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        error_message = ""

        if date and time:
            now = timezone.localtime(timezone.now())
            input_datetime = timezone.make_aware(
                datetime.combine(date, datetime.strptime(time, "%H:%M").time()),
                timezone.get_current_timezone()
            )

            user = self.user
            existing_reservations = Reservation.objects.filter(user=user)
            if self.instance.pk is not None:
                existing_reservations = existing_reservations.exclude(pk=self.instance.pk)

            # Check for reservations on date
            reservations_for_date = existing_reservations.filter(date=date)
            

            # Check if user already has a booking on the chosen date
            if reservations_for_date.exists():
                error_message = "You already have a booking on this date."
                self.add_error('date', error_message)

            # Check if booking time is in the past
            elif input_datetime < now:
                error_message = "Booking time cannot be in the past."
                self.add_error('time', error_message)

            # Check if there is enough available capacity for the booking
            else:
                reservations = Reservation.objects.filter(date=date).exclude(user=user)

                if self.instance.pk is not None:
                    reservations = reservations.exclude(pk=self.instance.pk)

                available_capacity_for_duration = [
                    MAX_CAPACITY - self.guests_during_booking(
                        reservations,
                        (interval_start := input_datetime + timedelta(minutes=15 * i)),
                        (interval_end := input_datetime + timedelta(minutes=15 * (i + 1)))
                    )
                    for i in range(4)
                ]

                if all(capacity >= cleaned_data['party_size'] for capacity in available_capacity_for_duration):
                    return cleaned_data
                else:
                    min_available_capacity = min(available_capacity_for_duration)
                    error_message = f"Booking not available. Maximum available capacity at this time is {min_available_capacity}."
                    self.add_error('party_size', error_message)

            cleaned_data['error_message'] = error_message

        return cleaned_data
