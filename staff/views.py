from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseNotFound, HttpResponseForbidden
import os
from django.conf import settings
from menu.models import MenuItem
from django.shortcuts import render

def is_staffteam_or_admin(user):
    return user.groups.filter(name='StaffTeam').exists() or user.is_superuser

def staff_menu(request):
    items = MenuItem.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'staff_templates/staff_menu.html', context)



# @user_passes_test(is_staffteam_or_admin)
# def staff_menu(request):
#     items = MenuItem.objects.all()
#     response = render(request, 'staff_templates/staff_menu.html', {'items': items})
#     return response

