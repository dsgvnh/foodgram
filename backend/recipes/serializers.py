from rest_framework import serializers
from .models import Tag, Ingredient, Recipes, RecipesIngredient, Favorite, Shopping_cart
from users.serializers import UserListSerializer, Base64ImageField


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
        fields = ('id', 'amount',)

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Количество должно быть больше 1')
        return value


class RecipSerializer(serializers.ModelSerializer):
    author = UserListSerializer(required=False)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField()
    ingredients = RecipIngredientSerializer(many=True,)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        else:
            return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Shopping_cart.objects.filter(user=user, recipe=obj).exists()
        else:
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
        recip.tags.set(tags_data)
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data['id']
            ingredient_amount = ingredient_data['amount']
            ingredient = Ingredient.objects.get(id=ingredient_id)
            RecipesIngredient.objects.create(recipe=recip, ingredient=ingredient, amount=ingredient_amount)
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
        if not value:
            raise serializers.ValidationError('Ингредиенты не могут быть пустыми', 400)
        ingredients = []
        for item in value:
            try:
                exist_ingredient = Ingredient.objects.get(id=item['id'])
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError('Введен ингредиент с несуществующим id', 400)
            if item in ingredients:
                raise serializers.ValidationError('Ингредиенты должны быть уникальными', 400)
            ingredients.append(item)
        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError("Теги не могут быть пустыми", 400)
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Теги должны быть уникальными", 400)
        return value

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        tags_data = validated_data.get('tags', None)
        if tags_data:
            instance.tags.set(tags_data)
        else:
            raise serializers.ValidationError("Теги не могут быть пустыми", 400)
        ingredients_data = validated_data.get('ingredients', [])
        if ingredients_data:
            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data['id']
                amount = ingredient_data['amount']
                ingredient = Ingredient.objects.get(id=ingredient_id)
                RecipesIngredient.objects.create(
                    recipe=instance, ingredient=ingredient, amount=amount)
        else:
            raise serializers.ValidationError("Ингредиенты не могут быть пустыми", 400)
        instance.save()
        return instance


class FavoriteAndShopCartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Favorite
        fields = ('id', )

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'image': str(instance.image),
            'cooking_time': instance.cooking_time
        }


class RecipForSubscribersSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
