from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# from users.models import CustomUser
from users.serializer import CustomUserSerializers
from foodgram.serializer import RecipeSerializers

from .models import ShoppingCart


class ShoppingCartSerializers(serializers.ModelSerializer):
    """Serializer to work on the ShoppingCart model."""
    name = serializers.CharField(
        max_length=200,
        validators=[UniqueValidator(queryset=ShoppingCart.objects.all())],
    )
    user = serializers.ReadOnlyField(source='user.username')
    recipe = RecipeSerializers(many=True)
    pub_date = serializers.DateTimeField()

    class Meta:
        fields = ('id', 'name', 'user', 'recipe', 'pub_date')
        model = ShoppingCart
