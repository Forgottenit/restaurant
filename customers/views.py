from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden
import os
from django.conf import settings


def maps(request):
    context = {
        'google_maps_key': settings.GOOGLE_MAPS_KEY
    }
    return render(request, 'home_page.html', context=context)


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def error_403(request, exception=None):
    return render(request, '403.html', status=403)


def error_404(request, exception=None):
    return render(request, '404.html', status=404)


def error_500(request, exception=None):
    return render(request, '500.html', status=500)


def trigger_404(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def trigger_403(request):
    return HttpResponseForbidden('<h1>Forbidden</h1>')


# TEST to create a 500 error
def simulate_500(request):
    raise Exception("Something went wrong")
