from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (download_shopping_cart,
                    IngredientsViwset,
                    RecipeViewSet, TagsViewSet)

router_v1 = DefaultRouter()
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('ingredients', IngredientsViwset, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('recipes/download_shopping_cart/', download_shopping_cart),
    path('', include(router_v1.urls))]
