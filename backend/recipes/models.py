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
