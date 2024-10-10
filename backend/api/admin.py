from django.contrib import admin
from recipes.models import Tag, Ingredient, Recipes
from users.models import User

admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Ingredient)
admin.site.register(Recipes)