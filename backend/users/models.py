from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from .validators import username_regex_validator


class User(AbstractUser):
    email = models.EmailField('Электронная почта', max_length=254, unique=True)
    username = models.CharField('Имя пользователя', max_length=150,
                                validators=(username_regex_validator, ),
                                unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    is_subscribed = models.BooleanField('Подписка', blank=True,
                                        null=True, default=False)
    avatar = models.ImageField('Фото профиля', blank=True,
                               null=True, upload_to='users/avatars/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    class Meta:
        verbose_name, verbose_name_plural = 'Пользователь', 'Пользователи'

    def __str__(self) -> str:
        return self.username
