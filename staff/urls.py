from django.urls import path
from . import views

urlpatterns = [

    path('staff_menu/', views.staff_menu, name='staff_menu'),
]