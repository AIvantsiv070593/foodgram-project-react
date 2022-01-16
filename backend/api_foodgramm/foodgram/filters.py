from django_filters import rest_framework as filters

from .models import Ingredients, Recipe


class RecipeFilter(filters.FilterSet):
    """Filter Recipe by Tags, Author, Favorite"""
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='shopping_cart')

    class Meta:
        model = Recipe
        fields = ['author', 'tags']

    def favorited(self, queryset, name, value):
        if value is True:
            return queryset.filter(favorite_recipe__user=self.request.user)
        else:
            return queryset.filter(favorite_recipe__isnull=True)

    def shopping_cart(self, queryset, name, value):
        if value is True:
            return queryset.filter(shoppingcart_recipe__user=self.request.user)
        else:
            return queryset.filter(shoppingcart_recipe__isnull=True)


class IngredientsFilter(filters.FilterSet):
    """Filter Ingredients by name"""
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredients
        fields = ['name']
