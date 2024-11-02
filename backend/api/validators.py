from django.core.validators import (RegexValidator,
                                    MinValueValidator,
                                    MaxValueValidator)

from .constants import (MIN_VALUE_FOR_VALIDATOR,
                        MAX_VALUE_FOR_VALIDATOR,
                        MAX_AMOUNT_VALUE_VALIDATOR)

username_regex_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Неверный формат имени пользователя'
)

tag_regex_validator = RegexValidator(
    regex=r'^[-a-zA-Z0-9_]+$',
    message='Неверный формат названия slug'
)

cooking_time_validator = (
    MinValueValidator(MIN_VALUE_FOR_VALIDATOR,
                      f'Минимальное значение - {MIN_VALUE_FOR_VALIDATOR}'),
    MaxValueValidator(MAX_VALUE_FOR_VALIDATOR,
                      f'Максимальное значение - {MAX_VALUE_FOR_VALIDATOR}')
)

amount_validator = (
    MinValueValidator(MIN_VALUE_FOR_VALIDATOR,
                      f'Минимальное значение - {MIN_VALUE_FOR_VALIDATOR}'),
    MaxValueValidator(MAX_AMOUNT_VALUE_VALIDATOR,
                      f'Максимальное значение - {MAX_AMOUNT_VALUE_VALIDATOR}')
)
