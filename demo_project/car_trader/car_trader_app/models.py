from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# from cart.models import Cart

User = settings.AUTH_USER_MODEL


def upload_to(self, filename):
    path = 'images'
    if self.car and self.car.brand:
        path += '/{brand}'.format(brand=self.car.brand)
    if self.car and self.car.code:
        path += '/{code}'.format(code=self.car.code)
    if self.car and self.car.color:
        path += '/{color}'.format(color=self.car.color)

    path += '/{filename}'.format(filename=filename)
    return path


class Type(models.Model):
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.type


class Car(models.Model):
    code = models.CharField(max_length=30, null=False, blank=False, unique=True)
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    number_of_kilometers_traveled = models.DecimalField(max_digits=95, decimal_places=2, default=0, null=True,
                                                        blank=True)
    number_of_doors = models.IntegerField()
    seat = models.IntegerField()
    date_of_manufacture = models.DateField()
    color = models.CharField(max_length=50)
    type = models.ForeignKey(Type, related_name='cars', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=95, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    fuel = models.CharField(max_length=100)
    gear = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cars', on_delete=models.CASCADE)
    # cart = models.ManyToManyField(Cart, related_name='cars', blank=True)

    def __str__(self):
        return self.name

    def get_first_img_url(self):
        first_item = self.images.first()
        if first_item:
            return first_item.image.url
        else:
            return None


class Images(models.Model):
    image = models.ImageField(upload_to=upload_to, default='images/default.jpg')
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='reviews', on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    review_content = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    class Meta:
        unique_together = ('user', 'car',)
