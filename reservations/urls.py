from django.urls import path
from . import views

urlpatterns = [
    path('reservations/', views.reservations, name='reservations'),
    path('user_reservations/', views.user_reservations, name='user_reservations'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('edit_reservation/<int:reservation_id>/', views.edit_reservation, name='edit_reservation')
   
]
