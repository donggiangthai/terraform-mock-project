# Generated by Django 4.0.2 on 2022-03-15 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car_trader_app', '0011_merge_0006_images_0010_alter_car_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='cart',
        ),
    ]
