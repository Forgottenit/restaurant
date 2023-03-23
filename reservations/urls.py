from django.urls import path
from .views import reservations

urlpatterns = [
    path('reservations/', reservations, name='reservations'),
]
