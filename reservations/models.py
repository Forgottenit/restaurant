from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
    ]
    name = models.CharField(max_length=30, blank=False, null=False, help_text="Enter your name")
    email = models.EmailField(blank=False, null=False, help_text="We will email you your booking")
    date = models.DateField(blank=False, null=False)
    time = models.TimeField(blank=False, null=False)
    special_requests = models.TextField(blank=True, help_text="Enter any special requests (optional)")
    party_size = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], blank=False, null=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, blank=False, null=False, help_text="Select the reservation status")
    created_on = models.DateTimeField(auto_now_add=True, help_text="Reservation creation timestamp")

    def __str__(self):
        return f'Bookings are {self.name} {self.email} - {self.date} {self.time} {self.party_size}'
