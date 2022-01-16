import io
from django.db.models import Sum
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from action.models import Favorite, ShoppingCart

from .filters import IngredientsFilter, RecipeFilter
from .models import Ingredients, Recipe, Tags, IngredientInRicepe
from .serializer import (
    IngredientsSerializers,
    RecipeSerializers,
    RecipeViewSerializers,
    TagsSerializers,
    ActionSerializers
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 6

class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """ GET Tags list or one Tag"""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializers


class IngredientsViwset(viewsets.ReadOnlyModelViewSet):
    """ GET Ingredients list or one Ingredient"""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializers
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IngredientsFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """ GET List Recipe. GET, POST, PUT, DEL Recipe"""
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeViewSerializers
        return RecipeSerializers

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['GET', 'DELETE'])
    def shopping_cart(self, request, pk=None):
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
    data = IngredientInRicepe.objects.filter(
         recipe__shoppingcart_recipe__user=request.user).values(
             'ingredients__name', 'ingredients__measurement_unit').annotate(
                 amount=Sum('amount'))
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Verdana', 'verdana.ttf'))
    textobject = p.beginText()
    textobject.setTextOrigin(50, 790)

    textobject.setFont('Verdana', 30)
    textobject.textLine('Список Покупок')

    textobject.setTextOrigin(50, 700)
    textobject.setFont('Verdana', 15)

    for items in data:
        row = ('{} {} {}'.format(items['ingredients__name'], items['amount'], items['ingredients__measurement_unit']))
        textobject.textLine(row)

    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='ShopList.pdf')