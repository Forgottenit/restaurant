# Generated by Django 3.2.18 on 2023-04-16 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_alter_menucategory_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menucategory',
            name='name',
            field=models.CharField(choices=[('Appetizers', 'Appetizers'), ('Main Course', 'Main Course'), ('Desserts', 'Desserts'), ('Sides', 'Sides'), ('Specials', 'Specials')], max_length=20, unique=True),
        ),
    ]
