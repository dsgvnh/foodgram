from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tag, Ingredient, Recipes
from .serializers import TagSerializer, IngredientSerializer, RecipSerializer
from api.filters import IngredientsNameFilter


class TagsViewSet(ReadOnlyModelViewSet):
    model = Tag
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    model = Ingredient
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientsNameFilter
    pagination_class = None


class RecipViewSet(ModelViewSet):
    model = Recipes
    queryset = Recipes.objects.all()
    serializer_class = RecipSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)