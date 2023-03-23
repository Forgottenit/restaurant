from django.shortcuts import render
from .models import MenuItem


def index(request):
    items = MenuItem.objects.all()
    return render(request, 'index.html', {'items': items})