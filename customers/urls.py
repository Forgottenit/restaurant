from django.urls import path
from .views import index, about

handler403 = views.error_403
handler404 = views.error_404
handler500 = views.error_500

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about')
]