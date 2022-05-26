from rest_framework import serializers
from car_trader_app.models import Review
from cart.models import Cart


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    other_reviews = serializers.SerializerMethodField(read_only=True)

    def get_other_reviews(self, obj):
        user = obj
        qs = user.reviews.all()
        return [ReviewPublicSerializer(review, many=False, context=self.context).data for review in qs]


class ReviewPublicSerializer(serializers.Serializer):
    review_url = serializers.HyperlinkedIdentityField(view_name='review-detail', read_only=True, many=False)
    car_url = serializers.HyperlinkedIdentityField(view_name='car-detail', read_only=True, many=False)
    subject = serializers.CharField(read_only=True)
    review_content = serializers.CharField(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'url',
            'car_url',
            'subject',
            'review_content',
            'rating',
        ]


class UserDataSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='dealer-detail', read_only=True)
    username = serializers.CharField(read_only=True)


class CartDataSerializer(serializers.Serializer):
    user = UserDataSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = [
            'pk',
            'url',
            'user',
        ]


class CartItemDataSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='cartitem-detail', read_only=True)
    car = serializers.HyperlinkedRelatedField(view_name='car-detail', read_only=True)
