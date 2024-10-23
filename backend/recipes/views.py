from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tag, Ingredient, Recipes, Favorite
from .serializers import TagSerializer, IngredientSerializer, RecipSerializer, FavoriteSerializer
from api.filters import IngredientsNameFilter, RecipeFilter
from api.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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
    http_method_names = ['get', 'post', 'patch']
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['GET', ],
        permission_classes=(AllowAny, ),
        url_path='get-link'
    )
    def get_link(self, request, pk):
        recipe = get_object_or_404(Recipes, id=pk)
        shortlink = f'http://127.0.0.1:8000/s/{recipe.id}'
        return Response({'short-link': shortlink})
    
    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated, ),
        serializer_class=FavoriteSerializer
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipes, id=pk)
        serializer = FavoriteSerializer(recipe)
        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(user=recipe.author, recipe=recipe)
            if created:
                return Response(serializer.data, status=201)
            else:
                return Response({'Ошибка': 'Рецепт уже в избранном'}, status=400)
