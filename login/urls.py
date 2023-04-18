from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import send_email_view

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('send_email/', send_email_view, name='send_email'),
]