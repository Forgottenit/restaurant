from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('staff_menu/', views.staff_menu, name='staff_menu'),
    path('edit_menu_item/<int:menu_item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('delete_menu_item/<int:menu_item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('create_menu_item/', views.create_menu_item, name='create_menu_item'),
]
