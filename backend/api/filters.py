from django_filters.rest_framework import CharFilter, FilterSet, filters
from recipes.models import Ingredient, Tag, Recipes, Shopping_cart


class IngredientsNameFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(FilterSet):

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method='is_favorited_filter', label='В избранном')
    is_in_shopping_cart = filters.BooleanFilter(method='is_in_shopping_cart_filter', label='В корзине')

    class Meta:
        model = Recipes
        fields = ('tags', 'author',)

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorite__user=user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopcart__user=user)
        return queryset
