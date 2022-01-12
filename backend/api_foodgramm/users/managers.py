from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager.
    """
    def create_user(self, username, first_name, last_name,
                    email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError("The username must be set")
        if not first_name:
            raise ValueError(_('The first_name must be set'))
        if not last_name:
            raise ValueError(_('The last_name must be set'))
        if not email:
            raise ValueError(_('The Email must be set'))
        user = self.model(username=username, first_name=first_name,
                          last_name=last_name, email=email,
                          password=password, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, first_name, last_name,
                         email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username=username, first_name=first_name,
                                last_name=last_name, email=email,
                                password=password, **extra_fields)
