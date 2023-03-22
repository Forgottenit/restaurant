from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic,View
from django.views.generic.base import TemplateView
from .models import MenuItem

class HomeTemplateView(TemplateView):
    template_name = "index.html"


def index(request):
    items = MenuItem.objects.all()
    return render(request, 'index.html', {'items': items})