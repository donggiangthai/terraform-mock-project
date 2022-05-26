from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from car_trader_app.models import Car, Type, Review
from car_trader_app.serializers import CarSerializer, TypeSerializer, ReviewSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from . import authentication



# Create your views here.
@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'All cars': '/car',
        'All types': '/type'
    }

    return Response(api_urls)


class CarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def perform_create(self, serializer):
        description = serializer.validated_data.get('description') or None
        if description is None:
            origin = serializer.validated_data.get('origin')
            brand = serializer.validated_data.get('brand')
            name = serializer.validated_data.get('name')
            _type = serializer.validated_data.get('type')
            description = f"This is a powerful {_type} - {brand} {name} come from {origin}."
        serializer.save(description=description)


class CarDetailAPIView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarUpdateAPIView(generics.UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.description:
            instance.description = f"This is a powerful {instance.type} - {instance.brand} {instance.name} come from " \
                                   f"{instance.origin}."
        serializer.save(description=instance.description)


class CarDestroyAPIView(generics.DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        description = serializer.validated_data.get('description') or None
        if description is None:
            origin = serializer.validated_data.get('origin')
            brand = serializer.validated_data.get('brand')
            name = serializer.validated_data.get('name')
            _type = serializer.validated_data.get('type')
            description = f"This is a powerful {_type} - {brand} {name} come from {origin}."
        serializer.save(description=description)

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.description:
            instance.description = f"This is a powerful {instance.type} - {instance.brand} {instance.name} come from " \
                                   f"{instance.origin}."
        serializer.save(description=instance.description)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class TypeViewSet(viewsets.ModelViewSet):
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
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def save(self):
        owner = self.request.user


class CartraderAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': "{key} {token}".format(key=authentication.TokenAuthentication.keyword,token = token.key)
        })