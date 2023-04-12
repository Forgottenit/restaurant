from django import forms
from django.forms.widgets import DateInput, RadioSelect
from django.core.exceptions import ValidationError
from datetime import date, datetime, time, timedelta
from django.utils import timezone
from .models import Reservation

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


class CheckDateValid(forms.DateField):

    """
    Check todays date and display validation error
    if booking attempt is in the past
    """
    def validate(self, value):
        super().validate(value)
        now = timezone.localtime(timezone.now()).date()
        if value < now:
            raise ValidationError("Booking date cannot be in the past.")


class BookingForm(forms.ModelForm):

    # Max booking capacity for each booking set to 6
    party_size = forms.IntegerField(min_value=1, max_value=6)
    # Call CheckDateValid for booking
    date = CheckDateValid(widget=DateInput(attrs={'type': 'date'}))
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
            reservations = Reservation.objects.filter(date=date, user=user)
            existing_booking = Reservation.objects.filter(date=date).exclude(pk=self.instance.pk).exists()

            if self.instance.pk is not None:
                reservations = reservations.exclude(pk=self.instance.pk)
            if existing_booking:
                error_message = "A booking already exists for this date and time slot."
                self.add_error(None, error_message)
            elif reservations.exists() and not (self.instance.pk is not None and self.instance.date == date):
                error_message = "You already have a booking on this date."
                self.add_error(None, error_message)
            elif input_datetime < now:
                error_message = "Booking time cannot be in the past."
                self.add_error('time', error_message)
            else:
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

            # Add the error message to the cleaned data dictionary
            cleaned_data['error_message'] = error_message

            return cleaned_data






        # if date and time:
        #     now = timezone.localtime(timezone.now())
        #     input_datetime = timezone.make_aware(
        #                         datetime.combine(date, datetime.strptime(time, "%H:%M").time()),
        #                         timezone.get_current_timezone()
        #                     )
        #     user = self.user
        #     reservations = Reservation.objects.filter(date=date, user=user)
        #     # Check if there is an existing booking for that user on that slot
        #     if self.instance.pk is not None:
        #         reservations = reservations.exclude(pk=self.instance.pk)
        #         existing_booking = Reservation.objects.filter(date=date).exclude(pk=self.instance.pk).exists()
        #     else:
        #         existing_booking = Reservation.objects.filter(date=date).exists()

        #     # Booking exists error

        #     if existing_booking:
        #        raise forms.ValidationError("A booking already exists for this date and time slot.")

        #     if reservations.exists() and not (self.instance.pk is not None and self.instance.date == date):
        #         raise forms.ValidationError("You already have a booking on this date.")

        #     # Check that the time of the booking is later than the current time
        #     if input_datetime < now:
        #         self.add_error(
        #             'time',
        #             ValidationError("Booking time cannot be in the past.")
        #         )

        #     """
        #     Calculate the available capacity from 0 then every 15 minutes of
        #     the booking duration. This ensures there is capacity for the whole
        #     duration of the booking (1hr or 4 x 15mins)
        #     """
        #     available_capacity_for_duration = [
        #         MAX_CAPACITY - self.guests_during_booking(
        #             reservations,
        #             (interval_start := input_datetime +
        #                 timedelta(minutes=15 * i)),
        #             (interval_end := input_datetime +
        #                 timedelta(minutes=15 * (i + 1)))
        #         )
        #         for i in range(4)
        #     ]

        #     if all(capacity >= cleaned_data['party_size']
        #             for capacity in available_capacity_for_duration):
        #         return cleaned_data
        #     else:
        #         """
        #         Return Validation error and show availability
        #         for the chosen booking time
        #         """
        #         min_available_capacity = min(available_capacity_for_duration)
        #         error_message = f"Booking not available. Maximum available " \
        #                         f"capacity at this time is "\
        #                         f"{min_available_capacity}."
        #         self.add_error('party_size', ValidationError(error_message))
