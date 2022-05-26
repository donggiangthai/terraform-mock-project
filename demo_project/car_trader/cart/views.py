from django.db import connection
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Cart


class CartListView(ListView):
    model = Cart
    template_name = 'cart/home.html'


def add_to_cart(request, car_id):
    user = request.user
    cart = Cart.objects.filter(user_id=user.id)
    check_exist_car = cart[0].cars.filter(pk=car_id)

    if check_exist_car:
        return redirect('cart_home')
    else:
        with connection.cursor() as cursor:
            cursor.execute(f"call cart_insert_data({car_id},{cart[0].pk})")
            return redirect('cart_home')


def remove_from_cart(request, car_id):
    user = request.user
    cart = Cart.objects.filter(user_id=user.id)

    with connection.cursor() as cursor:
        cursor.execute(f"call cart_delete_data({car_id},{cart[0].pk})")
        return redirect('cart_home')

