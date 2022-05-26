# Generated by Django 4.0.2 on 2022-03-05 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_trader_app', '0006_car_owner'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(to='car_trader_app.Car'),
        ),
    ]
