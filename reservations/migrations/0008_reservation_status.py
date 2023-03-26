# Generated by Django 3.2.18 on 2023-03-26 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0007_auto_20230326_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')], default='Pending', max_length=20),
        ),
    ]
