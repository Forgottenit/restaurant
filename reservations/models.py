from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Reservation(models.Model):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    # CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        # (CANCELLED, 'Cancelled'),
    ]
    name = models.CharField(max_length=100) 
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    special_requests = models.TextField()
    party_size = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'Bookings are {self.name} {self.email} - {self.date} {self.time} {self.party_size}'
