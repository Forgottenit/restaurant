# Generated by Django 3.2.18 on 2023-04-14 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0014_alter_reservation_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]