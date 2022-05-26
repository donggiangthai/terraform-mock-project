from rest_framework import serializers
from cart.models import Cart, CartItem
from api.serializers import UserDataSerializer, CartItemDataSerializer
from rest_framework.validators import UniqueTogetherValidator


class CartSerializers(serializers.ModelSerializer):
    user_data = UserDataSerializer(read_only=True, source='user')
    cart_item = CartItemDataSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = [
            'pk',
            'url',
            'user',
            'user_data',
            'cart_item',
        ]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'pk',
            'url',
            'cart',
            'car',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=CartItem.objects.all(),
                fields=[
                    'cart',
                    'car',
                ]
            )
        ]
