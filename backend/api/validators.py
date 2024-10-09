from django.core.validators import RegexValidator

username_regex_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Неверный формат имени пользователя'
)

tag_regex_validator = RegexValidator(
    regex=r'^[-a-zA-Z0-9_]+$',
    message='Неверный формат названия slug'
)
