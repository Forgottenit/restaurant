from django.shortcuts import render
from .forms import ContactForm


def reservations(request):
   form = ContactForm(request.POST)
   return render(request, 'reservations.html', {'form': form})
    