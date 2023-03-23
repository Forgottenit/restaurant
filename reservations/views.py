from django.shortcuts import render
from .models import Reservation


def reservations(request):
    booking = Reservation.objects.all()
    return render(request, 'reservations.html', {'booking': booking})