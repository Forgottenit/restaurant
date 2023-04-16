from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden
import os
from django.conf import settings

def is_staffteam_or_admin(user):
    return user.groups.filter(name='StaffTeam').exists() or user.is_superuser






@user_passes_test(is_staffteam_or_admin)
# def staffteam_and_admin_view(request):
    
#     pass

