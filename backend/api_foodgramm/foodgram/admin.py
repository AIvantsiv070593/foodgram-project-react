from api_foodgramm import settings
from django import forms
from django.contrib import admin

from action.models import Favorite
from foodgram.form import TagsForm

from .models import IngredientInRicepe, Ingredients, Recipe, Tags


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    empty_value_display = settings.empty_value


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'favorite_count'
    )
    filter_horizontal = ('tags', 'ingredients')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = settings.empty_value

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    favorite_count.short_description = 'В Избранном'


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    form = TagsForm
    fieldsets = (
        (None, {
            'fields': (('name', 'slug'), 'color')
            }),
        )
    empty_value_display = settings.empty_value


@admin.register(IngredientInRicepe)
class IngredientInRicepeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredients',
        'amount',
    )
    empty_value_display = settings.empty_value
