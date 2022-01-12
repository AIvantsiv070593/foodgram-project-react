from django.db import models
from foodgram.models import Recipe
from users.models import CustomUser


class ShoppingCart(models.Model):
    name = models.CharField('Список покупок',
                            unique=True,
                            max_length=200,
                            default='')
    user = models.ForeignKey(CustomUser, verbose_name=('Создатель'),
                             on_delete=models.CASCADE,
                             null=False)
    recipe = models.ManyToManyField(Recipe,
                                    verbose_name=('Рецепт'),
                                    blank=True,
                                    related_name='shoppingcart_recipe')
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Cписок покупок'
        verbose_name_plural = 'Списки покупок'
        # constraints = [
        #     models.UniqueConstraint(fields=['user', 'recipe'],
        #                             name="unique_shopping_cart")
        # ]

    def __str__(self):
        return self.name


class Favorite(models.Model):
    name = models.CharField('Избранное',
                            unique=True,
                            max_length=200,
                            default='')
    user = models.ForeignKey(CustomUser, verbose_name=('Создатель'),
                             on_delete=models.CASCADE,
                             null=False)
    recipe = models.ManyToManyField(Recipe,
                                    verbose_name=('Рецепт'),
                                    blank=True,
                                    related_name='favorite_recipe')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        # constraints = [
        #     models.UniqueConstraint(fields=['user', 'recipe'],
        #                             name="unique_favorite")
        # ]

    def __str__(self):
        return self.name
