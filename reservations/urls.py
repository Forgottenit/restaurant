from django.urls import path
from . import views

urlpatterns = [
    path('reservations/', views.reservations, name='reservations'),
    path('success/', views.success, name='success'),  # add a new path for the success URL
   
]
