from rest_framework import serializers

from foodgram.models import Recipe

from .models import CustomUser, Follow


class UserRecipeSerializers(serializers.ModelSerializer):
    """Serializer to work on the Recipe model."""

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class CustomUserSerializers(serializers.ModelSerializer):
    """Serializer to work on the CustomUser model."""
    is_subscribed = serializers.SerializerMethodField('subscribe')

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        model = CustomUser

    def subscribe(self, obj):
        try:
            return Follow.objects.filter(
                user=self.context['request'].user,
                following=obj).exists()
        except TypeError:
            return False


class FollowUserSerializers(serializers.ModelSerializer):
    """Serializer to work on the CustomUser model."""
    recipes = UserRecipeSerializers(many=True, source='recipe_author')
    recipes_count = serializers.SerializerMethodField('count')
    is_subscribed = serializers.SerializerMethodField('subscribe')

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        model = CustomUser

    def count(self, obj):
        return obj.recipe_author.count()

    def subscribe(self, obj):
        try:
            return Follow.objects.filter(
                user=self.context['request'].user,
                following=obj).exists()
        except TypeError:
            return False
