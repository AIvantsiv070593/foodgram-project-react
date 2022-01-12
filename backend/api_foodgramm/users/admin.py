from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow

IF_NONE = "-пусто-"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "username",
        "email",
    )
    list_filter = (
        "username",
        "email",
    )

    search_fields = ("email",)
    ordering = ("email",)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    model = Follow
    list_display = (
        'user',
        'following'
    )
