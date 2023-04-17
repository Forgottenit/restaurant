from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseNotFound, HttpResponseForbidden
import os
from django.conf import settings
from menu.models import MenuItem, MenuCategory
from django.shortcuts import render
from reservations.models import Reservation
from datetime import date
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from reservations.forms import BookingForm
from django.db.models import Prefetch


def is_staffteam_or_admin(user):
    return user.groups.filter(name='StaffTeam').exists() or user.is_superuser


@user_passes_test(is_staffteam_or_admin)
def staff_menu(request):
    categories = MenuCategory.objects.all().prefetch_related(
        Prefetch('menuitem_set', queryset=MenuItem.objects.all().order_by('name'))
    )
    context = {'categories': categories}
    return render(request, 'staff_templates/staff_menu.html', context)


@user_passes_test(is_staffteam_or_admin)
def all_reservations(request):
    past_reservations = Reservation.objects.filter(date__lt=date.today()).order_by('date', 'time')
    today_reservations = Reservation.objects.filter(date=date.today()).order_by('time')

    today = timezone.now().date()
    first_day_current_month = today.replace(day=1)
    future_reservations_by_month = []

    while True:
        last_day_of_month = (first_day_current_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        reservations = Reservation.objects.filter(date__gte=first_day_current_month, date__lte=last_day_of_month).order_by('date', 'time')

        future_reservations_by_month.append({
            'title': first_day_current_month.strftime('%B %Y'),
            'reservations': reservations
        })

        first_day_current_month = last_day_of_month + timedelta(days=1)
        if first_day_current_month > today + timedelta(days=365):  # Display reservations for the next 12 months
            break

    context = {
        'todays_reservations': today_reservations,
        'future_reservations_by_month': future_reservations_by_month,
        'past_reservations': past_reservations,
    }
    return render(request, 'staff_templates/all_reservations.html', context)

