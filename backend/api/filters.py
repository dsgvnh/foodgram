from django_filters.rest_framework import CharFilter, FilterSet
from recipes.models import Ingredient


class IngredientsNameFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name', )
