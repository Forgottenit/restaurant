from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, MenuCategory
from .forms import MenuItemForm
from django.contrib.auth.decorators import user_passes_test

def is_staffteam_or_admin(user):
    return user.groups.filter(name='StaffTeam').exists() or user.is_superuser


def menu(request):
    items = MenuItem.objects.all()
    categories = MenuCategory.objects.all()
    return render(request, 'menu.html', {'items': items, 'categories': categories})

@user_passes_test(is_staffteam_or_admin)
def edit_menu_item(request, menu_item_id):
    item = get_object_or_404(MenuItem, pk=menu_item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('staff_menu')
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'staff_templates/edit_menu_item.html', {'form': form})

@user_passes_test(is_staffteam_or_admin)
def delete_menu_item(request, menu_item_id):
    item = get_object_or_404(MenuItem, pk=menu_item_id)
    item.delete()
    return redirect('staff_menu')

@user_passes_test(is_staffteam_or_admin)
def create_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_menu')
    else:
        form = MenuItemForm()

    return render(request, 'staff_templates/edit_menu_item.html', {'form': form})
