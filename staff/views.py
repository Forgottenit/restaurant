from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseNotFound, HttpResponseForbidden
import os
from django.conf import settings

def is_staffteam_or_admin(user):
    return user.groups.filter(name='StaffTeam').exists() or user.is_superuser


