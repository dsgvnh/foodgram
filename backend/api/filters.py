from django_filters.rest_framework import CharFilter, FilterSet, filters
from recipes.models import Ingredient, Tag, Recipes


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

    class Meta:
        model = Recipes
        fields = ('tags', 'author',)
