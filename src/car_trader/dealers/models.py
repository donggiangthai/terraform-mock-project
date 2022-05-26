from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class Dealer(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.MALE)
    birthday = models.DateField(null=True)
    phone = PhoneNumberField(region='VN')
    address = models.TextField(max_length=500, blank=True)
