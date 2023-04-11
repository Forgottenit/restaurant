from django import forms
from .models import Reservation
from django.forms.widgets import DateInput, RadioSelect
from django.core.exceptions import ValidationError
from datetime import date, datetime, time, timedelta
from django.utils import timezone

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

        if date and time:
            now = timezone.localtime(timezone.now())
            input_datetime = timezone.make_aware(
                                datetime.combine(date, datetime.strptime(time, "%H:%M").time()),
                                timezone.get_current_timezone()
                            )

            # Check if there is an existing booking for that user on that slot
            # existing_booking = Reservation.objects.filter(date=date).exists()
            # if existing_booking:
            #     raise forms.ValidationError("A booking already exists for this date and time slot.")
            
            if self.instance.pk is not None:
                existing_booking = Reservation.objects.filter(date=date).exclude(pk=self.instance.pk).exists()
            else:
                existing_booking = Reservation.objects.filter(date=date).exists()

            if existing_booking:
                raise forms.ValidationError("A booking already exists for this date and time slot.")

            user = self.user
            
            reservations = Reservation.objects.filter(date=date, user=user)
            # reservations = Reservation.objects.filter(date=date)
            # double_booking = Reservation.objects.filter(user=user, date=date, time=time).exists()
            # double_booking = Reservation.objects.filter(user=user, date=date).exists()

            """
            Exclude the current reservation's party size if editing a booking
            by checking if it has a primary key
            """
            if self.instance.pk is not None:
                reservations = reservations.exclude(pk=self.instance.pk)

            if reservations.exists() and not (self.instance.pk is not None and self.instance.date == date):
                raise forms.ValidationError("You already have a booking on this date.")
            #     double_booking = Reservation.objects.filter(user=user, date=date).exclude(pk=self.instance.pk).exists()
            # else:
            #     double_booking = Reservation.objects.filter(user=user, date=date).exists()

            # if self.instance.pk is not None:
            # if self.instance.pk:
                # exclude the current reservation's party size if editing a booking
            #     reservations = reservations.exclude(pk=self.instance.pk)
            # if reservations.exists():
            #     raise forms.ValidationError("You already have a booking on this date.")
            # existing_booking = reservations.filter(date=date).exists()
            # if existing_booking:
            #     raise forms.ValidationError("You have a booking that day already.")
                
            # if double_booking:
            #     raise forms.ValidationError("You have a booking that day already.")
            # if reservations.exists():
            #     raise forms.ValidationError("You have a booking that day already.")
            # Check that the time of the booking is later than the current time
            if input_datetime < now:
                self.add_error(
                    'time',
                    ValidationError("Booking time cannot be in the past.")
                )

            


            """
            Calculate the available capacity from 0 then every 15 minutes of
            the booking duration. This ensures there is capacity for the whole
            duration of the booking (1hr or 4 x 15mins)
            """
            available_capacity_for_duration = [
                MAX_CAPACITY - self.guests_during_booking(
                    reservations,
                    (interval_start := input_datetime +
                        timedelta(minutes=15 * i)),
                    (interval_end := input_datetime +
                        timedelta(minutes=15 * (i + 1)))
                )
                for i in range(4)
            ]

            if all(capacity >= cleaned_data['party_size']
                    for capacity in available_capacity_for_duration):
                return cleaned_data
            else:
                """
                Return Validation error and show availability
                for the chosen booking time
                """
                min_available_capacity = min(available_capacity_for_duration)
                error_message = f"Booking not available. Maximum available " \
                                f"capacity at this time is "\
                                f"{min_available_capacity}."
                self.add_error('party_size', ValidationError(error_message))
