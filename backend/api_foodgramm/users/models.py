from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Custom user."""
    username = models.CharField('username', max_length=150, unique=True)
    email = models.EmailField('email address', unique=True, max_length=254)
    first_name = models.CharField('first_name', max_length=150)
    last_name = models.CharField('last-name', max_length=150)
    is_active = models.BooleanField(default=True)
    # is_subscribed = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользовтаель'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Follow(models.Model):
    """Follow on users."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='following')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  related_name='followers')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name="unique_followers")
        ]

        ordering = ["-created"]

    # def __str__(self):
    #     return f'Подписок {self.user.count()},'
    #     f'Подписавшихся {self.following.count()}'
