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
    amount = serializers.IntegerField(default=0)

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
    image = serializers.CharField(max_length=None, allow_blank=False)
    ingredients = RecipIngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(default=True)
    is_in_shopping_cart = serializers.SerializerMethodField(default=True)

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False
    
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
        recip = Recipes.objects.create(**validated_data)
        if tags_data and len(tags_data) == len(set(tags_data)):
            recip.tags.set(tags_data)
        else:
            raise serializers.ValidationError('Необходимо указать теги', 400)
        if ingredients_data:
            try:
                for ingredient_data in ingredients_data:
                    ingredient_id = ingredient_data['id']
                    ingredient_amount = ingredient_data['amount']
                    ingredient = Ingredient.objects.get(id=ingredient_id)
                    RecipesIngredient.objects.create(recipe=recip, ingredient=ingredient, amount=ingredient_amount)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError('Введен ингредиент с несуществующим id', 400)
        else:
            raise serializers.ValidationError('Необходимо указать ингредиенты', 400)
        return recip


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = [{
            'id': tag.id,
            'name': tag.name,
            'slug': tag.slug
        } for tag in instance.tags.all()]
        representation['ingredients'] = [{
            'id': ingredient.ingredient.id,
            'name': ingredient.ingredient.name,
            'measurement_unit': ingredient.ingredient.measurement_unit,
            'amount': ingredient.amount
        } for ingredient in instance.recipeingredients.all()]
        return representation

    def validate_ingredients(self, value):
        ingredients = []
        for item in value:
            if item in ingredients:
                raise serializers.ValidationError('Ингредиенты должны быть уникальными')
            ingredients.append(item)
        return value

    def create_avatar(self, avatar_base64):
        format, imgstr = avatar_base64.split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name=f"avatar.{ext}")

    def update(self, instance, validated_data):
        if 'avatar' in validated_data:
            avatar_base64 = validated_data.pop('avatar')
            instance.avatar = self.create_avatar(avatar_base64)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        tags_data = validated_data.get('tags', None)
        if tags_data and len(tags_data) == len(set(tags_data)):
            instance.tags.set(tags_data)
        else:
            raise serializers.ValidationError('Необходимо добавить теги', 400)
        ingredients_data = validated_data.get('ingredients', [])
        if ingredients_data:
            try:
                for ingredient_data in ingredients_data:
                    ingredient_id = ingredient_data['id']
                    amount = ingredient_data['amount']
                    ingredient = Ingredient.objects.get(id=ingredient_id)
                    RecipesIngredient.objects.create(
                        recipe=instance, ingredient=ingredient, amount=amount)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError('Введен несуществующий ингредиент', 400)
        else:
            raise serializers.ValidationError('Необходимо добавить ингредиенты', 400)
        instance.save()
        return instance