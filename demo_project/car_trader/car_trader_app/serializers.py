from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import Car, Type, Review, Images
from api.serializers import UserPublicSerializer, ReviewPublicSerializer, CartDataSerializer
from django.db import connection

class ViewCarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('code', 'brand', 'name', 'origin', 'number_of_kilometers_traveled', 'number_of_doors', 'seat',
                  'date_of_manufacture', 'color', 'type', 'reviews', 'price', 'description', 'fuel', 'gear')


class ResponseSerializers():
    def __init__(self):
        self.code = 0
        self.message = 'The operation completed successfully.'
        self.data = {}

    def addErrorMessage(self, code, message):
        self.data = {}
        self.code = code
        self.message = message

    @classmethod
    def create_message(cls):
        return cls()


class CarSerializer(serializers.ModelSerializer):
    review_data = serializers.SerializerMethodField(read_only=True)
    owner = serializers.HyperlinkedRelatedField(view_name='dealer-detail', read_only=True)
    images = serializers.SerializerMethodField('get_images')
    cart_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = [
            'pk',
            'url',
            'owner',
            # 'cart',
            'cart_data',
            'code',
            'brand',
            'name',
            'origin',
            'number_of_kilometers_traveled',
            'number_of_doors',
            'seat',
            'date_of_manufacture',
            'color',
            'type',
            'price',
            'description',
            'fuel',
            'gear',
            'review_data',
            'images'
        ]

    def get_review_data(self, obj):
        qs = obj.reviews.all()
        return [ReviewPublicSerializer(review, many=False, context=self.context).data for review in qs]

    def get_cart_data(self, obj):
        qs = obj.carts.all()
        return [CartDataSerializer(cart, context=self.context).data for cart in qs]

    def get_images(self, obj):
        imgs = obj.images.all()
        return [ImageSerializer(imgs, many=True, context=self.context).data]


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['url', 'type']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'url',
            'pk',
            'user',
            'car',
            'rating',
            'subject',
            'review_content',
            'create_at',
            'update_at',
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['pk', 'url', 'image', 'car']

    def get_image_url(self, obj):
        return obj.image.url

    def validate(self, data):
        path = 'images'
        car = data['car']
        image = data['image']
        if car.brand:
            path += '/{brand}'.format(brand=car.brand)
        if car.code:
            path += '/{code}'.format(code=car.code)
        if car.color:
            path += '/{color}'.format(color=car.color)
        path += '/{name}'.format(name=image.name)

        image_exists = Images.objects.filter(image=path)
        if(len(image_exists) > 0):
            raise serializers.ValidationError({'mesage': 'The image name already exist, Please change the name image.'})
        return data

    @staticmethod
    def get_image_by_car(str_car_id):
        if not str_car_id or not str_car_id.isnumeric():
            return {'message': 'Param is incorrect.'}
        car_id = int(str_car_id)
        columns = ['pk','image','car']
        try:
            with connection.cursor() as cur:
                cur.callproc('get_image_from_car_id', [car_id,])
                result = cur.fetchall()
                return [dict(zip(columns,row)) for row in result]
        except:
            return {'message': 'Please check your database connection or the stored procedure created.'}

    @staticmethod
    def create_func_get_image_by_car():
        try:
            query = "CREATE OR REPLACE function get_image_from_car_id(id_car bigint)"
            query+=" returns table (id bigint, image varchar, car_id bigint)"
            query+=" LANGUAGE plpgsql as $$ begin return query SELECT * FROM car_trader_app_images as a where a.car_id=id_car; end; $$;"
            with connection.cursor() as cur:
                cur.execute(query)
        except:
            return {'message': 'Please check your database connection or the stored procedure created.'}

       

    


