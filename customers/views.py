from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden
# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def error_403(request, exception):
    return render(request, '403.html', status=403)

def error_404(request, exception):
    return render(request, '404.html')

def error_500(request):
    return render(request, '500.html', status=500)

def trigger_404(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')

def trigger_403(request):
    return HttpResponseForbidden('<h1>Forbidden</h1>')

# TEST to create a 500 error
def simulate_500(request):
    raise Exception("Something went wrong")