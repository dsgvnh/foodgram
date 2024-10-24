from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tag, Ingredient, Recipes, Favorite, Shopping_cart
from .serializers import TagSerializer, IngredientSerializer, RecipSerializer, FavoriteAndShopCartSerializer
from api.filters import IngredientsNameFilter, RecipeFilter
from api.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse

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
        serializer_class=FavoriteAndShopCartSerializer
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipes, id=pk)
        serializer = FavoriteAndShopCartSerializer(recipe)
        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(user=recipe.author, recipe=recipe)
            if created:
                return Response(serializer.data, status=201)
            else:
                return Response({'Ошибка': 'Рецепт уже в избранном'}, status=400)
    
    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated, ),
        serializer_class=FavoriteAndShopCartSerializer,
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipes, id=pk)
        serializer = FavoriteAndShopCartSerializer(recipe)
        if request.method == 'POST':
            shop_cart, created = Shopping_cart.objects.get_or_create(user=request.user, recipe=recipe)
            if created:
                return Response(serializer.data, status=201)
            else:
                return Response({'Ошибка': 'Рецепт уже в корзине'}, status=400)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated, ),
    )
    def download_shopping_cart(self, request):
        items = Shopping_cart.objects.filter(user=request.user)
        recipes = [item.recipe for item in items]
        if not recipes:
            return Response({'errors': 'Корзина пуста'}, status=400)
        ingredients = {}
        for recipe in recipes:
            for ingredient in recipe.ingredients.all():
                name = ingredient.name
                measurement_unit = ingredient.measurement_unit
                items_amount = recipe.recipeingredients.filter(ingredient=ingredient)
                amount = sum(item.amount for item in items_amount)
                key = f"{name} ({measurement_unit})"
                if key in ingredients:
                    ingredients[key] += amount
                else:
                    ingredients[key] = amount
        shopping_list_text = "Список покупок:\n\n"
        for item, total_amount in ingredients.items():
            shopping_list_text += f"{item} — {total_amount}\n"
        response = HttpResponse(shopping_list_text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response
