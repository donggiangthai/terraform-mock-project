from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarListView.as_view(), name='car_home'),
]
