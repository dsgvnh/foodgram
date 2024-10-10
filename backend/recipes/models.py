from django.db import models
from django.core.validators import MinValueValidator
from api.validators import tag_regex_validator
from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=32,
                            unique=True, blank=False)
    slug = models.SlugField('Slug', max_length=32,
                            unique=True, blank=False,
                            validators=(tag_regex_validator,))

    class Meta:
        verbose_name, verbose_name_plural = 'Тег', 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=128, blank=False)
    measurement_unit = models.CharField('Ед. измерения', max_length=64,
                                        blank=False)

    class Meta:
        verbose_name, verbose_name_plural = 'Ингредиент', 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


class Recipes(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes',
                                  verbose_name='Тег')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор',)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes',
                                         verbose_name='Ингредиенты')
    name = models.CharField('Название', max_length=256, blank=False)
    image = models.ImageField('Картинка', upload_to='recipes/images/',
                              blank=False)
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время готовки',
        validators=(MinValueValidator(1, 'Минимальное значение - 1'), ))

    class Meta:
        verbose_name, verbose_name_plural = 'Рецепт', 'Рецепты'

    def __str__(self) -> str:
        return self.name
