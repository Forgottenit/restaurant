from django.shortcuts import render, redirect, get_object_or_404, redirect
from .forms import BookingForm
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


@login_required
def reservations(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        print(request.POST)  # print request.POST to the console
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('user_reservations')
        else:
            print(form.errors)  # print form.errors to the console
    else:
        form = BookingForm()
    return render(request, 'reservations.html', {'form': form})

@login_required
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'successful_booking.html', {'reservations': reservations})

def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.user != request.user:
        return HttpResponseForbidden()
    reservation.delete()
    # Send an email to the user about the cancellation here (see step 2)
    return redirect('user_reservations')