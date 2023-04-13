from django.urls import path
from .views import index, about, simulate_500, maps
from . import views


handler403 = views.error_403
handler404 = views.error_404
handler500 = views.error_500

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('403/', views.error_403, name='error_403'),
    path('404/', views.error_404, name='error_404'),
    path('500/', views.error_500, name='error_500'),
    path('trigger-404/', views.trigger_404),
    path('trigger-403/', views.trigger_403),
    path('simulate-500/', simulate_500, name='simulate_500'),
    path("maps/", maps, name="maps"),
]