from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Reservation


def reservations(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        print(request.POST)  # print request.POST to the console
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            print(form.errors)  # print form.errors to the console
    else:
        form = BookingForm()
    return render(request, 'reservations.html', {'form': form})

def success(request):
    # Get the latest booking from the database
    latest_booking = Reservation.objects.latest('id')
    return render(request, 'successful_booking.html', {'latest_booking': latest_booking})