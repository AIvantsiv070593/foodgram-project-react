from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from action.models import Favorite, ShoppingCart

from .filters import IngredientsFilter, RecipeFilter
from .models import IngredientInRicepe, Ingredients, Recipe, Tags
from .serializer import (ActionSerializers, IngredientsSerializers,
                         RecipeSerializers, RecipeViewSerializers,
                         TagsSerializers)
from .utils import get_pdf_file


class StandardResultsSetPagination(PageNumberPagination):
    """Pagination for recipe"""
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 6


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """ A ViewSet for Tags model"""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializers


class IngredientsViwset(viewsets.ReadOnlyModelViewSet):
    """A ViewSet for Ingredients model"""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializers
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IngredientsFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """A ViewSet for Recipe model"""
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeViewSerializers
        return RecipeSerializers

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['GET', 'DELETE'])
    def shopping_cart(self, request, pk=None):
        """ADD, DELETE recipe from shoping_cart"""
        recipe = get_object_or_404(Recipe, pk=pk)
        username = self.request.user.username
        if request.method == 'DELETE':
            shoplist = ShoppingCart.objects.get(user=self.request.user)
            shoplist.recipe.remove(recipe)
            recipe.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            shoplist, _ = ShoppingCart.objects.get_or_create(
                name='Список Покупок ' + username,
                user=self.request.user)
            shoplist.recipe.add(recipe)
            recipe.save()
            serializer = ActionSerializers(recipe,
                                           context={'request': request})
            return Response(serializer.data)

    @action(detail=True, methods=['GET', 'DELETE'])
    def favorite(self, request, pk=None):
        """ADD, DELETE recipe from favorite"""
        recipe = get_object_or_404(Recipe, pk=pk)
        username = self.request.user.username
        if request.method == 'DELETE':
            favorite = Favorite.objects.get(user=self.request.user)
            favorite.recipe.remove(recipe)
            recipe.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            favorite, _ = Favorite.objects.get_or_create(
                name='Избранные рецепты ' + username,
                user=self.request.user)
            favorite.recipe.add(recipe)
            recipe.save()
            serializer = ActionSerializers(recipe,
                                           context={'request': request})
            return Response(serializer.data)


@api_view(['GET'])
def download_shopping_cart(request):
    """Download shopping list"""
    data = IngredientInRicepe.objects.filter(
         recipe__shoppingcart_recipe__user=request.user).values(
             'ingredients__name', 'ingredients__measurement_unit').annotate(
                 amount=Sum('amount'))
    return get_pdf_file(data)
