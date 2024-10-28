from django.db import models
from django.contrib.auth.models import AbstractUser
from api.validators import username_regex_validator


class User(AbstractUser):
    email = models.EmailField('Электронная почта', max_length=254, unique=True)
    username = models.CharField('Имя пользователя', max_length=150,
                                validators=(username_regex_validator, ),
                                unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    avatar = models.ImageField('Фото профиля', blank=True,
                               null=True, upload_to='users/avatars/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    class Meta:
        verbose_name, verbose_name_plural = 'Пользователь', 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Subscribers(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber', verbose_name='Пользователь')
    subscribe_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber_to', verbose_name='Автор')

    class Meta:
        verbose_name, verbose_name_plural = 'Подписка', 'Подписки'
