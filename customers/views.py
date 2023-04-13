from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden
# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def error_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)

def trigger_404(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')

def trigger_403(request):
    return HttpResponseForbidden('<h1>Forbidden</h1>')