from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from recipes.models import (Favorite, Ingredient, Recipes, RecipesIngredient,
                            Shopping_cart, Tag)
from users.models import Subscribers, User


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'avatar')
    search_fields = ('email', 'username')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'sum_favorites')
    search_fields = ('name',)
    list_filter = ('tags',)

    def sum_favorites(self, obj):
        return obj.favorite.all().count()
    sum_favorites.short_description = 'Кол-во в избранном'


class RecipesIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class Shopping_cart_Admin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribe_to')


admin.site.register(Tag, TagAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(RecipesIngredient, RecipesIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Shopping_cart, Shopping_cart_Admin)
admin.site.register(Subscribers, SubscribersAdmin)
admin.site.unregister(Group)
