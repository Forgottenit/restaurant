# Generated by Django 3.2.18 on 2023-03-22 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MenuItems',
            new_name='MenuItem',
        ),
    ]