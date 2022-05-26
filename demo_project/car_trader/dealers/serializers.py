from rest_framework import serializers
from .models import Dealer


class DealerSerializer(serializers.ModelSerializer):
    cars = serializers.HyperlinkedRelatedField(view_name='car-detail', read_only=True, many=True)
    cart = serializers.HyperlinkedRelatedField(view_name='cart-detail', read_only=True)

    class Meta:
        model = Dealer
        fields = [
            'url',
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'gender',
            'birthday',
            'phone',
            'address',
            'cars',
            'cart',
        ]
