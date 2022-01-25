from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class IngredientInRicepe(models.Model):
    """Ingredient in Recipe models"""
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients_related_recipe')

    ingredients = models.ForeignKey(
        'Ingredients',
        on_delete=models.CASCADE,
        related_name='ingredients_related')

    amount = models.FloatField(
        'Колличество',
        null=False,
        name='amount',
        validators=[MinValueValidator(0.1), ])

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints=[models.UniqueConstraint(
            fields=['recipe', 'ingredients'],
            name='unique ingredients')]

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super(IngredientInRicepe, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.amount)


class Ingredients(models.Model):
    """Ingredient model"""
    name = models.CharField(
        'Название Ингредиента',
        max_length=200,
        null=False)

    measurement_unit = models.CharField(
        'Еденицы измерения',
        max_length=20,
        null=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tags(models.Model):
    """Tags model"""
    name = models.CharField(
        'Название Тэга',
        unique=True,
        max_length=200,
        default='',
        null=False)

    slug = models.SlugField(
        'uniqueSlug',
        unique=True,
        default='',
        null=False)

    color = models.CharField(
        'Цвет',
        unique=True,
        max_length=200,
        null=False)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe model"""
    name = models.CharField(
        'Название Рецепта',
        unique=False,
        max_length=200,
        null=False)

    image = models.ImageField(
        'Фото',
        upload_to='static/images/',
        help_text='Добавте картинку',
        null=False)

    text = models.CharField(
        'Описание',
        default='',
        max_length=200,
        null=False)

    author = models.ForeignKey(
        CustomUser,
        verbose_name=('Автор'),
        related_name='recipe_author',
        on_delete=models.CASCADE,
        null=False)

    tags = models.ManyToManyField(
        Tags,
        verbose_name=('Тэги'),
        blank=False,
        related_name='recipe_teg')

    ingredients = models.ManyToManyField(
        'Ingredients',
        verbose_name=('Ингридиенты'),
        blank=False,
        related_name='recipe',
        through=IngredientInRicepe)

    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        null=False,
        validators=[MinValueValidator(1), ])

    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return (
            f'{self.name}')
