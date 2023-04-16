from django.shortcuts import render
from .models import MenuItem
from django.contrib.auth.decorators import user_passes_test

def is_staffteam_or_admin(user):
    return user.groups.filter(name='StaffTeam').exists() or user.is_superuser


def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'menu.html', {'items': items})


@user_passes_test(is_staffteam_or_admin)
def staff_menu(request):
    items = MenuItem.objects.all()
    return render(request, 'staff_templates/staff_menu.html', {'items': items})