from django.shortcuts import render, redirect, get_object_or_404, redirect
from .forms import BookingForm
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


# @login_required
# def reservations(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST, user=request.user)
#         print(request.POST)  # print request.POST to the console
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.user = request.user
#             reservation.save()
#             return redirect('user_reservations')
#         else:
#             print(form.errors)  # print form.errors to the console
#     else:
#         form = BookingForm(user=request.user)
#     return render(request, 'reservations.html', {'form': form})

@login_required
def reservations(request):
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
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'successful_booking.html', {'reservations': reservations})


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.user != request.user:
        return HttpResponseForbidden()
    reservation.delete()
    return redirect('user_reservations')


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.user != request.user:
        return HttpResponseForbidden()

    form_errors = ""
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('user_reservations')
        else:
            form_errors = form.errors.as_json()
    else:
        form = BookingForm(instance=reservation)

    return render(request, 'edit_reservation.html', {'form': form, 'form_errors': form_errors})

# @login_required
# def edit_reservation(request, reservation_id):
#     reservation = get_object_or_404(Reservation, id=reservation_id)
#     if reservation.user != request.user:
#         return HttpResponseForbidden()

#     form = BookingForm(instance=reservation)  # define form here

#     if request.method == 'POST':
#         form = BookingForm(request.POST, instance=reservation)
#         if form.is_valid():
#             form.save()
#             return redirect('user_reservations')
#     return render(request, 'edit_reservation.html', {'form': form})


#     from django.shortcuts import render_to_response
# from django.template import RequestContext


# def handler404(request, *args, **argv):
#     response = render_to_response('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 404
#     return response


# def handler500(request, *args, **argv):
#     response = render_to_response('500.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 500
#     return response