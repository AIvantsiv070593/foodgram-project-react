from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from action.models import Favorite, ShoppingCart
from users.serializer import CustomUserSerializers

from .models import IngredientInRicepe, Ingredients, Recipe, Tags


class TagsSerializers(serializers.ModelSerializer):
    """Serialization of Tags model."""

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tags


class IngredientInRicepeSerializers(serializers.ModelSerializer):
    """Serialization of IngredientInRicepe model."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredients',
        queryset=Ingredients.objects.all()
    )

    amount = serializers.FloatField()

    class Meta:
        fields = ('id', 'amount')
        model = IngredientInRicepe


class IngredientsSerializers(serializers.ModelSerializer):
    """Serialization of Ingredients model."""

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredients


class IngredientInRicepeViewSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredients',
        queryset=Ingredients.objects.all()
    )

    name = serializers.StringRelatedField(source='ingredients')
    measurement_unit = serializers.SlugRelatedField(
        source='ingredients',
        slug_field='measurement_unit',
        read_only=True)

    amount = serializers.FloatField()

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = IngredientInRicepe


class RecipeViewSerializers(serializers.ModelSerializer):
    """Serialization of Recipe model to view in shoppingcart."""
    ingredients = IngredientInRicepeViewSerializers(
        many=True, source='ingredients_related_recipe')
    tags = TagsSerializers(many=True, read_only=True)
    image = Base64ImageField(use_url=True)
    author = CustomUserSerializers()
    cooking_time = serializers.IntegerField(min_value=1)
    is_favorited = serializers.SerializerMethodField('favorite')
    is_in_shopping_cart = serializers.SerializerMethodField('shopping_cart')

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'name',
                  'is_favorited', 'is_in_shopping_cart', 'image',
                  'text', 'cooking_time')
        model = Recipe

    def favorite(self, obj):
        try:
            return Favorite.objects.filter(user=self.context['request'].user,
                                           recipe=obj).exists()
        except TypeError:
            return False

    def shopping_cart(self, obj):
        try:
            return ShoppingCart.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        except TypeError:
            return False


class RecipeSerializers(serializers.ModelSerializer):
    """Serialization of Recipe model."""
    ingredients = IngredientInRicepeSerializers(
        many=True,
        source='ingredients_related_recipe')
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tags.objects.all())
    image = Base64ImageField()
    name = serializers.CharField(
        max_length=200,
        validators=[UniqueValidator(queryset=Recipe.objects.all())])
    text = serializers.CharField(max_length=200)
    cooking_time = serializers.IntegerField(min_value=1)
    author = CustomUserSerializers(required=False)
    is_favorited = serializers.SerializerMethodField('favorite')
    is_in_shopping_cart = serializers.SerializerMethodField('shopping_cart')

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'image', 'name', 'text', 'cooking_time')
        read_only_fields = ('id', 'author')
        model = Recipe

    def validate(self, data):
        check_list = []
        for ingredient in data.get('ingredients_related_recipe'):
            if ingredient['ingredients'] not in check_list:
                check_list.append(ingredient['ingredients'])
            else:
                raise serializers.ValidationError('Ингредиент уже добавлен')
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError('Количество должно быть > 0')
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients_related_recipe')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            IngredientInRicepe.objects.create(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredients=ingredient['ingredients'])
        recipe.tags.add(*tags)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients_related_recipe')
        instance.image = validated_data.get('image', instance.image)
        IngredientInRicepe.objects.filter(recipe=instance).delete()
        instance.tags.set(tags)
        instance.save()
        for ingredient in ingredients_data:
            IngredientInRicepe.objects.create(
                recipe=instance,
                amount=ingredient['amount'],
                ingredients=ingredient['ingredients'])
        return instance

    def favorite(self, obj):
        try:
            return Favorite.objects.filter(user=self.context['request'].user,
                                           recipe=obj).exists()
        except TypeError:
            return False

    def shopping_cart(self, obj):
        try:
            return ShoppingCart.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        except TypeError:
            return False


class ActionSerializers(serializers.ModelSerializer):
    """Serialization of Favorit and ShoppingCart"""

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe
