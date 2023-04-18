from django.urls import path
from . import views

urlpatterns = [

    path('staff_menu/', views.staff_menu, name='staff_menu'),
    path('all_reservations/', views.all_reservations, name='all_reservations'),

]
