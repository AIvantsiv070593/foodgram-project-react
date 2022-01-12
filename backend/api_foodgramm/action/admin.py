from django.contrib import admin
from .models import Favorite, ShoppingCart


@admin.register(ShoppingCart)
class ShoppimgCartAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    list_filter = ('name',)
    filter_horizontal = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    filter_horizontal = ('recipe',)
    empty_value_display = '-пусто-'
