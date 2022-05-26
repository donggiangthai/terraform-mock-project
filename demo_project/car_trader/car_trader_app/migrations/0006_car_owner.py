# Generated by Django 4.0.2 on 2022-03-04 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car_trader_app', '0005_alter_car_type_alter_review_car_alter_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
