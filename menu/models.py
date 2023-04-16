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

    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


