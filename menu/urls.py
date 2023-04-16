from django.urls import path
from .views import menu, staff_menu

urlpatterns = [
    path('menu/', menu, name='menu'),
    path('staff_menu/', staff_menu, name='staff_menu'),
]

