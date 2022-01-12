from django.contrib import admin
from action.models import Favorite
from .models import IngredientInRicepe, Ingredients, Recipe, Tags


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'favorite_count'
    )
    filter_horizontal = ('tags', 'ingredients')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    favorite_count.short_description = 'В Избранном'


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        # "color",
        'slug',
    )
    empty_value_display = '-пусто-'


@admin.register(IngredientInRicepe)
class IngredientInRicepeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredients',
        'amount',
    )
    empty_value_display = '-пусто-'
