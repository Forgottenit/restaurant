from django.core.validators import MinValueValidator
from django.db import models

class MenuCategory(models.Model):
    APPETIZERS = 'Appetizers'
    MAINS = 'Main Course'
    DESSERTS = 'Desserts'
    SIDES = 'Sides'
    SPECIALS = 'Specials'

    CATEGORY_CHOICES = [
        (APPETIZERS, 'Appetizers'),
        (MAINS, 'Main Course'),
        (DESSERTS, 'Desserts'),
        (SIDES, 'Sides'),
        (SPECIALS, 'Specials'),
    ]

    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True, blank=False, null=False, help_text="Select the category")

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, default=None, blank=False, null=False, help_text="Select the category of the menu item")
    name = models.CharField(max_length=50, blank=False, null=False, help_text="Enter the name of the menu item")
    description = models.TextField(blank=False, null=False, help_text="Enter a description for the menu item")
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False, validators=[MinValueValidator(0)], help_text="Enter the price of the menu item")

    def __str__(self):
        return self.name
