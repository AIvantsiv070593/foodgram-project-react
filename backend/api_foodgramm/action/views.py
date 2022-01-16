from rest_framework import viewsets

from .models import ShoppingCart
from .serializer import ShoppingCartSerializers


class ShoppingCartViewSet(viewsets.ReadOnlyModelViewSet):
    """ GET Recipe list or one ShoppingCart"""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializers
