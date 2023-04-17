from django.shortcuts import render, redirect, get_object_or_404, redirect
from .forms import BookingForm
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def is_staffteam_or_admin(user):
    return user.groups.filter(name='StaffTeam').exists() or user.is_superuser

@login_required
def reservations(request):
    print(f"User CHECK IN VIEWS: {request.user}")
    form_errors = ""
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('user_reservations')
        else:
            form_errors = form.errors.as_json()
    else:
        form = BookingForm(user=request.user)
    return render(request, 'reservations.html', {'form': form, 'form_errors': form_errors})


@login_required
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('date')
    return render(request, 'successful_booking.html', {'reservations': reservations})


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if not (reservation.user == request.user or is_staffteam_or_admin(request.user)):
        raise PermissionDenied
    reservation.delete()
    if is_staffteam_or_admin(request.user):
        return redirect('all_reservations')
    else:
        return redirect('user_reservations')

@login_required
def edit_reservation(request, reservation_id):
    print(f"User CHECK IN EDIT: {request.user}")
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if not (reservation.user == request.user or is_staffteam_or_admin(request.user)):
        raise PermissionDenied

    form_errors = ""
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=reservation, user=request.user)
        if form.is_valid():
            form.save()
            if is_staffteam_or_admin(request.user):
                return redirect('all_reservations')
            else:
                return redirect('user_reservations')
        else:
            form_errors = form.errors.as_json()
    else:
        form = BookingForm(instance=reservation, user=request.user)

    return render(request, 'edit_reservation.html', {'form': form, 'form_errors': form_errors})
