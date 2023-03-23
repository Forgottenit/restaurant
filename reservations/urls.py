from django.urls import path
from . import views

urlpatterns = [
    path('reservations/', views.reservations, name='reservations'),
]
