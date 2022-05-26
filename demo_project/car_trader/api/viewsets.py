from django.db import connection
from rest_framework import viewsets, permissions, status
from car_trader_app.models import Car, Type, Review, Images
from car_trader_app.serializers import CarSerializer, TypeSerializer, ReviewSerializer, ImageSerializer
from dealers.serializers import DealerSerializer
from dealers.models import Dealer
from cart.models import Cart, CartItem
from cart.serializers import CartSerializers, CartItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication


class CarViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        description = serializer.validated_data.get('description') or None
        if description is None:
            origin = serializer.validated_data.get('origin')
            brand = serializer.validated_data.get('brand')
            name = serializer.validated_data.get('name')
            _type = serializer.validated_data.get('type')
            description = f"This is a powerful {_type} - {brand} {name} come from {origin}."
        serializer.save(description=description, owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.description:
            instance.description = f"This is a powerful {instance.type} - {instance.brand} {instance.name} come from " \
                                   f"{instance.origin}."
        serializer.save(description=instance.description)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class TypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated,)  

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

    @action(detail=False, methods=['get'], name='Get Image By Car Id', url_path='get-image-by-car')
    def get_image_by_car(self, request, pk=None):
        str_car_id = request.GET.get('car_id');
        response = ImageSerializer.get_image_by_car(str_car_id)
        return Response(response,status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], name='Create Get Image By Car Id', url_path='create-func')
    def create_func_get_image_by_car(self, request, pk=None):
        ImageSerializer.create_func_get_image_by_car()
        return Response({'message':'Created successfully.'},status=status.HTTP_200_OK)


class DealerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CartViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=['POST'], detail=True, url_path='add-to-cart', url_name='add-to-cart',
            serializer_class=CartItemSerializer)
    def add_to_cart(self, request, pk=None):
        data = {
            "cart_id": request.data['cart'],
            "car_id": request.data['car'],
        }
        if not data['cart_id']:
            return Response({"message": "Param is missing: 'cart'"}, status=status.HTTP_400_BAD_REQUEST)
        elif not data['cart_id'].isnumeric():
            return Response({"message": "'cart' must be a number"}, status=status.HTTP_400_BAD_REQUEST)
        if not data['car_id']:
            return Response({"message": "Param is missing: 'car'"}, status=status.HTTP_400_BAD_REQUEST)
        elif not data['car_id'].isnumeric():
            return Response({"message": "Need a param 'car' and must be a number"}, status=status.HTTP_400_BAD_REQUEST)

        cart_id = int(data['cart_id'])
        car_id = int(data['car_id'])
        cart_item = CartItem.objects.filter(cart_id=cart_id, car_id=car_id)
        if cart_item:
            return Response({"message": "Car is already exist"}, status=status.HTTP_409_CONFLICT)
        with connection.cursor() as cursor:
            cursor.execute(f'CALL cart_insert_data({car_id},{cart_id})')
        return Response({"message": "Success!"}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True, url_path='remove-from-cart', url_name='remove-from-cart',
            serializer_class=CartItemSerializer)
    def remove_from_cart(self, request, pk=None):
        data = {
            "cart_id": request.data['cart'],
            "car_id": request.data['car'],
        }
        if not data['cart_id']:
            return Response({"message": "Param is missing: 'cart'"}, status=status.HTTP_400_BAD_REQUEST)
        elif not data['cart_id'].isnumeric():
            return Response({"message": "'cart' must be a number"}, status=status.HTTP_400_BAD_REQUEST)
        if not data['car_id']:
            return Response({"message": "Param is missing: 'car'"}, status=status.HTTP_400_BAD_REQUEST)
        elif not data['car_id'].isnumeric():
            return Response({"message": "Need a param 'car' and must be a number"}, status=status.HTTP_400_BAD_REQUEST)

        cart_id = int(data['cart_id'])
        car_id = int(data['car_id'])
        cart_item = CartItem.objects.filter(cart_id=cart_id, car_id=car_id)
        if not cart_item:
            return Response({"message": "Car doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        with connection.cursor() as cursor:
            cursor.execute(f'CALL cart_delete_data({car_id},{cart_id})')
        return Response({"message": "Success!"}, status=status.HTTP_200_OK)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
