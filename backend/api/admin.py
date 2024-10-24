from django.contrib import admin
from recipes.models import Tag, Ingredient, Recipes, RecipesIngredient, Favorite, Shopping_cart
from users.models import User

admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Ingredient)
admin.site.register(Recipes)
admin.site.register(RecipesIngredient)
admin.site.register(Favorite)
admin.site.register(Shopping_cart)