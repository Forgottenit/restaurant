from django.db import models

# Create your models here.

# insert a menu category model
# class MenuCategory(models.Model):
#     name = models.CharField(max_length=20)
   
class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # link to category

    def __str__(self):
        return self.name
