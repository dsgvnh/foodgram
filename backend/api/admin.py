from django.contrib import admin
from recipes.models import Tag
from users.models import User


admin.site.register(Tag)
admin.site.register(User)
