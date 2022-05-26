from django.urls import path, include
from . import viewsets
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register(r'dealer', viewsets.DealerViewSet)
router.register(r'car', viewsets.CarViewSet)
router.register(r'type', viewsets.TypeViewSet)
router.register(r'review', viewsets.ReviewViewSet)
router.register(r'cart', viewsets.CartViewSet)
router.register(r'cart-item', viewsets.CartItemViewSet)
router.register(r'image', viewsets.ImagesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', views.CartraderAuthToken.as_view(), name='token-auth')
]
