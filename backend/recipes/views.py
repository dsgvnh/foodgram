import io

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.constants import (FONT_SIZE, SHOPPING_CART_OFFSET_X,
                           SHOPPING_CART_OFFSET_Y, SHOPPING_CART_X_SIZE)
from api.filters import IngredientsNameFilter, RecipeFilter
from api.permissions import IsOwnerOrReadOnly

from .models import Favorite, Ingredient, Recipes, Shopping_cart, Tag
from .serializers import (FavoriteAndShopCartSerializer, IngredientSerializer,
                          RecipSerializer, TagSerializer)


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
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['GET'],
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
        permission_classes=(IsAuthenticated, IsOwnerOrReadOnly),
        serializer_class=FavoriteAndShopCartSerializer
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipes, id=pk)
        serializer = FavoriteAndShopCartSerializer(recipe)
        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(
                user=recipe.author, recipe=recipe)
            if created:
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'Ошибка': 'Рецепт уже в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            if Favorite.objects.filter(user=request.user, recipe=recipe
                                       ).exists():
                Favorite.objects.filter(user=request.user, recipe=recipe
                                        ).delete()
                return Response({'Сообщение': 'Рецепт удален из избранного!'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'Ошибка': 'Рецепт не найден в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated, IsOwnerOrReadOnly),
        serializer_class=FavoriteAndShopCartSerializer,
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipes, id=pk)
        serializer = FavoriteAndShopCartSerializer(recipe)
        if request.method == 'POST':
            shop_cart, created = Shopping_cart.objects.get_or_create(
                user=request.user, recipe=recipe)
            if created:
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'Ошибка': 'Рецепт уже в корзине'},
                                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            if Shopping_cart.objects.filter(user=request.user, recipe=recipe
                                            ).exists():
                Shopping_cart.objects.filter(user=request.user, recipe=recipe
                                             ).delete()
                return Response({'Сообщение': 'Рецепт удален из корзины!'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'Ошибка': 'Рецепт не найден в корзине'},
                                status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated, ),
    )
    def download_shopping_cart(self, request):
        items = Shopping_cart.objects.filter(user=request.user)
        recipes = [item.recipe for item in items]
        if not recipes:
            return Response({'Ошибка': 'Корзина пуста'},
                            status=status.HTTP_400_BAD_REQUEST)
        ingredients = {}
        for recipe in recipes:
            for ingredient in recipe.ingredients.all():
                name = ingredient.name
                measurement_unit = ingredient.measurement_unit
                items_amount = recipe.recipeingredients.filter(
                    ingredient=ingredient)
                amount = sum(item.amount for item in items_amount)
                key = f'{name} ({measurement_unit})'
                if key in ingredients:
                    ingredients[key] += amount
                else:
                    ingredients[key] = amount
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        pdfmetrics.registerFont(TTFont('Tahoma', 'tahoma.ttf'))
        p.setFont('Tahoma', FONT_SIZE)
        p.drawString(SHOPPING_CART_X_SIZE, height - SHOPPING_CART_OFFSET_X,
                     "Список покупок:")
        y_position = height - SHOPPING_CART_OFFSET_Y
        for item, total_amount in ingredients.items():
            p.drawString(SHOPPING_CART_X_SIZE, y_position,
                         f"{item} — {total_amount}")
            y_position -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.pdf"')
        return response
