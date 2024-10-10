from django.db import models
from api.validators import tag_regex_validator


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
