from django.views.generic import ListView
from .models import Car


class CarListView(ListView):
    model = Car
    template_name = 'car_trader_app/home.html'
