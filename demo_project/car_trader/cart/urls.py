from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartListView.as_view(), name='cart_home'),
    path('add_to_cart/<int:car_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:car_id>/', views.remove_from_cart, name='remove_from_cart'),
]