from rest_framework import serializers
from .models import Tag, Ingredient, Recipes, RecipesIngredient
from django.core.files.base import ContentFile
from users.serializers import UserListSerializer
import base64


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    measurement_unit = serializers.CharField(required=False)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

class RecipIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipesIngredient
        fields = ['id', 'amount']

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Параметр "amount" должен быть больше 1')
        return value

class RecipSerializer(serializers.ModelSerializer):
    author = UserListSerializer(required=False)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = serializers.CharField(max_length=None, allow_blank=True)
    ingredients = RecipIngredientSerializer(many=True, required=False)
    is_favorited = serializers.BooleanField(read_only=True, default=False)
    is_in_shopping_cart = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = Recipes
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(**validated_data)
        if tags_data:
            recipe.tags.set(tags_data)
        else:
            raise serializers.ValidationError('Нужно выбрать теги', 400)
        if ingredients_data:
            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data.pop('id')
                ingredient_amount = ingredient_data.pop('amount')
                ingredient2 = Ingredient.objects.get(id=ingredient_id)
                print(ingredient2)
        else:
            raise serializers.ValidationError('Необходимо выбрать ингредиенты', 400)
        return recipe


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = [{
            'id': tag.id,
            'name': tag.name,
            'slug': tag.slug
        } for tag in instance.tags.all()]
        representation['ingredients'] = [{
            'id': ingredient.id,
            'name': ingredient.name,
            'measurement_unit': ingredient.measurement_unit,
            #'amount': RecipesIngredient.amount
        } for ingredient in instance.ingredients.all()]
        return representation

    def create_avatar(self, avatar_base64):
        format, imgstr = avatar_base64.split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name=f"avatar.{ext}")

    def update(self, instance, validated_data):
        if 'avatar' in validated_data:
            avatar_base64 = validated_data.pop('avatar')
            instance.avatar = self.create_avatar(avatar_base64)
        return super().update(instance, validated_data)
